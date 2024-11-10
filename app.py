from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine

app = Flask(__name__)

DATABASE_URI = 'postgresql://postgres:pamet123@db:5432/postgres'  # db is the service name from docker-compose.yml
engine = create_engine(DATABASE_URI)


# PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        host='db',
        database='postgres',
        user='postgres',
        password='pamet123'
    )
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    if task_name:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (name) VALUES (%s)', (task_name,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))


@app.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
