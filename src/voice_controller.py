import requests  # type: ignore
from faster_whisper import WhisperModel
from nava import play


class VoiceController:
    def __init__(self, host: str):
        model_size = "large-v3"
        model_size = "turbo"

        # Run on GPU with FP16
        # self.model = WhisperModel(model_size, device="cuda", compute_type="float16")
        self.model = WhisperModel(model_size, device="cpu", compute_type="float32")
        self.tts_server = "{}:5002/api/tts".format(host)
        print("Hello VoiceController!")

    def text_to_speech(self, text: str, output_file: str):
        print("> TTS starting TTS request")
        headers = {
            # "text": text,
            # "speaker-id": "0",
            "language-id": "fr",
            "style-wav": "",
        }
        params = {"text": text}
        response = requests.post(self.tts_server, headers=headers, params=params)
        with open(output_file, "wb") as f:
            f.write(response.content)

        print(f" > TTS output saved to: {output_file}")

    def transcribe_audio(self, audio_file_path) -> str:
        # or run on GPU with INT8
        # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
        # or run on CPU with INT8
        # model = WhisperModel(model_size, device="cpu", compute_type="int8")

        segments, info = self.model.transcribe(
            audio_file_path, language="fr", beam_size=5
        )

        print(
            "Whisper > Detected language '%s' with probability %f"
            % (info.language, info.language_probability)
        )

        transcription = ""
        for segment in segments:
            print(
                "Whisper > [%.2fs -> %.2fs] %s"
                % (segment.start, segment.end, segment.text)
            )
            transcription = segment.text + " "

        print("Whisper > Transcription complete.")
        return transcription

    def play_audio_file(self, audio_file_path: str):
        print(f"Playing audio file: {audio_file_path}")
        play(audio_file_path, async_mode=True)
