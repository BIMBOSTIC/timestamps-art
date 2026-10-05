# Verifying your token

You own a Timestamps token. This page shows you how to check, yourself, that
what you own is what it claims to be — without trusting anyone who made it.

**The quickest way:** open the
[browser verifier](https://bimbostic.github.io/timestamps-art/verify.html), type
your record number, and read the result. It fetches the public dataset and the
file stored on Arweave and does the arithmetic in your own browser — nothing is
computed on our servers, so there is nothing of ours to trust.

The rest of this page is the long way round, which is worth doing once if you
care about the answer.

There are four levels. Each one is independent. You can stop at any of them.

---

## Level 0 — Check the history. No tools, two minutes.

Open your token on any marketplace. The description carries three things:

- **what happened**
- **the date it happened**
- **where that date came from**

Click the source. Read it. Does the date on the page match the date on the
token?

This is the level that matters most and almost nobody does it. The art is
downstream of the dataset; if a date is wrong, nothing else saves it.

If you find a date that disagrees with its source, **open an issue**. A
corrected record is worth more to this project than an uncontested one.

---

## Level 1 — Check the art seed. One command, no download.

Every derived card is computed from one number:

```
seed = sha256( "<event date>|<event title>" )
```

Your token's metadata contains that seed under `timestamps.art_seed`. Compute it
yourself from the date and title printed on the card:

```bash
echo -n "2008-10-31|Bitcoin whitepaper published" | sha256sum
```

```
13359d1ccc63e6c67ba490ff70d9473d0ba6f9a76151f7016dd89617183bd633
```

On macOS use `shasum -a 256` instead of `sha256sum`. On Windows, use Git Bash,
WSL, or skip to Level 2 which works everywhere.

The date and title go in exactly as printed, separated by a single `|`, with no
spaces around it. If the hash you compute matches the one in the metadata, the
seed is honest — the art really was derived from that record, not attached to it
afterwards.

---

## Level 2 — Regenerate your token's art. Five minutes.

This is the real test: rebuild the image from scratch and compare it to the one
on-chain.

You need Python 3.9 or newer. Nothing else — no pip install, no dependencies.

```bash
git clone https://github.com/BIMBOSTIC/timestamps-art
cd timestamps-art
python3 verify.py 189
```

Replace `189` with your token's record number — the `No. 0189` printed at the
top of the card.

```
No. 0189  2017-02-02  EIP-196: Precompiled contracts for addition and scalar …
  kind      derived card
  art seed  a65172adcfd4…
  expected  2e2cdb50b30823ba0d42585fa6cae77404a72046dd70f8b1405c5533f49b757f
  got       2e2cdb50b30823ba0d42585fa6cae77404a72046dd70f8b1405c5533f49b757f
  MATCH
```

To look at the regenerated card rather than just its hash:

```bash
python3 generate.py 189 -o check.svg
```

Open `check.svg` in a browser and put it next to your token. Same palette, same
layout, same barcode, same seed hash in the corner. It is the same file.

### Comparing against the live image, not just the checksum

The checksum above comes from this repository. To compare against what is
actually stored on Arweave, fetch that too:

1. Read `tokenURI(<your token id>)` on the contract. You'll get `ar://<tx>/…json`.
2. Swap `ar://` for `https://arweave.net/` and open it. That's your metadata.
3. Take its `image` field, swap `ar://` the same way, and download it.
4. Compare that file to your regenerated one:

```bash
sha256sum check.svg
```

Three numbers should agree: the repository's checksum, the file on Arweave, and
the file you just generated. If all three match, the art you own is exactly what
this code produces from that historical record — and no one, including the
collection's creator, can quietly change it.

---

## Level 3 — Verify the entire collection. One command.

```bash
python3 verify.py
```

```
checked 1031 tokens
  derived from the seed : 1016
  composed plates       : 15
  mismatches            : 0

OK — every token matches its published checksum.
```

This regenerates all 1,031 and checks every one. It takes under a minute.

You can also skip the script entirely and use standard tools:

```bash
python3 generate.py          # writes all 1,031 into out/
cd out && sha256sum -c ../CHECKSUMS.txt
```

If you'd rather not run anything at all, the **verify** badge on the README is
this same check, run by GitHub on a clean machine against three Python versions
every time the repository changes. Click it to read the log.

---

## The one honest exception

**1,016 tokens are derived.** The code computes them from the seed. Those are
the ones Level 2 regenerates.

**15 tokens are composed.** The grails are one-off artworks drawn for their
specific event — not generated from a hash. They cannot be regenerated, because
there is no formula that produces them.

They ship in `grails/` as source files and are checksummed exactly like the
rest, so you can still prove the file backing a grail token is the file that was
published and has not been swapped since. `verify.py` tells you which kind
you're looking at — "derived card" or "composed plate" — on every check.

This distinction is stated here rather than buried, because a collection built
on verifiability does not get to be vague about what is and isn't verifiable.

---

## If something doesn't match

That's worth knowing about, and worth reporting.

A mismatch means one of: the art on Arweave was changed after publication, the
dataset in this repository was changed after the art was generated, or there's a
bug in the generator.

Open an issue with the token number and the two hashes. Don't take anyone's word
that it's nothing — including ours.

---

## What verification can and cannot tell you

**It can tell you** the art follows deterministically from the record, the
record carries a source, and nothing has been altered since publication.

**It cannot tell you** that a source is itself correct. Level 0 is the only
check for that, and it's the one that needs a human. The dataset was compiled
from public record by people, and people make mistakes.

That's the honest boundary of what this proves.
