import pytest
from fastapi import HTTPException

from app.job_store import JobStore
from app.main import app, get_questions
from app.models import QuestionMode


def test_start_process_exposes_file_picker_in_openapi():
    schema = app.openapi()

    assert "/start_process" in schema["paths"]
    assert "/upload_info" not in schema["paths"]

    request_body = schema["paths"]["/start_process"]["post"]["requestBody"]
    multipart_schema = request_body["content"]["multipart/form-data"]["schema"]
    form_schema_name = multipart_schema["$ref"].rsplit("/", 1)[-1]
    form_schema = schema["components"]["schemas"][form_schema_name]

    files_schema = form_schema["properties"]["files"]
    assert files_schema["type"] == "array"
    assert files_schema["items"] == {"type": "string", "format": "binary"}
    assert "files" not in form_schema.get("required", [])


@pytest.fixture
def completed_job(tmp_path):
    store = JobStore(tmp_path)
    process_id = store.create_job(
        text="case", files=[], combined_text="case", question_count=1, language="English"
    )
    store.write_json(process_id, "baseline_questions.json", ["Baseline?"])
    store.write_json(process_id, "enriched_questions.json", ["Enriched?"])
    store.update_status(process_id, "completed", 100)
    return store, process_id


@pytest.mark.parametrize("mode", ["baseline", "enriched", "both"])
@pytest.mark.parametrize("case_ids", [["case_b", "case_a"], []])
def test_questions_return_used_cases_with_source_filenames(completed_job, mode, case_ids):
    store, process_id = completed_job
    store.write_json(process_id, "retrieval/relevant_cases.json", {"case_ids": case_ids})
    # The retrieval shortlist can contain cases rejected by the relevance filter.
    store.write_json(process_id, "retrieval/candidates.json", [{"case_id": "rejected"}])

    response = get_questions(process_id, "user", store, QuestionMode(mode))

    assert response.model_dump(mode="json") == {
        "process_id": process_id,
        "mode": mode,
        "baseline": ["Baseline?"] if mode in {"baseline", "both"} else None,
        "enriched": ["Enriched?"] if mode in {"enriched", "both"} else None,
        "similar_cases": [
            {"case_id": case_id, "file_name": f"{case_id}.md"} for case_id in case_ids
        ],
    }


@pytest.mark.parametrize("status,code", [("filtering", 202), ("failed", 409)])
def test_unfinished_questions_do_not_require_reference_results(completed_job, status, code):
    store, process_id = completed_job
    store.update_status(process_id, status, 75)

    if code == 409:
        with pytest.raises(HTTPException) as error:
            get_questions(process_id, "user", store)
        assert error.value.status_code == code
    else:
        response = get_questions(process_id, "user", store)
        assert response.status_code == code
        assert b"similar_cases" not in response.body


def test_questions_unknown_process(completed_job):
    store, _ = completed_job
    with pytest.raises(HTTPException) as error:
        get_questions("00000000-0000-0000-0000-000000000000", "user", store)
    assert error.value.status_code == 404
