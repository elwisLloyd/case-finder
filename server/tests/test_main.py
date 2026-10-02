from app.main import app


def test_start_process_exposes_file_picker_in_openapi():
    schema = app.openapi()

    # Swagger UI treats an array of binary strings as a multiple-file input in
    # OpenAPI 3.0, but renders it as "Add string item" in OpenAPI 3.1.
    assert schema["openapi"] == "3.0.3"
    assert "/start_process" in schema["paths"]
    assert "/upload_info" not in schema["paths"]

    request_body = schema["paths"]["/start_process"]["post"]["requestBody"]
    multipart_schema = request_body["content"]["multipart/form-data"]["schema"]
    form_schema_name = multipart_schema["$ref"].rsplit("/", 1)[-1]
    form_schema = schema["components"]["schemas"][form_schema_name]

    assert "files" not in form_schema["properties"]
    for number in range(1, 11):
        file_schema = form_schema["properties"][f"file_{number}"]
        binary_schema = next(
            (
                item
                for item in file_schema.get("anyOf", [])
                if item.get("format") == "binary"
            ),
            file_schema,
        )
        assert binary_schema["type"] == "string"
        assert binary_schema["format"] == "binary"
        assert f"file_{number}" not in form_schema.get("required", [])
