import ollama
from . import env

client = ollama.Client(
    host = env.OLLAMA_HOST,
    timeout = env.TIMEOUT_SEC,
)

class LLMModel:
    name: str
    system_prompt: str
    default_error_msg: str

    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def get_name(self):
        return self.name
    
    def generate(self, prompt):
        return client.generate(
            model = self.name,
            system = self.system_prompt,
            think = env.THINK,
            prompt = prompt,
        )

    def chat(self, new_message, context):
        message = [{"role": "system", "content": self.system_prompt}] \
            + context \
            + [{"role": "user", "content": new_message}]
        print("message", message)
        return client.chat(
            model = self.name,
            messages = message,
            think = env.THINK,
        )
    
cur_model = LLMModel(env.DEFAULT_MODEL, env.DEFAULT_SYSTEM_PROMPT)
cur_model.default_error_msg = "出错了喵，看看日志喵"

def change_llm_model(model_name=env.DEFAULT_MODEL, system_prompt=env.DEFAULT_SYSTEM_PROMPT):
    global cur_model
    cur_model = LLMModel(model_name, system_prompt)
