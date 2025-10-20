from ollama import Client


class OllamaController:
    def __init__(self):
        print("Hello OllamaController!")

        self.client = Client(
            host="http://localhost:11434", headers={"x-some-header": "some-value"}
        )

    def text_to_seech(self, text):
        print(f"Converting text to speech: {text}")

    def speech_to_text(self, audio):
        print("Converting speech to text...")
