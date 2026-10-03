# Timestamps — the generator

[![verify](https://github.com/<BIMBOSTIC>/timestamps-art/actions/workflows/verify.yml/badge.svg)](https://github.com/<BIMBOSTIC>/timestamps-art/actions/workflows/verify.yml)

One token per documented event in blockchain history. **1,031 records, every date carrying its source.**

Most NFT collections invent their lore. This one didn't. The dataset was compiled first, from public record, and the art is derived from it — which means you don't have to take anyone's word for any of it. This repository is here so you can check.

---

## Check a token yourself

No installation. No dependencies. Python 3.9 or newer, standard library only.

```bash
git clone https://github.com/<BIMBOSTIC>/timestamps-art
cd timestamps-art
python3 verify.py
```

On Windows the command is `python` rather than `python3`. You can also skip
git entirely: use the green **Code → Download ZIP** button, unzip it, and run
`python verify.py` inside the folder.

```
checked 1031 tokens
  derived from the seed : 1016
  composed plates       : 15
  mismatches            : 0

OK — every token matches its published checksum.
```

One token at a time:

```bash
python3 verify.py 2
```

```
No. 0002  2008-10-31  Bitcoin whitepaper published
  kind      composed plate
  art seed  13359d1ccc63e6c67ba490ff70d9473d0ba6f9a76151f7016dd89617183bd633
  ...
  MATCH
```

Don't want to run anything? The badge above is this same check, run by GitHub
on a clean machine against Python 3.9, 3.11 and 3.13 every time the repository
changes. Click it to read the log.

---

## How the art is derived

Every archive card is computed from one number:

```
seed = sha256( "<event date>|<event title>" )
```

That's the whole input. The palette, the classification glyph, the paper
texture, the registration strip along the bottom, the magnitude stamp — each
one reads bytes off that hash. Nothing is random; nothing was placed by hand.
Feed the same date and title in, get a byte-identical file out, on any machine,
any time.

You can reproduce the seed without this code at all:

```bash
echo -n "2008-10-31|Bitcoin whitepaper published" | sha256sum
# 13359d1ccc63e6c67ba490ff70d9473d0ba6f9a76151f7016dd89617183bd633
```

That value is printed in token 0002's metadata. If they don't match, something
is wrong, and you should want to know.

### Two kinds of token, and the honest difference

| | count | how it's made | how you check it |
|---|---|---|---|
| **Archive card** | 1,016 | **Computed** from the seed. `generate.py` rebuilds the file from scratch. | Regenerate it and compare. |
| **Grail plate** | 15 | **Composed** — a one-off scene drawn for that specific event. | Checksum it against `CHECKSUMS.txt`. |

The grails are hand-composed artwork, not seed-derived, and this README is not
going to pretend otherwise. They ship here as source in `grails/`, so you can
still confirm that the file backing a grail token is the file that was
published and has not been swapped since. `verify.py` covers both kinds and
tells you which is which.

---

## Regenerate the artwork

```bash
python3 generate.py            # all 1,031 into out/
python3 generate.py 341        # one token to stdout
python3 generate.py 341 -o black-thursday.svg
```

Output is SVG — vector, so it stays sharp at any size, and small enough that
the whole collection is a few megabytes rather than a few hundred.

---

## What's in here

```
data/collection.csv     the 1,031 records: date, title, summary, era,
                        classification, tier, and the source for each
timestamps/             the generator
  archive.py            the catalogue card
  vitrine.py            the case it's presented in
grails/                 the 15 composed plates, as source
generate.py             regenerate the art
verify.py               check it against CHECKSUMS.txt
CHECKSUMS.txt           sha256 of all 1,031 token files
```

### The dataset

Token id, row id and chronological order are the same number: token 1 is the
earliest record, token 1,031 the latest. That ordering is fixed at mint and
cannot be changed afterwards, which is why it's worth checking before you
trust anything else here.

Sources, by count:

| source | records | what it covers |
|---|---|---|
| DeFiHackLabs | 292 | DeFi exploits, dates and loss amounts |
| Editorial research | 254 | hand-compiled from public record |
| Ethereum ERCs | 142 | finalised token and interface standards |
| Ethereum EIPs | 141 | finalised improvement proposals |
| Bitcoin Core | 124 | dated release history |
| Bitcoin BIPs | 78 | deployed proposals |

Every record has a source. Where a record has a canonical URL of its own it's
in the `source_url` column, and it travels with the token as `external_url`.

Found a date that's wrong? Open an issue. A corrected record is worth more to
this project than an uncontested one.

---

## Licence

Code: MIT, see `LICENSE`.

The dataset is a compilation of public facts; the facts themselves belong to
nobody. Artwork rights are stated at the collection's mint page.
