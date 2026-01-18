#!/bin/bash
# D1 마이그레이션: db import 제거 스크립트

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
    "src/routes/stats/+page.server.ts"
    "src/routes/sitemap.xml/+server.ts"
    "src/routes/api/crawler/posts/+server.ts"
)

echo "🔄 Removing db imports..."

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✏️  $file"
        # db import 제거
        sed -i "/^import { db } from '\$lib\/server\/db'/d" "$file"
        sed -i '/^import { db } from "$lib\/server\/db"/d' "$file"
    fi
done

echo "✅ Done! Now manually add 'const db = locals.db' to each function"
