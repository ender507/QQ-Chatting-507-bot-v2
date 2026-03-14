import ollama
from . import env

client = ollama.Client(
    host = env.OLLAMA_HOST,
    timeout = env.TIMEOUT_SEC,
)

class LLMModel:
    name: str
    system_prompt: str
    system_prompt_user: str
    system_prompt_internal: str

    def __init__(self, name, system_prompt, system_prompt_user="", system_prompt_internal=""):
        self.name = name
        self.system_prompt = system_prompt
        self.system_prompt_user = system_prompt_user
        self.system_prompt_internal = system_prompt_internal

    def get_name(self):
        return self.name
    
    def user_prompt(self):
        return self.system_prompt + self.system_prompt_user

    def internal_prompt(self):
        return self.system_prompt + self.system_prompt_internal

    def generate(self, prompt, from_user=True):
        system_prompt = self.user_prompt()
        if not from_user:
            system_prompt = self.internal_prompt()
        return client.generate(
            model = self.name,
            system = system_prompt,
            think = env.THINK,
            prompt = prompt,
        )

    def chat(self, new_message, context, from_user=True):
        system_prompt = self.user_prompt()
        if not from_user:
            system_prompt = self.internal_prompt()
        message = [{"role": "system", "content": system_prompt}] \
            + context \
            + [{"role": "user", "content": new_message}]
        print("message", message)
        return client.chat(
            model = self.name,
            messages = message,
            think = env.THINK,
        )
    
cur_model = LLMModel(env.DEFAULT_MODEL, env.DEFAULT_SYSTEM_PROMPT, env.DEFAULT_SYSTEM_PROMPT_USER, env.DEFAULT_SYSTEM_PROMPT_INSTERNAL)

def change_llm_model(model_name=env.DEFAULT_MODEL, system_prompt=env.DEFAULT_SYSTEM_PROMPT, \
    system_prompt_user=env.DEFAULT_SYSTEM_PROMPT_USER, system_prompt_internal=env.DEFAULT_SYSTEM_PROMPT_INSTERNAL):
    global cur_model
    cur_model = LLMModel(model_name, system_prompt, system_prompt_user, system_prompt_internal)
