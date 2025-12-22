"""Fix duplicate images by moving image gallery inside else block"""
import re

# Read file
with open('webapp/src/routes/post/[id]/+page.svelte', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the section
# We need to add proper indentation to image gallery section
old_pattern = r'''(\t\t\t{:else}
\t\t\t\t<!-- Fallback: 텍스트 \+ 이미지 갤러리 \(기존 방식\) -->
\t\t\t\t{#if post\.content}
\t\t\t\t\t<div class="prose prose-gray max-w-none">
\t\t\t\t\t\t<p class="whitespace-pre-wrap text-gray-700">{post\.content}</p>
\t\t\t\t\t</div>
\t\t\t\t{/if}

\t\t\t<!-- 이미지 갤러리 -->
\t\t\t{#if images\.length > 0})'''

new_text = r'''\1

\t\t\t\t<!-- 이미지 갤러리 (content_html이 없을 때만) -->
\t\t\t\t{#if images.length > 0}'''

content = re.sub(old_pattern, new_text, content, flags=re.MULTILINE)

# Also need to add proper indentation to the gallery content
content = content.replace(
    '\t\t\t{#if images.length > 0}\n\t\t\t\t<div class="mt-6 space-y-4">',
    '\t\t\t\t{#if images.length > 0}\n\t\t\t\t\t<div class="mt-6 space-y-4">'
)
content = content.replace(
    '\t\t\t\t\t{#each images as image, index}',
    '\t\t\t\t\t\t{#each images as image, index}'
)
content = content.replace(
    '\t\t\t\t\t\t<div class="overflow-hidden rounded-lg border border-gray-200">',
    '\t\t\t\t\t\t\t<div class="overflow-hidden rounded-lg border border-gray-200">'
)
content = content.replace(
    '\t\t\t\t\t\t\t<img\n\t\t\t\t\t\t\t\tsrc={image.r2_url}',
    '\t\t\t\t\t\t\t\t<img\n\t\t\t\t\t\t\t\t\tsrc={image.r2_url}'
)
content = content.replace(
    '\t\t\t\t\t\t\t\tloading="lazy"\n\t\t\t\t\t\t\t/>',
    '\t\t\t\t\t\t\t\t\tloading="lazy"\n\t\t\t\t\t\t\t\t/>'
)
content = content.replace(
    '\t\t\t\t\t\t\t{#if image.media_type === \'gif\'}',
    '\t\t\t\t\t\t\t\t{#if image.media_type === \'gif\'}'
)
content = content.replace(
    '\t\t\t\t\t\t\t\t<div class="bg-gray-50 px-3 py-1 text-xs text-gray-600">',
    '\t\t\t\t\t\t\t\t\t<div class="bg-gray-50 px-3 py-1 text-xs text-gray-600">'
)
content = content.replace(
    '\t\t\t\t\t\t\t\t\tGIF {image.duration_seconds ?',
    '\t\t\t\t\t\t\t\t\t\tGIF {image.duration_seconds ?'
)
content = content.replace(
    '\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t{/if}',
    '\t\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t\t{/if}'
)
content = content.replace(
    '\t\t\t\t\t\t</div>\n\t\t\t\t\t{/each}',
    '\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t{/each}'
)
content = content.replace(
    '\t\t\t\t</div>\n\t\t\t\t{/if}\n\t\t{/if}',
    '\t\t\t\t\t</div>\n\t\t\t\t{/if}\n\t\t\t{/if}'
)

# Write back
with open('webapp/src/routes/post/[id]/+page.svelte', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed duplicate images!")
print("Image gallery now only shows when content_html is not available")
