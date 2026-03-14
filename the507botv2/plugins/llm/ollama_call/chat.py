from nonebot.log import logger
from . import model, context

# 单次调用llm生成回复，不带任何上下文信息
def generate(message):
    try:
        res = model.cur_model.generate(message)
        return res
    except Exception as e:
        logger.error(e)
    return None

# 附带上下文的聊天
def chat(user_id, message):
    try:
        ctx = context.contextManager.get(user_id)
        logger.info(f"context of user({user_id})'s length is: {len(ctx)}")
        res = model.cur_model.chat(message, ctx)
        context.contextManager.append(user_id, message, res.message.content)
        return res.message
    except Exception as e:
        logger.error(e)
    return None

if __name__ == "__main__":
    res = generate("你好")
    