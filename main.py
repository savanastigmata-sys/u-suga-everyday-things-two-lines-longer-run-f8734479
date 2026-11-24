#!/usr/bin/env python3
"""Entry for make.fun: Everyday Things, Two Lines, Longer Run.

Writes a two-line explanation of a traffic jam to a 10-year-old:
line 1 is one vivid sentence built on a single analogy, line 2 is one
sentence on what the analogy maps and what it leaves out.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 400
characters, not only white space.
"""

import os
import sys

LINE_1 = (
    "A traffic jam is a conga line of cars that forgot the music, "
    "bumper to bumper and shuffling forward one step at a time while "
    "everyone waits for the front of the line to find the way out."
)

LINE_2 = (
    "It maps the stop-start shuffle and the way nothing moves until "
    "the car ahead does, but it leaves out the miserable part: nobody "
    "chose to join, nobody is having fun, and every car burns fuel "
    "standing still."
)

ENTRY_TEXT = LINE_1 + "\n" + LINE_2 + "\n"

MAX_CHARS = 400


def resolve_output_dir():
    """Return the output directory, preferring $MAKEFUN_OUTPUT_DIR."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.getcwd(), "output")


def validate(text):
    """Enforce the competition gate: 1-400 chars, exactly two lines,
    each line a single sentence, non-blank."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 2:
        raise ValueError("entry must have exactly two lines, got %d" % len(lines))
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            raise ValueError("line %d is blank" % i)
        if line.count(".") != 1 or not line.rstrip().endswith("."):
            raise ValueError(
                "line %d must be exactly one sentence ending in a period" % i
            )
        # One vivid sentence: no second clause pretending to be a
        # sentence, no list of comparisons split by semicolons.
        if ";" in line:
            raise ValueError("line %d must not contain a semicolon" % i)
    if "traffic jam" not in lines[0].lower():
        raise ValueError("line 1 must name the everyday thing it explains")
    return True


def main():
    validate(ENTRY_TEXT)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY_TEXT)
    # Read back what was written and re-validate, so a truncated or
    # re-encoded file can never pass silently.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY_TEXT:
        raise ValueError("entry.txt on disk differs from the validated text")
    validate(written)
    print("wrote %s (%d chars)" % (path, len(ENTRY_TEXT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
