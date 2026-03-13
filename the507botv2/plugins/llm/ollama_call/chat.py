from nonebot.log import logger
from . import model

# 单次调用llm生成回复，不带任何上下文信息
def generate(prompt):
    try:
        res = model.cur_model.generate(prompt)
        return res
    except Exception as e:
        logger.error(e)
    return None

def errorMsg():
    return model.cur_model.default_error_msg

if __name__ == "__main__":
    res = generate("你好")
    