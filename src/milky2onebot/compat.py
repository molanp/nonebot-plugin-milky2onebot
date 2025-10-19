import asyncio
from nonebot.log import logger
import websockets


from .v11 import relay_v11, process_milky_to_v11, process_v11_to_milky
from .config import ClientInfo, onebot_base


async def start_v11(info: ClientInfo):
    """启动 Milky2OneBot_V11 适配器"""
    milky_url = info.ws_url()
    onebot_url = f"{onebot_base}v11"
    headers = info.get_headers()

    while True:
        try:
            # if onebot_url:
            # 同时连接 Milky 与 OneBot，建立双向转发
            async with websockets.connect(
                milky_url, additional_headers=headers
            ) as milky_ws, websockets.connect(onebot_url) as onebot_ws:
                logger.info(
                    f"已连接 Milky({milky_url}) 和 OneBot({onebot_url})，开始双向转发"
                )
                t1 = asyncio.create_task(
                    relay_v11(milky_ws, onebot_ws, process_milky_to_v11, "Milky→OneBot")
                )
                t2 = asyncio.create_task(
                    relay_v11(onebot_ws, milky_ws, process_v11_to_milky, "OneBot→Milky")
                )
                done, pending = await asyncio.wait(
                    {t1, t2}, return_when=asyncio.FIRST_EXCEPTION
                )
                for p in pending:
                    p.cancel()
        # else:
        #     # 仅连接 Milky
        #     async with websockets.connect(
        #         milky_url, additional_headers=headers
        #     ) as milky_ws:
        #         logger.info(
        #             f"已连接 Milky({milky_url})，onebot_ws 未配置，仅处理 Milky 消息"
        #         )
        #         try:
        #             async for raw in milky_ws:
        #                 try:
        #                     data = json.loads(raw)
        #                 except Exception:
        #                     logger.warning("无法解析 Milky 消息为 JSON，跳过")
        #                     continue
        #                 # 结果发送到 OneBot
        #                 await process_milky_to_onebot(data)
        #         except websockets.exceptions.WebSocketException as e:
        #             logger.error(f"{milky_url!s} 意外关闭: {e}")
        #         except Exception as e:
        #             logger.exception(f"处理 Milky 时发生错误，正在重连...: {e}")
        except Exception as e:
            logger.exception(f"连接发生错误，正在重连...: {e}")
            await asyncio.sleep(2)


async def start_v12(info: ClientInfo):
    """启动 Milky2OneBot_V12 适配器"""
    logger.warning("暂未实现 Milky2OneBot_V12 适配器")
    # await start_v11(info)
