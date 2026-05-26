import psycopg

def create_conversation():
    # Connect to an existing database
    with psycopg.connect(conninfo="postgresql://chatbot_user:localpassword@0.0.0.0:5432/chatbot") as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute("INSERT INTO conversations DEFAULT VALUES RETURNING id, session_id, created_at;")
            row = cur.fetchone()
            return {
                "id": row[0],
                "session_id": row[1],
                "created_at": row[2]
            }