import redis
from flask import Flask, render_template, request

app = Flask(__name__)
# Connect to Redis. The hostname 'redis' is used because Docker Compose
# creates a network where services can find each other by their name.
r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/')
def index():
    """Serves the main polling page."""
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    """Accepts votes and pushes them to the Redis queue."""
    vote_option = request.form['vote']
    # 'lpush' adds the vote to the beginning of a list named 'votes' in Redis
    r.lpush('votes', vote_option)
    return f"Voted for {vote_option}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)