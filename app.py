from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Endpoint para obtener el precio del dólar blue
@app.route('/dolar-blue', methods=['GET'])
def get_dolar_blue():
    url = "https://api.bluelytics.com.ar/v2/latest"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        dolar_blue = {
            "compra": data["blue"]["value_buy"],
            "venta": data["blue"]["value_sell"],
            "variacion": data["blue"]["value_sell"] - data["blue"]["value_buy"]
        }
        return jsonify(dolar_blue)
    else:
        return jsonify({"error": "No se pudo obtener la información"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
