
import argparse
import base64
import mimetypes
import os
import sys

from openai import OpenAI


def _guess_mime_type(path: str) -> str:
	mime, _ = mimetypes.guess_type(path)
	return mime or "application/octet-stream"


def _data_url_for_image(path: str) -> str:
	with open(path, "rb") as f:
		raw = f.read()
	b64 = base64.b64encode(raw).decode("ascii")
	mime = _guess_mime_type(path)
	return f"data:{mime};base64,{b64}"


def main(argv: list[str]) -> int:
	parser = argparse.ArgumentParser(description="Send an image + prompt to an OpenAI-compatible server")
	parser.add_argument("--image", default="plate.jpg", help="Path to image file (default: plate.jpg)")
	parser.add_argument(
		"--prompt",
		default="analisa apa yang ada di gambar ini",
		help='Prompt text (default: "analisa apa yang ada di gambar ini")',
	)
	parser.add_argument(
		"--model",
		default=os.getenv("OPENAI_MODEL", ""),
		help="Model name (or set OPENAI_MODEL)",
	)
	parser.add_argument(
		"--base-url",
		default=os.getenv("OPENAI_BASE_URL", "http://localhost:8000/v1"),
		help="OpenAI-compatible base URL (default: http://localhost:8000/v1)",
	)
	parser.add_argument(
		"--api-key",
		default=os.getenv("OPENAI_API_KEY", "EMPTY"),
		help="API key (or set OPENAI_API_KEY; default: EMPTY)",
	)
	parser.add_argument("--stream", action="store_true", help="Stream output tokens")
	args = parser.parse_args(argv)

	if not args.model:
		print(
			"ERROR: --model is required for most servers (or set OPENAI_MODEL).\n"
			"Tip: use a vision-capable model (e.g. Qwen2-VL, LLaVA, etc.)",
			file=sys.stderr,
		)
		return 2

	if not os.path.exists(args.image):
		print(f"ERROR: image file not found: {args.image}", file=sys.stderr)
		return 2

	client = OpenAI(base_url=args.base_url, api_key=args.api_key)

	image_url = _data_url_for_image(args.image)
	messages = [
		{
			"role": "user",
			"content": [
				{"type": "text", "text": args.prompt},
				{"type": "image_url", "image_url": {"url": image_url}},
			],
		}
	]

	stream = client.chat.completions.create(
		model=args.model,
		messages=messages,
		stream=args.stream,
	)

	if args.stream:
		for chunk in stream:
			delta = chunk.choices[0].delta
			if delta and delta.content:
				print(delta.content, end="", flush=True)
		print()
		return 0

	content = stream.choices[0].message.content
	print(content)
	return 0


if __name__ == "__main__":
	raise SystemExit(main(sys.argv[1:]))
