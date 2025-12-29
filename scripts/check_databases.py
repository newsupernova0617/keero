import sqlite3

db_path = r"c:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone\data\app.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Tables in app.db:")
print("-" * 80)
for table in tables:
    print(f"  - {table[0]}")

print("\n" + "=" * 80 + "\n")

# Check if posts.db has the content instead
print("Checking posts.db...")
posts_db_path = r"c:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone\data\posts.db"
conn2 = sqlite3.connect(posts_db_path)
cursor2 = conn2.cursor()

cursor2.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables2 = cursor2.fetchall()

print("Tables in posts.db:")
print("-" * 80)
for table in tables2:
    print(f"  - {table[0]}")

# Check posts table schema in posts.db
if any(t[0] == 'posts' for t in tables2):
    cursor2.execute("PRAGMA table_info(posts)")
    columns = cursor2.fetchall()
    print("\nPosts table columns in posts.db:")
    print("-" * 80)
    for col in columns:
        print(f"{col[1]:20s} {col[2]:15s}")

conn.close()
conn2.close()
