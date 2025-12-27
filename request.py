# Import the main agent function and the logging helper
from agent import run_telekom_agent, log_result, get_models_to_test
import os

#os.chdir(r"C:\Users\salam\Desktop\Ali\ai_telekom_agent")

# Helper function: read floats
def input_float(prompt: str, default=None):
    """
    Read a float from stdin.
    - Empty input returns `default` (default None).
    - Invalid input triggers a re-prompt.
    """
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return default
        try:
            return float(raw)
        except ValueError:
            print("Invalid number. Please enter a numeric value (e.g., 10 or 10.5) or press Enter to skip.")

# Collect user tariff + usage data
def get_user_data():
    print("Please enter your CURRENT mobile plan details (press Enter to skip any field):")

    # current_price_eur = input_float("Current monthly price (€): ")
    # current_data_gb = input_float("Included data (GB), 0 means unlimited: ")
    # current_minutes = input_float("Included minutes: ")
    # current_sms = input_float("Included SMS: ")

    current_price_eur = 10
    current_data_gb = 100
    current_minutes = 1000
    current_sms = 500

    print("\nPlease enter your ACTUAL monthly usage (press Enter to skip any field):")

    # actual_data_usage_gb = input_float("Actual data used (GB): ")
    # actual_minutes_used = input_float("Actual minutes used: ")
    # actual_sms_used = input_float("Actual SMS used: ")

    actual_data_usage_gb = 150
    actual_minutes_used = 300
    actual_sms_used = 10

    return {
        "current_price_eur": current_price_eur,
        "current_data_gb": current_data_gb,
        "current_minutes": current_minutes,
        "current_sms": current_sms,
        "actual_data_usage_gb": actual_data_usage_gb,
        "actual_minutes_used": actual_minutes_used,
        "actual_sms_used": actual_sms_used,
    }

# Choose where tariffs come from
def get_tariff_source() -> str:
    """
    Let user pick:
      1 -> 'json'
      2 -> 'internet'
    Returns: 'json' or 'internet'
    """
    while True:
        print("\nChoose tariff source:")
        print("1 - json (local tariffs.json)")
        print("2 - internet (provider websites)\n")

        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            return "json"
        if choice == "2":
            return "internet"

        print("Invalid input. Please enter 1 or 2.")

# Main program entry point
def main():
    # Collect user input first
    user_data = get_user_data()

    query = "Suggest exactly one cost improvement based on this usage and price ration."
    models_to_test = get_models_to_test()

    TARIFF_SOURCE = get_tariff_source()  # "json" or "internet"

    for model in models_to_test:
        print(f"\n--- Running Telekom Agent with {model} ---")
        print("\n🔍 We are searching for the best alternative offer based on your current plan...\n")

        answer, time_taken, prompt_version = run_telekom_agent(
            model,
            user_data,
            query,
            tariffs_source=TARIFF_SOURCE
        )

        print("Response:")
        print(answer)
        print("Response Time taken:", time_taken, "seconds")

        log_result(model, prompt_version, query, answer, time_taken)

# Run only if executed directly
if __name__ == "__main__":
    main()

