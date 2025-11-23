import json
from agent import run_telekom_agent

#----- Load your usage data -----
user_data = {
    "current_plan": "Monthly 20GB",
    "price_usd": 45,
    "data_used_gb": 28,
    "minutes_used": 400,
    "sms_used": 300
}

#----- The instruction you want the agent to perform -----
query = "Suggest exactly one cost improvement based on this usage."

#----- Choose your model -----
model_name = "llama3"

print(f"\nRunning Telekom Agent using model: {model_name}")

answer, time_taken = run_telekom_agent(model_name, user_data, query)

print("\n--- Agent Output ---")
print(answer)
print("\nTime taken:", time_taken, "seconds")