import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(system_prompt: str, user_message: str, temperature: float = 0.2) -> str:
    """
    Low temperature (0.2) = factual, grounded answers.
    We don't want creative answers for industrial data.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=temperature,
        max_tokens=1024
    )
    return response.choices[0].message.content