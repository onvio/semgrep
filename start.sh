#!/bin/sh
set -x

# Start scan
semgrep --config auto --output /var/reports/semgrep.json --metrics=off --json /src

# Parse Report for SEQHUB
python3 /opt/semgrep/seqhub_report.py

cat /var/reports/seqhub.json