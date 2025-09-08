from flask import Flask
import os
import psycopg2
import time
import pytz
from datetime import datetime

utc_time = datetime.utcnow()
kiev_tz = pytz.timezone('Europe/Kiev')
kiev_time = utc_time.replace(tzinfo=pytz.utc).astimezone(kiev_tz)

print("Kiev time:", kiev_time)

app = Flask(__name__)


def get_db_connection():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                dbname=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                host="db"
            )
            return conn
        except Exception as e:
            print(f"DB connection failed, retrying... ({i+1}/10)")
            time.sleep(2)
    raise Exception("Cannot connect to DB after 10 attempts")


@app.route("/")
def home():
    return "🚀 Hello from Flask running in Docker!"


@app.route("/db")
def db_check():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="db"
        )
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        return f"✅ DB connected! Time: {result}"
    except Exception as e:
        return f"❌ DB connection failed: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
