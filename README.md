# QQ Chatting 507-bot v2
## 简介
507-bot(v2)是基于[nonebot2](https://github.com/nonebot/nonebot2)和[ollama](https://github.com/ollama/ollama)的、使用onebotv11协议的聊天机器人，前身是[507-bot(v1)](https://github.com/ender507/QQ-Chatting-507-bot)。507bot以nonebot2插件的形式调用ollama接口，通过大语言模型，实现对用户请求的识别和回复。

507bot的核心内容为nonebot2的llm插件。通过nonebot2实现的不同协议，507bot理论上还可以用于QQ之外的多种聊天软件。

## 项目特点
- 构成相对简单，适合个人开发者管理维护：
  - 没有纷繁复杂的服务器/进程需要管理。只需要部署nonebot2、ollama，以及直接对接消息来源的协议端服务（如[NapCat](https://github.com/NapNeko/NapCatQQ)）即可使用
  - 侧重维护一个nonebot插件，通过大语言模型实现多种能力，而不是维护多个实现各自能力的插件
- 不怕烧钱：功能的实现均可以不使用第三方的付费功能（当然有需要也可以简单地改成使用），免费也能跑

## 注意
- 本项目的侧重点是实现基于大语言模型的聊天能力而非自动回复的机器人的实现。关于nonebot2和ollama服务的部署请参阅其各自的项目与文档
- `\the507botv2\plugins\llm\ollama_call\env.py`中是对llv模型于ollama连接的基本设置，可以按需调整