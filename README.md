# flask-api-socketio-example-backend

Example of realtime chat-app project for flask api, socket-io

# Requirement

- python >= 3.9.5
- SQL Database

#### Extra Requirement for windows system

- WSL (Windows subsystem for linux)


# Installation
```bash
> pip install -r requirements.txt
```

# Usage

## Windows
```bash
> wsl
> python3 -m venv venv
> . venv/bin/activate
> pip install -r requirements.txt
> export PORT=8000
> gunicorn -k eventlet -w 1 -b :$PORT app:app
```

## MacOS/Linux
```bash
> python3 -m venv venv
> . venv/bin/activate
> pip install -r requirements.txt
> export PORT=8000
> gunicorn -k eventlet -w 1 -b :$PORT app:app
```
