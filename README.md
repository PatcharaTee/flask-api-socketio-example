# flask-api-socketio-example

Example real-time chatapp (backend) project for flask api and flask socket-io

# Requirement

- python >= 3.9.5

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
> flask init-db
> export PORT=80
> gunicorn -k eventlet -w 1 -b :$PORT app:app
```

## MacOS/Linux
```bash
> python3 -m venv venv
> . venv/bin/activate
> pip install -r requirements.txt
> flask init-db
> export PORT=80
> gunicorn -k eventlet -w 1 -b :$PORT app:app
```
