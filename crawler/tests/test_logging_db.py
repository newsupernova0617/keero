"""
logging_db.py 모듈 테스트

SQLite 로깅 핸들러, 로그 검색, 정리 기능을 테스트합니다.
"""

import logging
import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from logging_db import LogQuery, SQLiteHandler, cleanup_old_logs, setup_logging


class TestSQLiteHandler:
    """SQLiteHandler 클래스 테스트"""

    def test_handler_creates_database(self):
        """핸들러가 데이터베이스를 생성하는지 확인"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        _ = SQLiteHandler(db_path=db_path)
        assert Path(db_path).exists()

        # 테이블 확인
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='logs'"
            )
            assert cursor.fetchone() is not None

        Path(db_path).unlink()

    def test_handler_saves_log_record(self):
        """로그 레코드가 DB에 저장되는지 확인"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        handler = SQLiteHandler(db_path=db_path)
        logger = logging.getLogger("test_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        # 로그 기록
        logger.info("Test message")

        # DB에서 확인
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("SELECT message, level FROM logs")
            row = cursor.fetchone()
            assert row is not None
            assert row[0] == "Test message"
            assert row[1] == "INFO"

        Path(db_path).unlink()

    def test_handler_saves_exception_info(self):
        """예외 정보가 저장되는지 확인"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        handler = SQLiteHandler(db_path=db_path)
        logger = logging.getLogger("test_exception")
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)

        # 예외 발생 및 로그
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.error("Error occurred", exc_info=True)

        # DB에서 확인
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("SELECT exception FROM logs WHERE level='ERROR'")
            row = cursor.fetchone()
            assert row is not None
            assert "ValueError: Test exception" in row[0]

        Path(db_path).unlink()


class TestLogQuery:
    """LogQuery 클래스 테스트"""

    @pytest.fixture
    def populated_db(self):
        """테스트용 로그가 채워진 DB"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        handler = SQLiteHandler(db_path=db_path)
        logger = logging.getLogger("test_query")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        # 다양한 로그 기록
        logger.debug("Debug message")
        logger.info("Info message 1")
        logger.info("Info message 2")
        logger.warning("Warning message")
        logger.error("Error message")

        yield db_path

        Path(db_path).unlink()

    def test_get_recent_logs(self, populated_db):
        """최근 로그 조회"""
        query = LogQuery(db_path=populated_db)
        logs = query.get_recent_logs(limit=10)

        assert len(logs) == 5
        # 최신 로그가 먼저 (역순)
        assert logs[0]["message"] == "Error message"
        assert logs[-1]["message"] == "Debug message"

    def test_get_errors(self, populated_db):
        """에러 로그만 조회"""
        query = LogQuery(db_path=populated_db)
        errors = query.get_errors()

        assert len(errors) == 1
        assert errors[0]["level"] == "ERROR"
        assert errors[0]["message"] == "Error message"

    def test_get_logs_by_level(self, populated_db):
        """특정 레벨의 로그 조회"""
        query = LogQuery(db_path=populated_db)
        info_logs = query.get_logs_by_level("INFO")

        assert len(info_logs) == 2
        assert all(log["level"] == "INFO" for log in info_logs)

    def test_search_logs(self, populated_db):
        """키워드로 로그 검색"""
        query = LogQuery(db_path=populated_db)
        results = query.search_logs("Info")

        assert len(results) == 2
        assert all("Info" in log["message"] for log in results)

    def test_get_stats(self, populated_db):
        """로그 통계 조회"""
        query = LogQuery(db_path=populated_db)
        stats = query.get_stats()

        assert stats["DEBUG"] == 1
        assert stats["INFO"] == 2
        assert stats["WARNING"] == 1
        assert stats["ERROR"] == 1

    def test_get_stats_by_logger(self, populated_db):
        """모듈별 통계 조회"""
        query = LogQuery(db_path=populated_db)
        stats = query.get_stats_by_logger()

        assert "test_query" in stats
        assert stats["test_query"]["INFO"] == 2


class TestCleanupOldLogs:
    """cleanup_old_logs 함수 테스트"""

    def test_cleanup_deletes_old_logs(self):
        """오래된 로그 삭제 확인"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        # DB 생성 및 오래된 로그 삽입
        with sqlite3.connect(db_path) as conn:
            conn.execute("""
                CREATE TABLE logs (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME,
                    level TEXT,
                    level_no INTEGER,
                    logger TEXT,
                    message TEXT,
                    function TEXT,
                    line_number INTEGER,
                    exception TEXT,
                    extra_data TEXT
                )
            """)

            # 35일 전 로그
            old_date = (datetime.now(timezone.utc) - timedelta(days=35)).isoformat()
            conn.execute(
                "INSERT INTO logs (timestamp, level, level_no, logger, message) VALUES (?, ?, ?, ?, ?)",
                (old_date, "INFO", 20, "test", "Old log"),
            )

            # 최근 로그
            recent_date = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "INSERT INTO logs (timestamp, level, level_no, logger, message) VALUES (?, ?, ?, ?, ?)",
                (recent_date, "INFO", 20, "test", "Recent log"),
            )
            conn.commit()

        # 30일 이상 된 로그 삭제
        deleted = cleanup_old_logs(db_path=db_path, days=30)

        assert deleted == 1

        # 남은 로그 확인
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM logs")
            assert cursor.fetchone()[0] == 1

        Path(db_path).unlink()


class TestSetupLogging:
    """setup_logging 함수 테스트"""

    def test_setup_logging_creates_handlers(self):
        """setup_logging이 핸들러를 생성하는지 확인"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        logger = setup_logging(db_path=db_path, level=logging.INFO, console=True)

        # 핸들러 확인 (SQLite + Console)
        assert len(logger.handlers) == 2

        # 타입 확인
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "SQLiteHandler" in handler_types
        assert "StreamHandler" in handler_types

        Path(db_path).unlink()

    def test_setup_logging_without_console(self):
        """콘솔 핸들러 없이 설정"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        logger = setup_logging(db_path=db_path, level=logging.INFO, console=False)

        # SQLite 핸들러만 있어야 함
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], SQLiteHandler)

        Path(db_path).unlink()
