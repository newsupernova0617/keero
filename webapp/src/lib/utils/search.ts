/**
 * 검색어를 하이라이트 처리하는 함수
 */
export function highlightText(text: string, query: string): string {
	if (!query || !text) return text

	const regex = new RegExp(`(${escapeRegex(query)})`, 'gi')
	return text.replace(regex, '<mark class="bg-yellow-200 dark:bg-yellow-800">$1</mark>')
}

/**
 * 정규식 특수문자 이스케이프
 */
function escapeRegex(str: string): string {
	return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/**
 * 텍스트에서 검색어 주변 컨텍스트 추출
 */
export function extractContext(text: string, query: string, contextLength: number = 100): string {
	if (!query || !text) return text.substring(0, contextLength * 2) + '...'

	const lowerText = text.toLowerCase()
	const lowerQuery = query.toLowerCase()
	const index = lowerText.indexOf(lowerQuery)

	if (index === -1) {
		return text.substring(0, contextLength * 2) + '...'
	}

	const start = Math.max(0, index - contextLength)
	const end = Math.min(text.length, index + query.length + contextLength)

	let excerpt = text.substring(start, end)
	
	if (start > 0) excerpt = '...' + excerpt
	if (end < text.length) excerpt = excerpt + '...'

	return excerpt
}
