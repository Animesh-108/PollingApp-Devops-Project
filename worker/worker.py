import redis
import psycopg2
import os
import time

def connect_to_postgres():
    """Continuously tries to connect to the PostgreSQL database."""
    while True:
        try:
            # The 'host' is 'db', which will be the name of our Postgres service.
            conn = psycopg2.connect(
                host="db",
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD")
            )
            return conn
        except psycopg2.OperationalError as e:
            print(f"Could not connect to PostgreSQL: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

# Connect to Redis
r = redis.Redis(host='redis', port=6379, db=0)

# Connect to PostgreSQL
conn = connect_to_postgres()
cur = conn.cursor()

# Create the 'votes' table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        vote VARCHAR(255) NOT NULL
    )
""")
conn.commit()

print("Worker is running and waiting for votes...")

while True:
    try:
        # 'brpop' waits for an item to appear on the 'votes' list in Redis
        # It's a "blocking" operation that waits forever (timeout=0)
        work = r.brpop('votes', 0)
        
        # The result from brpop is a tuple (list_name, item)
        vote = work[1].decode('utf-8')
        
        # Insert the vote into the PostgreSQL table
        cur.execute("INSERT INTO votes (vote) VALUES (%s)", (vote,))
        conn.commit()
        
        print(f"Processed a vote for: {vote}")

    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred: {e}")
        # In case of a database error, try to reconnect
        conn.close()
        conn = connect_to_postgres()
        cur = conn.cursor()