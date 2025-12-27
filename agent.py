import ollama
import time
import os
import json

# Optional (used only for source="internet")
try:
    import requests
    from bs4 import BeautifulSoup
except Exception:
    requests = None
    BeautifulSoup = None

# Provider websites used when source="internet"
PROVIDER_URLS = {
    "Magenta": "https://www.magenta.at/handytarife/tarife-ohne-handy",
    "A1": "https://www.a1.net/handys-tarife/tarife-ohne-bindung",
}

# Load tariffs from local JSON file
def load_tariffs_from_json(json_path: str = "tariffs.json") -> dict:
    """
    Loads tariffs from a local JSON file in the same folder.
    Expected: any JSON structure is okay; we pass it through to the model.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f'Local tariffs file not found: "{json_path}"')
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Download raw HTML from a website
def _fetch_html(url: str, timeout_s: int = 20) -> str:
    if requests is None:
        raise RuntimeError(
            "requests/bs4 not available in this environment, cannot use source='internet'. "
            "Install: pip install requests beautifulsoup4"
        )
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; tariff-bot/1.0)"
    }
    r = requests.get(url, headers=headers, timeout=timeout_s)
    r.raise_for_status()
    return r.text

# Load tariffs by scraping websites
def load_tariffs_from_internet() -> dict:
    """
    Best-effort scrape: downloads HTML and extracts text blocks that likely contain tariff info.
    We keep it simple and robust (no site-specific brittle selectors).
    """
    html_map = {k: _fetch_html(v) for k, v in PROVIDER_URLS.items()}
    extracted = {}

    for provider, html in html_map.items():
        if BeautifulSoup is None:
            # Fallback: just pass raw HTML (model can still parse)
            extracted[provider] = {"url": PROVIDER_URLS[provider], "raw_html": html[:250000]}
            continue

        soup = BeautifulSoup(html, "html.parser")

        # Remove scripts/styles to reduce noise
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text("\n")
        # Basic cleanup: keep non-empty lines
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        # Limit size to keep prompt sane
        extracted[provider] = {
            "url": PROVIDER_URLS[provider],
            "lines": lines[:4000],  # adjust if needed
        }

    return extracted

# Main agent function
def run_telekom_agent(
    model_name: str,
    user_data: dict,
    query: str,
    prompt_version: str = "V2",
    tariffs_source: str = "",
    tariffs_json_path: str = "tariffs.json"
):
    """
    tariffs_source:
      - "json": read ./tariffs.json
      - "internet": fetch provider pages and extract text
    """

    if tariffs_source not in {"json", "internet"}:
        raise ValueError("tariffs_source must be 'json' or 'internet'")

    if tariffs_source == "json":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, tariffs_json_path)
        tariffs_payload = load_tariffs_from_json(json_path)
        tariffs_context = (
            "Tariffs source: LOCAL JSON FILE.\n"
            f"File: {tariffs_json_path}\n"
            "Use ONLY the tariffs provided in the JSON below. Do NOT browse the web.\n"
            f"JSON:\n{json.dumps(tariffs_payload, ensure_ascii=False)}\n"
        )
    else:
        tariffs_payload = load_tariffs_from_internet()
        tariffs_context = (
            "Tariffs source: INTERNET.\n"
            "You are given extracted page content from the provider URLs below.\n"
            "Use ONLY what is present in this extracted content. If a tariff cannot be verified from it, say 'not available'.\n"
            f"Extracted content:\n{json.dumps(tariffs_payload, ensure_ascii=False)[:350000]}\n"
        )

    system_prompt = """
You are a Telecom Cost Optimization Expert.

Rules:
- You MUST base your recommendation ONLY on the provided tariffs context (JSON or extracted page content).
- You MUST explicitly evaluate and compare tariffs from ALL providers present in the tariffs context.
- If multiple providers offer suitable tariffs, choose the best one based on price-to-usage ratio.
- If current_data_gb is null or 0, the current plan has UNLIMITED mobile data.
- If there is no clearly better offer according to usage and price, recommend keeping the current plan.
- If usage is higher than current plan even if the new price is higher, user needs a new plan (reason is: overage charges).
- Do NOT recommend random tariffs that are not present in the provided tariffs context.
- Do NOT add extra text outside the required output format.

Output format must be exactly:

Current Plan: <provide current offer details, like gb, minutes, sms, price in euro as the user entered them>
New Plan details: <provide details of the new tariff like name, gb, minutes, sms, price>
Recommendation: <one recommended tariff name + ISP, or "keep current plan">
Offer Link: <get url from JSON file>
Estimated savings: <EUR/month OR if we keep current plan "none" OR if price is higher "reduced overage costs">
Reason: <one sentence referencing the details>
""".strip()

    user_prompt = f"""
Tariffs context:
{tariffs_context}

Customer usage data: {user_data}

Task: {query}
""".strip()

    start_time = time.time()
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    end_time = time.time()

    return response["message"]["content"], (end_time - start_time), prompt_version

# Save results to a log file
def log_result(model_name, prompt_version, query, answer, time_taken,
               accuracy=None, clarity=None):
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "results.log")
    print("Logs written to:", log_path)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\nModel: {model_name}\n")
        f.write(f"Prompt Version: {prompt_version}\n")
        f.write(f"Query: {query}\n")
        f.write(f"Response: \n")
        f.write(f"{answer}\n")
        f.write(f"Time taken: {time_taken:.2f} seconds\n")
        if accuracy is not None:
            f.write(f"Accuracy rating: {accuracy}/5\n")
        if clarity is not None:
            f.write(f"Clarity rating: {clarity}/5\n")
        f.write("-" * 40 + "\n")
