from nonebot.log import logger
from . import model

def defaultErrorMsg():
    return translate("发生错误了，请查看日志")

def translate(msg):
    try:
        res =  model.cur_model.generate(msg, False)
        return res.response
    except Exception as e:
        logger.error("failed to transplate msg({msg}) by llm: {e}")
    return ""