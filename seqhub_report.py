import json
import os.path


def create_empty_seqhub_report():
    with open('/var/reports/seqhub.json', 'w') as f:
        json.dump({"vulnerabilities": []}, f, indent=4)
    return


def parse_report(semgrep_report, seqhub_report):

    semgrep_findings = []
    seqhub_findings = {"vulnerabilities": []}

    if not os.path.isfile(semgrep_report):
        return print("Semgrep report not found. Error during scan / No Results ?")
    if os.path.getsize(semgrep_report) == 0:
        return print("Semgrep report is empty. 0 Results ?")

    try:
        with open(semgrep_report, 'r') as file:
            semgrep_json = file.read()
            semgrep_findings = json.loads(semgrep_json)

        for vuln in semgrep_findings['results']:
            type = vuln["extra"]["severity"]
            file = vuln['path'].replace('/var/src', '')
            linenumber = vuln['start']['line']
            message = vuln["extra"]["message"][:100]
            severity = vuln["extra"]["metadata"]["impact"]

            with open(seqhub_report, 'w'):
                seqhub_findings["vulnerabilities"].append({
                    "title": f"{type} in {file} at line {linenumber}",
                    "description": message,
                    "severity": severity,
                })

            with open(seqhub_report, 'w') as f:
                json.dump(seqhub_findings, f, indent=4)
    except Exception as ex:
        error = "Error Parsing Semgrep JSON Report. An exception of type {0} occurred. Arguments:\n{1!r}"
        error = error.format(type(ex).__name__, ex.args)
        print(error)


create_empty_seqhub_report()
parse_report('/var/reports/semgrep.json', '/var/reports/seqhub.json')