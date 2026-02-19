# 🎮 Hanging Man Game

This project is a containerized implementation of the Hanging Man game, developed as part of the **DevOps & Containerization (M2)** module. 
It aims to industrialize a web application deployment by focusing on reliability, reproducibility, and security, using a modern microservices architecture and a fully automated CI/CD pipeline.


## 👥 Authors

- **Matthieu HOSTE**
- **Edouard LAMBERT**
- **Henri OMS**


## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Security & Best Practices](#-security--best-practices)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [CI/CD & Versioning Strategy](#-cicd--versioning-strategy)
- [Technologies](#-technologies)


## 🎯 Overview

Players attempt to guess a randomly selected word letter by letter, with a limited number of attempts. The project demonstrates microservices architecture, containerization, and modern web development practices.


## ✨ Features

- **Interactive Web Interface**: Clean, Apple-inspired design built with Streamlit
- **Real-time Gameplay**: Instant feedback on letter guesses
- **Visual Feedback**: SVG-based hangman drawing that updates with each incorrect guess
- **Game Statistics**: Track total games played
- **RESTful API**: Well-documented FastAPI backend
- **Microservices Architecture**: Separated concerns with API, Worker, Proxy, and Frontend services
- **Containerized Deployment**: Easy setup with Docker Compose
- **Health Monitoring**: Built-in health checks for services


## 🏗️ Architecture

The application consists of four main services:

```
┌─────────────┐
│  Frontend   │ (Streamlit - Port 80)
│   (UI)      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Proxy    │ (Port 8080)
│   (NGINX)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌─────────────┐
│     API     │◄─────┤   Worker    │
│  (FastAPI)  │      │   (Flask)   │
│  Port 8000  │      │  Port 5001  │
└─────────────┘      └─────────────┘
```

- **Frontend**: Streamlit-based user interface with modern, responsive design
- **Proxy**: NGINX reverse proxy for routing requests
- **API**: FastAPI backend handling game logic and state management
- **Worker**: Service responsible for providing random words for the game


## 🔒 Security & Best Practices

This project implements several security best practices required for modern DevOps standards:

- **Non-Root Users**: All containers (API, Worker, Frontend, Proxy) run as dedicated non-privileged users (`appuser`, `worker`, `nginxuser`, `streamlituser`) to minimize security risks.
- **Network Isolation**: Services communicate through a private Docker bridge network (`appnet`). Only the Proxy and Frontend ports are exposed to the host.
- **Reverse Proxy**: NGINX acts as a gateway, preventing direct external access to the API backend.
- **Dependency Management**: Strict version pinning in `requirements.txt` to ensure reproducibility and prevent supply chain attacks.


## 📦 Prerequisites

- Docker
- Docker Compose
- (Optional) Python 3.x for local development


## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Hanging-Man-Project/Hanging-Man.git
   cd Hanging-Man
   ```

2. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```bash
   PROXY_PORT=8080
   ```

3. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend: http://localhost
   - Proxy: http://localhost:8080
   - API Health: http://localhost:8080/health


## 🎮 Usage

1. Open your browser and navigate to `http://localhost`
2. Click the **"New Game"** button to start a new game
3. A random word will be selected and displayed as underscores
4. Click on letters in the virtual keyboard to make guesses
5. You have **6 attempts** to guess the word correctly
6. Win by revealing all letters before running out of attempts!


## 📡 API Endpoints

### Game Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status and version |
| GET | `/health` | Health check endpoint |
| POST | `/start` | Start a new game |
| POST | `/guess` | Make a letter guess |
| GET | `/status/{game_id}` | Get current game status |
| DELETE | `/game/{game_id}` | Delete a game |
| GET | `/games` | List all active games |

### Example Requests

**Start a new game**:
```bash
curl -X POST http://localhost:8080/start \
  -H "Content-Type: application/json" \
  -d '{"max_attempts": 6}'
```

**Make a guess**:
```bash
curl -X POST http://localhost:8080/guess \
  -H "Content-Type: application/json" \
  -d '{"game_id": "your-game-id", "letter": "A"}'
```


## 📁 Project Structure

```
Hanging-Man/
├── api/                    # FastAPI backend service
│   ├── app.py              # Main API application
│   ├── Dockerfile          # API container configuration
│   └── requirements.txt    # Python dependencies
├── frontend/               # Streamlit frontend service
│   ├── app.py              # Frontend application
│   ├── Dockerfile          # Frontend container configuration
│   └── requirements.txt    # Python dependencies
├── worker/                 # Worker service for word generation
│   ├── Dockerfile
│   └── ...
├── proxy/                  # NGINX reverse proxy
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml      # Docker Compose configuration
├── .env                    # Environment variables
└── README.md
```


## 🔄 CI/CD & Versioning Strategy

The project uses **GitHub Actions** for continuous integration and deployment:

### Pipeline Stages
1. **Build**: Docker images are built for every push on any branch.
2. **Test**: Integration tests check the API health and game logic (creation, guessing) using `curl` commands.
3. **Deploy**: On the `prod` branch, images are pushed to Docker Hub.

### Versioning
- **Docker Tags**: We do not use the `latest` tag. Instead, images are tagged with the **Git Commit SHA** (`${{ github.sha }}`) to ensure traceability and immutability.
- **Branching**:
    - `prod` (default): Stable releases.
    - `dev`: Active development and testing.
    

## 🛠 Technologies

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **httpx**: Async HTTP client for inter-service communication
- **uvicorn**: ASGI server

### Frontend
- **Streamlit**: Python framework for building interactive web apps
- **SVG Graphics**: Custom hangman visualization
- **Requests**: HTTP library for API communication

### Infrastructure
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **NGINX**: Reverse proxy and load balancer


## 📄 License

This project is open source and available for educational purposes.


## 📝 Notes

- Games are stored in memory and will be lost when the API container restarts
- The application uses a bridge network for inter-service communication
- Health checks are configured with 30-second intervals

---

**Happy Gaming! 🎮**