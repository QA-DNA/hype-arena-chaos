import csv
import json
import os
import subprocess
import sys
import time

MODE = os.environ.get("MODE", "good")
OUT = "/output"

CLAIMS = [
    ["e1", "compare", "Hooly Gemini has more monthly active users than Hooly Jules.",
     {"left": {"subject": "Hooly Gemini", "attribute": "monthly_active_users"}, "right": {"subject": "Hooly Jules", "attribute": "users"}, "op": "gt"}, "0.9"],
    ["e2", "at_event", "At Hooly I/O 2026, Hooly Gemini had 9,000 users.",
     {"subject": "Hooly Gemini", "attribute": "monthly_active_users", "event": "Hooly I/O 2026", "value": {"kind": "quantity", "value": 9000, "unit": "user"}}, "0.9"],
]


def rows():
    with open("/universe/universe.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_labels(given, delimiter=",", decimal="."):
    with open(f"{OUT}/labels.csv", "w", encoding="utf-8-sig" if delimiter == ";" else "utf-8", newline="") as f:
        w = csv.writer(f, delimiter=delimiter)
        w.writerow(["id", "label", "confidence"])
        for r in given:
            if not r["label"]:
                w.writerow([r["id"], "true", "0.8".replace(".", decimal)])


def write_claims(delimiter=",", decimal=".", label=None, extra=0):
    with open(f"{OUT}/output.csv", "w", encoding="utf-8-sig" if delimiter == ";" else "utf-8", newline="") as f:
        w = csv.writer(f, delimiter=delimiter)
        w.writerow(["id", "type", "text", "form"] + (["label"] if label else []) + ["confidence"])
        for c in CLAIMS:
            w.writerow(c[:3] + [json.dumps(c[3])] + ([label] if label else []) + [c[4].replace(".", decimal)])
        for i in range(extra):
            w.writerow([f"x{i}", "fact", "Hooly AI Pro costs €59 per month. " + "x" * 200, "{}", "0.9"])


def main():
    given = rows()
    print(f"mode {MODE}: {len(given)} rows", file=sys.stderr)
    if MODE == "good":
        write_labels(given)
        write_claims()
    elif MODE == "pip-at-runtime":
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        write_labels(given)
    elif MODE == "write-home":
        os.makedirs(os.path.expanduser("~/.cache/model"), exist_ok=True)
        write_labels(given)
    elif MODE == "oom":
        write_labels(given)
        hog = []
        while True:
            hog.append(bytearray(256 * 1024 * 1024))
    elif MODE == "forkbomb":
        write_labels(given)
        procs = [subprocess.Popen(["sleep", "60"]) for _ in range(400)]
        write_claims()
    elif MODE == "only-labels":
        write_labels(given)
    elif MODE == "old-format":
        write_claims(label="false")
    elif MODE == "excel":
        write_labels(given, ";", ",")
        write_claims(";", ",")
    elif MODE == "huge-table":
        write_labels(given)
        write_claims(extra=80000)
    elif MODE == "symlink":
        write_labels(given)
        os.symlink("/universe/universe.csv", f"{OUT}/output.csv")
    elif MODE == "crash":
        raise SystemExit("crashed before writing anything")
    elif MODE == "late-writer":
        write_labels(given)
        tmp = f"{OUT}/output.csv.tmp"
        with open(tmp, "w") as f:
            f.write("id,type,text,form,confidence\n")
        os.replace(tmp, f"{OUT}/output.csv")
        write_claims()


if __name__ == "__main__":
    main()
