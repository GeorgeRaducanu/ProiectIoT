import random
from flask import Flask, render_template, request, g, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    return db

@app.teardown_appcontext
def close_connection(e):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())

        db.commit()

def add_entry_to_db(temperature, humidity):
    with app.app_context():
        db = get_db()
        db.execute('INSERT INTO measurements (temperature, humidity) VALUES (?, ?)', [temperature, humidity])
        db.commit()

def get_entries_from_db():
    with app.app_context():
        db = get_db()
        cur = db.execute('SELECT * FROM measurements')
        entries = cur.fetchall()
        return entries
    
@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        add_entry_to_db(temperature, humidity)
        return jsonify({'status': 'Entry added'})
    except:
        return jsonify({'status': 'Entry not added'})
    
@app.route('/show', methods=['GET'])
def show_entries():
    entries = get_entries_from_db()
    return jsonify(entries)

@app.route('/dataVisualization')
def dataVisualization():
    return render_template('dataVisualization.html')

@app.route('/turnFanOn')
def turnFanOn():
    return render_template('turnFanOn.html')

@app.route('/turnFanOff')
def turnFanOff():
    return render_template('turnFanOff.html')

@app.route('/data')
def get_data():
    # Get the data from the database
    entries = get_entries_from_db()
    # In the format of 
    '''
     data = {
        "timestamps": [],
        "temperature": [],
        "humidity": [],
    }'''
    data = {'timestamps': [], 'temperature': [], 'humidity': []}
    for (_, timestamp, temperature, humidity) in entries:
        data['timestamps'].append(timestamp)
        data['temperature'].append(temperature)
        data['humidity'].append(humidity)
    return jsonify(data)
        

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()

    # Insert into the database
    # for i in range(20):
    #     add_entry_to_db(random.randint(20, 30), random.randint(40, 60))
    # Show all entries in the database
    print(get_entries_from_db())

    app.run(host='0.0.0.0', port=5001, debug=True)
    # , ssl_context=('cert.pem', 'key.pem')
