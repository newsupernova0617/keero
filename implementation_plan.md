# Initial Implementation Plan: Crawler & SvelteKit Setup

This plan outlines the first concrete steps for implementing the `aagag_clone` project, focusing on setting up the crawler and initializing the web application.

## 🤖 Part 1: Crawler Implementation

### 1. Dependency Installation
- **Goal**: Resolve `ModuleNotFoundError: No module named 'bs4'` and other missing dependencies.
- **Action**: Run `pip install -r requirements.txt` within the `crawler/venv`.
- **Verification**: Run `python -c "from bs4 import BeautifulSoup"` and `pytest --version`.

### 2. Target Site Configuration
- **Goal**: Replace example placeholders in `crawler/config.py` with real humor community data.
- **Action**: Analyze target site HTML (e.g., humor univ, bobae dream) and update `TARGET_SITES` with correct selectors.
- **Verification**: Run `python main.py` and verify console logs show successful parsing.

### 3. Media Optimization & GIF/Video Support
- **Goal**: Implement WebP conversion for images and MP4/WebP animation for GIF/Video to save R2 costs.
- **Action**:
  - Integrate `Pillow` for image optimization.
  - Setup `ffmpeg` for video/GIF processing.
  - Update `storage.py` and `scraper.py` to handle new media types and metadata.
- **Verification**: Check image sizes in the R2 bucket and verify `optimized_size_bytes` in `app.db`.

---

## 🌐 Part 2: SvelteKit Web App Implementation

### 4. Project Initialization
- **Goal**: Create a clean SvelteKit project with TypeScript and modern UI tools.
- **Action**: 
  - Run `npx sv create .` (Skeleton project, TypeScript).
  - Install Tailwind CSS and `shadcn-svelte`.
  - Configure `better-sqlite3` and `Drizzle ORM` to connect to `data/app.db`.
- **Verification**: Run `npm run dev` and confirm the landing page renders with shadcn components.

### 5. Supabase Auth Integration
- **Goal**: Implement secure Kakao and Google OAuth.
- **Action**: 
  - Configure Supabase project and OAuth providers.
  - Implement `/auth/callback` and session management.
  - Add logic to sync Supabase users to the local `users` table in SQLite.
- **Verification**: Successfully log in via Google/Kakao and see a new row in the local `users` table.

### 6. Core Pages & Search
- **Goal**: Display original posts and provide full-text search.
- **Action**:
  - Implement `/` (Post list with pagination, filtering `related_post_id IS NULL`).
  - Implement `/post/[id]` (Detail view with image gallery).
  - Implement `/search` using SQLite FTS5.
- **Verification**: Search for a known keyword and verify results are relevant and rank-sorted.

---

## 🚀 Verification Plan

### Automated Tests
- **Crawler**: Run `pytest crawler/tests/` to ensure no regressions in parsing logic.
- **Web App**: Use `npm run build` to verify TypeScript and Svelte compilation.

### Manual Verification
1.  **Crawler Run**: Manually execute `python main.py` and inspect `data/app.db` using a SQLite browser to verify data integrity.
2.  **OAuth Flow**: Test the full login loop from a guest user to a logged-in user.
3.  **R2 Check**: Verify that optimized images are correctly uploaded to R2 and served via the custom domain.
