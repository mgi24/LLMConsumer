# LLMConsumer
Waste LLM Token for my projects!

## Run (image + prompt)

This repo assumes you already have an OpenAI-compatible server running at `http://localhost:8000/v1`.

1) Install deps

```bash
pip install -r requirements.txt
```

2) Set a vision-capable model name (example)

```bash
setx OPENAI_MODEL "<your-vision-model>"
```

3) Send `plate.jpg` with prompt "analisa apa yang ada di gambar ini"

```bash
python imagethink.py --image plate.jpg --prompt "analisa apa yang ada di gambar ini"
```

Optional:

```bash
python imagethink.py --image plate.jpg --prompt "analisa apa yang ada di gambar ini" --stream
```
