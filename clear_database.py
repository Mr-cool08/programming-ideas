import sqlite3
import os
import time

# Get the absolute path to the database file
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'idea.db')

print("\nDatabase Clearing Script")
print("-" * 30)

try:
    # Check if database exists
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        input("Press Enter to exit...")
        exit()

    # Connect to database
    print("📂 Connecting to database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get current count
    cursor.execute('SELECT COUNT(*) FROM ideas')
    count_before = cursor.fetchone()[0]
    print(f"➤ Current records: {count_before}")
    
    # Clear the database
    print("🗑️  Clearing records...")
    cursor.execute('DELETE FROM ideas')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="ideas"')
    conn.commit()
    
    # Verify
    cursor.execute('SELECT COUNT(*) FROM ideas')
    count_after = cursor.fetchone()[0]
    print(f"✅ Database cleared! Records now: {count_after}")
    
except sqlite3.Error as e:
    print(f"❌ Database error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
    print("\nScript finished!")
    time.sleep(2)  # Keep the window open briefly
