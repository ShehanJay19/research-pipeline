import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client=Groq()

response = client.chat.completions.create(
    model ="llama-3.3-70b-versatile",
    max_tokens=200,
    messages=[
        {"role":"user","content":"Say hello and tell me some fact about animal name deer. "}
    ]
)
print(response.choices[0].message.content)
print("_______")
print(response.usage)