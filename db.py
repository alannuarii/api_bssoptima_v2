import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def connection(query, action):
        conn = None
        try:
            conn = mysql.connector.connect(
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                user = os.getenv('DB_USER'), 
                password = os.getenv('DB_PASSWORD'),
                db = os.getenv('DB_NAME'), 
                )

            cur = conn.cursor(dictionary=True)
            if conn.is_connected():
                if action == 'select':
                    cur.execute(query)
                    result = cur.fetchall()
                    return result
                elif action == 'insert':
                    cur.execute(query)
                    conn.commit()
                elif action == 'update':
                    cur.execute(query)
                    conn.commit()
                elif action == 'delete':
                    cur.execute(query)
                    conn.commit()
        except Exception as error:
            print(error)
        finally:
            if conn and conn.is_connected():
                cur.close()
                conn.close()


