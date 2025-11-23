from agent import run_telekom_agent, log_result

user_data = {
    "current_plan": "Monthly 20GB",
    "price_usd": 45,
    "data_used_gb": 28,
    "minutes_used": 400,
    "sms_used": 300
}

query = "Suggest exactly one cost improvement based on this usage."
models_to_test = ["llama3:8b", "mistral:7b", "qwen2.5:7b"]

for model in models_to_test:
    print(f"\n--- Running Telekom Agent with {model} ---")
    answer, time_taken, prompt_version = run_telekom_agent(model, user_data, query)
    print("Answer:", answer)
    print("Time taken:", time_taken, "seconds")

    # Log results (ratings can be filled manually later)
    log_result(model, prompt_version, query, answer, time_taken)
