from flask import Flask, render_template, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

def connect_to_postgres():
    """Continuously tries to connect to the PostgreSQL database."""
    while True:
        try:
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

conn = connect_to_postgres()

@app.route('/')
def index():
    """Serves the results page."""
    return render_template('index.html')

@app.route('/results')
def results():
    """Provides the vote counts as JSON."""
    cur = conn.cursor()
    cur.execute("SELECT vote, COUNT(id) AS count FROM votes GROUP BY vote")
    result_data = cur.fetchall()
    cur.close()
    
    # Convert list of tuples to a dictionary
    votes = dict(result_data)
    
    # Ensure both options are always present
    if 'cats' not in votes:
        votes['cats'] = 0
    if 'dogs' not in votes:
        votes['dogs'] = 0
        
    return jsonify(votes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)