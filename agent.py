import ollama
import time

def run_telekom_agent(model_name: str, user_data: dict, query: str):
    system_prompt = """
You are a Telecom Cost Optimization Expert.

Your job:
Analyze user mobile data usage, minutes, SMS, and current plan.
Identify EXACTLY ONE improvement the user can make.
Show estimated cost savings.
Explain your reasoning clearly.
Do NOT add extra text outside your recommendation.
"""

    user_prompt = f"""
Here is the customer's usage data:
{user_data}

Task:
{query}
"""

    start_time = time.time()

    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    end_time = time.time()

    return response["message"]["content"], (end_time - start_time)