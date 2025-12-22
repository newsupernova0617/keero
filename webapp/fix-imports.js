const fs = require('fs');
const path = require('path');

const files = [
  'src/lib/components/DarkModeToggle.svelte',
  'src/lib/components/EmptyState.svelte',
  'src/lib/components/Footer.svelte',
  'src/lib/components/MobileNav.svelte',
  'src/lib/components/UserMenu.svelte',
  'src/routes/+layout.svelte',
  'src/routes/+page.svelte',
  'src/routes/search/+page.svelte',
  'src/routes/post/[id]/+page.svelte'
];

files.forEach(file => {
  try {
    let content = fs.readFileSync(file, 'utf8');
    content = content.replace(/from 'lucide-svelte'/g, "from '@lucide/svelte'");
    fs.writeFileSync(file, content, 'utf8');
    console.log(`Fixed: ${file}`);
  } catch (err) {
    console.log(`Skip: ${file} - ${err.message}`);
  }
});
