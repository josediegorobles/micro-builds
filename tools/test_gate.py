#!/usr/bin/env python3
"""Adversarial self-test for the publication gate in `build_showcase.py`.

The gate is only worth something if it is loud when it is unsure. These cases are the ways a
sanitised copy could still leak, and every one of them must be either rewritten or refused:

    python3 tools/test_gate.py        # no dependencies, exits non-zero on any failure

Case list
    plain text with the blocked string        -> rewritten, no blocklisted string left
    blocked string in a stored text member    -> rewritten
    blocked string in a binary member         -> refused (cannot be rewritten safely)
    blocked string in a member *name*         -> refused
    blocked string as UTF-16 LE / BE          -> refused
    corrupt archive that starts with PK       -> refused
    non-UTF-8 plain file                      -> refused
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SECRET = "Ploverton"
CITY = "12 Rue Principale, Ploverton"          # the string that must not survive
CLEAN = "12 Rue Principale, Springfield"
POLICY = {
    "blocklist": [SECRET.lower()],
    "replacements": [[CITY, CLEAN]],
}


def _zip(entries: list[tuple[str, bytes]]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for name, data in entries:
            zf.writestr(name, data)
    return buffer.getvalue()


CASES: dict[str, tuple[bytes, str]] = {
    # name: (content, expectation) — "rewritten" | "refused"
    "plain.txt": (f"client: {CITY}".encode(), "rewritten"),
    "stored-member.xlsx": (_zip([("xl/worksheets/sheet1.xml",
                                 f"<t>{CITY}</t>".encode())]), "rewritten"),
    "plain-utf16.csv": (f"client,{SECRET}".encode("utf-16-le"), "refused"),
    "binary-member.xlsx": (_zip([("xl/vbaProject.bin", f"...{SECRET}...".encode())]), "refused"),
    "name-leak.xlsx": (_zip([(f"xl/{SECRET}-report.xml", b"<x/>")]), "refused"),
    "utf16-member.xlsx": (_zip([("xl/worksheets/sheet1.xml",
                                 f"{SECRET}".encode("utf-16-le"))]), "refused"),
    "utf16be-member.xlsx": (_zip([("xl/worksheets/sheet1.xml",
                                   f"{SECRET}".encode("utf-16-be"))]), "refused"),
    "corrupt.xlsx": (b"PK\x03\x04" + b"\x00" * 64, "refused"),
    "non-utf8.csv": (b"ok,\xff\xfe\xfa" + SECRET.lower().encode(), "refused"),
}


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        src, dest = root / "src", root / "out"
        src.mkdir()
        for name, (content, _) in CASES.items():
            (src / name).write_bytes(content)

        policy = dict(POLICY)
        policy["files"] = [{"from": n, "to": n} for n in CASES]
        rules = root / "policy.json"
        rules.write_text(json.dumps(policy))

        proc = subprocess.run(
            [sys.executable, str(HERE / "build_showcase.py"),
             "--rules", str(rules), "--src", str(src), "--dest", str(dest)],
            capture_output=True, text=True,
        )

        def published(name: str) -> bytes | None:
            path = dest / name
            return path.read_bytes() if path.is_file() else None

        def readable(blob: bytes) -> str:
            """Text a reader could reach: the file itself, plus every decompressed member.

            Checking only the raw container bytes would be a weak assertion: in a deflated
            archive the payload is not visible there, so a sanitiser that did nothing would
            still look clean.
            """
            parts = [blob.decode("utf-8", "ignore")]
            if blob[:2] == b"PK":
                import io as _io
                import zipfile as _zip
                with _zip.ZipFile(_io.BytesIO(blob)) as zf:
                    parts += [zf.read(n).decode("utf-8", "ignore") for n in zf.namelist()]
            return "\n".join(parts)

        for name, (_, expectation) in CASES.items():
            blob = published(name)
            if expectation == "refused":
                ok = blob is None
                detail = "not published" if ok else "PUBLISHED — should have been refused"
            else:
                text = readable(blob) if blob is not None else ""
                ok = blob is not None and SECRET.lower() not in text.lower() and CLEAN in text
                detail = "rewritten and clean" if ok else "wrong, still leaking, or not rewritten"
            print(f"{'PASS' if ok else 'FAIL'}  {name:22} {expectation:9} ({detail})")
            failures += not ok

        if proc.returncode == 0 and any(e == "refused" for _, e in CASES.values()):
            print("FAIL  exit code 0 despite refused files")
            failures += 1

    print(f"\n{'all cases behave' if not failures else f'{failures} failure(s)'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
