from datetime import datetime

import requests
import serial
import serial.tools.list_ports
from flask import Flask, jsonify, render_template, request

DOMAIN = "localhost"
PORT = 5000

INFORMATION_TYPES = [
    {"id": "spot_price", "label": "Spot-Price"},
    {"id": "total_load", "label": "Total Load"},
    {"id": "flow_in", "label": "Flow-In"},
    {"id": "flow_out", "label": "Flow-Out"},
]

app = Flask(__name__, template_folder=".")


@app.route("/")
def index():
    return render_template("index.html", info_types=INFORMATION_TYPES)


@app.route("/ports")
def list_ports():
    ports = [p.device for p in serial.tools.list_ports.comports()]
    return jsonify(ports)


@app.route("/send", methods=["POST"])
def send():
    body = request.get_json(force=True)
    info_type = body.get("info_type", "")
    timestamp = body.get("timestamp", "")

    if not info_type or not timestamp:
        return jsonify({"ok": False, "error": "Missing info_type or timestamp"}), 400

    try:
        # Fetch data snapshot
        snapshot = request_snapshot(timestamp=timestamp)
        match info_type:
            case "spot_price":
                data = extract_spot_price(snapshot)
            case "total_load":
                data = extract_total_load(snapshot)
            case "flow_in":
                data = extract_flow_in(snapshot)
            case "flow_out":
                data = extract_flow_out(snapshot)

        # Normalize data
        data = normalize(data)
        payload = f"{data}"
        # send_over_serial(data)
        return jsonify({"ok": True, "payload": payload})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/fetch", methods=["POST"])
def fetch():
    body = request.get_json(force=True)
    timestamp = body.get("timestamp", "")

    if not timestamp:
        return jsonify({"ok": False, "error": "Missing timestamp"}), 400

    try:
        # Fetch data snapshot
        return request_snapshot(timestamp=timestamp)

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


def request_snapshot(timestamp: datetime | None = None):

    if timestamp is not None:
        req = requests.get(f"http://{DOMAIN}:{PORT}/api/snapshot/{timestamp}")
    else:
        req = requests.get(f"http://{DOMAIN}:{PORT}/api/snapshot/fresh")

    assert req.status_code == 200

    return req.json()


def extract_spot_price(data) -> list[float]:
    return list(data[region]["price"] for region in sorted(data.keys()))


def extract_total_load(data) -> list[float]:
    return list(data[region]["load"] for region in sorted(data.keys()))


def extract_flow_in(data) -> list[float]:
    return list(data[region]["total_flow_in"] for region in sorted(data.keys()))


def extract_flow_out(data) -> list[float]:
    return list(data[region]["total_flow_out"] for region in sorted(data.keys()))


def normalize(data: list[float]) -> list[int]:
    """Normalize data into integers from 0 to 255"""

    minv = min(data)
    maxv = max(data)

    return list(int(((x - minv) / (maxv - minv)) * 255) for x in data)


def send_serial(data: list[int]):
    """Send byte array over serial. Assumes all integers are in range 0-255"""
    port = serial.Serial(port="COM4", baudrate=115200, timeout=0.1)
    return port.write(bytes(data))


if __name__ == "__main__":
    app.run(debug=True, port=5050)
