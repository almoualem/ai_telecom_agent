# AI Telecom Agent (Ollama Project)

This project explores the feasibility of a Telecom Provider Agent that leverages a local/cloud LLM to analyze user usage data and compare it against available telecom tariffs. The goal is to recommend cost improvements while providing clear reasoning and ensuring full reproducibility of results.

## Requirements
- Python >= 3.12
- Ollama installed locally ([download here](https://ollama.com/download/windows))

## Setup
```bash
git clone https://github.com/username/ai_telecom_agent.git
cd ai_telecom_agent
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
