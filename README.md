# flask-api-socketio-example-backend

Example of realtime chat-app project for flask api, socket-io

# Requirement

- Python >= 3.9.5
- SQL Database

** Required package for this project list in requirements.txt

#### Extra Requirement for windows system

- WSL (Windows subsystem for linux)


# Installation
```bash
> pip install -r requirements.txt
```

# Usage

### Windows
```bash
> wsl
> python3 -m venv venv
> . venv/bin/activate
> pip install -r requirements.txt
> export PORT=8000
> gunicorn -k eventlet -w 1 -b :$PORT app:app
```

### MacOS/Linux
```bash
> python3 -m venv venv
> . venv/bin/activate
> pip install -r requirements.txt
> export PORT=8000
> gunicorn -k eventlet -w 1 -b :$PORT app:app
```

# Other
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [WSL](https://docs.microsoft.com/en-us/windows/wsl/install)
