import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="fake_profile_db",
    user="goku"
)

cursor = conn.cursor()

print("PostgreSQL connected successfully")