from typing import Any


async def process_milky_to_onebot(data: dict[str, Any]) -> dict[str, Any] | None:
    """
    在转发到 OneBot 之前处理 Milky 消息
    返回要发送给 OneBot 的消息，或返回 None 表示丢弃
    TODO: 实现转换逻辑
    """
    return data


async def process_onebot_to_milky(data: dict[str, Any]) -> dict[str, Any] | None:
    """
    在转发到 Milky 之前处理 OneBot 消息
    返回要发送给 Milky 的消息，或返回 None 表示丢弃
    TODO: 实现转换逻辑
    """
    return data
