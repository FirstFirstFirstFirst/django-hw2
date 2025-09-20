import json
import re
import ast
from statistics import mean
from .models import Prompt, TestCase, Result
from django.conf import settings
from anthropic import Anthropic

# Initialize Anthropic client
client = Anthropic(api_key=settings.CLAUDE_API_KEY)
model = "claude-3-5-haiku-latest"

# Helper functions
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }

    if system:
        params["system"] = system

    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    message = client.messages.create(**params)
    return message.content[0].text

def generate_dataset():
    """Generate evaluation dataset using Claude API"""
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex for various programming tasks. Generate an array of JSON objects,
each representing a task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task",
        "format": "json" or "python" or "regex",
        "solution_criteria": "Key criteria for evaluating the solution"
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code
* Include a variety of domains: data processing, text manipulation, configuration, validation, etc.

Please generate 3 objects.
"""

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text)


def run_prompt(test_case, user_prompt_text):
    """Run the user's prompt with a test case through Claude API"""
    prompt = f"""
{user_prompt_text}

Task: {test_case["task"]}

* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation
"""

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```code")
    output = chat(messages, stop_sequences=["```"])
    return output


def validate_json(text):
    """Validate JSON syntax"""
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    """Validate Python syntax"""
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    """Validate regex pattern"""
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0

def grade_syntax(response, test_case):
    """Grade the syntax validity of the response"""
    format_type = test_case["format"]
    if format_type == "json":
        return validate_json(response)
    elif format_type == "python":
        return validate_python(response)
    else:
        return validate_regex(response)

def grade_by_model(test_case, output):
    """Grade a test case + output using a model"""
    eval_prompt = f"""
You are an expert code reviewer. Your task is to evaluate the following AI-generated solution.

Original Task:
<task>
{test_case["task"]}
</task>

Solution to Evaluate:
<solution>
{output}
</solution>

Criteria you should use to evaluate the solution:
<criteria>
{test_case["solution_criteria"]}
</criteria>

Output Format
Provide your evaluation as a structured JSON object with the following fields, in this specific order:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement
- "reasoning": A concise explanation of your overall assessment
- "score": A number between 1-10

Respond with JSON. Keep your response concise and direct.
Example response shape:
{{
    "strengths": string[],
    "weaknesses": string[],
    "reasoning": string,
    "score": number
}}
    """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)


def run_test_case(test_case, user_prompt_text):
    """Execute a single test case and grade the output"""
    output = run_prompt(test_case, user_prompt_text)

    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    syntax_score = grade_syntax(output, test_case)

    # Combined score: average of model and syntax scores
    score = (model_score + syntax_score) / 2

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
        "reasoning": reasoning,
        "model_grade": model_grade,
        "syntax_score": syntax_score
    }

def run_evaluation(prompt_text, description="", version="1.0"):
    """
    Run the complete evaluation pipeline:
    1. Save prompt to database
    2. Generate test cases using Claude
    3. Run user prompt with each test case through Claude
    4. Grade responses using model + syntax validation
    5. Save results to database
    """

    # Create and save prompt
    prompt = Prompt.objects.create(
        text=prompt_text,
        description=description,
        version=version
    )

    # Generate dataset of test cases
    dataset = generate_dataset()

    results = []
    total_score = 0

    for test_case_data in dataset:
        # Create and save test case
        test_case = TestCase.objects.create(
            prompt=prompt,
            input=test_case_data["task"],
            expected_type=test_case_data["format"]
        )

        # Run test case evaluation
        result_data = run_test_case(test_case_data, prompt_text)

        # Create and save result
        result = Result.objects.create(
            prompt=prompt,
            test_case=test_case,
            output=result_data["output"],
            score=int(result_data["score"]),
            reasoning=result_data["reasoning"]
        )

        results.append({
            "test_case": test_case,
            "result": result,
            "grade_details": result_data
        })

        total_score += result_data["score"]

    # Calculate average score
    average_score = total_score / len(results) if results else 0

    return {
        "prompt": prompt,
        "results": results,
        "average_score": round(average_score, 2),
        "total_test_cases": len(results)
    }