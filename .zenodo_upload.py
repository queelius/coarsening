#!/usr/bin/env python3
"""
Create draft Zenodo depositions for the masked-data coarsening series papers.

Reads .zenodo.json from each paper repo, creates a draft deposition via the
Zenodo REST API, and uploads the named artifact files. Does NOT publish.
The user reviews each draft on the Zenodo web UI and clicks publish (or
discards) themselves.

Usage:
    python3 .zenodo_upload.py              # plan (no uploads)
    python3 .zenodo_upload.py ALL          # upload all seven papers
    python3 .zenodo_upload.py <repo> ...   # upload specific repos
"""

import json
import sys
import os
import tomllib
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path("/home/spinoza/github/coarsening/papers").resolve()

def load_token():
    with open(os.path.expanduser("~/.zenodo.toml"), "rb") as f:
        return tomllib.load(f)["tokens"]["production"]

# Map: paper_dir -> list of artifact files (relative paths from paper root)
ARTIFACTS = {
    "masked-causes-in-series-systems": ["paper.pdf"],
    "mdrelax": ["paper/main.pdf"],
    "scrna-coarsening": ["main.pdf"],
    "spatial-coarsening": ["main.pdf"],
    "dp-coarsening": ["main.pdf"],
    "weaksup-coarsening": ["main.pdf"],
    "phenotype-coarsening": ["main.pdf"],
}

def api_request(method, url, token, data=None, content_type="application/json"):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data is not None:
        if content_type == "application/json":
            body = json.dumps(data).encode()
            req.add_header("Content-Type", "application/json")
        else:
            body = data
            req.add_header("Content-Type", content_type)
    else:
        body = None
    try:
        with urllib.request.urlopen(req, data=body) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def zenodo_metadata_from_json(zj):
    """Convert .zenodo.json shape to Zenodo deposition API metadata shape."""
    md = {
        "title": zj["title"],
        "upload_type": zj.get("upload_type", "publication"),
        "description": zj["description"],
        "creators": zj["creators"],
        "access_right": zj.get("access_right", "open"),
        "language": zj.get("language", "eng"),
        "version": zj.get("version", "0.1.0"),
        "keywords": zj.get("keywords", []),
    }
    if "publication_type" in zj:
        md["publication_type"] = zj["publication_type"]
    if "license" in zj:
        md["license"] = zj["license"]["id"] if isinstance(zj["license"], dict) else zj["license"]
    if "related_identifiers" in zj:
        md["related_identifiers"] = zj["related_identifiers"]
    return md

def create_draft(project_dir, token):
    proj_path = ROOT / project_dir
    zj_path = proj_path / ".zenodo.json"
    if not zj_path.exists():
        return None, f"No .zenodo.json in {project_dir}"
    with open(zj_path) as f:
        zj = json.load(f)

    md = zenodo_metadata_from_json(zj)

    # Step 1: create empty deposition (DRAFT only, no publish call)
    status, resp = api_request(
        "POST",
        "https://zenodo.org/api/deposit/depositions",
        token,
        data={"metadata": md},
    )
    if status not in (200, 201):
        return None, f"Create failed ({status}): {resp}"

    dep_id = resp["id"]
    bucket_url = resp["links"]["bucket"]
    html_url = resp["links"]["html"]
    reserved_doi = resp.get("metadata", {}).get("prereserve_doi", {}).get("doi", "(none)")
    created_at = resp.get("created", "(unknown)")

    # Step 2: upload each artifact via bucket (PUT new files API)
    artifacts = ARTIFACTS.get(project_dir, [])
    uploaded = []
    for a in artifacts:
        fp = proj_path / a
        if not fp.exists():
            uploaded.append(f"  ! missing: {a}")
            continue
        with open(fp, "rb") as f:
            data = f.read()
        fname = fp.name
        status, resp_u = api_request(
            "PUT",
            f"{bucket_url}/{fname}",
            token,
            data=data,
            content_type="application/octet-stream",
        )
        if status in (200, 201):
            uploaded.append(f"  OK {fname} ({len(data):,} bytes)")
        else:
            uploaded.append(f"  FAIL {fname} ({status}): {resp_u[:200] if isinstance(resp_u, str) else resp_u}")

    return {
        "project": project_dir,
        "deposition_id": dep_id,
        "html_url": html_url,
        "reserved_doi": reserved_doi,
        "uploaded": uploaded,
        "created_at": created_at,
    }, None

def main():
    args = sys.argv[1:]
    if not args:
        print("Plan (no uploads performed). Pass paper dirs as args to upload.\n")
        for p, files in ARTIFACTS.items():
            print(f"  {p}")
            zj_path = ROOT / p / ".zenodo.json"
            zmarker = "OK" if zj_path.exists() else "MISSING"
            print(f"    [{zmarker}] .zenodo.json")
            for f in files:
                fp = ROOT / p / f
                marker = "OK" if fp.exists() else "MISSING"
                size = fp.stat().st_size if fp.exists() else 0
                print(f"    [{marker}] {f} ({size:,} bytes)")
        print("\nUsage: python3 .zenodo_upload.py <paper_dir> [<paper_dir>...]")
        print("       python3 .zenodo_upload.py ALL")
        return

    if args == ["ALL"]:
        targets = list(ARTIFACTS.keys())
    else:
        targets = args

    token = load_token()
    results = []
    for t in targets:
        if t not in ARTIFACTS:
            print(f"Skipping unknown paper: {t}")
            continue
        print(f"\n=== {t} ===")
        result, err = create_draft(t, token)
        if err:
            print(f"  ERROR: {err}")
            continue
        print(f"  Deposition ID: {result['deposition_id']}")
        print(f"  Reserved DOI:  {result['reserved_doi']}")
        print(f"  Review URL:    {result['html_url']}")
        print(f"  Created:       {result['created_at']}")
        for line in result["uploaded"]:
            print(line)
        results.append(result)

    # Save summary
    summary_path = ROOT / ".zenodo_drafts.json"
    summary = {}
    # Preserve any existing summary entries
    if summary_path.exists():
        try:
            with open(summary_path) as f:
                summary = json.load(f)
        except Exception:
            summary = {}
    for r in results:
        summary[r["project"]] = {
            "draft_id": r["deposition_id"],
            "reserved_doi": r["reserved_doi"],
            "draft_url": r["html_url"],
            "status": "draft",
            "created_at": r["created_at"],
        }
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n{len(results)} draft(s) created. Summary saved to {summary_path}")
    print("Review and publish at https://zenodo.org/me/uploads")

if __name__ == "__main__":
    main()
