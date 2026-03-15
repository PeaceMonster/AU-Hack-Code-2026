from datetime import datetime, timezone

from flask import Flask, Response, jsonify

from src.broker import get_info, get_info_timestamp
from src.model import Region

app = Flask(__name__)


AVAILABLE_REGIONS = [
    Region.AT,
    Region.BE,
    Region.CH,
    Region.CZ,
    Region.DE,
    Region.DK1,
    Region.FR,
    Region.NL,
    Region.PL,
]

# TODO: Error handling


@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"


@app.route("/api/snapshot/fresh", methods=["GET"])
def snapshot():
    data = {region: get_info(region) for region in AVAILABLE_REGIONS}
    return jsonify(data)


@app.route("/api/snapshot/fresh/<region>", methods=["GET"])
def snapshot_region(region):
    data = get_info(Region(region))
    return jsonify(data)


@app.route("/api/snapshot/<timestamp>", methods=["GET"])
def snapshot_timed(timestamp):

    # parse datetime
    ts = datetime.fromisoformat(timestamp).replace(tzinfo=timezone.utc)
    data = {region: get_info_timestamp(region, ts) for region in AVAILABLE_REGIONS}
    return jsonify(data)


@app.route("/api/snapshot/<timestamp>/<region>", methods=["GET"])
def snapshot_timed_region(timestamp, region):

    # Parse datetime and region
    ts = datetime.fromisoformat(timestamp).replace(tzinfo=timezone.utc)
    region = Region(region)
    data = get_info_timestamp(region, ts)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
