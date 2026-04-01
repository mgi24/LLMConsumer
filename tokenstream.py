from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

stream = client.chat.completions.create(
    model="Qwen/Qwen3.5-4B",
    messages=[
        {"role": "user", "content": "Ceritakan kisah pendek tentang robot"}
    ],
    stream=True  # 🔥 ini kuncinya
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)