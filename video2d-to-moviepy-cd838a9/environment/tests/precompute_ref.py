#!/usr/bin/env python3
"""Precompute per-task anti-cheat thresholds from the oracle source scene.

Run at Docker build time. Reads /tmp/source_scene.py (the oracle solution),
computes numeric literal count, max array size, and string literal stats,
then writes /tests/gate_thresholds.json with per-task thresholds used by
compute_reward.py at verify time.
"""
from __future__ import annotations

import json
import os
import sys

from compute_reward import (
    DUMP_LITERAL_FLOOR,
    DUMP_LITERAL_MARGIN,
    FLAT_ARRAY_FLOOR,
    FLAT_ARRAY_MARGIN,
    STRING_LIT_FLOOR,
    STRING_LIT_MARGIN,
    TOTAL_STR_FLOOR,
    TOTAL_STR_MARGIN,
    SOURCE_SIZE_MULTIPLIER,
    count_literals,
    max_flat_array_size,
    max_string_literal_length,
    total_string_literal_length,
)


def main():
    source_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/source_scene.py"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "/tests/gate_thresholds.json"

    if not os.path.exists(source_path):
        print(f"ERROR: {source_path} not found", file=sys.stderr)
        sys.exit(1)

    source_bytes = os.path.getsize(source_path)
    with open(source_path) as f:
        text = f.read()

    source_literals = count_literals(text)
    source_max_array = max_flat_array_size(text)
    oracle_max_string = max_string_literal_length(text)
    oracle_total_string = total_string_literal_length(text)

    thresholds = {
        "source_size_limit": source_bytes * SOURCE_SIZE_MULTIPLIER,
        "source_bytes": source_bytes,
        "dump_threshold": max(DUMP_LITERAL_MARGIN * source_literals, DUMP_LITERAL_FLOOR),
        "source_literals": source_literals,
        "flat_array_threshold": max(FLAT_ARRAY_MARGIN * source_max_array, FLAT_ARRAY_FLOOR),
        "source_max_array": source_max_array,
        "string_lit_threshold": max(STRING_LIT_MARGIN * oracle_max_string, STRING_LIT_FLOOR),
        "oracle_max_string": oracle_max_string,
        "total_str_threshold": max(TOTAL_STR_MARGIN * oracle_total_string, TOTAL_STR_FLOOR),
        "oracle_total_string": oracle_total_string,
    }

    print(f"Oracle source: {source_bytes} bytes")
    print(f"  literals={source_literals}  dump_threshold={thresholds['dump_threshold']}")
    print(f"  max_array={source_max_array}  flat_array_threshold={thresholds['flat_array_threshold']}")
    print(f"  max_string={oracle_max_string}  string_lit_threshold={thresholds['string_lit_threshold']}")
    print(f"  total_string={oracle_total_string}  total_str_threshold={thresholds['total_str_threshold']}")
    print(f"  source_size_limit={thresholds['source_size_limit']}")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(thresholds, f, indent=2)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
