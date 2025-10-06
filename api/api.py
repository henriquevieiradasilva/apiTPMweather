from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'ml'))

from weather_model import prever_data_futura

app = Flask(__name__)
CORS(app)  # habilita CORS para todos os domínios

@app.route('/healthz', methods=['GET'])
def health():
    return "ok", 200

# POST original
@app.route('/prever', methods=['POST'])
def prever_post():
    data_json = request.get_json()
    if not data_json:
        return jsonify({'erro': 'É necessário enviar um JSON.'}), 400

    data = data_json.get('data')
    lat = data_json.get('lat', -23.08720429991206)
    lon = data_json.get('lon', -47.2100151415641)

    if not data:
        return jsonify({'erro': 'Parametro "data" é obrigatório. Use formato YYYY-MM-DD.'}), 400

    try:
        previsao = prever_data_futura(
            data_futura_str=data,
            lat=lat,
            lon=lon,
            alvos=["T2M", "PRECTOTCORR", "RH2M", "WS2M"]
        )
        resultado = {
            'data': data,
            'lat': lat,
            'lon': lon,
            'temperatura': previsao.get('Temperatura (°C)'),
            'precipitacao': previsao.get('Precipitação (mm)'),
            'umidade': previsao.get('Umidade (%)'),
            'vento': previsao.get('Vento (m/s)')
        }
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/prever', methods=['GET'])
def prever_get():
    data = request.args.get('data')
    lat = float(request.args.get('lat', -23.08720429991206))
    lon = float(request.args.get('lon', -47.2100151415641))

    if not data:
        return jsonify({'erro': 'Parametro "data" é obrigatório.'}), 400

    # fallback de teste
    resultado = {
        'data': data,
        'lat': lat,
        'lon': lon,
        'temperatura': 25.0,
        'precipitacao': 0.0,
        'umidade': 60,
        'vento': 3.0
    }
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

