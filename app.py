import os
from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "API de Dólar Blue funcionando"}), 200

@app.route('/dolar-blue', methods=['GET'])
def get_dolar_blue():
    url_actual = "https://api.bluelytics.com.ar/v2/latest"
    url_historial = "https://api.bluelytics.com.ar/v2/evolution.json"

    try:
        # Obtener el valor actual
        response_actual = requests.get(url_actual)
        response_actual.raise_for_status()
        data_actual = response_actual.json()
        
        compra_actual = data_actual["blue"]["value_buy"]
        venta_actual = data_actual["blue"]["value_sell"]

        # Obtener el valor de ayer
        response_historial = requests.get(url_historial)
        response_historial.raise_for_status()
        data_historial = response_historial.json()

        # Filtrar por la fecha de ayer
        fecha_ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        valores_ayer = next((item for item in data_historial if item["date"] == fecha_ayer), None)

        if valores_ayer:
            compra_ayer = valores_ayer["value_buy"]
            venta_ayer = valores_ayer["value_sell"]

            # Calcular variación porcentual
            variacion_compra = ((compra_actual - compra_ayer) / compra_ayer) * 100
            variacion_venta = ((venta_actual - venta_ayer) / venta_ayer) * 100
        else:
            variacion_compra = None
            variacion_venta = None

        dolar_blue = {
            "compra": compra_actual,
            "venta": venta_actual,
            "variacion_compra_%": variacion_compra,
            "variacion_venta_%": variacion_venta
        }
        return jsonify(dolar_blue)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de solicitud: {e}"}), 500
    except KeyError:
        return jsonify({"error": "Estructura de respuesta de la API inesperada"}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
