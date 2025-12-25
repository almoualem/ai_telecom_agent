import ollama
import time
import os

def run_telekom_agent(model_name: str, user_data: dict, query: str, prompt_version: str = "V1"):
    system_prompt = """
    You are a Telecom Cost Optimization Expert.
    Your job: Analyze user mobile data usage, minutes, SMS, and current plan.
    Search in internet service provider in Austria like Magenta and Drei and A1.
    Do NOT add extra text outside your recommendation.

    Output format must be exactly 3 lines:

    Recommendation: <offer name and service provider>
    Alternative Plan Details: <provide offer details, like gb, minutes, sms, price in euro>
    Estimated savings: <EUR/month or say "unknown" if price not provided>
    Reason: <one sentence referencing the deltas>
    """

    user_prompt = f"""
    Here is the customer's usage data: {user_data}
    Task: {query}
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

    return response["message"]["content"], (end_time - start_time), prompt_version


def log_result(model_name, prompt_version, query, answer, time_taken,
               accuracy=None, clarity=None):
    # Ensure logs folder exists
    os.makedirs("logs", exist_ok=True)

    log_path = os.path.join("logs", "results.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\nModel: {model_name}\n")
        f.write(f"Prompt Version: {prompt_version}\n")
        f.write(f"Query: {query}\n")
        f.write(f"Answer: {answer}\n")
        f.write(f"Time taken: {time_taken:.2f} seconds\n")
        if accuracy is not None:
            f.write(f"Accuracy rating: {accuracy}/5\n")
        if clarity is not None:
            f.write(f"Clarity rating: {clarity}/5\n")
        f.write("-" * 40 + "\n")
