"""Optional periodic refresh runner for the Streamlit demonstration.

Run with: python src/refresh_service.py --interval 300
This reprocesses the currently available input telemetry and rewrites result
artifacts. It does not provide live meter ingestion or generate new readings.
"""

import argparse
import time

import pipeline


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interval", type=int, default=300, help="Refresh period in seconds (minimum 30).")
    args = parser.parse_args()
    interval = max(30, args.interval)
    while True:
        pipeline.run_full_pipeline()
        time.sleep(interval)


if __name__ == "__main__":
    main()
