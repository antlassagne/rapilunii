from faster_whisper import WhisperModel


class VoiceController:
    def __init__(self):
        model_size = "large-v3"
        model_size = "turbo"

        # Run on GPU with FP16
        # self.model = WhisperModel(model_size, device="cuda", compute_type="float16")
        self.model = WhisperModel(model_size, device="cpu")
        print("Hello VoiceController!")

    def transcribe_audio(self, audio_file_path):
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
