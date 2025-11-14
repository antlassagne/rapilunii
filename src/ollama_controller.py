from ollama import Client

from src.types import ErrorCode


class OllamaController:
    def __init__(self, host: str):
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

    def generate_story(self, prompt):
        print(f"Getting story for prompt: {prompt}")
        story = ""
        for chunk in self.client.generate(
            model=self.story_model,
            prompt=self.preprompt + prompt,
            stream=True,
        ):
            # print(chunk)
            # print(type(chunk))
            print(".", end="", flush=True)
            story += chunk["response"]
        print("Ollama > Story generation complete: ", story)
        return story, ErrorCode.SUCCESS
