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
    
    def generate(self, prompt):
        return client.generate(
            model = self.name,
            system = self.system_prompt,
            think = env.THINK,
            prompt = prompt,
        )

cur_model = LLMModel(env.DEFAULT_MODEL, env.DEFAULT_SYSTEM_PROMPT)
cur_model.default_error_msg = "出错了喵，看看日志喵"

def change_llm_model(model_name=env.DEFAULT_MODEL, system_prompt=env.DEFAULT_SYSTEM_PROMPT):
    global cur_model
    cur_model = LLMModel(model_name, system_prompt)
