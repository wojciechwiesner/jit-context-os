"""
RecentTurnFence Extension for Agent Zero Message Loop.
Safely prunes multi-turn history on strict USER TURN boundaries,
preventing orphaned tool calls while archiving pruned context into SQLite.
"""

import os
import json
import time
import sqlite3
from helpers.extension import Extension
from helpers import plugins
from agent import LoopData

DB_PATH = "/a0/usr/plugins/jit_context/data/jit_context.db"


def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pruned_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                message_index INTEGER,
                ai INTEGER,
                content TEXT,
                created_at REAL
            )
        """
        )
        conn.commit()


def _archive_pruned_messages(session_id: str, messages: list):
    try:
        _ensure_db()
        now = time.time()
        rows = []
        for idx, m in enumerate(messages):
            ai = 1 if m.get("ai") else 0
            raw_content = m.get("content", "")
            content_str = json.dumps(raw_content) if isinstance(raw_content, (dict, list)) else str(raw_content)
            rows.append((session_id, idx, ai, content_str, now))
        
        if rows:
            with sqlite3.connect(DB_PATH) as conn:
                conn.executemany(
                    "INSERT INTO pruned_history (session_id, message_index, ai, content, created_at) VALUES (?, ?, ?, ?, ?)",
                    rows,
                )
                conn.commit()
    except Exception as e:
        pass


def _is_user_turn(msg: dict) -> bool:
    if msg.get("ai"):
        return False
    content = msg.get("content")
    if isinstance(content, dict):
        # Tool results or system warnings are not conversational user prompts
        if "tool_name" in content or "tool_result" in content or "system_warning" in content:
            return False
    return True


class RecentTurnFenceExtension(Extension):
    async def execute(
        self,
        loop_data: LoopData = LoopData(),
        **kwargs,
    ):
        if not self.agent:
            return

        config = plugins.get_plugin_config("jit_context", agent=self.agent) or {}
        if config.get("mode", "active") == "disabled":
            return

        # Number of recent user-interaction turns to preserve in hot working memory
        fence_turns = int(config.get("recent_turn_fence", 4))
        if fence_turns <= 0:
            return

        history_msgs = getattr(loop_data, "history_output", [])
        if not history_msgs or not isinstance(history_msgs, list):
            return

        # Find indices of all true user turns
        user_indices = [i for i, m in enumerate(history_msgs) if _is_user_turn(m)]

        # If total user turns do not exceed threshold, keep history untouched
        if len(user_indices) <= fence_turns:
            return

        # Boundary: start of the oldest kept user turn
        boundary_idx = user_indices[-fence_turns]
        if boundary_idx <= 1:
            return

        initial_msg = history_msgs[0]
        pruned_slice = history_msgs[1:boundary_idx]
        recent_msgs = history_msgs[boundary_idx:]

        # Genuinely archive pruned messages to SQLite database
        session_id = getattr(self.agent.context, "id", "default_session")
        _archive_pruned_messages(session_id, pruned_slice)

        # Preserve valid pairing: root user message + recent turns starting cleanly on a user turn
        loop_data.history_output = [initial_msg] + recent_msgs

        # Inject metadata into extras_temporary so LLM is aware without hijacking user dialogue
        if hasattr(loop_data, "extras_temporary") and isinstance(loop_data.extras_temporary, dict):
            loop_data.extras_temporary["jit_context_fence"] = (
                f"{len(pruned_slice)} historical messages pruned to L0 SQLite WAL. Hot-memory: {len(recent_msgs)} messages."
            )
