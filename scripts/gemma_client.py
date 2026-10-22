import json
import urllib.request
import urllib.error

GEMMA_API_URL = "http://localhost:1234/api/v1/chat"
MODEL_NAME = "google/gemma-3n-e4b"


def query_gemma(prompt: str, system_prompt: str = "You are an expert financial analyst. Extract and structure data concisely.") -> str:
    """Send a prompt to the local Gemma model on localhost:1234."""
    payload = {
        "model": MODEL_NAME,
        "system_prompt": system_prompt,
        "input": prompt,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GEMMA_API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            outputs = res_json.get("output", [])
            if outputs and "content" in outputs[0]:
                return outputs[0]["content"].strip()
            return str(res_json)
    except Exception as e:
        return f"Error calling Gemma: {e}"


if __name__ == "__main__":
    test_res = query_gemma("Summarize in 2 sentences why Credit Suisse was distressed in 2022.")
    print("Gemma Response:")
    print(test_res)
