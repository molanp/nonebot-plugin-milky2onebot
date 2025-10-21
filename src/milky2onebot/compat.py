import asyncio
from nonebot.log import logger
import websockets

from .process import process_milky_to_onebot, process_onebot_to_milky


from .relay import relay
from .config import ClientInfo, system_config


async def start_v11(info: ClientInfo):
    """启动 Milky2OneBot_V11 适配器"""
    milky_url = info.ws_url()
    onebot_url = f"ws://{system_config.host}:{system_config.port}/onebot/v11"
    milky_headers = (
        {"Authorization": f"Bearer {info.access_token}"} if info.access_token else {}
    )
    onebot_headers = (
        {"Authorization": f"Bearer {system_config.ONEBOT_ACCESS_TOKEN}"}
        if system_config.ONEBOT_ACCESS_TOKEN
        else {}
    )
    if not onebot_headers and system_config.ONEBOT_V11_ACCESS_TOKEN:
        onebot_headers = {
            "Authorization": f"Bearer {system_config.ONEBOT_V11_ACCESS_TOKEN}"
        }

    while True:
        try:
            async with websockets.connect(
                milky_url, additional_headers=milky_headers
            ) as milky_ws, websockets.connect(
                onebot_url, additional_headers=onebot_headers
            ) as onebot_ws:
                logger.info(
                    f"已连接 Milky({milky_url}) 和 OneBot({onebot_url})，开始双向转发"
                )
                t1 = asyncio.create_task(
                    relay(
                        info,
                        milky_ws,
                        onebot_ws,
                        process_milky_to_onebot,
                        "Milky2OneBot",
                    )
                )
                t2 = asyncio.create_task(
                    relay(
                        info,
                        onebot_ws,
                        milky_ws,
                        process_onebot_to_milky,
                        "OneBot2Milky",
                    )
                )
                done, pending = await asyncio.wait(
                    {t1, t2}, return_when=asyncio.FIRST_EXCEPTION
                )
                for p in pending:
                    p.cancel()
        except Exception as e:
            logger.exception(f"连接发生错误，正在重连...: {e}")
            await asyncio.sleep(2)
