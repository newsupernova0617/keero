#!/bin/bash
# Cloudflare D1 마이그레이션: db import를 locals.db로 자동 변환

# 수정할 파일 목록
files=(
    "src/lib/server/auth.ts"
    "src/routes/search/+page.server.ts"
    "src/routes/stats/+page.server.ts"
    "src/routes/api/crawler/posts/+server.ts"
    "src/routes/admin/reports/+page.server.ts"
    "src/routes/admin/database/+page.server.ts"
    "src/routes/admin/stats/+page.server.ts"
    "src/routes/admin/users/+page.server.ts"
    "src/routes/admin/comments/+page.server.ts"
    "src/routes/sitemap.xml/+server.ts"
    "src/routes/admin/posts/+page.server.ts"
    "src/routes/highlights/weekly/+page.server.ts"
    "src/routes/profile/activity/+page.server.ts"
    "src/routes/settings/+page.server.ts"
    "src/routes/best-comments/+page.server.ts"
    "src/routes/post/[id]/+page.server.ts"
)

echo "🔄 Converting files to use locals.db..."

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✏️  Processing: $file"
        
        # 1. db import 제거
        sed -i "/import { db } from '\$lib\/server\/db'/d" "$file"
        sed -i "/import { db } from \"\$lib\/server\/db\"/d" "$file"
        
        # 2. 함수 시그니처에 locals 추가 (이미 있으면 스킵)
        # PageServerLoad, RequestHandler, Actions 등 다양한 패턴 처리
        
        echo "    ✅ Done"
    else
        echo "    ⚠️  File not found: $file"
    fi
done

echo ""
echo "✅ Conversion complete!"
echo "⚠️  Manual review required:"
echo "   - Add 'locals' parameter to function signatures"
echo "   - Add 'const db = locals.db' at the start of each function"
