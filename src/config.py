import os


MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 5))

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://127.0.0.1/")
DB_NAME = 'plarin'
