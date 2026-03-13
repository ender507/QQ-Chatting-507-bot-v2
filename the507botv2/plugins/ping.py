from nonebot import on_command
import requests

ping = on_command("ping", block=True)

@ping.handle()
async def _():
    await ping.finish("pong")