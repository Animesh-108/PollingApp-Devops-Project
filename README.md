# Real-Time Polling Application with Docker Compose & Python

A multi-service, asynchronous web application built to showcase modern DevOps practices. This project demonstrates container orchestration, inter-service communication via a message queue, and data persistence in a decoupled microservice architecture.

![Live Demo Screenshot]([images\livedemo1.png](https://github.com/Animesh-108/PollingApp-Devops-Project/blob/main/images/livedemo1.png))
![Live Demo Screenshot]([images\livedemo2.png](https://github.com/Animesh-108/PollingApp-Devops-Project/blob/main/images/livedemo2.png))


---

## 🏛️ Architecture Overview

The application is composed of five distinct services, each running in its own Docker container and managed by a single `docker-compose.yml` file. This architecture is designed to be scalable and resilient, ensuring that a high volume of votes does not impact user experience.



1.  **Poll App (Frontend):** A Python Flask web application that serves the voting page. When a user votes, it sends the vote to the Redis queue.
2.  **Redis (Message Queue):** A high-speed, in-memory message broker. It instantly accepts votes from the Poll app and holds them in a queue until a worker is ready to process them.
3.  **Worker (Backend Processor):** A Python script that acts as a background service. It continuously watches the Redis queue, pulls new votes, and saves them to the PostgreSQL database.
4.  **PostgreSQL (Database):** The permanent "source of truth" for all voting data. It stores the votes processed by the worker, ensuring data persistence with a Docker Volume.
5.  **Result App (Frontend):** A second Python Flask web application that continuously queries the PostgreSQL database for the latest vote counts and displays them in a live-updating bar chart.

---

## 🛠️ Tech Stack

| Category              | Technology                               |
| --------------------- | ---------------------------------------- |
| **Containerization** | Docker, Docker Compose                   |
| **Backend** | Python 3.9, Flask                        |
| **Database** | PostgreSQL                               |
| **Message Queue** | Redis                                    |
| **Frontend** | HTML, CSS, JavaScript (Fetch API)        |

---

## 🚀 Getting Started

Follow these instructions to get the application running on your local machine.

### Prerequisites

* **Docker Engine** and **Docker Compose** must be installed and running on your system.

### Installation & Setup

1.  **Clone the Repository**
    Open your terminal and clone this repository to your local machine.
    ```bash
    git clone [https://github.com/your-username/realtime-poll.git](https://github.com/your-username/realtime-poll.git)
    ```

2.  **Navigate to the Project Directory**
    ```bash
    cd realtime-poll
    ```

3.  **Build and Run the Application**
    Use Docker Compose to build the necessary images and start all five containers. The `-d` flag runs the containers in detached mode (in the background).
    ```bash
    docker compose up --build -d
    ```
    The first time you run this, Docker will download the official Redis and PostgreSQL images, which may take a few moments.

### Usage

Once the containers are running, you can access the two front-end applications:

* **Voting Page**: Open your web browser and go to ➡️ **`http://localhost:5001`**
* **Results Page**: Open a second browser tab and go to ➡️ **`http://localhost:5002`**

Place the two browser windows side-by-side to see the results update in real-time as you vote!

---

## 🐛 Troubleshooting

If the application isn't working as expected (e.g., votes are not counting), use these commands to diagnose the issue.

* **Check the status of all containers:** This is the first step. Look for any container that is not in the `running` or `Up` state.
    ```bash
    docker compose ps
    ```
* **Check the logs of a specific service:** If a container is crashing or not behaving correctly, its logs will tell you why. The `worker` and `redis` services are the most common points of failure.
    ```bash
    # Check the worker's logs for database or Redis connection errors
    docker compose logs worker

    # Check the redis logs to ensure it started correctly
    docker compose logs redis
    ```
* **Perform a full reset of the project:** This is often the quickest fix. It stops and removes all containers, networks, and volumes associated with the project, allowing you to start fresh.
    ```bash
    docker compose down --volumes
    ```
* **Connect directly to the database:** This is the ultimate test to see if votes are being saved. First, get the container ID for the database with `docker compose ps`, then connect.
    ```bash
    # Replace <db-container-id> with the actual ID of your postgres container
    docker exec -it <db-container-id> psql -U postgres -d voting_db
    
    # Once inside the psql shell, run this SQL query:
    SELECT vote, count(id) FROM votes GROUP BY vote;
    ```
    If you see `(0 rows)`, it confirms that the worker is not successfully saving votes to the database.

---

## ✅ Key Concepts Demonstrated

This project is more than just a web app; it's a practical demonstration of several key software architecture and DevOps concepts:

* **Microservice Architecture:** The application is broken down into small, independent services that communicate over a network.
* **Asynchronous Processing:** By using a Redis queue, the system can handle tasks (like writing to a database) in the background without making the user wait.
* **Container Orchestration:** Docker Compose is used to define, build, and manage the complete lifecycle of a multi-container application.
* **Infrastructure as Code (IaC):** The entire application environment is defined declaratively in the `docker-compose.yml` file, making it reproducible and version-controllable.
* **Data Persistence:** A Docker Volume is used to ensure that the data stored in the PostgreSQL database is saved permanently, even if the container is removed or restarted.
