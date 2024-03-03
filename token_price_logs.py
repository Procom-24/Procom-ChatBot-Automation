
import openai
import langchain
from langchain_community.llms import OpenAI
from langchain_community.callbacks import get_openai_callback



def get_openai_model_cost_table(model_name='gpt-3.5-turbo', is_completion=False):
    model_cost_mapping = {
        "gpt-4": 0.03,
        "gpt-4-0314": 0.03,
        "gpt-4-completion": 0.06,
        "gpt-4-0314-completion": 0.06,
        "gpt-4-32k": 0.06,
        "gpt-4-32k-0314": 0.06,
        "gpt-4-32k-completion": 0.12,
        "gpt-4-32k-0314-completion": 0.12,
        "gpt-3.5-turbo": 0.002,
        "gpt-3.5-turbo-0301": 0.002,
        "text-ada-001": 0.0004,
        "ada": 0.0004,
        "text-babbage-001": 0.0005,
        "babbage": 0.0005,
        "text-curie-001": 0.002,
        "curie": 0.002,
        "text-davinci-003": 0.02,
        "text-davinci-002": 0.02,
        "code-davinci-002": 0.02,
    }
    cost = model_cost_mapping.get(
        model_name.lower()
        + ("-completion" if is_completion and model_name.startswith("gpt-4") else ""),
        None,
    )
    if cost is None:
        raise ValueError(
            f"Unknown model: {model_name}. Please provide a valid OpenAI model name."
            "Known models are: " + ", ".join(model_cost_mapping.keys())
        )
    return cost


def get_openai_cost(response):
    """
    Pass openai response object and get total cost.
    """
    total_cost = 0
    if "usage" in response:
        completion_cost = get_openai_model_cost_table(
            model_name=response["model"],
            is_completion=True,
        ) * (response["usage"].get("completion_tokens", 0) / 1000.0)
        prompt_cost = get_openai_model_cost_table(
            model_name=response["model"]
        ) * (response["usage"].get("prompt_tokens", 0) / 1000.0)
        total_cost = prompt_cost + completion_cost
    return total_cost
openai.api_key = 'API KEY'

llm = OpenAI(model_name="text-davinci-002", n=2, best_of=2)

with get_openai_callback() as cb:
    result = llm("Tell me a joke")
    print(cb)
