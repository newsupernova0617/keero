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
import time
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


class APILogHandler(logging.Handler):
    """API로 로그를 전송하는 핸들러 (배치 처리)"""

    def __init__(self, api_client, batch_size: int = 10, flush_interval: int = 5):
        """
        Args:
            api_client: CrawlerAPIClient 인스턴스
            batch_size: 배치 크기 (이 개수만큼 모이면 전송)
            flush_interval: 강제 전송 간격 (초)
        """
        super().__init__()
        self.api_client = api_client
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.buffer: List[Dict] = []
        self.last_flush_time = time.time()
        self._is_flushing = False

    def emit(self, record: logging.LogRecord):
        """로그를 버퍼에 추가하고 조건에 따라 전송"""
        if self._is_flushing:
            return  # 전송 중 발생하는 로그는 무시 (무한 루프 방지)

        try:
            # 예외 정보 포맷팅
            exc_text = None
            if record.exc_info:
                exc_text = "".join(traceback.format_exception(*record.exc_info))

            # extra 데이터 (있으면)
            extra_data = None
            if hasattr(record, "extra"):
                extra_data = json.dumps(record.extra)

            # 로그 데이터 구성
            log_data = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "level_no": record.levelno,
                "logger": record.name,
                "message": record.getMessage(),
                "function": record.funcName,
                "line_number": record.lineno,
                "exception": exc_text,
                "extra_data": extra_data
            }

            self.buffer.append(log_data)

            # 버퍼가 가득 차거나 시간이 지나면 전송
            current_time = time.time()
            if (len(self.buffer) >= self.batch_size or 
                current_time - self.last_flush_time >= self.flush_interval):
                self.flush()

        except Exception:
            self.handleError(record)

    def flush(self):
        """버퍼의 로그를 API로 전송"""
        if self.buffer and not self._is_flushing:
            self._is_flushing = True
            try:
                self.api_client.save_logs(self.buffer)
                self.buffer.clear()
                self.last_flush_time = time.time()
            except Exception as e:
                # 로그 전송 실패는 무시 (무한 루프 방지)
                # print 호출이 다시 logging을 유발하여 무한 루프가 생기지 않도록 주의
                pass
            finally:
                self._is_flushing = False

    def close(self):
        """핸들러 종료 시 남은 로그 전송"""
        self.flush()
        super().close()



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
