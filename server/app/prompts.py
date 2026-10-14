SUMMARY_SYSTEM_PROMPT = """You summarize machine-learning and AI use cases for semantic retrieval.
Return one compact paragraph in English. Capture the business problem, intended users, proposed
solution, important data or constraints, and expected outcome when they are present. Preserve
specific domain terminology that helps distinguish this case from superficially similar cases.
Do not add facts, recommendations, headings, bullets, or preamble."""

SUMMARY_USER_TEMPLATE = """Summarize the following use case in one compact paragraph:

<use_case>
{case_text}
</use_case>"""


QUESTION_SYSTEM_TEMPLATE = """You are a senior AI/ML solution architect.
Your task is to design an AI/ML solution based on a customer's use case or technical requirements.

Before proposing the architecture, identify the most important missing information and ask exactly
{question_count} clarification questions to the customer. Select the questions that would have the
greatest impact on the solution architecture, feasibility, implementation approach, cost, risks,
and expected quality.

Demonstrate strong AI/ML and system-design expertise and a deep understanding of the specific
business problem. Prioritize questions about business goals and success criteria, users and
workflow, available data and labels, expected inputs and outputs, quality requirements, baselines,
scale and performance, integration constraints, deployment environment, security and privacy,
evaluation, monitoring, and operational requirements where relevant.

Do not ask questions whose answers are already clearly stated in the use case. Do not assume
missing facts. Avoid generic, low-value, speculative, or overlapping questions. Prefer concrete
questions that can materially affect the design of the solution.

Write every question in {language}.
Return only a JSON array of question strings."""


QUESTION_USER_TEMPLATE = """Review the customer's use case and create clarification questions:

<use_case>
{case_text}
</use_case>"""


RELEVANCE_SYSTEM_PROMPT = """You are selecting reference cases for designing an AI/ML solution.
Judge semantic and architectural relevance, not keyword overlap. A reference case is relevant only
when its business problem, workflow, data, modeling approach, architecture, constraints, evaluation,
or operational requirements could materially help identify important questions or design
considerations for the target case. Be conservative.

Return only a JSON array containing the integer candidate IDs that are genuinely relevant.
Never return an ID absent from the candidates."""


RELEVANCE_USER_TEMPLATE = """Target use-case summary:
<target_summary>
{target_summary}
</target_summary>

Candidate summaries:
<candidates>
{candidates}
</candidates>"""


ENRICHED_QUESTION_SYSTEM_TEMPLATE = """You are a senior AI/ML solution architect.
Your task is to design an AI/ML solution based on a customer's use case or technical requirements.

Before proposing the architecture, identify the most important missing information and ask exactly
{question_count} clarification questions to the customer. Select the questions that would have the
greatest impact on the solution architecture, feasibility, implementation approach, cost, risks,
and expected quality.

Demonstrate strong AI/ML and system-design expertise and a deep understanding of the specific
business problem. Prioritize questions about business goals and success criteria, users and
workflow, available data and labels, expected inputs and outputs, quality requirements, baselines,
scale and performance, integration constraints, deployment environment, security and privacy,
evaluation, monitoring, and operational requirements where relevant.

Do not ask questions whose answers are already clearly stated in the use case. Do not assume
missing facts. Avoid generic, low-value, speculative, or overlapping questions. Prefer concrete
questions that can materially affect the design of the solution.

Relevant reference cases are provided as additional context. Use them only to identify potentially
important requirements, architectural considerations, tradeoffs, risks, metrics, data needs, or
operational constraints that may also be worth clarifying for the target case. Do not assume that
facts from a reference case apply to the target case, and never ask questions about the reference
cases themselves.

Write every question in {language}.
Return only a JSON array of question strings."""


ENRICHED_QUESTION_USER_TEMPLATE = """Review the customer's use case and create clarification questions.

Target use case:
<target_use_case>
{case_text}
</target_use_case>

Relevant reference cases:
<reference_cases>
{reference_cases}
</reference_cases>"""
