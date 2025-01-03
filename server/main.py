import random
from flask import Flask, render_template, request, g, jsonify
import sqlite3
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

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

fan_status = {'status': 'off'}

@app.route('/fan_status', methods=['GET'])
def fan_info():
    global fan_status
    return jsonify(fan_status)

@app.route('/dataVisualization')
def dataVisualization():
    return render_template('dataVisualization.html')

@app.route('/turnFanOn')
def turnFanOn():
    global fan_status
    fan_status['status'] = 'on'
    #print(fan_status)
    return render_template('turnFanOn.html')

@app.route('/turnFanOff')
def turnFanOff():
    global fan_status
    fan_status['status'] = 'off'
    #print(fan_status)
    return render_template('turnFanOff.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/calculate')
def calculate():
    entries = get_entries_from_db()
    if len(entries) < 10:
        return jsonify({'status': 'Not enough data to predict'})
    min_temp = min([entry[2] for entry in entries])
    min_hum = min([entry[3] for entry in entries])
    max_temp = max([entry[2] for entry in entries])
    max_hum = max([entry[3] for entry in entries])
    avg_temp = sum([entry[2] for entry in entries]) / len(entries)
    avg_hum = sum([entry[3] for entry in entries]) / len(entries)

    # use arima model to predict the temperature and humidity
    # use the last 10 entries to predict the next entry

    temps = [entry[2] for entry in entries][-10:]
    hums = [entry[3] for entry in entries][-10:]

    temp_model = ARIMA(temps, order=(1, 0, 0))
    temp_model_fit = temp_model.fit()
    temp_forecast = temp_model_fit.forecast(steps=1)[0]
    # Round the forecasted value to 2 decimal places
    temp_forecast = np.round(temp_forecast, 1)

    hum_model = ARIMA(hums, order=(1, 0, 0))
    hum_model_fit = hum_model.fit()
    hum_forecast = hum_model_fit.forecast(steps=1)[0]
    hum_forecast = np.round(hum_forecast, 2)

    return jsonify({
        'min_temp': min_temp,
        'min_hum': min_hum,
        'max_temp': max_temp,
        'max_hum': max_hum,
        'avg_temp': avg_temp,
        'avg_hum': avg_hum,
        'predicted_temp': temp_forecast,
        'predicted_hum': hum_forecast
    })

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
    for i in range(20):
        add_entry_to_db(random.randint(20, 25), random.randint(40, 45))
    # Show all entries in the database
    print(get_entries_from_db())

    app.run(host='0.0.0.0', port=5001, ssl_context=('cert.pem', 'key.pem'), debug=True)
    # , ssl_context=('cert.pem', 'key.pem')
