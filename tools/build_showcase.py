#!/usr/bin/env python3
"""Build and verify the published copies of the sample outputs.

The five tools live in a private working tree. This repository publishes **documentation plus
finished sample outputs** — never source code, never a client proposal, never client-identifying
information. This script is the publication step, and it is deliberately readable: the point is
that you can check *how* the published copies were produced rather than take it on trust.

    python3 tools/build_showcase.py --rules <rules.json> [--src <dir>] [--dest <dir>]
    python3 tools/build_showcase.py --rules <rules.json> --check     # verify the published copies

`--rules` points at the publication policy: the artefact list, the strings that must not reach the
repository, and their replacements. The real policy is kept outside this repository, because the
blocklist itself names the clients it protects. See `tools/sanitize.example.json` for the schema.

**It fails closed.** A file that cannot be read, decoded or rewritten is *not published*, and an
artefact is only copied after the sanitised result has been re-read and found clean. The whole
point of the gate is that it is loud when it is unsure, so nothing here is allowed to swallow an
error and continue.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import zipfile
from pathlib import Path

#: Extensions whose contents are plain text once an OOXML container is opened.
TEXT_EXT = (".xml", ".rels", ".csv", ".txt", ".json")


class PublicationError(RuntimeError):
    """Raised whenever the policy cannot be applied with certainty. Never swallowed."""


def _replacements(policy: dict) -> list[list[str]]:
    return [[str(old), str(new)] for old, new in policy["replacements"]]


def _apply(text: str, replacements: list[list[str]]) -> str:
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def _decode(raw: bytes, where: str) -> str:
    """Strict decode. A member we cannot decode is a member we cannot sanitise, so we stop."""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PublicationError(
            f"{where}: not valid UTF-8, so it cannot be sanitised safely ({exc}). "
            "Refusing to publish rather than publish half-sanitised content."
        ) from exc


def sanitize(blob: bytes, replacements: list[list[str]], where: str) -> bytes:
    """Apply the replacements to a plain file *and* inside OOXML containers.

    A byte-level replacement does not work on `.xlsx`: members are deflated, so the text is not
    visible in the container bytes. The archive is rewritten member by member, touching only text
    members and leaving every other entry untouched.
    """
    if blob[:2] != b"PK":
        return _apply(_decode(blob, where), replacements).encode("utf-8")

    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as zf:
            if zf.testzip() is not None:
                raise PublicationError(f"{where}: corrupt OOXML archive (bad member CRC).")
            infos = zf.infolist()
            members = {i.filename: zf.read(i.filename) for i in infos}
    except zipfile.BadZipFile as exc:
        raise PublicationError(
            f"{where}: starts like an OOXML archive but cannot be read ({exc}). "
            "Refusing to publish unsanitised content."
        ) from exc

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as out:
        for info in infos:
            data = members[info.filename]
            if info.filename.endswith(TEXT_EXT):
                text = _apply(_decode(data, f"{where}!{info.filename}"), replacements)
                data = text.encode("utf-8")
            out.writestr(info, data)
    return buffer.getvalue()


def leaks(blob: bytes, patterns: list[str], where: str) -> list[str]:
    """Every blocklisted string visible anywhere in the document.

    Scans raw bytes **and** decoded text, and scans *every* archive member rather than only the
    text ones: metadata, stored binary members (`vbaProject.bin`, `embeddings/`, `printerSettings`)
    and even member names are all reachable by a reader.
    """
    as_bytes = re.compile(b"|".join(p.encode("utf-8") for p in patterns), re.IGNORECASE)
    as_text = re.compile("|".join(patterns), re.IGNORECASE)

    def scan(raw: bytes, label: str, found: set[str]) -> None:
        for m in as_bytes.finditer(raw):
            found.add(m.group(0).decode("utf-8", "ignore").lower())
        # Try the encodings a text member can plausibly use. Errors are ignored *here* because
        # this is a detector, not a rewrite: a garbage decode that happens to match is a false
        # positive, which is the safe direction for a publication gate.
        for encoding in ("utf-8", "utf-16-le", "utf-16-be"):
            for m in as_text.finditer(raw.decode(encoding, "ignore")):
                found.add(m.group(0).lower())

    found: set[str] = set()
    scan(blob, where, found)
    if blob[:2] == b"PK":
        try:
            with zipfile.ZipFile(io.BytesIO(blob)) as zf:
                for info in zf.infolist():
                    scan(info.filename.encode("utf-8"), f"{where}!name", found)
                    scan(zf.read(info.filename), f"{where}!{info.filename}", found)
        except zipfile.BadZipFile:
            # Not readable as an archive: the byte scan above is all we have, and `sanitize`
            # will already have refused to publish it.
            pass
    return sorted(found)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rules", required=True, help="publication policy JSON (kept private)")
    ap.add_argument("--src", default=".", help="root of the private working tree")
    ap.add_argument("--dest", default=".", help="root of this repository")
    ap.add_argument("--check", action="store_true",
                    help="verify the published copies in --dest instead of rebuilding them")
    args = ap.parse_args()

    policy = json.loads(Path(args.rules).read_text())
    replacements = _replacements(policy)
    patterns: list[str] = policy["blocklist"]
    src_root = Path(args.src).expanduser()
    dest_root = Path(args.dest).expanduser()

    problems = 0
    for entry in policy["files"]:
        target = entry["to"]
        try:
            if args.check:
                # Check what is *published*, not what is in the source tree: a copy edited by hand
                # after publication has to fail this too.
                dst = dest_root / target
                if not dst.is_file():
                    print(f"MISSING  {target}")
                    problems += 1
                    continue
                found = leaks(dst.read_bytes(), patterns, target)
            else:
                src = src_root / entry["from"]
                if not src.is_file():
                    print(f"MISSING  {entry['from']}")
                    problems += 1
                    continue
                # Sanitise first, then re-read the result: a survivor means the policy is wrong,
                # not that we publish it anyway.
                patched = sanitize(src.read_bytes(), replacements, entry["from"])
                found = leaks(patched, patterns, target)
        except PublicationError as exc:
            print(f"REFUSED  {target}: {exc}")
            problems += 1
            continue

        if found:
            print(f"LEAK     {target}: {', '.join(found)}")
            problems += 1
            continue

        if args.check:
            print(f"ok       {target}")
            continue

        dst = dest_root / target
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(patched)
        print(f"wrote    {target}  ({len(patched):,} bytes)")

    if problems:
        print(f"\n{problems} problem(s) — nothing published for those files.", file=sys.stderr)
        return 1
    suffix = " Published copies verified." if args.check else " Sanitised copies written."
    print(f"\n{len(policy['files'])} artefact(s) clean.{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
