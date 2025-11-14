## Lunii hacking

## Step 0: Ollama setting

```
sudo snap install ollama
sudo apt-get install portaudio19-dev ffmpeg
```

## TTS setting

Using https://github.com/coqui-ai/TTS

````
docker run --gpus all --rm -it -p 5002:5002 --entrypoint /bin/bash ghcr.io/coqui-ai/tts-cpu
python3 TTS/server/server.py --model_name tts_models/fr/mai/tacotron2-DDC --use_cuda True
and configure the right server IP / port```

Then the function is like this
````

@app.route("/api/tts", methods=["GET", "POST"])
def tts():
with lock:
text = request.headers.get("text") or request.values.get("text", "")
speaker_idx = request.headers.get("speaker-id") or request.values.get("speaker_id", "")
language_idx = request.headers.get("language-id") or request.values.get("language_id", "")
style_wav = request.headers.get("style-wav") or request.values.get("style_wav", "")
style_wav = style_wav_uri_to_dict(style_wav)

```
    print(f" > Model input: {text}")
    print(f" > Speaker Idx: {speaker_idx}")
    print(f" > Language Idx: {language_idx}")
    wavs = synthesizer.tts(text, speaker_name=speaker_idx, language_name=language_idx, style_wav=style_wav)
    out = io.BytesIO()
    synthesizer.save_wav(wavs, out)
return send_file(out, mimetype="audio/wav")
```

```


### Stack

```

```
```
