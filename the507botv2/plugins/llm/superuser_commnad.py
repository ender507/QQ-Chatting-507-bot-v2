from nonebot.permission import SUPERUSER
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.exception import MatcherException
from nonebot.log import logger

from .ollama_call import internal_call, env 

think = on_command("think", rule=to_me(), priority=9, permission=SUPERUSER)

@think.handle()
async def hanle_think():
    try:
        env.THINK = not env.THINK
        res = internal_call.translate(f"THNIK更新为({env.THINK})")
        if res == "":
            raise ValueError("translate return empty string")
        await think.finish(res)
    except MatcherException:
        raise
    except Exception as e:
        logger.error(e)
        msg = internal_call.defaultErrorMsg()
        if msg != "":
            await think.finish(msg)