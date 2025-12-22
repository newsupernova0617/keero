"""
SQLite 로깅 모듈

역할:
- Python logging 모듈과 통합하는 SQLite 핸들러
- 로그 검색 및 분석 기능
- 자동 로그 정리
"""

import json
import logging
import sqlite3
import traceback
from datetime import datetime
from typing import Dict, List, Optional


class SQLiteHandler(logging.Handler):
    """SQLite에 로그를 저장하는 커스텀 핸들러"""

    def __init__(self, db_path: str = "../data/logs.db"):
        """
        Args:
            db_path: 로그 데이터베이스 경로
        """
        super().__init__()
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """데이터베이스 및 테이블 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    level TEXT NOT NULL,
                    level_no INTEGER NOT NULL,
                    logger TEXT NOT NULL,
                    message TEXT NOT NULL,
                    function TEXT,
                    line_number INTEGER,
                    exception TEXT,
                    extra_data TEXT
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp)"
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_logger ON logs(logger)")
            conn.commit()

    def emit(self, record: logging.LogRecord):
        """로그 레코드를 SQLite에 저장"""
        try:
            # 예외 정보 포맷팅
            exc_text = None
            if record.exc_info:
                exc_text = "".join(traceback.format_exception(*record.exc_info))

            # extra 데이터 (있으면)
            extra_data = None
            if hasattr(record, "extra"):
                extra_data = json.dumps(record.extra)

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO logs (
                        timestamp, level, level_no, logger, message,
                        function, line_number, exception, extra_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        datetime.fromtimestamp(record.created).isoformat(),
                        record.levelname,
                        record.levelno,
                        record.name,
                        record.getMessage(),
                        record.funcName,
                        record.lineno,
                        exc_text,
                        extra_data,
                    ),
                )
                conn.commit()
        except Exception:
            self.handleError(record)


class LogQuery:
    """로그 검색 및 분석 유틸리티"""

    def __init__(self, db_path: str = "../data/logs.db"):
        """
        Args:
            db_path: 로그 데이터베이스 경로
        """
        self.db_path = db_path

    def get_recent_logs(self, limit: int = 100) -> List[Dict]:
        """
        최근 로그 조회

        Args:
            limit: 조회할 로그 개수

        Returns:
            로그 레코드 리스트
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_errors(self, since: Optional[datetime] = None) -> List[Dict]:
        """
        에러 로그 조회

        Args:
            since: 이 시간 이후의 에러만 조회 (선택)

        Returns:
            에러 로그 리스트
        """
        query = "SELECT * FROM logs WHERE level IN ('ERROR', 'CRITICAL')"
        params: List = []
        if since:
            query += " AND timestamp >= ?"
            params.append(since.isoformat())
        query += " ORDER BY timestamp DESC"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_logs_by_level(self, level: str, limit: int = 100) -> List[Dict]:
        """
        특정 레벨의 로그 조회

        Args:
            level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            limit: 조회할 로그 개수

        Returns:
            로그 레코드 리스트
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM logs WHERE level = ? ORDER BY timestamp DESC LIMIT ?",
                (level.upper(), limit),
            )
            return [dict(row) for row in cursor.fetchall()]

    def search_logs(self, keyword: str, limit: int = 100) -> List[Dict]:
        """
        메시지 키워드로 로그 검색

        Args:
            keyword: 검색 키워드
            limit: 조회할 로그 개수

        Returns:
            매칭된 로그 리스트
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM logs WHERE message LIKE ? ORDER BY timestamp DESC LIMIT ?",
                (f"%{keyword}%", limit),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, int]:
        """
        레벨별 로그 통계

        Returns:
            레벨별 로그 개수 딕셔너리
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT level, COUNT(*) as count
                FROM logs
                GROUP BY level
            """
            )
            return {row[0]: row[1] for row in cursor.fetchall()}

    def get_stats_by_logger(self) -> Dict[str, Dict[str, int]]:
        """
        모듈별, 레벨별 로그 통계

        Returns:
            모듈별 레벨별 로그 개수
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT logger, level, COUNT(*) as count
                FROM logs
                GROUP BY logger, level
                ORDER BY logger, level
            """
            )
            result: Dict[str, Dict[str, int]] = {}
            for logger, level, count in cursor.fetchall():
                if logger not in result:
                    result[logger] = {}
                result[logger][level] = count
            return result


def cleanup_old_logs(db_path: str = "../data/logs.db", days: int = 30) -> int:
    """
    오래된 로그 삭제

    Args:
        db_path: 로그 데이터베이스 경로
        days: 보관할 일수 (이보다 오래된 로그 삭제)

    Returns:
        삭제된 로그 개수
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            """
            DELETE FROM logs
            WHERE timestamp < datetime('now', ?)
        """,
            (f"-{days} days",),
        )
        deleted_count = cursor.rowcount
        conn.commit()
        return deleted_count


def setup_logging(
    db_path: str = "../data/logs.db",
    level: int = logging.INFO,
    console: bool = True,
) -> logging.Logger:
    """
    로깅 설정 헬퍼 함수

    Args:
        db_path: 로그 데이터베이스 경로
        level: 로깅 레벨
        console: 콘솔 출력 여부

    Returns:
        설정된 루트 로거
    """
    # 루트 로거 가져오기
    logger = logging.getLogger()
    logger.setLevel(level)

    # 기존 핸들러 제거 (중복 방지)
    logger.handlers.clear()

    # 포맷 설정
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # SQLite 핸들러 추가
    sqlite_handler = SQLiteHandler(db_path=db_path)
    sqlite_handler.setLevel(level)
    sqlite_handler.setFormatter(formatter)
    logger.addHandler(sqlite_handler)

    # 콘솔 핸들러 추가 (선택)
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
