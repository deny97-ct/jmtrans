// JM Trans — interaksi halaman
const WA_NUMBER = "6281291828887";

// Header berbayang saat di-scroll
const header = document.getElementById("header");
const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 10);
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

// Menu mobile
const nav = document.getElementById("nav");
const navToggle = document.getElementById("navToggle");
const setNav = (open) => {
  nav.classList.toggle("is-open", open);
  navToggle.setAttribute("aria-expanded", String(open));
  navToggle.setAttribute("aria-label", open ? "Tutup menu" : "Buka menu");
};
navToggle.addEventListener("click", () => setNav(!nav.classList.contains("is-open")));
nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setNav(false)));

// Tahun di footer
document.getElementById("year").textContent = new Date().getFullYear();

// Animasi muncul saat di-scroll
const revealTargets = document.querySelectorAll(".feature, .service, .route, .car, .steps li, .faq details, .section__head");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("is-visible");
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  revealTargets.forEach((el) => { el.classList.add("reveal"); io.observe(el); });
}

// Lightbox galeri
const lightbox = document.getElementById("lightbox");
const lightboxImg = lightbox.querySelector("img");
const closeLightbox = () => { lightbox.hidden = true; document.body.style.overflow = ""; };
document.querySelectorAll(".gallery__item").forEach((btn) => {
  btn.addEventListener("click", () => {
    lightboxImg.src = btn.dataset.full;
    lightboxImg.alt = btn.querySelector("img").alt;
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
  });
});
lightbox.addEventListener("click", (e) => { if (e.target !== lightboxImg) closeLightbox(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !lightbox.hidden) closeLightbox(); });

// ===== Formulir pemesanan → WhatsApp =====
const form = document.getElementById("pesan");
const errorBox = document.getElementById("formError");
const conditionalFields = form.querySelectorAll("[data-only]");
const jumlahLabel = document.getElementById("jumlahLabel");
const jemputLabel = document.getElementById("jemputLabel");
const tujuanLabel = document.getElementById("tujuanLabel");
const LABEL_JUMLAH = {
  "Travel Reguler": "Jumlah kursi",
  "Kirim Paket": "Jumlah paket",
};
const labelJumlah = (layanan) => LABEL_JUMLAH[layanan] || "Jumlah penumpang";

// Tanggal minimal = hari ini
const dateInput = form.elements.tanggal;
const today = new Date();
const toISO = (d) => new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
dateInput.min = toISO(today);
dateInput.value = toISO(today);

// Ganti tampilan form sesuai layanan
const syncLayanan = () => {
  const layanan = form.elements.layanan.value;
  const paket = layanan === "Kirim Paket";
  conditionalFields.forEach((el) => { el.hidden = !el.dataset.only.split("|").includes(layanan); });
  jumlahLabel.textContent = labelJumlah(layanan);
  jemputLabel.textContent = paket ? "Alamat pengambilan paket" : "Alamat penjemputan";
  tujuanLabel.textContent = paket ? "Alamat & nama penerima" : "Alamat tujuan";
};
form.querySelectorAll('input[name="layanan"]').forEach((r) => r.addEventListener("change", syncLayanan));
syncLayanan();

const formatTanggal = (iso) =>
  new Date(iso + "T00:00:00").toLocaleDateString("id-ID", { weekday: "long", day: "numeric", month: "long", year: "numeric" });

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const f = form.elements;
  const wajib = ["nama", "hp", "tanggal", "jumlah", "jemput", "tujuan"];
  let kosong = [];
  wajib.forEach((name) => {
    const el = f[name];
    const ok = el.value.trim() !== "" && el.checkValidity();
    el.classList.toggle("is-invalid", !ok);
    if (!ok) kosong.push(el);
  });

  if (kosong.length) {
    errorBox.textContent = "Mohon lengkapi data yang ditandai merah.";
    errorBox.hidden = false;
    kosong[0].focus();
    return;
  }
  errorBox.hidden = true;

  const reguler = f.layanan.value === "Travel Reguler";
  const bandara = f.layanan.value === "Antar-Jemput Bandara";
  const paket = f.layanan.value === "Kirim Paket";
  const baris = [
    "Halo JM Trans, saya mau pesan:",
    "",
    `*Layanan:* ${f.layanan.value}`,
    reguler || paket ? `*Arah:* ${f.arah.value}` : null,
    paket && f.isiPaket.value.trim() ? `*Isi paket:* ${f.isiPaket.value.trim()}` : null,
    bandara ? `*Bandara:* ${f.bandara.value} — ${f.arahBandara.value}` : null,
    bandara && f.penerbangan.value.trim() ? `*Penerbangan:* ${f.penerbangan.value.trim()}` : null,
    `*Tanggal:* ${formatTanggal(f.tanggal.value)}`,
    `*${labelJumlah(f.layanan.value)}:* ${f.jumlah.value}`,
    `*${paket ? "Nama pengirim" : "Nama"}:* ${f.nama.value.trim()}`,
    `*No. HP:* ${f.hp.value.trim()}`,
    `*${paket ? "Alamat pengambilan" : "Alamat jemput"}:* ${f.jemput.value.trim()}`,
    `*${paket ? "Alamat & nama penerima" : "Alamat tujuan"}:* ${f.tujuan.value.trim()}`,
    f.catatan.value.trim() ? `*Catatan:* ${f.catatan.value.trim()}` : null,
    "",
    "Mohon info harga dan ketersediaannya. Terima kasih.",
  ].filter((b) => b !== null);

  const url = `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(baris.join("\n"))}`;
  window.open(url, "_blank", "noopener");
});

// Hapus tanda merah saat diketik ulang
form.addEventListener("input", (e) => e.target.classList.remove("is-invalid"));
