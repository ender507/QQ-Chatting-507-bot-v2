from nonebot import on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.exception import MatcherException

import the507botv2.plugins.llm.ollama_call.chat as chat
import the507botv2.plugins.llm.ollama_call.env as env

# priority越小优先级越高
generate = on_command("", priority=10)
think = on_command("think", rule=to_me(), priority=9)

@generate.handle()
async def _(args: Message = CommandArg()):
    try:
        res = chat.generate(args.extract_plain_text())
        if res is None:
            return
        # 对Qwen之类的模型，就算THINK=false也会触发思考。总之打印出来看看
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
async def _():
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