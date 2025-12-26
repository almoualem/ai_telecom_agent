from agent import run_telekom_agent, log_result

def get_user_data():
    print("Please enter your CURRENT mobile plan details:")
    current_price_eur = float(input("Current monthly price (€): "))
    current_data_gb = float(input("Included data (GB): "))
    current_minutes = int(input("Included minutes: "))
    current_sms = int(input("Included SMS: "))

    #current_price_eur = 40
    #current_data_gb = 20
    #current_minutes = 1000
    #current_sms = 500

    print("\nPlease enter your ACTUAL monthly usage:")
    actual_data_usage_gb = float(input("Actual data used (GB): "))
    actual_minutes_used = int(input("Actual minutes used: "))
    actual_sms_used = int(input("Actual SMS used: "))

    #actual_data_usage_gb = 25
    #actual_minutes_used = 300
    #actual_sms_used = 10

    return {
        "current_price_eur": current_price_eur,
        "current_data_gb": current_data_gb,
        "current_minutes": current_minutes,
        "current_sms": current_sms,
        "actual_data_usage_gb": actual_data_usage_gb,
        "actual_minutes_used": actual_minutes_used,
        "actual_sms_used": actual_sms_used
    }

# Collect user input first
user_data = get_user_data()

query = "Suggest exactly one cost improvement based on this usage."
models_to_test = ["gpt-oss:120b-cloud"]

for model in models_to_test:
    print(f"\n--- Running Telekom Agent with {model} ---")
    print("\n🔍 We are searching for the best alternative offer based on your current plan and usage...\n")
    answer, time_taken, prompt_version = run_telekom_agent(
        model,
        user_data,
        query
    )
    print("Answer:", answer)
    print("Response Time taken:", time_taken, "seconds")

    log_result(model, prompt_version, query, answer, time_taken)

