from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/dolar-blue', methods=['GET'])
def get_dolar_blue():
    url = "https://dolarapi.com/v1/dolares/blue"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza error si la respuesta no es 200 OK
        data = response.json()
        
        # Se asume que la API devuelve un JSON con las claves "compra" y "venta"
        compra = float(data.get("compra"))
        venta = float(data.get("venta"))
        variacion = venta - compra
        
        resultado = {
            "compra": compra,
            "venta": venta,
            "variacion": variacion
        }
        return jsonify(resultado)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "No se pudo obtener la información", "detalle": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error al procesar la información", "detalle": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
