import json
from typing import Any, Awaitable, Callable
from nonebot import logger
import websockets
import httpx

from .config import ClientInfo


def clean_params(data: dict[str, Any]) -> dict[str, Any]:
    return {
        k: v
        for k, v in data.items()
        if not k.startswith("_") and k != "self" and v is not None
    }


async def relay(
    info: ClientInfo,
    src_ws: websockets.ClientConnection,
    dst_ws: websockets.ClientConnection,
    transform: Callable[[ClientInfo, dict[str, Any]], Awaitable[dict[str, Any] | None]],
    name: str,
):
    """
    从 src 读，经过 transform（可返回 None 表示丢弃），再发到 dst。
    支持 transform 返回三种格式：
      1. None -> 丢弃
      2. 普通 dict -> 发送到目标 dst_ws（原行为）
      3. 包含 "_action" == "drop" -> 显式丢弃
      4. 包含 "_action" == "callback" 且 "_url" -> 对该 URL 做 POST(JSON payload)，并把回调结果发回源端 src_ws（作为字符串或 JSON）
    transform 可以返回任意字典，推荐使用字段 "payload" 承载实际要发送的数据。
    """
    try:
        async for raw in src_ws:
            try:
                data = json.loads(raw)
            except Exception:
                logger.warning(f"{name}: 无法解析 JSON")
                logger.warning(f"{name}: {raw}")
                continue

            try:
                out = await transform(info, data)
                # None 或显式丢弃
                if out is None:
                    continue
                if isinstance(out, dict) and out.get("_action") == "drop":
                    continue

                # 回调逻辑: {"_action":"callback","_endpoint":"get_login_info",...}
                if isinstance(out, dict) and out.get("_action") == "callback":
                    endpoint = out.get("_endpoint")
                    payload = clean_params(out)
                    timeout = out.get("_timeout", 10)
                    if not endpoint:
                        logger.warning(f"{name}: callback 缺少 _url，忽略该消息")
                        continue
                    header = {"Content-Type": "application/json"}
                    try:
                        if info.access_token:
                            header["Authorization"] = f"Bearer {info.access_token}"
                        url = info.get_url(endpoint)
                        async with httpx.AsyncClient() as session:
                            resp = await session.post(
                                url,
                                json=payload,
                                timeout=timeout,
                                headers=header,
                            )
                            resp_json = await resp.json()
                            await src_ws.send(json.dumps(resp_json, ensure_ascii=False))
                    except Exception as e:
                        logger.exception(f"{name}: callback 请求失败: {e}")
                    continue

                # 默认：发送到目标（与原行为一致）
                await dst_ws.send(json.dumps(clean_params(out), ensure_ascii=False))

            except Exception as e:
                logger.exception(f"{name}: 处理/转发消息时出错: {e}")
    except websockets.exceptions.ConnectionClosedOK:
        logger.info(f"{name}: 连接正常关闭")
    except websockets.exceptions.ConnectionClosedError as e:
        logger.warning(f"{name}: 连接关闭错误: {e}")
    except Exception as e:
        logger.exception(f"{name}: relay 异常: {e}")
