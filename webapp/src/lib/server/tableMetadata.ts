// Table metadata definitions

export interface TableMetadata {
	name: string
	displayName: string
	description: string
	icon: string
	schema: unknown
	columns: ColumnMetadata[]
	primaryKey: string
	canCreate: boolean
	canEdit: boolean
	canDelete: boolean
}

export interface ColumnMetadata {
	key: string
	label: string
	type: 'text' | 'number' | 'date' | 'boolean' | 'badge' | 'textarea' | 'select'
	sortable: boolean
	searchable: boolean
	required: boolean
	editable: boolean
	width?: string
	options?: { value: string; label: string }[]
	placeholder?: string
	maxLength?: number
}

export const tableMetadata: Record<string, TableMetadata> = {
	posts: {
		name: 'posts',
		displayName: '게시글',
		description: '크롤링된 게시글 데이터',
		icon: 'FileText',
		schema: null, // Will be set dynamically
		primaryKey: 'id',
		canCreate: true,
		canEdit: true,
		canDelete: true,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'site_name', label: '사이트', type: 'badge', sortable: true, searchable: true, required: true, editable: true, width: '120px', options: [
				{ value: 'FMKorea', label: 'FMKorea' },
				{ value: 'DCInside', label: 'DCInside' },
				{ value: 'Ruliweb', label: 'Ruliweb' },
				{ value: 'Instiz', label: 'Instiz' },
				{ value: 'TheQoo', label: 'TheQoo' },
				{ value: 'MLB Park', label: 'MLB Park' },
				{ value: 'SLR Club', label: 'SLR Club' },
				{ value: 'Ppomppu', label: 'Ppomppu' }
			]},
			{ key: 'title', label: '제목', type: 'text', sortable: true, searchable: true, required: true, editable: true, maxLength: 500 },
			{ key: 'content', label: '내용 (텍스트)', type: 'textarea', sortable: false, searchable: true, required: false, editable: true },
			{ key: 'content_html', label: '내용 (HTML)', type: 'textarea', sortable: false, searchable: false, required: false, editable: true },
			{ key: 'content_hash', label: '콘텐츠 해시', type: 'text', sortable: false, searchable: true, required: false, editable: false },
			{ key: 'source_url', label: '원본 URL', type: 'text', sortable: false, searchable: true, required: true, editable: true },
			{ key: 'created_at', label: '작성일', type: 'date', sortable: true, searchable: false, required: true, editable: true },
			{ key: 'crawled_at', label: '크롤일', type: 'date', sortable: true, searchable: false, required: false, editable: false },
			{ key: 'related_post_id', label: '관련 게시글 ID', type: 'number', sortable: true, searchable: true, required: false, editable: true }
		]
	},
	images: {
		name: 'images',
		displayName: '이미지',
		description: '게시글에 첨부된 이미지 및 미디어',
		icon: 'Image',
		schema: null,
		primaryKey: 'id',
		canCreate: false,
		canEdit: true,
		canDelete: true,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'post_id', label: '게시글 ID', type: 'number', sortable: true, searchable: true, required: true, editable: false },
			{ key: 'media_type', label: '미디어 타입', type: 'badge', sortable: true, searchable: true, required: false, editable: true },
			{ key: 'r2_key', label: 'R2 키', type: 'text', sortable: false, searchable: true, required: true, editable: false },
			{ key: 'r2_url', label: 'R2 URL', type: 'text', sortable: false, searchable: true, required: true, editable: false },
			{ key: 'original_url', label: '원본 URL', type: 'text', sortable: false, searchable: true, required: false, editable: false },
			{ key: 'order_index', label: '순서', type: 'number', sortable: true, searchable: false, required: true, editable: true, width: '80px' },
			{ key: 'width', label: '너비', type: 'number', sortable: true, searchable: false, required: false, editable: false, width: '80px' },
			{ key: 'height', label: '높이', type: 'number', sortable: true, searchable: false, required: false, editable: false, width: '80px' },
			{ key: 'file_size', label: '파일 크기', type: 'number', sortable: true, searchable: false, required: false, editable: false }
		]
	},
	users: {
		name: 'users',
		displayName: '사용자',
		description: '가입한 사용자 정보',
		icon: 'Users',
		schema: null,
		primaryKey: 'id',
		canCreate: false,
		canEdit: true,
		canDelete: true,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'supabase_id', label: 'Supabase ID', type: 'text', sortable: false, searchable: true, required: true, editable: false },
			{ key: 'email', label: '이메일', type: 'text', sortable: true, searchable: true, required: true, editable: true },
			{ key: 'display_name', label: '닉네임', type: 'text', sortable: true, searchable: true, required: false, editable: true },
			{ key: 'avatar_url', label: '아바타 URL', type: 'text', sortable: false, searchable: false, required: false, editable: true },
			{ key: 'role', label: '권한', type: 'select', sortable: true, searchable: false, required: true, editable: true, width: '100px', options: [
				{ value: '0', label: 'Guest' },
				{ value: '1', label: 'User' },
				{ value: '99', label: 'Admin' }
			]},
			{ key: 'created_at', label: '가입일', type: 'date', sortable: true, searchable: false, required: false, editable: false }
		]
	},
	comments: {
		name: 'comments',
		displayName: '댓글',
		description: '사용자가 작성한 댓글',
		icon: 'MessageSquare',
		schema: null,
		primaryKey: 'id',
		canCreate: false,
		canEdit: true,
		canDelete: true,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'post_id', label: '게시글 ID', type: 'number', sortable: true, searchable: true, required: true, editable: false },
			{ key: 'user_id', label: '사용자 ID', type: 'number', sortable: true, searchable: true, required: true, editable: false },
			{ key: 'parent_comment_id', label: '부모 댓글 ID', type: 'number', sortable: true, searchable: true, required: false, editable: false },
			{ key: 'content', label: '내용', type: 'textarea', sortable: false, searchable: true, required: true, editable: true },
			{ key: 'created_at', label: '작성일', type: 'date', sortable: true, searchable: false, required: false, editable: false },
			{ key: 'updated_at', label: '수정일', type: 'date', sortable: true, searchable: false, required: false, editable: false },
			{ key: 'is_deleted', label: '삭제됨', type: 'boolean', sortable: true, searchable: false, required: false, editable: true, width: '80px' }
		]
	},
	likes: {
		name: 'likes',
		displayName: '좋아요',
		description: '게시글 및 댓글 좋아요',
		icon: 'Heart',
		schema: null,
		primaryKey: 'id',
		canCreate: false,
		canEdit: false,
		canDelete: true,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'user_id', label: '사용자 ID', type: 'number', sortable: true, searchable: true, required: true, editable: false },
			{ key: 'post_id', label: '게시글 ID', type: 'number', sortable: true, searchable: true, required: false, editable: false },
			{ key: 'comment_id', label: '댓글 ID', type: 'number', sortable: true, searchable: true, required: false, editable: false },
			{ key: 'created_at', label: '생성일', type: 'date', sortable: true, searchable: false, required: false, editable: false }
		]
	},
	bookmarks: {
		name: 'bookmarks',
		displayName: '북마크',
		description: '사용자가 저장한 북마크',
		icon: 'Bookmark',
		schema: null,
		primaryKey: 'id',
		canCreate: false,
		canEdit: false,
		canDelete: true,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'user_id', label: '사용자 ID', type: 'number', sortable: true, searchable: true, required: true, editable: false },
			{ key: 'post_id', label: '게시글 ID', type: 'number', sortable: true, searchable: true, required: true, editable: false },
			{ key: 'created_at', label: '생성일', type: 'date', sortable: true, searchable: false, required: false, editable: false }
		]
	},
	reports: {
		name: 'reports',
		displayName: '신고',
		description: '사용자 신고 내역',
		icon: 'AlertTriangle',
		schema: null,
		primaryKey: 'id',
		canCreate: false,
		canEdit: true,
		canDelete: true,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'user_id', label: '신고자 ID', type: 'number', sortable: true, searchable: true, required: true, editable: false },
			{ key: 'post_id', label: '게시글 ID', type: 'number', sortable: true, searchable: true, required: false, editable: false },
			{ key: 'comment_id', label: '댓글 ID', type: 'number', sortable: true, searchable: true, required: false, editable: false },
			{ key: 'reason', label: '사유', type: 'select', sortable: true, searchable: true, required: true, editable: true, options: [
				{ value: 'spam', label: '스팸' },
				{ value: 'inappropriate', label: '부적절한 콘텐츠' },
				{ value: 'harassment', label: '괴롭힘' },
				{ value: 'other', label: '기타' }
			]},
			{ key: 'description', label: '설명', type: 'textarea', sortable: false, searchable: true, required: false, editable: true },
			{ key: 'status', label: '상태', type: 'select', sortable: true, searchable: false, required: true, editable: true, options: [
				{ value: 'pending', label: '대기 중' },
				{ value: 'reviewed', label: '검토됨' },
				{ value: 'resolved', label: '해결됨' },
				{ value: 'rejected', label: '거부됨' }
			]},
			{ key: 'created_at', label: '신고일', type: 'date', sortable: true, searchable: false, required: false, editable: false },
			{ key: 'resolved_at', label: '해결일', type: 'date', sortable: true, searchable: false, required: false, editable: true },
			{ key: 'resolved_by', label: '처리자 ID', type: 'number', sortable: true, searchable: true, required: false, editable: true }
		]
	},
	highlights: {
		name: 'highlights',
		displayName: '하이라이트',
		description: '주간 하이라이트 게시글',
		icon: 'Star',
		schema: null,
		primaryKey: 'id',
		canCreate: true,
		canEdit: true,
		canDelete: true,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'weekStart', label: '주 시작일', type: 'date', sortable: true, searchable: false, required: true, editable: true },
			{ key: 'weekEnd', label: '주 종료일', type: 'date', sortable: true, searchable: false, required: true, editable: true },
			{ key: 'postId', label: '게시글 ID', type: 'number', sortable: true, searchable: true, required: true, editable: true },
			{ key: 'rank', label: '순위', type: 'number', sortable: true, searchable: false, required: true, editable: true, width: '80px' },
			{ key: 'editorComment', label: '에디터 코멘트', type: 'textarea', sortable: false, searchable: true, required: false, editable: true },
			{ key: 'createdAt', label: '생성일', type: 'date', sortable: true, searchable: false, required: false, editable: false }
		]
	},
	audit_logs: {
		name: 'audit_logs',
		displayName: '감사 로그',
		description: 'DB 변경 이력',
		icon: 'FileSearch',
		schema: null,
		primaryKey: 'id',
		canCreate: false,
		canEdit: false,
		canDelete: false,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'userId', label: '사용자 ID', type: 'number', sortable: true, searchable: true, required: false, editable: false },
			{ key: 'action', label: '액션', type: 'badge', sortable: true, searchable: true, required: true, editable: false },
			{ key: 'tableName', label: '테이블', type: 'badge', sortable: true, searchable: true, required: true, editable: false },
			{ key: 'recordId', label: '레코드 ID', type: 'number', sortable: true, searchable: true, required: false, editable: false },
			{ key: 'query', label: 'SQL 쿼리', type: 'textarea', sortable: false, searchable: true, required: false, editable: false },
			{ key: 'createdAt', label: '생성일', type: 'date', sortable: true, searchable: false, required: false, editable: false }
		]
	},
	backup_settings: {
		name: 'backup_settings',
		displayName: '백업 설정',
		description: '자동 백업 설정',
		icon: 'Settings',
		schema: null,
		primaryKey: 'id',
		canCreate: false,
		canEdit: true,
		canDelete: false,
		columns: [
			{ key: 'id', label: 'ID', type: 'number', sortable: true, searchable: true, required: true, editable: false, width: '80px' },
			{ key: 'enabled', label: '활성화', type: 'boolean', sortable: true, searchable: false, required: true, editable: true, width: '80px' },
			{ key: 'frequency', label: '주기', type: 'select', sortable: true, searchable: false, required: true, editable: true, options: [
				{ value: 'daily', label: '매일' },
				{ value: 'weekly', label: '매주' },
				{ value: 'monthly', label: '매월' }
			]},
			{ key: 'time', label: '시간', type: 'text', sortable: false, searchable: false, required: true, editable: true, placeholder: 'HH:MM' },
			{ key: 'retentionDays', label: '보관 기간 (일)', type: 'number', sortable: true, searchable: false, required: true, editable: true },
			{ key: 'lastBackupAt', label: '마지막 백업', type: 'date', sortable: true, searchable: false, required: false, editable: false },
			{ key: 'updatedAt', label: '수정일', type: 'date', sortable: true, searchable: false, required: false, editable: false }
		]
	}
}

// Whitelist of allowed table names to prevent SQL injection
export const ALLOWED_TABLES = [
	'posts',
	'images',
	'users',
	'comments',
	'likes',
	'bookmarks',
	'reports',
	'highlights',
	'audit_logs',
	'backup_settings'
] as const

/**
 * Validates if a table name is in the allowed whitelist
 * @param tableName - The table name to validate
 * @returns true if the table name is valid, false otherwise
 */
export function isValidTableName(tableName: string): boolean {
	return (ALLOWED_TABLES as readonly string[]).includes(tableName)
}

export function getTableMetadata(tableName: string): TableMetadata | undefined {
	return tableMetadata[tableName]
}

export function getAllTables(): TableMetadata[] {
	return Object.values(tableMetadata)
}
