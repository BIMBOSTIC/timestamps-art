#!/usr/bin/env python3
"""
Regenerate the artwork.

    python3 generate.py                 all 1,031 into out/
    python3 generate.py 2               one token, printed to stdout
    python3 generate.py 2 -o card.svg   one token, to a file
    python3 generate.py --checksums     rewrite CHECKSUMS.txt

Needs nothing installed. Python 3.9 or newer, standard library only.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timestamps as ts

ROOT = os.path.dirname(os.path.abspath(__file__))


def main(argv):
    if "--checksums" in argv:
        lines = [f"# Timestamps v{ts.__version__} — sha256 of every token's SVG.",
                 "# Check them yourself:  python3 verify.py", ""]
        for r in ts.records():
            lines.append(f'{ts.digest(r)}  {int(r["id"]):04d}.svg')
        with open(os.path.join(ROOT, "CHECKSUMS.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"wrote CHECKSUMS.txt ({len(ts.records())} tokens)")
        return 0

    if argv and argv[0].isdigit():
        svg = ts.render(ts.by_id()[int(argv[0])])
        if "-o" in argv:
            path = argv[argv.index("-o") + 1]
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"wrote {path} ({len(svg)/1024:.1f} KiB)")
        else:
            sys.stdout.write(svg)
        return 0

    out = os.path.join(ROOT, "out")
    os.makedirs(out, exist_ok=True)
    total = 0
    for r in ts.records():
        svg = ts.render(r)
        with open(os.path.join(out, f'{int(r["id"]):04d}.svg'), "w", encoding="utf-8") as f:
            f.write(svg)
        total += len(svg)
    print(f"wrote {len(ts.records())} files to out/  ({total/1024/1024:.1f} MiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
