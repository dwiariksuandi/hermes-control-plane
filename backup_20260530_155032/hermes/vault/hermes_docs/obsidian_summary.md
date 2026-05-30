# Obsidian.md — Ringkasan Resmi & Relevansi dengan Hermes Agent

> Sumber: https://obsidian.md (Website resmi)

---

## Apa Itu Obsidian?

Obsidian adalah **aplikasi knowledge base pribadi** yang dibangun di atas file Markdown lokal. Berikut fitur-fitur utamanya berdasarkan website resmi:

---

## Fitur Utama

### 1. Knowledge Base / Second Brain
- Pengguna membuat catatan dalam format **Markdown**
- Hubungkan antar catatan menggunakan **[[wikilink]]**
- Membentuk jaringan ide yang saling terkait (seperti otak kedua)

### 2. Graph View
- Visualisasi hubungan antar catatan
- Membantu menemukan koneksi tersembunyi
- Berguna untuk eksplorasi pengetahuan

### 3. Plugins & Themes
- **Ribuan plugin** komunitas dan resmi
- Contoh plugin terkenal:
  - **Canvas**: ruang tak terbatas untuk brainstorming visual
  - **Templater**: otomatisasi template catatan
  - **Dataview**: query data dari catatan
  - **Excalidraw**: menggambar diagram/sketsa
- **Open API**: developer bisa membuat plugin sendiri

### 4. Local-First Philosophy
- Data disimpan di **folder lokal pengguna**
- Privasi dan kepemilikan data sepenuhnya milik pengguna
- Tidak ada vendor lock-in

### 5. Plain Text (Markdown)
- Catatan mudah diakses, diporting, dan diarsipkan
- Tidak tergantung pada format proprietary
- Bisa diedit dengan teks editor apapun

### 6. Cross-Platform
- Tersedia di: **Windows, macOS, Linux, iOS, Android**
- Sinkronisasi antar perangkat (fitur berbayar)

### 7. Obsidian Sync (Berbayar)
- Sinkronisasi terenkripsi end-to-end antar perangkat
- Mendukung versioning & konflik resolution

### 8. Obsidian Publish (Berbayar)
- Publikasikan catatan sebagai situs web
- Kontrol penuh atas apa yang dipublikasikan

### 9. Community & Resources
- **Discord**: komunitas pengguna aktif
- **Forum**: diskusi, feature requests, bug report
- **Developer Docs**: dokumentasi untuk membuat plugin

---

## Relevansi dengan Hermes Agent

### Vault sebagai AI Control Plane
Obsidian vault di `/home/hiryu/.hermes/vault` berfungsi sebagai **pusat kendali** untuk Hermes Agent:
- Menyimpan **Dashboard**: ringkasan status sistem
- **Decision Log**: log keputusan operasi
- **Agent Silos**: dokumentasi masing-masing agen
- **Evidence Ledger**: bukti hasil kerja

### Self-Learning Engine
Hermes Agent menggunakan Obsidian sebagai **mesin belajar mandiri**:
- Menulis "learnings" ke vault setelah tugas kompleks
- Membangun basis pengetahuan yang dapat diakses di sesi mendatang
- Skill `obsidian-self-learning` mengelola proses sync memori → vault

### Dokumentasi & SOP
- **Standard Operating Procedures (SOPs)**: langkah-langkah operasi
- **Dokumentasi internal**: konfigurasi, skill, cron jobs
- **Audit trail**: jejak aktivitas untuk troubleshooting

### Manajemen Proyek
- Mencatat rencana, tugas, status proyek
- Format terstruktur dan saling terhubung
- Bisa di-query menggunakan Dataview plugin

### Manfaat untuk User
- Transparansi penuh atas apa yang Hermes kerjakan
- Riwayat keputusan dapat ditelusuri
- Pengetahuan terakumulasi seiring waktu

---

## Ringkasan

| Aspek | Keterangan |
|-------|-----------|
| **Tipe** | Knowledge Base / Second Brain |
| **Format** | Plain Text Markdown |
| **Storage** | Local-first (folder lokal) |
| **Platform** | Win/Mac/Linux/iOS/Android |
| **Biaya** | Free (core) + Paid sync/publish |
| **Ekstensi** | 1000+ plugins, Open API |
| **Untuk Hermes** | AI Control Plane, Self-learning, SOPs |

---

*Document created: Phase 5.3 Research*
*Agent: Hermes Smart_Agent*