#!/usr/bin/env python3
"""
Deposit the coarsening-at-random monograph to Zenodo.

The shared papers/.zenodo_upload.py is hardwired to the papers/ tree; the
monograph lives in the umbrella repo at monograph/, so it gets this focused
tool. Subcommands keep the reversible step (draft) cleanly separate from the
irreversible one (publish), per the repo's Zenodo guardrails.

  python3 .zenodo_deposit.py plan        # show metadata + artifact, no network
  python3 .zenodo_deposit.py enumerate   # list own depositions matching the title (dedup check)
  python3 .zenodo_deposit.py draft       # create DRAFT, upload PDF, read back, record state
  python3 .zenodo_deposit.py verify ID   # GET deposition ID and print title/files/doi
  python3 .zenodo_deposit.py publish ID  # PUBLISH deposition ID (IRREVERSIBLE), read back, record state

Token: ~/.zenodo.toml -> [tokens].production
State: written to the canonical repo-root .zenodo_drafts.json (monograph block).
"""

import json
import os
import sys
import tomllib
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent                  # .../coarsening/monograph
ZJSON = HERE / ".zenodo.json"
PDF = HERE / "coarsening-at-random.pdf"
STATE = HERE.parent / ".zenodo_drafts.json"             # canonical repo-root file
API = "https://zenodo.org/api/deposit/depositions"
TITLE_MATCH = "Coarsening at Random: A Small Monograph"  # for the dedup scan


def load_token():
    with open(os.path.expanduser("~/.zenodo.toml"), "rb") as f:
        return tomllib.load(f)["tokens"]["production"]


def api(method, url, token, data=None, ctype="application/json"):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    body = None
    if data is not None:
        if ctype == "application/json":
            body = json.dumps(data).encode()
            req.add_header("Content-Type", "application/json")
        else:
            body = data
            req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, data=body) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {"raw": "<unparseable error body>"}


def metadata():
    zj = json.load(open(ZJSON))
    md = {
        "title": zj["title"],
        "upload_type": zj.get("upload_type", "publication"),
        "description": zj["description"],
        "creators": zj["creators"],
        "access_right": zj.get("access_right", "open"),
        "language": zj.get("language", "eng"),
        "version": zj.get("version", "v0.1.0"),
        "keywords": zj.get("keywords", []),
    }
    if "publication_type" in zj:
        md["publication_type"] = zj["publication_type"]
    if "license" in zj:
        lic = zj["license"]
        md["license"] = lic["id"] if isinstance(lic, dict) else lic
    if "related_identifiers" in zj:
        md["related_identifiers"] = zj["related_identifiers"]
    return md


def load_state():
    if STATE.exists():
        return json.load(open(STATE))
    return {}


def save_state(state):
    json.dump(state, open(STATE, "w"), indent=2)
    print(f"  state -> {STATE}")


def cmd_plan():
    md = metadata()
    print("Metadata:")
    print(f"  title:   {md['title']}")
    print(f"  type:    {md['upload_type']}/{md.get('publication_type')}")
    print(f"  version: {md['version']}")
    print(f"  license: {md.get('license')}")
    print(f"  related: {len(md.get('related_identifiers', []))} concept DOIs (relation=references)")
    print(f"Artifact: {PDF.name}  ({PDF.stat().st_size:,} bytes)" if PDF.exists() else f"Artifact MISSING: {PDF}")


def cmd_enumerate():
    token = load_token()
    # Zenodo caps page size at 100; paginate through the whole account so the
    # dedup scan never misses a record.
    all_deps, page = [], 1
    while True:
        status, resp = api("GET", f"{API}?size=100&page={page}&sort=mostrecent", token)
        if status != 200:
            print(f"  list failed ({status}): {resp}")
            sys.exit(1)
        all_deps.extend(resp)
        if len(resp) < 100:
            break
        page += 1
    print(f"  {len(all_deps)} depositions in account. Matches for monograph title:")
    found = [d for d in all_deps if TITLE_MATCH.lower() in (d.get("title") or "").lower()]
    if not found:
        print("    (none) -> safe to create a fresh record")
    for d in found:
        print(f"    id={d['id']} state={d.get('state')} title={d.get('title')!r} doi={d.get('doi') or d.get('metadata',{}).get('prereserve_doi',{}).get('doi')}")
    return found


def cmd_draft():
    token = load_token()
    # Dedup guardrail: never create if a monograph record already exists.
    existing = cmd_enumerate()
    if existing:
        print("  ABORT: a monograph deposition already exists (see above). Not creating a duplicate.")
        sys.exit(1)
    if not PDF.exists():
        print(f"  ABORT: artifact missing: {PDF}")
        sys.exit(1)

    status, resp = api("POST", API, token, data={"metadata": metadata()})
    if status not in (200, 201):
        print(f"  create failed ({status}): {resp}")
        sys.exit(1)
    dep_id = resp["id"]
    bucket = resp["links"]["bucket"]
    html = resp["links"]["html"]
    reserved = resp.get("metadata", {}).get("prereserve_doi", {}).get("doi", "(none)")
    print(f"  draft created: id={dep_id}  reserved_doi={reserved}")

    data = PDF.read_bytes()
    status, ru = api("PUT", f"{bucket}/{PDF.name}", token, data=data, ctype="application/octet-stream")
    if status not in (200, 201):
        print(f"  upload FAILED ({status}): {ru}")
        sys.exit(1)
    print(f"  uploaded {PDF.name} ({len(data):,} bytes)")

    # Read back to verify by embedded content.
    ok = cmd_verify(dep_id, token=token)
    st = load_state()
    st["monograph"] = {
        "concept_doi": None,
        "cite_doi": None,
        "cite_doi_kind": "concept",
        "published": None,
        "draft": {
            "id": dep_id,
            "reserved_version_doi": reserved,
            "draft_url": html,
            "state": "draft",
            "verified_readback": ok,
        },
    }
    save_state(st)
    print(f"\n  Review at: {html}")
    print(f"  To mint (IRREVERSIBLE): python3 .zenodo_deposit.py publish {dep_id}")


def cmd_verify(dep_id, token=None):
    token = token or load_token()
    status, resp = api("GET", f"{API}/{dep_id}", token)
    if status != 200:
        print(f"  verify failed ({status}): {resp}")
        return False
    files = resp.get("files", [])
    md = resp.get("metadata", {})
    print(f"  read-back id={dep_id} state={resp.get('state')}")
    print(f"    title:   {md.get('title')!r}")
    print(f"    version: {md.get('version')}")
    print(f"    files:   {[(f.get('filename'), f.get('filesize')) for f in files]}")
    print(f"    doi:     {resp.get('doi') or md.get('prereserve_doi',{}).get('doi')}")
    title_ok = md.get("title") == metadata()["title"]
    file_ok = any(f.get("filename") == PDF.name and f.get("filesize") == PDF.stat().st_size for f in files)
    print(f"    checks:  title={'OK' if title_ok else 'MISMATCH'}  pdf={'OK' if file_ok else 'MISSING/SIZE-MISMATCH'}")
    return title_ok and file_ok


def cmd_publish(dep_id):
    token = load_token()
    print(f"  Verifying {dep_id} before publish...")
    if not cmd_verify(dep_id, token=token):
        print("  ABORT: read-back verification failed; not publishing.")
        sys.exit(1)
    status, resp = api("POST", f"{API}/{dep_id}/actions/publish", token)
    if status not in (200, 201, 202):
        print(f"  publish FAILED ({status}): {resp}")
        sys.exit(1)
    md = resp.get("metadata", {})
    version_doi = resp.get("doi") or md.get("doi")
    concept_doi = resp.get("conceptdoi") or md.get("conceptdoi")
    rec_url = resp.get("links", {}).get("record_html") or resp.get("links", {}).get("html")
    print(f"  PUBLISHED id={dep_id}")
    print(f"    version DOI: {version_doi}")
    print(f"    concept DOI: {concept_doi}")
    print(f"    record:      {rec_url}")
    st = load_state()
    st["monograph"] = {
        "concept_doi": concept_doi,
        "cite_doi": concept_doi,
        "cite_doi_kind": "concept",
        "published": {
            "id": dep_id,
            "version_doi": version_doi,
            "version": md.get("version"),
            "state": "done",
            "url": rec_url,
        },
        "draft": None,
    }
    save_state(st)


def main():
    args = sys.argv[1:]
    if not args or args[0] == "plan":
        cmd_plan()
    elif args[0] == "enumerate":
        cmd_enumerate()
    elif args[0] == "draft":
        cmd_draft()
    elif args[0] == "verify" and len(args) == 2:
        cmd_verify(int(args[1]))
    elif args[0] == "publish" and len(args) == 2:
        cmd_publish(int(args[1]))
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
