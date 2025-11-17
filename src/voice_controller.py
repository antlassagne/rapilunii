import threading
import time
from queue import Queue

import requests  # type: ignore
from faster_whisper import WhisperModel
from nava import play
from PySide6.QtCore import QObject, Signal


class VoiceController(QObject):
    tts_ready = Signal(str)

    # Queue for TTS worker
    tts_queue: Queue = Queue(maxsize=1000)
    # Queue for playback worker
    playback_queue: Queue = Queue(maxsize=1000)

    def __init__(self, host: str):
        super().__init__()
        model_size = "large-v3"
        model_size = "turbo"

        # Run on GPU with FP16
        # self.model = WhisperModel(model_size, device="cuda", compute_type="float16")
        self.model = WhisperModel(model_size, device="cpu", compute_type="float32")
        self.tts_server = "{}:5002/api/tts".format(host)

        self.running = True
        self.tts_thread = threading.Thread(target=self.tts_worker, daemon=True)
        self.tts_thread.start()
        self.playback_thread = threading.Thread(
            target=self.playback_worker, daemon=True
        )
        self.playback_thread.start()
        print("Hello VoiceController!")

    def __del__(self):
        self.stop()

    def stop(self):
        print("Stopping VoiceController...", end="", flush=True)
        self.running = False
        self.tts_thread.join()
        self.playback_thread.join()
        print(" done.")

    def push_to_tts_queue(self, text: str):
        print("> TTS queuing text: {}".format(text))
        self.tts_queue.put(text)
        print("> TTS queue size: {}".format(self.tts_queue.qsize()))

    def push_to_playback_queue(self, audio_file_path: str):
        print("> Playback queuing audio file: {}".format(audio_file_path))
        self.playback_queue.put(audio_file_path)
        print("> Playback queue size: {}".format(self.playback_queue.qsize()))

    def tts_worker(self):
        id = 0
        while self.running:
            if self.tts_queue.empty():
                time.sleep(1)
                continue

            text = self.tts_queue.get()
            id = id + 1
            print("> TTS worker got text: {}".format(text))
            output_file = "story_chunk_{}.wav".format(id)
            self.text_to_speech(text, output_file)
            self.tts_ready.emit(output_file)
            self.tts_queue.task_done()

    def playback_worker(self):
        while self.running:
            if self.playback_queue.empty():
                time.sleep(1)
                continue
            audio_file_path = self.playback_queue.get()
            print("> Playback worker got audio file: {}".format(audio_file_path))
            self.play_audio_file(audio_file_path)
            self.playback_queue.task_done()

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

    def speech_to_text(self, audio_file_path) -> str:
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
