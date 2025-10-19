import json
from typing import Any, Awaitable, Callable
from nonebot import logger
import websockets


async def _relay(
    src_ws: websockets.ClientConnection,
    dst_ws: websockets.ClientConnection,
    transform: Callable[[dict[str, Any]], Awaitable[dict[str, Any]|None]],
    name: str,
):
    """
    从 src 读，经过 transform（可返回 None 表示丢弃），再发到 dst。
    """
    try:
        async for raw in src_ws:
            try:
                data = json.loads(raw)
            except Exception:
                logger.warning(f"{name}: 无法解析 JSON，直接转发原始文本")
                # await dst_ws.send(raw)
                continue

            try:
                out = await transform(data)
                if out is None:
                    continue
                await dst_ws.send(json.dumps(out, ensure_ascii=False))
            except Exception as e:
                logger.exception(f"{name}: 处理/转发消息时出错: {e}")
    except websockets.exceptions.ConnectionClosedOK:
        logger.info(f"{name}: 连接正常关闭")
    except websockets.exceptions.ConnectionClosedError as e:
        logger.warning(f"{name}: 连接关闭错误: {e}")
    except Exception as e:
        logger.exception(f"{name}: relay 异常: {e}")
