from typing import Tuple, Literal

# 65-bit 可逆编码（scene:2, peer:32, seq:31）
_BITS_SCENE = 2
_BITS_PEER = 32
_BITS_SEQ = 31

_SHIFT_PEER = _BITS_SEQ
_SHIFT_SCENE = _BITS_SEQ + _BITS_PEER

_MASK_SEQ = (1 << _BITS_SEQ) - 1
_MASK_PEER = (1 << _BITS_PEER) - 1
_MASK_SCENE = (1 << _BITS_SCENE) - 1

_MAX_PEER = _MASK_PEER
_MAX_SEQ = _MASK_SEQ


# scene -> index 快速映射
def _scene_to_idx_fast(scene: Literal["friend", "group", "temp"]) -> int:
    if scene == "group":
        return 1
    if scene == "friend":
        return 0
    if scene == "temp":
        return 2
    raise ValueError("scene must be 'friend', 'group' or 'temp'")


def _idx_to_scene_fast(idx: int) -> Literal["friend", "group", "temp"]:
    if not isinstance(idx, int):
        raise TypeError("scene index must be int")
    if idx == 1:
        return "group"
    if idx == 2:
        return "temp"
    if idx == 0:
        return "friend"
    raise ValueError("invalid scene index")


def MsgtoId(scene: Literal["friend", "group", "temp"], peer_id: int, seq: int) -> int:
    """
    Milky scene, peer_id, seq to OneBot message_id

    :params "friend"|"group"|"temp" scene:
    """
    si = _scene_to_idx_fast(scene)
    if not isinstance(peer_id, int):
        raise TypeError("peer_id must be int")
    if not isinstance(seq, int):
        raise TypeError("seq must be int")
    if peer_id < 0 or seq < 0:
        raise ValueError("peer_id and seq must be non-negative")
    if peer_id > _MAX_PEER:
        raise ValueError(f"peer_id out of range 0..{_MAX_PEER}")
    if seq > _MAX_SEQ:
        raise ValueError(f"seq out of range 0..{_MAX_SEQ}")
    # 位拼接（全部整数操作）
    val = (si & _MASK_SCENE) << _SHIFT_SCENE
    val |= (peer_id & _MASK_PEER) << _SHIFT_PEER
    val |= seq & _MASK_SEQ
    return int(val)


def MsgtoSeq(msg_id: int) -> Tuple[str, int, int]:
    """
    OneBot message_id to Milky scene, peer_id, seq
    
    :return: "friend"|"group"|"temp", peer_id, seq
    """
    if not isinstance(msg_id, int):
        raise TypeError("msg_id must be int")
    if msg_id < 0:
        raise ValueError("msg_id must be non-negative")
    # 解出字段（全部位运算）
    scene_idx = (msg_id >> _SHIFT_SCENE) & _MASK_SCENE
    peer = (msg_id >> _SHIFT_PEER) & _MASK_PEER
    seq = msg_id & _MASK_SEQ
    scene = _idx_to_scene_fast(scene_idx)
    return scene, int(peer), int(seq)
