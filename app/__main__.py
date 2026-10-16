import argparse
import os

import uvicorn

parser = argparse.ArgumentParser(description="Start the synthetic training fixture on localhost.")
parser.add_argument("--port", type=int, default=8787)
args = parser.parse_args()
os.environ["CHARGING_DEMO"] = "1"
uvicorn.run("app.main:app", host="127.0.0.1", port=args.port, access_log=True)
