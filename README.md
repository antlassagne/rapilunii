## Lunii hacking

TODO

- [x] FreeCAD model --> A wood thingy will do
- [x] Hardware description (BOM)
- [x] Hardware soldering
- [ ] Displayed information design and implementation
- [ ] STT backend - running on a remote machine
- [ ] TTS backend - running on a remote machine
- [ ] Free conversation mode

## What is it

It's a small box that can tell stories. It's based on raspi zero with some addons and a little pieces of software.

### Harware:

- A Raspberry Pi zero 2 W (+ power)
- A KeyeStudio KS0314 hat ([ReSpeaker 2-Mic](https://docs.keyestudio.com/projects/KS0314/en/latest/))
- A speaker - which ever you can scavenge on any broken toy
- A display ([Waveshare 2inch LCD module](https://www.waveshare.com/wiki/2inch_LCD_Module))

### Software

- A controler running on the pi
- 3 services running on an external, more powerful, machine
  - Whisper to transcribe the voice input,
  - Ollama to generate a story from the transcription,
  - AllTalk to generate an voice back.

## Step 0: Ollama setting

```
sudo snap install ollama
sudo apt-get install portaudio19-dev ffmpeg
```

## Step 1: STT setting

```
git clone https://github.com/joshuaboniface/remote-faster-whisper
cd remote-faster-whisper
sudo ./setup.sh
```

## TTS setting

### Coqui (testing impl, not the right one)

Using https://github.com/coqui-ai/TTS

```bash
docker run --gpus all --restart always -p 5002:5002 --entrypoint /bin/bash ghcr.io/coqui-ai/tts-cpu
python3 TTS/server/server.py --model_name tts_models/fr/mai/tacotron2-DDC --use_cuda True
```

and configure the right server IP / port

### Alltalk, you are the chosen one

```
apt install libaio-dev espeak-ng
git clone -b alltalkbeta https://github.com/erew123/alltalk_tts
cd alltalk_tts
./atsetup.sh
./start_alltalk.sh
```

Then, use xTTS-v2, female voice 1 or 6

## STT setting

```
TODO, right now it's just a local whisper.
```

### Stack

```

```
