
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timezone
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder="static", static_url_path="/static")


# ==================== MONGODB ====================
# IMPORTANTE: Configure MONGO_URI como variável de ambiente!
# Nunca commite credenciais no código!

# Carregar variáveis do arquivo .env (desenvolvimento local)
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI não configurada! Configure a variável de ambiente.")

MONGO_DB = os.getenv("MONGO_DB", "lat-long-superacao")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "locations")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
locations_col = db[MONGO_COLLECTION]


def init_mongo():
    """Create indexes used by the app."""
    locations_col.create_index("timestamp")


def serialize_location(doc):
    """Prepare Mongo document for JSON responses."""
    return {
        "id": str(doc.get("_id")),
        "latitude": doc.get("latitude"),
        "longitude": doc.get("longitude"),
        "timestamp": doc.get("timestamp").isoformat() if isinstance(doc.get("timestamp"), datetime) else doc.get("timestamp"),
        "agent_name": doc.get("agent_name", "Anônimo"),
        "municipio": doc.get("municipio", ""),
        "observacoes": doc.get("observacoes", ""),
        "accuracy": doc.get("accuracy"),
        "altitude": doc.get("altitude"),
        "speed": doc.get("speed"),
    }


def salvar_localizacao(lat, lon, agent_name, municipio, observacoes, accuracy=None, altitude=None, speed=None):
    """Salva localização no MongoDB."""
    doc = {
        "latitude": float(lat),
        "longitude": float(lon),
        "timestamp": datetime.now(timezone.utc),
        "agent_name": agent_name,
        "municipio": municipio,
        "observacoes": observacoes,
        "accuracy": float(accuracy) if accuracy is not None else None,
        "altitude": float(altitude) if altitude not in (None, "") else None,
        "speed": float(speed) if speed not in (None, "") else None,
    }
    result = locations_col.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


# ==================== ROTAS ====================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/save-location', methods=['POST'])
def save_location():
    """API para salvar localização."""
    try:
        data = request.get_json(force=True) or {}
        lat = float(data.get("latitude"))
        lon = float(data.get("longitude"))

        saved = salvar_localizacao(
            lat,
            lon,
            data.get("agent_name", "Anônimo"),
            data.get("municipio", ""),
            data.get("observacoes", ""),
            data.get("accuracy"),
            data.get("altitude"),
            data.get("speed"),
        )

        return jsonify({
            "success": True,
            "message": "Localização salva com sucesso!",
            "location": serialize_location(saved),
        })
    except Exception as exc:  # noqa: BLE001
        return jsonify({"success": False, "message": str(exc)}), 400


@app.route('/api/get-locations', methods=['GET'])
def get_locations():
    """API para obter todas as localizações."""
    try:
        cursor = locations_col.find().sort("timestamp", -1)
        locations = [serialize_location(doc) for doc in cursor]
        return jsonify(locations)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 400


@app.route('/api/delete-location/<string:location_id>', methods=['DELETE'])
def delete_location(location_id):
    """API para deletar uma localização."""
    try:
        result = locations_col.delete_one({"_id": ObjectId(location_id)})
        return jsonify({"success": result.deleted_count == 1})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"success": False, "error": str(exc)}), 400


if __name__ == '__main__':
    init_mongo()
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG") == "1")

