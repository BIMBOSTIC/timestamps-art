#!/usr/bin/env python3
"""
Check the collection against its published checksums.

    python3 verify.py              check all 1,031
    python3 verify.py 2            check one token
    python3 verify.py --seed 2     just print that token's art seed

Needs nothing installed. Python 3.9 or newer, standard library only.

Exit code is 0 if everything matched and 1 if anything didn't, so this works
in a script or a CI job as well as by hand.
"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timestamps as ts

CHECKSUMS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CHECKSUMS.txt")


def load_checksums():
    out = {}
    with open(CHECKSUMS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            h, name = line.split(None, 1)
            out[int(name.strip().split(".")[0])] = h
    return out


def main(argv):
    if "--seed" in argv:
        tid = int(argv[argv.index("--seed") + 1])
        r = ts.by_id()[tid]
        print(f'sha256( {r["date"]}|{r["title"]} )')
        print(ts.seed(r))
        return 0

    want = load_checksums()
    rows = ts.records()
    if argv and argv[0].isdigit():
        rows = [ts.by_id()[int(argv[0])]]

    bad, n_derived, n_composed = [], 0, 0
    for r in rows:
        tid = int(r["id"])
        got = ts.digest(r)
        ok = (got == want.get(tid))
        if ts.is_grail(r):
            n_composed += 1
        else:
            n_derived += 1
        if not ok:
            bad.append((tid, want.get(tid), got))
        if len(rows) == 1:
            kind = "composed plate" if ts.is_grail(r) else "derived card"
            print(f'No. {tid:04d}  {r["date"]}  {r["title"]}')
            print(f'  kind      {kind}')
            print(f'  art seed  {ts.seed(r)}')
            print(f'  expected  {want.get(tid)}')
            print(f'  got       {got}')
            print(f'  {"MATCH" if ok else "MISMATCH"}')

    if len(rows) > 1:
        print(f"checked {len(rows)} tokens")
        print(f"  derived from the seed : {n_derived}")
        print(f"  composed plates       : {n_composed}")
        print(f"  mismatches            : {len(bad)}")
    for tid, w, g in bad[:20]:
        print(f"  MISMATCH {tid:04d}  expected {w}  got {g}")
    if not bad:
        print("\nOK — every token matches its published checksum.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
