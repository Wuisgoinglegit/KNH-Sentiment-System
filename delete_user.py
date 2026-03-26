import sqlite3

DB_NAME = "knh_feedback.db"

def delete_staff():
    staff_id = input("Enter the Staff ID you want to delete: ").strip().upper()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM admin_users WHERE staff_id = ?', (staff_id,))
    if not cursor.fetchone():
        print(f"Error: Staff ID '{staff_id}' not found in the database.")
    else:
        cursor.execute('DELETE FROM admin_users WHERE staff_id = ?', (staff_id,))
        conn.commit()
        print(f"SUCCESS: User '{staff_id}' has been permanently deleted.")
        
    conn.close()

if __name__ == '__main__':
    delete_staff()