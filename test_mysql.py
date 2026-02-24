
import pymysql   

def test_mysql_connection():
    try:
        # Step 1: Create connection
        conn = pymysql.connect(
            host="localhost",       # MySQL server host
            user="root",            # MySQL username
            password="Balaji@12345",# Your actual MySQL password
            database="earthquakes"  # Database name
        )

        # Step 2: Create a cursor object
        cursor = conn.cursor()

        # Step 3: Run a simple query to check connection
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print("✅ Connected successfully!")
        print("Current MySQL time:", result[0])

        # Step 4: Close cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Connection failed!")
        print("Error details:", e)

# Run the function
if __name__ == "__main__":
    test_mysql_connection()

