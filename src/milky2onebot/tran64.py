from typing import Literal, Tuple

# 支持两种 scen
# scene_bit: 0 = friend, 1 = group
_SCENE_TO_BIT = {"friend": 0, "group": 1}
_BIT_TO_SCENE: dict[int, Literal["friend", "group"]] = {0: "friend", 1: "group"}

# 位宽（共 64 位）
_BITS_SCENE = 1
_BITS_PEER = 32
_BITS_SEQ = 31

_MAX_PEER = (1 << _BITS_PEER) - 1  # 32-bit unsigned max
_MAX_SEQ = (1 << _BITS_SEQ) - 1  # <= 2147483647
_MAX_UINT64 = (1 << 64) - 1


def MsgtoId(scene: Literal["friend", "group"], peer_id: int, seq: int) -> int:
    """
    布局（高位->低位）： [scene:1][peer_id:32][seq:31]
    """
    if peer_id > _MAX_PEER or seq > _MAX_SEQ:
        raise ValueError("invalid seq or peer_id")
    scene_bit = _SCENE_TO_BIT.get(scene, 0) & 1
    val = (
        (scene_bit << (_BITS_PEER + _BITS_SEQ))
        | ((peer_id & _MAX_PEER) << _BITS_SEQ)
        | (seq & _MAX_SEQ)
    )
    if val < 0 or val > _MAX_UINT64:
        raise ValueError("invalid seq")
    return int(val)


def MsgtoSeq(msg_id: int) -> Tuple[Literal["friend", "group"], int, int]:
    """
    将 MsgtoId 返回的整数解包为 (scene, peer_id, seq)
    """
    if not isinstance(msg_id, int):
        raise TypeError("msg_id must be int")
    if msg_id < 0 or msg_id > _MAX_UINT64:
        raise ValueError("msg_id is invalid")
    scene_bit = (msg_id >> (_BITS_PEER + _BITS_SEQ)) & 0x1
    peer = (msg_id >> _BITS_SEQ) & _MAX_PEER
    seq = msg_id & _MAX_SEQ
    scene = _BIT_TO_SCENE[scene_bit]
    return scene, int(peer), int(seq)
