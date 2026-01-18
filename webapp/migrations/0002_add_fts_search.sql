-- 1. FTS5 가상 테이블 생성 (Korean/Emoji 지원을 위해 unicode61 토크나이저 사용)
CREATE VIRTUAL TABLE IF NOT EXISTS posts_fts USING fts5(
    title,
    content,
    content='posts',
    content_rowid='id',
    tokenize='unicode61'
);

-- 2. 기존 데이터 동기화
INSERT INTO posts_fts(rowid, title, content)
SELECT id, title, content FROM posts;

-- 3. 데이터 변경 시 자동 동기화를 위한 트리거 생성
-- INSERT 트리거
CREATE TRIGGER IF NOT EXISTS posts_fts_insert AFTER INSERT ON posts BEGIN
    INSERT INTO posts_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
END;

-- UPDATE 트리거
CREATE TRIGGER IF NOT EXISTS posts_fts_update AFTER UPDATE ON posts BEGIN
    INSERT INTO posts_fts(posts_fts, rowid, title, content) VALUES ('delete', old.id, old.title, old.content);
    INSERT INTO posts_fts(rowid, title, content) VALUES (new.id, new.title, new.content);
END;

-- DELETE 트리거
CREATE TRIGGER IF NOT EXISTS posts_fts_delete AFTER DELETE ON posts BEGIN
    INSERT INTO posts_fts(posts_fts, rowid, title, content) VALUES ('delete', old.id, old.title, old.content);
END;
