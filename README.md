## Lunii hacking

TODO

- [ ] FreeCAD model
- [ ] Hardware description (fritzing?)
- [ ] Hardware soldering
- [ ] Displayed information design
- [ ] STT properly dockerized to run on a remote machine
- [ ] Better TTS quality (piper?)
- [ ] TTS properly dockerized to run on a remote machine
- [ ] Free conversation mode

## Step 0: Ollama setting

```
sudo snap install ollama
sudo apt-get install portaudio19-dev ffmpeg
```

## TTS setting

Using https://github.com/coqui-ai/TTS

```bash
docker run --gpus all --restart always -p 5002:5002 --entrypoint /bin/bash ghcr.io/coqui-ai/tts-cpu
python3 TTS/server/server.py --model_name tts_models/fr/mai/tacotron2-DDC --use_cuda True
```

and configure the right server IP / port

## STT setting

```
TODO, right now it's just a local whisper.
```

### Stack

```

```
