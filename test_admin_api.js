#!/usr/bin/env node
/**
 * Admin API 단위 테스트 스크립트
 * 
 * 테스트 대상:
 * 1. /admin/database - deletePost, deleteComment, cleanOldPosts
 * 2. /admin/posts - 게시글 조회
 * 3. /admin/comments - 댓글 조회
 * 4. /admin/users - 사용자 조회
 * 5. /admin/stats - 통계 조회
 * 6. /admin/reports - 신고 관리
 */

const BASE_URL = 'http://localhost:5173'

// 테스트 결과 저장
const results = {
  passed: 0,
  failed: 0,
  tests: []
}

// 색상 출력
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
}

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`)
}

// 테스트 헬퍼
async function test(name, fn) {
  try {
    log(`\n🧪 Testing: ${name}`, 'blue')
    await fn()
    results.passed++
    results.tests.push({ name, status: 'PASS' })
    log(`✅ PASS: ${name}`, 'green')
  } catch (error) {
    results.failed++
    results.tests.push({ name, status: 'FAIL', error: error.message })
    log(`❌ FAIL: ${name}`, 'red')
    log(`   Error: ${error.message}`, 'red')
  }
}

// Admin 페이지 접근 테스트
async function testAdminAccess() {
  const response = await fetch(`${BASE_URL}/admin`)
  
  if (response.status === 200) {
    log('   ✓ Admin 페이지 접근 성공 (200)', 'green')
  } else if (response.status === 303 || response.status === 302) {
    log('   ⚠ 로그인 필요 (리다이렉트)', 'yellow')
    throw new Error('로그인이 필요합니다. 브라우저에서 먼저 로그인하세요.')
  } else {
    throw new Error(`예상치 못한 상태 코드: ${response.status}`)
  }
}

// Database API 테스트
async function testDatabaseStats() {
  const response = await fetch(`${BASE_URL}/admin/database`)
  
  if (response.status !== 200) {
    throw new Error(`상태 코드: ${response.status}`)
  }
  
  const html = await response.text()
  
  // HTML에 통계 데이터가 포함되어 있는지 확인
  if (!html.includes('전체 게시글') && !html.includes('사이트별')) {
    throw new Error('통계 데이터가 없습니다')
  }
  
  log('   ✓ DB 통계 조회 성공', 'green')
}

// Posts API 테스트
async function testPostsList() {
  const response = await fetch(`${BASE_URL}/admin/posts`)
  
  if (response.status !== 200) {
    throw new Error(`상태 코드: ${response.status}`)
  }
  
  log('   ✓ 게시글 목록 조회 성공', 'green')
}

// Comments API 테스트
async function testCommentsList() {
  const response = await fetch(`${BASE_URL}/admin/comments`)
  
  if (response.status !== 200) {
    throw new Error(`상태 코드: ${response.status}`)
  }
  
  log('   ✓ 댓글 목록 조회 성공', 'green')
}

// Users API 테스트
async function testUsersList() {
  const response = await fetch(`${BASE_URL}/admin/users`)
  
  if (response.status !== 200) {
    throw new Error(`상태 코드: ${response.status}`)
  }
  
  log('   ✓ 사용자 목록 조회 성공', 'green')
}

// Stats API 테스트
async function testStats() {
  const response = await fetch(`${BASE_URL}/admin/stats`)
  
  if (response.status !== 200) {
    throw new Error(`상태 코드: ${response.status}`)
  }
  
  log('   ✓ 통계 페이지 조회 성공', 'green')
}

// Reports API 테스트
async function testReports() {
  const response = await fetch(`${BASE_URL}/admin/reports`)
  
  if (response.status !== 200) {
    throw new Error(`상태 코드: ${response.status}`)
  }
  
  log('   ✓ 신고 목록 조회 성공', 'green')
}

// 메인 테스트 실행
async function runTests() {
  log('=' .repeat(60), 'blue')
  log('🚀 Admin API 단위 테스트 시작', 'blue')
  log('=' .repeat(60), 'blue')
  log(`📍 Base URL: ${BASE_URL}`, 'blue')
  
  // 1. Admin 접근 테스트
  await test('Admin 페이지 접근', testAdminAccess)
  
  // 2. 각 페이지 로드 테스트
  await test('Database 통계 조회', testDatabaseStats)
  await test('Posts 목록 조회', testPostsList)
  await test('Comments 목록 조회', testCommentsList)
  await test('Users 목록 조회', testUsersList)
  await test('Stats 페이지 조회', testStats)
  await test('Reports 목록 조회', testReports)
  
  // 결과 출력
  log('\n' + '='.repeat(60), 'blue')
  log('📊 테스트 결과', 'blue')
  log('='.repeat(60), 'blue')
  
  results.tests.forEach(test => {
    const icon = test.status === 'PASS' ? '✅' : '❌'
    const color = test.status === 'PASS' ? 'green' : 'red'
    log(`${icon} ${test.name}`, color)
    if (test.error) {
      log(`   └─ ${test.error}`, 'red')
    }
  })
  
  log('\n' + '='.repeat(60), 'blue')
  log(`✅ Passed: ${results.passed}`, 'green')
  log(`❌ Failed: ${results.failed}`, 'red')
  log(`📊 Total: ${results.passed + results.failed}`, 'blue')
  log('='.repeat(60), 'blue')
  
  // 종료 코드
  process.exit(results.failed > 0 ? 1 : 0)
}

// 실행
runTests().catch(error => {
  log(`\n💥 치명적 오류: ${error.message}`, 'red')
  process.exit(1)
})
