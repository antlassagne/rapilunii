import logging
import threading
import time
from enum import Enum
from queue import Queue

import requests  # type: ignore
from faster_whisper import WhisperModel
from nava import play
from PyQt6.QtCore import QObject
from PyQt6.QtCore import pyqtSignal as Signal

from laboite.src.alltalk_controller import AllTalkController


class TTS_IMPL(Enum):
    ALLTALK = 0
    COQUI = 1


class STT_IMPL(Enum):
    FAST_WHISPER = 0
    REMOTE_FASTER_WHISPER = 1


class VoiceController(QObject):
    tts_ready = Signal(str)
    job_done = Signal

    tts_mode = TTS_IMPL.ALLTALK  # alltalk
    stt_mode = STT_IMPL.REMOTE_FASTER_WHISPER

    # Queue for TTS worker
    tts_queue: Queue = Queue(maxsize=1000)
    # Queue for playback worker
    playback_queue: Queue = Queue(maxsize=1000)

    def __init__(self, host: str):
        super().__init__()

        self.received_final_chunk = False
        self.received_final_chunk_to_play = False

        if self.stt_mode == STT_IMPL.FAST_WHISPER:
            model_size = "large-v3"
            model_size = "turbo"
            # Run on GPU with FP16
            self.model = WhisperModel(model_size, device="cpu", compute_type="float32")
            # or run on GPU with INT8
            # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
            # or run on CPU with INT8
            # model = WhisperModel(model_size, device="cpu", compute_type="int8")

        self.coqui_tts_server = "{}:5002/api/tts".format(host)
        self.remote_fast_whisper_stt_server = "{}:9876/api/v0/transcribe".format(host)

        self.alltalk_controller = AllTalkController()

        self.running = True
        self.tts_thread = threading.Thread(target=self.tts_worker, daemon=True)
        self.tts_thread.start()
        self.playback_thread = threading.Thread(
            target=self.playback_worker, daemon=True
        )
        self.playback_thread.start()
        logging.info("Hello VoiceController!")

    def __del__(self):
        self.stop()

    def reset(self):
        self.received_final_chunk = False
        self.received_final_chunk_to_play = False

    def stop(self):
        logging.info("Stopping VoiceController...")
        self.running = False
        self.tts_thread.join()
        self.playback_thread.join()
        logging.info(" done.")

    def signal_received_final_text_chunk(self):
        self.received_final_chunk = True

    def push_to_tts_queue(self, text: str):
        logging.info("> TTS queuing text: {}".format(text))
        self.tts_queue.put(text)
        logging.info("> TTS queue size: {}".format(self.tts_queue.qsize()))

    def push_to_playback_queue(self, audio_file_path: str, final: bool):
        logging.info("> Playback queuing audio file: {}".format(audio_file_path))
        self.playback_queue.put(audio_file_path)
        self.received_final_chunk_to_play = True
        logging.info("> Playback queue size: {}".format(self.playback_queue.qsize()))

    def tts_worker(self):
        id = 0
        while self.running:
            if self.tts_queue.empty():
                time.sleep(1)
                if self.received_final_chunk:
                    self.received_final_chunk_to_play = True
                continue

            text = self.tts_queue.get()
            id = id + 1
            logging.info("> TTS worker got text: {}".format(text))
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
            logging.info("> Playback worker got audio file: {}".format(audio_file_path))
            self.play_audio_file(audio_file_path)
            self.playback_queue.task_done()

            # was this the very final thing to do for this whole stt => generation => tts?
            if self.playback_queue.empty():
                if self.received_final_chunk_to_play:
                    # this was the final thing to do.
                    self.job_done.emit()
                    self.reset()

    def text_to_speech(self, text: str, output_file: str):
        logging.info("> TTS starting TTS request")

        if self.tts_mode == TTS_IMPL.ALLTALK:
            _ = self.alltalk_controller.generate_tts(
                text,
                character_voice="female_06.wav",
                language="fr",
                output_file_name="test_output",
                output_file=output_file,
            )

        else:
            headers = {
                # "text": text,
                # "speaker-id": "0",
                "language-id": "fr",
                "style-wav": "",
            }
            params = {"text": text}
            response = requests.post(
                self.coqui_tts_server, headers=headers, params=params
            )
            with open(output_file, "wb") as f:
                f.write(response.content)

        logging.info(f" > TTS output saved to: {output_file}")

    def speech_to_text(self, audio_file_path) -> str:
        if self.stt_mode == STT_IMPL.FAST_WHISPER:
            segments, info = self.model.transcribe(
                audio_file_path, language="fr", beam_size=5
            )

            transcription = ""
            for segment in segments:
                logging.info(
                    "Whisper > [%.2fs -> %.2fs] %s"
                    % (segment.start, segment.end, segment.text)
                )
                transcription = segment.text + " "

            logging.info("Whisper > Transcription complete.")
            return transcription
        elif self.stt_mode == STT_IMPL.REMOTE_FASTER_WHISPER:
            files = {"audio_file": open(audio_file_path, "rb")}
            r = requests.post(self.remote_fast_whisper_stt_server, files=files)
            logging.info(f"{r.status_code}: {r.json()}")
        return "NOT IMPLEMENTED"

    def play_audio_file(self, audio_file_path: str):
        logging.info(f"Playing audio file: {audio_file_path}")
        play(audio_file_path, async_mode=False)
        time.sleep(1)  # small delay to ensure smooth playback
