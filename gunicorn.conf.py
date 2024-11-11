# gunicorn.conf.py
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('WORKERS', (multiprocessing.cpu_count() * 2) + 1))
worker_class = os.getenv('WORKER_CLASS', 'sync')
threads = int(os.getenv('THREADS', '2'))
timeout = int(os.getenv('TIMEOUT', '120'))

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'gunicorn_flask'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

# Hook
def on_starting(server):
    server.log.info("Starting Gunicorn server...")

def on_reload(server):
    server.log.info("Reloading Gunicorn server...")

def worker_int(worker):
    worker.log.info("Worker shutting down...")
