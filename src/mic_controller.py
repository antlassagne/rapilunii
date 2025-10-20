import struct
import threading
import wave

from pvrecorder import PvRecorder


class MicController:
    prompt: str = ""

    def __init__(self):
        super().__init__()
        devices = PvRecorder.get_available_devices()
        for i in range(len(devices)):
            print("index: %d, device name: %s" % (i, devices[i]))
        print("Hello MicController!")

    def start_listening(self):
        print("Started listening for prompt...")
        self.running = True
        self.listener_thread = threading.Thread(target=self.run, daemon=True)
        self.listener_thread.start()

    def stop(self):
        self.running = False
        self.listener_thread.join()

    def run(self):
        # Create a temporary file to store the recorded audio (this will be deleted once we've finished transcription)
        # temp_file = tempfile.NamedTemporaryFile(suffix=".wav")
        # print(f"Recording audio to temporary file: {temp_file.name}")
        temp_file = "temp_audio.wav"

        recorder = PvRecorder(device_index=-1, frame_length=512)
        audio = []

        recorder.start()

        while self.running:
            frame = recorder.read()
            audio.extend(frame)

        recorder.stop()
        print("Finished recording audio - saving file")
        with wave.open(temp_file, "w") as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
        recorder.delete()

        # Open the wave file for writing
