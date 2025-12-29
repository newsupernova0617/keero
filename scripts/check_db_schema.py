import sqlite3

db_path = r"c:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone\data\app.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get table info for posts
cursor.execute("PRAGMA table_info(posts)")
columns = cursor.fetchall()

print("Posts table columns:")
print("-" * 80)
for col in columns:
    print(f"{col[1]:20s} {col[2]:15s} NOT NULL={col[3]} DEFAULT={col[4]} PK={col[5]}")

print("\n" + "=" * 80 + "\n")

# Check if content_html exists
has_content_html = any(col[1] == 'content_html' for col in columns)
print(f"Has content_html column: {has_content_html}")

conn.close()
