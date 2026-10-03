#!/usr/bin/env python3
"""
Vitrine — the glass case, composed as TRUE VECTOR.

The card is drawn inside the case as real geometry, not rasterised and
embedded. That keeps a mounted record at ~12-15 KiB instead of ~120 KiB,
keeps it sharp at any zoom, and keeps on-chain storage affordable.

Geometry matches the PNGs already approved: case at 190,120 820x860,
card at 220,182 sized 760.
"""
from . import archive

W = H = 1200
MONO = "ui-monospace,'DejaVu Sans Mono',Menlo,monospace"

# case colours per era: backdrop, floor, glow (frame), stone (posts/pedestal)
SET = {
 "Genesis Era (2008-2012)":      dict(back="#241a0b", floor="#100b05", glow="#f5b63c", stone="#5c4826"),
 "Early Era (2013-2015)":        dict(back="#122b28", floor="#061210", glow="#6ed9c8", stone="#2d635b"),
 "ICO Era (2016-2017)":          dict(back="#1a0c33", floor="#0d0619", glow="#c65cff", stone="#42256b"),
 "Bear Era (2018-2019)":         dict(back="#141a24", floor="#080b11", glow="#9fb4d0", stone="#36445a"),
 "DeFi & NFT Era (2020-2021)":   dict(back="#1b2d16", floor="#0a1209", glow="#c8ff5c", stone="#4a6b2a"),
 "Contagion Era (2022-2023)":    dict(back="#24100a", floor="#120705", glow="#ff5722", stone="#5e2a16"),
 "Institutional Era (2024-2026)":dict(back="#12161f", floor="#080a0e", glow="#d4bd7a", stone="#2f3d54"),
}

GX, GY, GW, GH = 190, 120, 820, 860
CARD_X, CARD_Y, CARD_S = 220, 182, 760          # 760/1200 = 0.63333 scale

def render(ev):
    P = SET.get(ev["era"], SET["Bear Era (2018-2019)"])
    uid = f"c{int(ev['id'])}"
    tid = int(ev["id"])
    scale = CARD_S / archive.W

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    o.append('<defs>')
    o.append(f'''<radialGradient id="bk{uid}" cx="50%" cy="38%" r="76%">
<stop offset="0%" stop-color="{P["back"]}"/><stop offset="100%" stop-color="{P["floor"]}"/></radialGradient>
<radialGradient id="spot{uid}" cx="50%" cy="10%" r="70%">
<stop offset="0%" stop-color="{P["glow"]}" stop-opacity=".22"/>
<stop offset="100%" stop-color="{P["glow"]}" stop-opacity="0"/></radialGradient>
<linearGradient id="plinth{uid}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{P["stone"]}"/><stop offset="100%" stop-color="{P["floor"]}"/></linearGradient>
<linearGradient id="face{uid}" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#ffffff" stop-opacity=".16"/>
<stop offset="60%" stop-color="#ffffff" stop-opacity=".02"/>
<stop offset="100%" stop-color="#000000" stop-opacity=".10"/></linearGradient>
<filter id="cast{uid}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="26"/></filter>
<filter id="soft{uid}"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="grain{uid}"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="4"/>
<feColorMatrix type="saturate" values="0"/>
<feComponentTransfer><feFuncA type="linear" slope=".05"/></feComponentTransfer></filter>''')
    o.append(archive.card_defs(ev, uid))
    o.append('</defs>')

    o.append(f'<rect width="{W}" height="{H}" fill="url(#bk{uid})"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#spot{uid})"/>')

    # pedestal
    o.append(f'<ellipse cx="600" cy="{GY+GH+18}" rx="420" ry="52" fill="#000" opacity=".6" filter="url(#cast{uid})"/>')
    o.append(f'<rect x="{GX-26}" y="{GY+GH}" width="{GW+52}" height="64" fill="url(#plinth{uid})"/>')
    o.append(f'<rect x="{GX-26}" y="{GY+GH}" width="{GW+52}" height="5" fill="{P["glow"]}" opacity=".3"/>')

    # the card, lit and shadowed, then drawn as vector
    o.append(f'<rect x="{CARD_X+10}" y="{CARD_Y+16}" width="{CARD_S}" height="{CARD_S}" fill="#000" opacity=".45" filter="url(#soft{uid})"/>')
    o.append(f'<rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_S}" height="{CARD_S}" fill="{P["glow"]}" opacity=".10" filter="url(#soft{uid})"/>')
    o.append(f'<g transform="translate({CARD_X} {CARD_Y}) scale({scale:.6f})">')
    o.append(archive.card_body(ev, uid, with_field=False))
    o.append('</g>')
    o.append(f'<rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_S}" height="{CARD_S}" fill="url(#face{uid})"/>')

    # floor inside the case
    o.append(f'<polygon points="{GX+30},{GY+822} {GX+790},{GY+822} {GX+760},{GY+856} {GX+60},{GY+856}" fill="#000" opacity=".5"/>')

    # the case
    o.append(f'<rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" fill="{P["glow"]}" opacity=".012"/>')
    o.append(f'<rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" fill="none" stroke="{P["stone"]}" stroke-width="7"/>')
    o.append(f'<rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" fill="none" stroke="{P["glow"]}" stroke-width="2" opacity=".45"/>')
    o.append(f'<rect x="{GX}" y="{GY}" width="{GW}" height="9" fill="{P["glow"]}" opacity=".5"/>')
    o.append(f'<rect x="{GX}" y="{GY+GH-9}" width="{GW}" height="9" fill="{P["glow"]}" opacity=".3"/>')
    for x in (GX, GX+GW):
        o.append(f'<rect x="{x-7}" y="{GY}" width="14" height="{GH}" fill="{P["stone"]}"/>')

    # glass: narrow reflections, not a tint
    o.append(f'<polygon points="{GX+62},{GY} {GX+134},{GY} {GX-6},{GY+GH} {GX-58},{GY+GH}" fill="#fff" opacity=".085"/>')
    o.append(f'<polygon points="{GX+168},{GY} {GX+196},{GY} {GX+52},{GY+GH} {GX+26},{GY+GH}" fill="#fff" opacity=".05"/>')
    o.append(f'<polygon points="{GX+GW-120},{GY} {GX+GW-84},{GY} {GX+GW-208},{GY+GH} {GX+GW-244},{GY+GH}" fill="#fff" opacity=".035"/>')

    # lot plate
    ly = GY + GH + 78
    o.append(f'<rect x="{W/2-210:.0f}" y="{ly}" width="420" height="52" rx="4" fill="{P["stone"]}" opacity=".5"/>')
    o.append(f'<text x="{W/2:.0f}" y="{ly+34}" text-anchor="middle" font-family="{MONO}" font-size="19" fill="{P["glow"]}" letter-spacing="4">LOT {tid:04d}</text>')

    o.append(f'<rect width="{W}" height="{H}" filter="url(#grain{uid})" opacity=".32" style="mix-blend-mode:overlay"/>')
    o.append('</svg>')
    return "".join(o)
