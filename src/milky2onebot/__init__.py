import asyncio
import contextlib
from nonebot.plugin import PluginMetadata
from nonebot.log import logger
import nonebot

from milky2onebot.compat import start_v11
from .config import Config, plugin_config

__plugin_meta__ = PluginMetadata(
    name="Milk2Ob Plugin",
    description="一个将 Milky 协议转换到 Onebot 协议的 Nonebot 插件",
    usage="",
    config=Config,
    extra={
        "author": "molanp",
        "version": "0.0.1",
    },
)

V11 = False
tasks: set["asyncio.Task"] = set()
with contextlib.suppress(ValueError):
    V11 = bool(nonebot.get_adapter("OneBot V11"))

if not V11:
    logger.error("未找到 Onebot V11 适配器，已自动禁用插件")

else:
    for info in plugin_config.MILKY2OB_CLIENTS:
        logger.info("正在启动 OneBot V11 转换器")
        task = asyncio.create_task(start_v11(info))
        task.add_done_callback(tasks.discard)
        tasks.add(task)
