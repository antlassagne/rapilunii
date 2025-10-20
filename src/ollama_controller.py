from ollama import Client


class OllamaController:
    def __init__(self):
        print("Hello OllamaController!")

        self.client = Client(
            host="http://localhost:11434", headers={"x-some-header": "some-value"}
        )
        self.story_model = "story-creator-7b"
        self.stt_model_size = "large-v3"
        # self.stt_model = WhisperModel(
        #     self.stt_model_size, device="cuda", compute_type="float16"
        # )
        self.preprompt = "You are a creative story writer. Create an engaging and imaginative story based on the following prompt: "

    def text_to_seech(self, text):
        print(f"Converting text to speech: {text}")

    def start_speech_to_text(self, audio):
        # segments, info = self.stt_model.transcribe("audio.mp3", beam_size=5)

        # print(
        #     "Detected language '%s' with probability %f"
        #     % (info.language, info.language_probability)
        # )

        # for segment in segments:
        #     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        pass

    def get_story(self, prompt):
        print(f"Getting story for prompt: {prompt}")
        # response = self.client.chat(
        #     model=self.story_model,
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": self.preprompt + prompt,
        #         },
        #     ],
        # )
