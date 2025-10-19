from pathlib import Path
from nonebot import require
import asyncio
import sqlite3
from collections import OrderedDict

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store  # noqa: E402


plugin_data_dir: Path = store.get_plugin_data_dir()
_DB_PATH = plugin_data_dir / "message_map.db"
_SQLITE_TIMEOUT = 5.0
_CACHE_MAX = 10000  # 内存缓存最大条目数

# LRU 缓存（OrderedDict: 最近使用移动到末尾）
_seq_to_id: "OrderedDict[str, int]" = OrderedDict()
_id_to_seq: "OrderedDict[int, str]" = OrderedDict()
_cache_lock = asyncio.Lock()

# 防止并发重复插入：seq -> asyncio.Event（等待创建完成）
_inflight: dict[str, asyncio.Event] = {}
_inflight_lock = asyncio.Lock()


def _ensure_db_sync(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), timeout=_SQLITE_TIMEOUT)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode = WAL;")
        cur.execute("PRAGMA synchronous = NORMAL;")
        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS message_map (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_seq TEXT NOT NULL UNIQUE
            )
            """
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_full_seq ON message_map(full_seq);")
        conn.commit()
    finally:
        conn.close()


def _get_or_create_id_sync(db_path: Path, full_seq: str) -> int:
    conn = sqlite3.connect(str(db_path), timeout=_SQLITE_TIMEOUT)
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM message_map WHERE full_seq = ?", (full_seq,))
        if row := cur.fetchone():
            return int(row[0])
        try:
            cur.execute("INSERT INTO message_map (full_seq) VALUES (?)", (full_seq,))
            conn.commit()
            return int(cur.lastrowid)  # pyright: ignore[reportArgumentType]
        except sqlite3.IntegrityError:
            # 并发插入时可能触发 UNIQUE 约束，重查
            cur.execute("SELECT id FROM message_map WHERE full_seq = ?", (full_seq,))
            row = cur.fetchone()
            return int(row[0]) if row else 0
    finally:
        conn.close()


def _get_full_seq_by_id_sync(db_path: Path, onebot_id: int) -> str | None:
    conn = sqlite3.connect(str(db_path), timeout=_SQLITE_TIMEOUT)
    try:
        cur = conn.cursor()
        cur.execute("SELECT full_seq FROM message_map WHERE id = ?", (onebot_id,))
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


async def _ensure_db():
    await asyncio.to_thread(_ensure_db_sync, _DB_PATH)


def _cache_put(seq: str, onebot_id: int):
    # 同时写入两个方向的缓存，维持最大容量
    _seq_to_id[seq] = onebot_id
    _seq_to_id.move_to_end(seq)
    _id_to_seq[onebot_id] = seq
    _id_to_seq.move_to_end(onebot_id)
    # 简单裁剪（FIFO from oldest）
    while len(_seq_to_id) > _CACHE_MAX:
        old_seq, old_id = _seq_to_id.popitem(last=False)
        _id_to_seq.pop(old_id, None)
    while len(_id_to_seq) > _CACHE_MAX:
        old_id, old_seq = _id_to_seq.popitem(last=False)
        _seq_to_id.pop(old_seq, None)


async def message_id_2_seq(message_id: int) -> str:
    """
    将 onebot 的 message_id 转换为 seq, 未找到返回空字符串。
    """
    # 先查内存缓存
    async with _cache_lock:
        if seq := _id_to_seq.get(message_id):
            # LRU: 移到末尾
            _id_to_seq.move_to_end(message_id)
            _seq_to_id.move_to_end(seq)
            return seq

    # 查询 DB
    await _ensure_db()
    full_seq = await asyncio.to_thread(_get_full_seq_by_id_sync, _DB_PATH, message_id)
    if not full_seq:
        return ""
    async with _cache_lock:
        _cache_put(full_seq, message_id)
    return full_seq


async def seq_2_message_id(seq: str) -> int:
    """
    将 Milky 的 seq 转换为 onebot 的 message_id
    若不存在则创建映射并返回新 id
    使用内存缓存优先，避免频繁 IO
    """
    # 先查内存缓存
    async with _cache_lock:
        if onebot_id := _seq_to_id.get(seq):
            _seq_to_id.move_to_end(seq)
            _id_to_seq.move_to_end(onebot_id)
            return onebot_id

    # 去重并发创建：如果已有一个协程在创建同一 seq，等待它完成
    async with _inflight_lock:
        ev = _inflight.get(seq)
        if ev is None:
            ev = asyncio.Event()
            _inflight[seq] = ev
            creator = True
        else:
            creator = False

    if not creator:
        # 等待创建完成
        await ev.wait()
        async with _cache_lock:
            return _seq_to_id.get(seq, 0)

    try:
        # 执行 DB 查询/插入（在线程池）
        await _ensure_db()
        onebot_id = await asyncio.to_thread(_get_or_create_id_sync, _DB_PATH, seq)
        if onebot_id:
            async with _cache_lock:
                _cache_put(seq, onebot_id)
        return onebot_id
    finally:
        # 通知等待者并清理 inflight
        ev.set()
        async with _inflight_lock:
            _inflight.pop(seq, None)
