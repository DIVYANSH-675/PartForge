"""Inspect exported Img2CAD command arrays without loading inference models."""
import argparse
import json
import math
from collections import Counter
from pathlib import Path


COMMANDS = ("Line", "Arc", "Circle", "EOS", "SOL", "Ext")


def inspect_vector(rows):
    errors, counts = [], Counter()
    ended = False
    if not isinstance(rows, list) or not rows:
        return {"valid": False, "errors": ["Expected a nonempty command array"], "commands": {}}
    for index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != 17:
            errors.append(f"row {index}: expected 17 columns")
            continue
        if any(type(x) not in (int, float) or not math.isfinite(x) for x in row):
            errors.append(f"row {index}: values must be finite numbers")
            continue
        command = row[0]
        if command != int(command) or not 0 <= command < len(COMMANDS):
            errors.append(f"row {index}: unknown command {command}")
            continue
        name = COMMANDS[int(command)]
        counts[name] += 1
        if ended and name != "EOS":
            errors.append(f"row {index}: command after end-of-sequence")
        ended = ended or name == "EOS"
    if not counts["Ext"]:
        errors.append("No extrusion command found")
    if not counts["SOL"]:
        errors.append("No start-of-loop command found")
    return {"valid": not errors, "rows": len(rows), "commands": dict(counts), "errors": errors}


def inspect_file(path):
    path = Path(path)
    try:
        if path.suffix.lower() in (".h5", ".hdf5"):
            import h5py
            with h5py.File(path, "r") as handle:
                vectors = {"vec": handle["vec"][()].tolist()}
        else:
            vectors = json.loads(path.read_text())
            if isinstance(vectors, list):
                vectors = {"vec": vectors}
        if not isinstance(vectors, dict) or "vec" not in vectors:
            raise ValueError("Expected a vec array")
        result = inspect_vector(vectors["vec"])
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        result = {"valid": False, "errors": [str(exc)]}
    return {"file": str(path), **result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {"checks": [inspect_file(path) for path in args.files],
              "scope": "Command structure only; not geometric validity or printability."}
    text = json.dumps(report, indent=2, allow_nan=False)
    if args.output:
        args.output.write_text(text + "\n")
    else:
        print(text)
    return int(any(not entry["valid"] for entry in report["checks"]))


if __name__ == "__main__":
    raise SystemExit(main())
