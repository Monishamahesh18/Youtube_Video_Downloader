# Gunicorn configuration for Railway
bind = "0.0.0.0:{}".format(os.environ.get('PORT', 5000))
workers = 2
threads = 4
timeout = 300
keepalive = 5
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
