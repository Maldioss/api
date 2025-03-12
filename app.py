from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/dolar-blue', methods=['GET'])
def get_dolar_blue():
    url = "https://api.bluelytics.com.ar/v2/latest"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP (4xx o 5xx)
        data = response.json()
        dolar_blue = {
            "compra": data["blue"]["value_buy"],
            "venta": data["blue"]["value_sell"],
            "variacion": data["blue"]["value_sell"] - data["blue"]["value_buy"]
        }
        return jsonify(dolar_blue)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error de solicitud: {e}"}), 500
    except KeyError:
        return jsonify({"error": "Estructura de respuesta de la API inesperada"}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
