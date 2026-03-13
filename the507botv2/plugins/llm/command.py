from nonebot import on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg
from nonebot.exception import MatcherException
from nonebot.permission import SUPERUSER

from .ollama_call import chat, env 

# priority越小优先级越高
normal_chat = on_command("", priority=10)
generate = on_command("generate", priority=9)
think = on_command("think", rule=to_me(), priority=9, permission=SUPERUSER)

@normal_chat.handle()
async def handle_normal_chat(event: Event, args: Message = CommandArg()):
    try:
        res = chat.chat(event.get_user_id(), args.extract_plain_text())
        if res is None:
            return
        if res.thinking is not None:
            logger.info(res.thinking)
            if env.THINK:
                await generate.send(f"思考一下：{res.thinking}")
        await normal_chat.finish(f"{res.content}")
    except MatcherException:
        raise
    except Exception as e:
        logger.error(e)
        msg = chat.errorMsg()
        if msg != "":
            await normal_chat.finish(msg)

@generate.handle()
async def handel_generate(args: Message = CommandArg()):
    try:
        res = chat.generate(args.extract_plain_text())
        if res is None:
            return
        if res.thinking is not None:
            logger.info(res.thinking)
            if env.THINK:
                await generate.send(f"思考一下：{res.thinking}")
        await generate.finish(f"{res.response}")
    except MatcherException:
        # nonebot的finish方法是通过raise MatcherException结束的。不要捕获这个错误
        raise
    except Exception as e:
        logger.error(e)
        msg = chat.errorMsg()
        if msg != "":
            await generate.finish(msg)

@think.handle()
async def hanle_think():
    try:
        env.THINK = not env.THINK
        await think.finish(f"THNIK更新为({env.THINK})")
    except MatcherException:
        raise
    except Exception as e:
        logger.error(e)
        msg = chat.errorMsg()
        if msg != "":
            await think.finish(msg)