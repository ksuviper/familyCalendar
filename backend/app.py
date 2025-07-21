from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_db():
    conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB', 'familycalendar'),
        user=os.environ.get('POSTGRES_USER', 'user'),
        password=os.environ.get('POSTGRES_PASSWORD', 'pass'),
        host=os.environ.get('POSTGRES_HOST', 'db'),
        port=5432
    )
    return conn

@app.route('/api/chores', methods=['GET'])
def get_chores():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, task, assignee, points, completed FROM chores ORDER BY id')
    chores = [
        dict(zip(['id', 'task', 'assignee', 'points', 'completed'], row))
        for row in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return jsonify(chores)

@app.route('/api/chores', methods=['POST'])
def add_chore():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO chores (task, assignee, points, completed) VALUES (%s, %s, %s, %s) RETURNING id, task, assignee, points, completed',
        (data['task'], data.get('assignee'), data.get('points', 1), False)
    )
    chore = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(zip(['id', 'task', 'assignee', 'points', 'completed'], chore)))

@app.route('/api/chores/<int:chore_id>', methods=['PUT'])
def update_chore(chore_id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'UPDATE chores SET completed=%s WHERE id=%s RETURNING id, task, assignee, points, completed',
        (data['completed'], chore_id)
    )
    chore = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(zip(['id', 'task', 'assignee', 'points', 'completed'], chore)))

@app.route('/api/chores/<int:chore_id>', methods=['DELETE'])
def delete_chore(chore_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM chores WHERE id=%s', (chore_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})

# --- Meals ---
@app.route('/api/meals', methods=['GET'])
def get_meals():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT day, meal FROM meals')
    meals = [dict(zip(['day', 'meal'], row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(meals)

@app.route('/api/meals', methods=['POST'])
def add_meal():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO meals (day, meal) VALUES (%s, %s) ON CONFLICT (day) DO UPDATE SET meal=EXCLUDED.meal RETURNING day, meal',
        (data['day'], data['meal'])
    )
    meal = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(zip(['day', 'meal'], meal)))

@app.route('/api/meals/<day>', methods=['DELETE'])
def delete_meal(day):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM meals WHERE day=%s', (day,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})

# --- Settings ---
@app.route('/api/settings', methods=['GET'])
def get_settings():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT key, value FROM settings')
    settings = {row[0]: row[1] for row in cur.fetchall()}
    cur.close()
    conn.close()
    # Fill missing keys with empty string
    for k in ['familyName', 'icsUrl', 'weatherApiKey', 'weatherCity']:
        settings.setdefault(k, '')
    return jsonify(settings)

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    for k, v in data.items():
        cur.execute(
            'INSERT INTO settings (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET value=EXCLUDED.value',
            (k, v)
        )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)