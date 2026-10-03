#!/usr/bin/env python3
"""
Archive card — the catalogue record.

Returns the card's INNER elements (no <svg> wrapper) so the vitrine can nest
them as real vector geometry. Every def id is suffixed with the token id so
two cards in one document never collide.
"""
import hashlib, math, re, datetime

W = H = 1200
M = 86
CX = W / 2
SERIF = "Georgia,'Times New Roman',serif"
MONO  = "ui-monospace,'DejaVu Sans Mono',Menlo,monospace"

ERA = {
 "Genesis Era (2008-2012)":      dict(field="#0a0805", paper="#efe6d2", ink="#1c160c", rule="#8a7a5c", acc="#b8791a", tint="#e3d6b8"),
 "Early Era (2013-2015)":        dict(field="#07100f", paper="#e4eeea", ink="#0e1b19", rule="#7f9a95", acc="#17796b", tint="#cfe2dc"),
 "ICO Era (2016-2017)":          dict(field="#120726", paper="#ece5f5", ink="#1b1030", rule="#8d81a8", acc="#a01f78", tint="#dcd0ec"),
 "Bear Era (2018-2019)":         dict(field="#0c0f14", paper="#e6e9ef", ink="#161b24", rule="#8c95a5", acc="#3d5573", tint="#d3d9e3"),
 "DeFi & NFT Era (2020-2021)":   dict(field="#0a0f0a", paper="#e9f0dd", ink="#141c11", rule="#8a9a7c", acc="#4a7a16", tint="#d6e4c2"),
 "Contagion Era (2022-2023)":    dict(field="#140806", paper="#f2e4dc", ink="#20100b", rule="#a58b80", acc="#b33b12", tint="#e6cfc2"),
 "Institutional Era (2024-2026)":dict(field="#0b0d12", paper="#eceef3", ink="#12151c", rule="#8f96a4", acc="#8a6f2e", tint="#dadee6"),
}
CODE = {"Genesis Era (2008-2012)":"GENESIS","Early Era (2013-2015)":"EARLY","ICO Era (2016-2017)":"ICO",
        "Bear Era (2018-2019)":"BEAR","DeFi & NFT Era (2020-2021)":"DEFI",
        "Contagion Era (2022-2023)":"CONTAGION","Institutional Era (2024-2026)":"INSTITUTIONAL"}

class R:
    def __init__(s, b): s.b, s.i = b, 0
    def _y(s):
        if s.i >= len(s.b): s.b, s.i = hashlib.sha256(s.b).digest(), 0
        v = s.b[s.i]; s.i += 1; return v
    def f(s): return (s._y() << 8 | s._y()) / 65535.0
    def r(s, a, b): return a + (b - a) * s.f()
    def i_(s, a, b): return int(s.r(a, b + .999))

def esc(t):
    return str(t or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def wrap(text, n):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= n: cur = (cur + " " + w).strip()
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def parse_usd(a):
    if not a: return 0.0
    s = str(a).lower().replace(",", "")
    m = re.search(r"\$\s*([\d.]+)\s*([kmb])?", s) or re.search(r"([\d.]+)\s*([kmb])\b", s)
    if not m: return 0.0
    try: v = float(m.group(1))
    except ValueError: return 0.0
    return v * {"k":1e3,"m":1e6,"b":1e9}.get(m.group(2) or "", 1)

def mag_label(v):
    if v >= 1e9: return "CATASTROPHIC"
    if v >= 1e8: return "SEVERE"
    if v >= 1e7: return "MAJOR"
    if v >= 1e6: return "SIGNIFICANT"
    if v > 0:    return "MINOR"
    return ""

def glyph(cx, cy, r, P, g, cat):
    o = [f'<g transform="translate({cx} {cy})">']
    o.append(f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="{P["acc"]}" stroke-width="2.5" opacity=".9"/>')
    o.append(f'<circle cx="0" cy="0" r="{r-9}" fill="none" stroke="{P["rule"]}" stroke-width="1" opacity=".7"/>')
    n = g.i_(5, 11)
    if cat.startswith("Standard"):
        for i in range(n):
            a = math.radians(i * 360/n)
            o.append(f'<line x1="0" y1="0" x2="{(r-16)*math.cos(a):.1f}" y2="{(r-16)*math.sin(a):.1f}" stroke="{P["ink"]}" stroke-width="1.8" opacity=".8"/>')
    elif cat == "Hack / Exploit":
        pts = " ".join(f"{g.r(-r+16, r-16):.0f},{g.r(-r+16, r-16):.0f}" for _ in range(g.i_(4,7)))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{P["acc"]}" stroke-width="2.6"/>')
    elif cat in ("Collapse", "Rug Pull"):
        for i in range(6):
            o.append(f'<rect x="{-r+14+i*2:.0f}" y="{-r+16+i*7:.0f}" width="{(r-16)*2-i*4:.0f}" height="3.4" fill="{P["ink"]}" opacity="{.85-i*.12:.2f}"/>')
    else:
        for i in range(3):
            o.append(f'<circle cx="0" cy="0" r="{(r-18)-i*8}" fill="none" stroke="{P["ink"]}" stroke-width="1.6" opacity=".75"/>')
    o.append('</g>'); return "".join(o)

def strip(x, y, w, h, seed, P):
    o, i, px = [], 0, x
    while px < x + w and i < 64:
        b = seed[i % len(seed)]
        bw = 1.6 + (b % 5) * 1.5
        if b % 3:
            o.append(f'<rect x="{px:.1f}" y="{y}" width="{bw:.1f}" height="{h}" fill="{P["ink"]}" opacity="{.35 + (b%5)*.13:.2f}"/>')
        px += bw + 2.2; i += 1
    return "".join(o)

def card_defs(ev, uid):
    """Defs the card needs, with ids namespaced so nesting is safe."""
    seed = hashlib.sha256(f'{ev["date"]}|{ev["title"]}'.encode()).digest()
    P = ERA.get(ev["era"], ERA["Bear Era (2018-2019)"])
    return (f'<linearGradient id="stock{uid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0%" stop-color="{P["paper"]}"/>'
            f'<stop offset="100%" stop-color="{P["tint"]}"/></linearGradient>'
            f'<filter id="fib{uid}"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" seed="{seed[1]}"/>'
            f'<feColorMatrix type="saturate" values="0"/>'
            f'<feComponentTransfer><feFuncA type="linear" slope="0.09"/></feComponentTransfer></filter>')

def card_body(ev, uid, with_field=True):
    """The card's inner elements. with_field=False omits the dark backdrop
    (the vitrine supplies its own)."""
    seed = hashlib.sha256(f'{ev["date"]}|{ev["title"]}'.encode()).digest()
    g = R(seed)
    P = ERA.get(ev["era"], ERA["Bear Era (2018-2019)"])
    tid = int(ev["id"])
    loss = parse_usd(ev.get("amount_usd", "")) or parse_usd(ev.get("title", ""))
    mag = mag_label(loss)
    cat = ev["category"]
    cx0, cy0, cw, ch = M, M, W - 2*M, H - 2*M
    o = []

    if with_field:
        o.append(f'<rect width="{W}" height="{H}" fill="{P["field"]}"/>')

    # crop marks
    for (mx, my, dx, dy) in ((cx0,cy0,1,1),(cx0+cw,cy0,-1,1),(cx0,cy0+ch,1,-1),(cx0+cw,cy0+ch,-1,-1)):
        o.append(f'<line x1="{mx-dx*36}" y1="{my}" x2="{mx-dx*8}" y2="{my}" stroke="{P["acc"]}" stroke-width="1.6" opacity=".75"/>')
        o.append(f'<line x1="{mx}" y1="{my-dy*36}" x2="{mx}" y2="{my-dy*8}" stroke="{P["acc"]}" stroke-width="1.6" opacity=".75"/>')

    o.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" fill="url(#stock{uid})"/>')

    # header band
    o.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="66" fill="{P["ink"]}"/>')
    o.append(f'<text x="{cx0+26}" y="{cy0+44}" font-family="{MONO}" font-size="25" fill="{P["paper"]}" letter-spacing="3">No. {tid:04d}</text>')
    o.append(f'<text x="{cx0+cw-26}" y="{cy0+44}" text-anchor="end" font-family="{MONO}" font-size="17" fill="{P["paper"]}" opacity=".8" letter-spacing="2.5">{CODE.get(ev["era"],"---")} · {esc(ev["year"])}</text>')

    # the year, oversized, behind everything
    o.append(f'<text x="{cx0+cw-18}" y="{cy0+ch-150}" text-anchor="end" font-family="{SERIF}" font-size="310" fill="{P["acc"]}" opacity=".11">{esc(ev["year"])}</text>')

    # classification
    y = cy0 + 116
    o.append(f'<text x="{cx0+26}" y="{y}" font-family="{MONO}" font-size="16" fill="{P["rule"]}" letter-spacing="4">CLASSIFICATION</text>')
    o.append(f'<text x="{cx0+26}" y="{y+34}" font-family="{MONO}" font-size="24" fill="{P["ink"]}" letter-spacing="1.5">{esc(cat.upper())}</text>')
    o.append(f'<line x1="{cx0+26}" y1="{y+56}" x2="{cx0+cw-26}" y2="{y+56}" stroke="{P["rule"]}" stroke-width="1.2" opacity=".8"/>')

    # title
    lines = wrap(ev["title"], 26)[:4]
    ty = cy0 + 246
    fs = 54 if len(lines) <= 2 else (46 if len(lines) == 3 else 39)
    for i, ln in enumerate(lines):
        o.append(f'<text x="{cx0+26}" y="{ty+i*(fs+10)}" font-family="{SERIF}" font-size="{fs}" fill="{P["ink"]}">{esc(ln)}</text>')

    # rule + specimen glyph
    ry = ty + len(lines)*(fs+10) + 30
    o.append(f'<line x1="{cx0+26}" y1="{ry}" x2="{cx0+cw-172}" y2="{ry}" stroke="{P["ink"]}" stroke-width="2.4"/>')
    o.append(glyph(cx0+cw-92, ry, 62, P, g, cat))

    # the account
    by = ry + 46
    for i, ln in enumerate(wrap(ev.get("summary",""), 54)[:8]):
        o.append(f'<text x="{cx0+26}" y="{by+i*34}" font-family="{SERIF}" font-size="24.5" fill="{P["ink"]}" opacity=".88">{esc(ln)}</text>')

    # provenance
    src = ev.get("source","") or "Archive"
    o.append(f'<text x="{cx0+26}" y="{cy0+ch-236}" font-family="{MONO}" font-size="15" fill="{P["rule"]}" letter-spacing="2">SOURCE · {esc(str(src).upper()[:46])}</text>')

    # data grid
    gy = cy0 + ch - 196
    o.append(f'<line x1="{cx0+26}" y1="{gy-30}" x2="{cx0+cw-26}" y2="{gy-30}" stroke="{P["rule"]}" stroke-width="1.2" opacity=".8"/>')
    cells = [("DATE OF RECORD", ev["date"]), ("ERA", CODE.get(ev["era"],"---"))]
    cells.append(("MAGNITUDE", mag) if mag else ("SERIES", "BLOCKCHAIN HISTORY"))
    cells.append(("VERIFIED", (ev.get("verify_status") or "ARCHIVE").upper()))
    colw = (cw - 52) / len(cells)
    for i, (k, v) in enumerate(cells):
        x = cx0 + 26 + i*colw
        o.append(f'<text x="{x:.0f}" y="{gy}" font-family="{MONO}" font-size="14" fill="{P["rule"]}" letter-spacing="2.5">{esc(k)}</text>')
        fsz = 19 if len(str(v)) < 10 else (15 if len(str(v)) < 14 else 12.5)
        o.append(f'<text x="{x:.0f}" y="{gy+29}" font-family="{MONO}" font-size="{fsz}" fill="{P["ink"]}">{esc(v)}</text>')

    if loss:
        amt = ev["amount_usd"] if len(str(ev.get("amount_usd",""))) < 30 else mag
        o.append(f'<text x="{cx0+26}" y="{gy+74}" font-family="{MONO}" font-size="16" fill="{P["acc"]}" letter-spacing="1.5">RECORDED LOSS · {esc(amt)}</text>')

    # registration strip + hash
    o.append(strip(cx0+26, cy0+ch-64, cw-190, 26, seed, P))
    o.append(f'<text x="{cx0+cw-26}" y="{cy0+ch-44}" text-anchor="end" font-family="{MONO}" font-size="15" fill="{P["rule"]}">{seed.hex()[:12].upper()}</text>')

    # magnitude overstamp
    if loss >= 1e7:
        o.append(f'<g transform="translate({cx0+cw-256} {cy0+ch-292}) rotate({g.r(-19,-9):.1f})" opacity=".34">')
        o.append(f'<rect x="-136" y="-38" width="272" height="76" fill="none" stroke="{P["acc"]}" stroke-width="5"/>')
        o.append(f'<text x="0" y="14" text-anchor="middle" font-family="{MONO}" font-size="30" fill="{P["acc"]}" letter-spacing="3">{mag}</text></g>')

    o.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" fill="none" stroke="{P["ink"]}" stroke-width="1.4" opacity=".35"/>')
    if with_field:
        o.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" filter="url(#fib{uid})" opacity=".5" style="mix-blend-mode:multiply"/>')
    return "".join(o)

def render(ev):
    """Standalone card (used for the grail-free archive plates)."""
    uid = f"c{int(ev['id'])}"
    P = ERA.get(ev["era"], ERA["Bear Era (2018-2019)"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<defs>{card_defs(ev, uid)}</defs>{card_body(ev, uid)}</svg>')
