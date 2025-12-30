import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { env } from '$env/dynamic/private';
import Database from 'better-sqlite3';

/**
 * Crawler API - 로그 저장 엔드포인트
 * 
 * POST /api/crawler/logs
 * 
 * Request Body:
 * {
 *   "logs": [
 *     {
 *       "timestamp": "2025-12-27T17:30:00",
 *       "level": "INFO",
 *       "level_no": 20,
 *       "logger": "crawler.scraper",
 *       "message": "Crawling started",
 *       "function": "crawl_site",
 *       "line_number": 45,
 *       "exception": null,
 *       "extra_data": null
 *     }
 *   ]
 * }
 */

const LOG_DB_PATH = '../data/logs.db';

export const POST: RequestHandler = async ({ request }) => {
	try {
		// 1. API Key 검증
		const apiKey = request.headers.get('X-API-Key');
		const expectedKey = env.CRAWLER_API_KEY;

		if (!expectedKey) {
			console.error('❌ CRAWLER_API_KEY not configured');
			return json({ error: 'Server configuration error' }, { status: 500 });
		}

		if (!apiKey || apiKey !== expectedKey) {
			console.warn('⚠️ Unauthorized API request');
			return json({ error: 'Unauthorized' }, { status: 401 });
		}

		// 2. 요청 데이터 파싱
		const body = await request.json();
		const { logs } = body;

		if (!logs || !Array.isArray(logs) || logs.length === 0) {
			return json({ error: 'Invalid request: missing logs array' }, { status: 400 });
		}

		// 3. 로그 저장
		const result = await saveLogs(logs);

		if (!result.success) {
			return json({ error: result.error }, { status: 500 });
		}

		return json({
			success: true,
			logs_saved: result.logsSaved
		});

	} catch (error) {
		console.error('❌ API Error:', error);
		return json({ 
			error: 'Internal server error',
			message: error instanceof Error ? error.message : 'Unknown error'
		}, { status: 500 });
	}
};

/**
 * 로그 배치 저장
 */
async function saveLogs(
	logs: Array<{
		timestamp: string;
		level: string;
		level_no: number;
		logger: string;
		message: string;
		function?: string;
		line_number?: number;
		exception?: string | null;
		extra_data?: string | null;
	}>
): Promise<{
	success: boolean;
	logsSaved?: number;
	error?: string;
}> {
	let sqlite: Database.Database | null = null;

	try {
		// 디렉토리 자동 생성
		const { mkdirSync, existsSync } = await import('fs');
		const { dirname } = await import('path');
		
		const dbDir = dirname(LOG_DB_PATH);
		if (!existsSync(dbDir)) {
			mkdirSync(dbDir, { recursive: true });
		}

		// logs.db 연결
		sqlite = new Database(LOG_DB_PATH);

		// WAL 모드 설정
		sqlite.pragma('journal_mode = WAL');
		sqlite.pragma('synchronous = NORMAL');

		// 테이블 생성 (없으면)
		sqlite.exec(`
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
		`);

		// 인덱스 생성 (없으면)
		sqlite.exec(`
			CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp);
			CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level);
			CREATE INDEX IF NOT EXISTS idx_logs_logger ON logs(logger);
		`);

		// 트랜잭션으로 배치 삽입
		const insert = sqlite.prepare(`
			INSERT INTO logs (
				timestamp, level, level_no, logger, message,
				function, line_number, exception, extra_data
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
		`);

		const transaction = sqlite.transaction((logEntries: typeof logs) => {
			for (const log of logEntries) {
				insert.run(
					log.timestamp,
					log.level,
					log.level_no,
					log.logger,
					log.message,
					log.function || null,
					log.line_number || null,
					log.exception || null,
					log.extra_data || null
				);
			}
		});

		transaction(logs);

		sqlite.close();

		return {
			success: true,
			logsSaved: logs.length
		};

	} catch (error) {
		if (sqlite) {
			try {
				sqlite.close();
			} catch {
				// Ignore close errors
			}
		}

		console.error('❌ Database error:', error);
		return {
			success: false,
			error: error instanceof Error ? error.message : 'Unknown database error'
		};
	}
}
