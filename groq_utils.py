from groq import Groq
import os, json, re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)

def get_disease_info(disease_name: str):
    prompt = f"""
    I detected a leaf disease called "{disease_name}". 
    Strictly respond with JSON only, in this format:

    {{
      "disease_type": "...",
      "severity": "...",
      "symptoms": ["..."],
      "possible_causes": ["..."],
      "treatment": ["..."]
    }}
    No explanations, no extra text, no markdown.
    """

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_completion_tokens=1024
    )

    content = completion.choices[0].message.content.strip()

    # Remove code blocks if present
    if content.startswith("```"):
        content = re.sub(r"```.*\n", "", content)
        content = content.replace("```", "").strip()

    # Attempt JSON parsing safely
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # fallback dictionary if parsing fails
        return {
            "disease_type": "unknown",
            "severity": "unknown",
            "symptoms": ["Could not parse symptoms"],
            "possible_causes": ["Could not parse causes"],
            "treatment": ["Could not parse treatment"]
        }

