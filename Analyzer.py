import os
from dotenv import load_dotenv
from openai import OpenAI

# Load Openai API key from .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ Aint got no OPENAI_API_KEY in .env gang")

# OpenAI client
client = OpenAI(api_key=API_KEY)

# Choose a gpt model
MODEL = "gpt-5.1"


def build_prompt(all_stats: dict) -> str:
    """
    Build a SHORT, tactical prompt for the analyst.

    We want:
      - Enemy playstyle
      - Most common operators
      - How to counter on DEFENSE
      - How to counter on ATTACK
    """
    prompt = (
        "You are a Rainbow Six Siege analyst. Keep the response SHORT, CLEAN and ACTIONABLE.\n"
        "Format the output EXACTLY like this:\n\n"
        "**Enemy Playstyle Summary:** (1–3 sentences)\n"
        "**Most Common Operators:** List per player (top 1–3 ops only)\n"
        "**How to Counter (Defense):** 3–5 bullet points\n"
        "**How to Counter (Attack):** 3–5 bullet points\n\n"
        "Avoid filler text and long explanations. Do NOT repeat raw stats back.\n"
        "Do NOT apologize or hedge; make confident predictions based on the data.\n\n"
        "=== RAW PLAYER DATA ===\n"
    )

    for username, data in all_stats.items():
        prompt += f"\nPLAYER: {username}\n"
        if not data:
            prompt += "  ⚠ No stats found.\n"
        else:
            for op, stats in data.items():
                prompt += f"  {op}:\n"
                for k, v in stats.items():
                    prompt += f"    - {k}: {v}\n"

    prompt += "\nNow generate the briefing using the required compact format.\n"
    return prompt


def analyze(all_stats: dict) -> str:
    
    # Call GPT with HIGH reasoning effort and MEDIUM verbosity.
    
    prompt = build_prompt(all_stats)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a professional Siege esports analyst. "
                           "You produce short, precise tactical intel."
            },
            {"role": "user", "content": prompt},
        ],
        reasoning_effort="high",   # <- high reasoning
        verbosity="medium",        # <- medium verbosity
    )

    return response.choices[0].message.content.strip()
