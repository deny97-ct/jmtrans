"""Bangun semua file logo JM Trans (konsep 1: Rumah ke Rumah) dari satu sumber.

Tulisan diubah menjadi path vektor memakai font Outfit (SIL OFL 1.1),
jadi file SVG tidak bergantung pada font yang terpasang di komputer.

Jalankan:  python build_logo.py
"""
from pathlib import Path
import subprocess

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = Path(__file__).parent
OUT = HERE.parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

NAVY = "#12304F"
GREEN = "#2FA84F"
AMBER = "#F5A623"
SLATE = "#5B6B7F"
WHITE = "#FFFFFF"

# ---------------------------------------------------------------- simbol ---
def mark(roof=NAVY, dash=WHITE, road=GREEN, door=AMBER):
    """Simbol dalam kotak 120x120: dua atap = huruf M, pintu lengkung, jalan berkelok."""
    return f'''<g>
  <path d="M6 99 C34 84 62 104 114 86" fill="none" stroke="{road}" stroke-width="12" stroke-linecap="round"/>
  <path d="M14 95 C38 85 62 102 106 89" fill="none" stroke="{dash}" stroke-width="2.4" stroke-dasharray="6 5"/>
  <path d="M15 76 V50 L38 27 L60 49 L82 27 L105 50 V76" fill="none" stroke="{roof}" stroke-width="11" stroke-linejoin="round" stroke-linecap="round"/>
  <path d="M31 75 V59 A7 7 0 0 1 45 59 V75 Z" fill="{door}"/>
  <path d="M75 75 V59 A7 7 0 0 1 89 59 V75 Z" fill="{door}"/>
</g>'''

MARK_BOX = (6 - 6, 21.5, 120, 104 - 21.5 + 6)  # x, y, w, h perkiraan isi simbol (dengan stroke)
MARK_TOP, MARK_BOTTOM = 21.5, 105.0

# ---------------------------------------------------------------- tulisan ---
_fonts = {}
def font(weight):
    if weight not in _fonts:
        f = TTFont(HERE / "Outfit.ttf")
        _fonts[weight] = instantiateVariableFont(f, {"wght": weight})
    return _fonts[weight]

def text_path(text, size, weight, x=0, baseline=0, tracking=0.0):
    """Kembalikan (d, lebar) path SVG untuk teks. tracking dalam em."""
    f = font(weight)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs)
    cursor = 0.0
    for i, ch in enumerate(text):
        gname = cmap[ord(ch)]
        tpen = TransformPen(pen, (s, 0, 0, -s, x + cursor, baseline))
        gs[gname].draw(tpen)
        cursor += hmtx[gname][0] * s
        if i < len(text) - 1:
            cursor += tracking * size
    return pen.getCommands(), cursor

def text_ink_bounds(text, size, weight):
    f = font(weight)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    s = size / f["head"].unitsPerEm
    bp = BoundsPen(gs)
    gs[cmap[ord(text[0])]].draw(bp)
    return bp.bounds[0] * s  # sisi kiri tinta huruf pertama

# ---------------------------------------------------------------- tata letak ---
def wordmark(x, baseline, size, jm_color, trans_color, tag, tag_color):
    """Tulisan JM TRANS + tagline. Kembalikan (svg, lebar)."""
    w900 = 900
    left = text_ink_bounds("J", size, w900)
    x0 = x - left  # rata kiri pada tinta huruf
    d1, w1 = text_path("JM", size, w900, x0, baseline, 0.01)
    space = size * 0.24
    d2, w2 = text_path("TRANS", size, w900, x0 + w1 + space, baseline, 0.01)
    total = w1 + space + w2
    tsize = size * 0.235
    tleft = text_ink_bounds(tag[0], tsize, 700)
    # tagline direntang agar lebarnya sama dengan "JM TRANS"
    _, raw = text_path(tag, tsize, 700)
    gaps = len(tag) - 1
    track = (total - raw) / gaps / tsize if gaps else 0
    d3, _ = text_path(tag, tsize, 700, x - tleft, baseline + size * 0.46, track)
    svg = (f'<path d="{d1}" fill="{jm_color}"/>'
           f'<path d="{d2}" fill="{trans_color}"/>'
           f'<path d="{d3}" fill="{tag_color}"/>')
    return svg, total

def svg_doc(w, h, body, bg=None):
    bgrect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}">{bgrect}{body}</svg>\n')

def horizontal(dark=False, tag="DOOR TO DOOR TRAVEL"):
    m = mark(roof=WHITE if dark else NAVY, dash=NAVY if dark else WHITE)
    pad = 10
    scale = 1.0
    mark_w = 120
    size = 56
    gap = 14
    # pusat vertikal tulisan disejajarkan dengan pusat simbol
    center = (MARK_TOP + MARK_BOTTOM) / 2
    cap_h = size * 0.70
    block_h = cap_h + size * 0.46 + size * 0.235 * 0.3
    baseline = center - block_h / 2 + cap_h
    wm, ww = wordmark(mark_w + gap, baseline, size,
                      WHITE if dark else NAVY, GREEN,
                      tag, "#C9D3DF" if dark else SLATE)
    w = mark_w + gap + ww + pad
    top, bottom = MARK_TOP - pad, MARK_BOTTOM + pad
    body = f'<g transform="translate(0 {-top})">{m}{wm}</g>'
    return svg_doc(w, bottom - top, body)

def vertical(dark=False, tag="DOOR TO DOOR TRAVEL"):
    m = mark(roof=WHITE if dark else NAVY, dash=NAVY if dark else WHITE)
    size = 46
    # hitung lebar tulisan dulu
    _, ww = wordmark(0, 0, size, NAVY, GREEN, tag, SLATE)
    w = max(ww, 120) + 30
    mark_x = (w - 120) / 2
    baseline = MARK_BOTTOM + 14 + size * 0.70
    wm, _ = wordmark((w - ww) / 2, baseline, size,
                     WHITE if dark else NAVY, GREEN, tag, "#C9D3DF" if dark else SLATE)
    top = MARK_TOP - 12
    h = baseline + size * 0.46 + 14 - top
    body = f'<g transform="translate(0 {-top})"><g transform="translate({mark_x} 0)">{m}</g>{wm}</g>'
    return svg_doc(w, h, body)

def mark_only(dark=False):
    m = mark(roof=WHITE if dark else NAVY, dash=NAVY if dark else WHITE)
    return svg_doc(120, 120, f'<g transform="translate(0 -3)">{m}</g>')

def avatar(bg=NAVY):
    """Foto profil persegi (WhatsApp/IG memotong jadi lingkaran)."""
    dark = bg != WHITE
    m = mark(roof=WHITE if dark else NAVY, dash=NAVY if dark else WHITE)
    # simbol 120 unit diperkecil ke ~62% lebar agar aman saat dipotong lingkaran
    return svg_doc(1024, 1024,
                   f'<g transform="translate(512 512) scale(5.3) translate(-60 -63)">{m}</g>', bg=bg)

# ---------------------------------------------------------------- ekspor ---
def export_png(svg_file, png_file, width, height):
    html = HERE / "_render.html"
    html.write_text(
        f'<html><body style="margin:0;background:transparent">'
        f'<img src="{svg_file.resolve().as_uri()}" style="width:{width}px;height:{height}px;display:block">'
        f'</body></html>', encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--default-background-color=00000000",
                    f"--window-size={width},{height}",
                    f"--screenshot={png_file.resolve()}", html.resolve().as_uri()],
                   check=True, capture_output=True)
    html.unlink()

def size_of(svg_text):
    import re
    w, h = re.search(r'width="(\d+)" height="(\d+)"', svg_text).groups()
    return int(w), int(h)

def main():
    files = {
        "jmtrans-simbol.svg": mark_only(),
        "jmtrans-simbol-putih.svg": mark_only(dark=True),
        "jmtrans-horizontal.svg": horizontal(),
        "jmtrans-horizontal-putih.svg": horizontal(dark=True),
        "jmtrans-vertikal.svg": vertical(),
        "jmtrans-vertikal-putih.svg": vertical(dark=True),
        "jmtrans-profil-navy.svg": avatar(NAVY),
        "jmtrans-profil-putih.svg": avatar(WHITE),
    }
    svg_dir = OUT / "svg"
    png_dir = OUT / "png"
    svg_dir.mkdir(exist_ok=True)
    png_dir.mkdir(exist_ok=True)
    for name, text in files.items():
        p = svg_dir / name
        p.write_text(text, encoding="utf-8")
        w, h = size_of(text)
        # PNG resolusi tinggi: lebar minimal 2000px kecuali profil (1024)
        k = 1 if "profil" in name else max(1, round(2000 / w))
        if "simbol" in name:
            k = 1024 // 120 + 1
        export_png(p, png_dir / name.replace(".svg", ".png"), w * k, h * k)
        print(f"{name:32s} {w}x{h}  -> png {w*k}x{h*k}")

if __name__ == "__main__":
    main()
