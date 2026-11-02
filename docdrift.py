#!/usr/bin/env python3
"""DocDrift: local documentation coverage receipts for changed public tokens."""
import argparse, json, re, subprocess, sys
from pathlib import Path

TOKEN = re.compile(r"(?:--[a-z][a-z0-9-]+\b|\b[A-Z][A-Z0-9_]{2,}\b|[\"']([a-z][a-z0-9_-]{2,})[\"']\s*:)")
DOC_NAMES = {"readme.md", "readme", "docs", "doc", "examples", "example"}

def patch(root, source):
    if source: return Path(source).read_text(encoding="utf-8")
    p = subprocess.run(["git", "-C", str(root), "diff", "--unified=0"], text=True, capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.strip() or "git diff failed")
    return p.stdout

def changed_tokens(text):
    found = set()
    for line in text.splitlines():
        if not line.startswith(("+", "-")) or line.startswith(("+++", "---")): continue
        for m in TOKEN.finditer(line[1:]): found.add(m.group(1) or m.group(0))
    return sorted(found)

def doc_files(root):
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.parts and (p.name.lower() in DOC_NAMES or any(x in DOC_NAMES for x in p.parts)):
            yield p

def receipt(root, diff):
    rows=[]
    for token in changed_tokens(diff):
        hits=[]; needle=re.compile(re.escape(token))
        for p in doc_files(root):
            try: lines=p.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError: continue
            for n,line in enumerate(lines,1):
                if needle.search(line): hits.append({"path":p.relative_to(root).as_posix(),"line":n,"text":line.strip()[:160]})
        rows.append({"token":token,"documentation_hits":hits})
    return {"tool":"DocDrift","tokens":rows,"limits":["Text matches are review leads, not proof of correct documentation.","Only changed flags, uppercase environment variables, and quoted config-like keys are recognized."]}

def md(data):
    lines=["# DocDrift receipt",f"- Changed public tokens: {len(data['tokens'])}",""]
    for row in data["tokens"]:
        lines.append(f"## `{row['token']}`")
        lines.append(f"- Documentation hits: {len(row['documentation_hits'])}")
        lines += [f"- `{h['path']}:{h['line']}` — {h['text']}" for h in row['documentation_hits']] or ["- No documentation text match found."]
        lines.append("")
    return "\n".join(lines+['## Limits']+[f"- {x}" for x in data['limits']])

def main():
    a=argparse.ArgumentParser(); a.add_argument("root",type=Path); a.add_argument("--patch"); a.add_argument("--json"); a.add_argument("--strict",action="store_true"); x=a.parse_args()
    try: data=receipt(x.root.resolve(),patch(x.root.resolve(),x.patch))
    except (OSError,RuntimeError) as e: print(f"docdrift: {e}",file=sys.stderr); return 1
    if x.json: Path(x.json).write_text(json.dumps(data,indent=2)+"\n")
    print(md(data)); return 2 if x.strict and any(not r['documentation_hits'] for r in data['tokens']) else 0
if __name__ == "__main__": raise SystemExit(main())
