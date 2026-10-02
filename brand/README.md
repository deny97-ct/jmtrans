# Logo JM Trans — "Rumah ke Rumah"

Dua atap rumah membentuk huruf **M** (rumah asal & rumah tujuan), pintu lengkung kuning = *door to door*, jalan hijau berkelok = perjalanan yang menghubungkannya.

## File

| File | Pakai untuk |
|---|---|
| `svg/jmtrans-horizontal.svg` / `png/…` | Kop surat, website, spanduk, kartu nama (latar terang) |
| `svg/jmtrans-horizontal-putih.svg` | Sama, untuk latar gelap/foto |
| `svg/jmtrans-vertikal(-putih).svg` | Stiker kaca mobil, kaos, area persegi |
| `svg/jmtrans-simbol(-putih).svg` | Ikon, favicon, cap, bordir kecil |
| `png/jmtrans-profil-navy.png` | Foto profil WhatsApp / Instagram / Google Maps (1024×1024) |
| `png/jmtrans-profil-putih.png` | Alternatif foto profil berlatar putih |

Untuk percetakan, kirim file **SVG** (vektor, bisa diperbesar tanpa pecah). PNG berlatar transparan.

## Warna

| Nama | HEX | Kira-kira CMYK |
|---|---|---|
| Navy | `#12304F` | 100 / 75 / 35 / 40 |
| Hijau | `#2FA84F` | 75 / 0 / 85 / 0 |
| Amber | `#F5A623` | 0 / 38 / 90 / 0 |

## Aturan singkat

- Beri ruang kosong di sekeliling logo minimal setinggi satu pintu kuning.
- Ukuran terkecil: simbol 16 px (layar) / 8 mm (cetak); logo horizontal 120 px / 30 mm.
- Jangan mengubah warna, memiringkan, menambah bayangan, atau meregangkan logo.

## Font

Tulisan memakai **Outfit** (SIL Open Font License 1.1, bebas untuk komersial; lisensi di `_src/OFL.txt`), sudah diubah menjadi kurva sehingga tidak perlu font terpasang.

## Membuat ulang

```bash
cd brand/_src && python build_logo.py
```

Butuh Python + `fontTools`, dan Google Chrome untuk ekspor PNG.
