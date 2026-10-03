"""
Timestamps — the generator.

One token per documented event in blockchain history. The dataset came first;
the art is derived from it. Nothing here needs installing — the whole thing is
Python standard library, so it runs on any Python 3.8+ with no dependencies.
"""
import csv, hashlib, os

__version__ = "1.0.0"

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA  = os.path.join(ROOT, "data", "collection.csv")
GRAIL = os.path.join(ROOT, "grails")


def records():
    """Every record, in token order. Token id == row id == chronological order."""
    with open(DATA, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: int(r["id"]))
    return rows


def by_id():
    return {int(r["id"]): r for r in records()}


def seed(record):
    """The art seed. Everything visual on a derived card traces back to this.

        sha256( "<event date>|<event title>" )

    Reproduce it yourself without this code:
        echo -n "2008-10-31|Bitcoin whitepaper published" | sha256sum
    """
    return hashlib.sha256(f'{record["date"]}|{record["title"]}'.encode()).hexdigest()


def is_grail(record):
    return record["tier"] == "GRAIL"


def render(record):
    """The token's SVG, as text.

    Archive cards (1,016 of them) are COMPUTED from the seed — the palette,
    the glyph, the registration strip, the paper texture all fall out of those
    bytes, so this function reconstructs the file from scratch every time.

    Grail plates (15) are COMPOSED, not computed — each is a one-off scene
    drawn for that specific event, and it ships in grails/ as source. For those
    this returns the published file. Both paths are checksummed the same way,
    so either kind can be checked against CHECKSUMS.txt.
    """
    if is_grail(record):
        with open(os.path.join(GRAIL, f'{int(record["id"]):04d}.svg'), encoding="utf-8") as f:
            return f.read()
    from . import vitrine
    return vitrine.render(record)


def digest(record):
    return hashlib.sha256(render(record).encode("utf-8")).hexdigest()
