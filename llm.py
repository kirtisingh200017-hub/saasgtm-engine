import os, json, re
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

def ask(prompt, system="You are a precise B2B SaaS GTM analyst.", max_tokens=1500):
    r = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=max_tokens,
        ),
    )
    return r.text or ""

def ask_json(prompt, system="Return ONLY valid JSON. No prose, no code fences."):
    r = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",   # forces JSON output
            max_output_tokens=2000,
        ),
    )
    text = (r.text or "").strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    return json.loads(text)

if __name__ == "__main__":
    print(ask("Say hello in five words."))