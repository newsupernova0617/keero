#!/bin/bash
# 나머지 파일들에 locals 파라미터와 const db 추가

files=(
    "src/routes/best-comments/+page.server.ts"
    "src/routes/settings/+page.server.ts"
    "src/routes/profile/activity/+page.server.ts"
    "src/routes/post/[id]/+page.server.ts"
    "src/routes/highlights/weekly/+page.server.ts"
    "src/routes/admin/posts/+page.server.ts"
    "src/routes/admin/comments/+page.server.ts"
    "src/routes/admin/users/+page.server.ts"
    "src/routes/admin/database/+page.server.ts"
    "src/routes/admin/stats/+page.server.ts"
    "src/routes/admin/reports/+page.server.ts"
    "src/routes/sitemap.xml/+server.ts"
)

echo "🔄 Adding locals parameter and const db..."

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✏️  $file"
        
        # PageServerLoad 패턴: async () => { 를 async ({ locals }) => { 로 변경
        sed -i 's/async () =>/async ({ locals }) =>/g' "$file"
        sed -i 's/async ({ \([^}]*\) }) =>/async ({ \1, locals }) =>/g' "$file"
        sed -i 's/async ({ locals, locals }) =>/async ({ locals }) =>/g' "$file"  # 중복 제거
        
        # RequestHandler 패턴도 처리
        sed -i 's/async ({ request }) =>/async ({ request, locals }) =>/g' "$file"
        sed -i 's/async ({ request, locals, locals }) =>/async ({ request, locals }) =>/g' "$file"
        
        # 함수 시작 부분에 const db = locals.db 추가 (첫 번째 const 앞에)
        # 이미 있으면 스킵
        if ! grep -q "const db = locals.db" "$file"; then
            # export const load 다음 줄에 추가
            sed -i '/export const load.*async.*{$/a\    const db = locals.db' "$file"
            sed -i '/export const GET.*async.*{$/a\    const db = locals.db' "$file"
            sed -i '/export const POST.*async.*{$/a\    const db = locals.db' "$file"
            sed -i '/export const actions.*async.*{$/a\        const db = locals.db' "$file"
        fi
    fi
done

echo "✅ Done!"
