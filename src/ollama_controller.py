import threading

from ollama import Client
from PySide6.QtCore import QObject, Signal

from src.types import ErrorCode

SENTENCES_SPLITTERS = [".", "!", "?"]
MINIMUM_SENTENCE_LENGTH = 20


class OllamaController(QObject):
    # Signal emitted when a new story chunk is ready in async mode
    story_chunk = Signal(str)

    # contains the story chunk that is ready to be published, or None
    story_to_publish = None

    # contains the current story being generated
    story = ""

    def __init__(self, host: str):
        super().__init__()
        print("Hello OllamaController!")

        self.client = Client(host="{}:11434".format(host))

        # fast, very ad quality
        # self.story_model = "wizardlm2:7b"
        # self.story_model = "deepseek-r1"

        self.story_model = "MathiasB/llama3fr"
        self.story_model = "jobautomation/OpenEuroLLM-French"
        self.preprompt = "Tu es un conteur d'histoires pour enfants de 3 ans. Crée une histoire captivante et imaginative. L'histoire doit durer 3 minutes. Évidemment tu tutoies l'enfant et tu parles un français correct, bien qu'adapté à cet âge. Pas d'introduction, tu commences l'histoire tout de suite, et n'ajoute rien non plus une fois l'histoire terminée. Donne un titre, mais ne commence pas par 'il était une fois.'. Base toi sur le prompt suivant: "

    def stop(self):
        print("Stopping OllamaController...")
        # stop ollama generation if possible

    def text_to_seech(self, text):
        print(f"Converting text to speech: {text}")

    def refine_and_publish_story_if_ready(self):
        if self.refine_story():
            print("\nOllama > Story chunk ready: ", self.story_to_publish)
            self.story_chunk.emit(self.story_to_publish)
            self.story_to_publish = None

    def refine_story(self):
        if self.story_to_publish is not None:
            print(
                "There is already a story chunk ready to publish: {}".format(
                    self.story_to_publish
                )
            )
            raise Exception(
                "There is already a story chunk ready to publish {}".format(
                    self.story_to_publish
                )
            )

        for splitter in SENTENCES_SPLITTERS:
            if splitter in self.story and len(self.story) >= MINIMUM_SENTENCE_LENGTH:
                split_index = self.story.rfind(splitter) + 1
                self.story_to_publish = self.story[:split_index].strip()
                self.story = self.story[split_index:].strip()
                return True
        return False

    def generate_story(self, prompt, async_mode: bool = False):
        if self.running:
            print("Story generation already in progress.")
            return "", ErrorCode.BUSY
        if async_mode:
            self.generation_thread = threading.Thread(
                target=self.generate_story_worker, args=(prompt, True), daemon=True
            )
            self.generation_thread.start()
            return "", ErrorCode.SUCCESS
        else:
            return self.generate_story_worker(prompt)

    def generate_story_worker(self, prompt, async_mode: bool = False):
        self.running = True
        print(f"Getting story for prompt: {prompt}")
        self.story = ""
        for chunk in self.client.generate(
            model=self.story_model,
            prompt=self.preprompt + prompt,
            stream=True,
        ):
            # print(chunk)
            # print(type(chunk))
            print(".", end="", flush=True)
            story_chunk = chunk["response"]
            self.story += story_chunk
            if async_mode:
                self.refine_and_publish_story_if_ready()

        print("Ollama > Story generation complete: ", self.story)
        self.running = False
        return self.story, ErrorCode.SUCCESS
