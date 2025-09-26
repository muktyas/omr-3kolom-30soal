from fpdf import FPDF
from datetime import datetime

sekarang = datetime.today().strftime('%y%m%d_%H%M%S')
versi = 230212

print('='*50)
print('Program pembuat lembar jawab LJK berformat .pdf')
print(f'dijalankan pada tanggal_jam {sekarang}')
print('-'*30)
##########################################
banyak_soal = int(input('Masukkan banyak soal [30]: ') or '30')
banyak_kolom = int(input('Masukkan banyak kolom [3]: ') or '3')
banyak_pilihan = int(
    input('Tiap soal ada berapa pilihan ganda? [5 (ABCDE)]: ') or '5')
tinggi = 9

judul = input('Masukkan judul: ') or 'Lembar Jawab STS Ganjil 2025/2026'
##########################################

banyak_baris = -(-banyak_soal//(banyak_kolom*5))*5

abc = 'ABCDE'
pdf = FPDF()
pdf.add_page()
pdf.set_font('Helvetica', 'B', size=11)
pdf.set_margins(tinggi, tinggi, tinggi)


pdf.cell(tinggi, tinggi, judul)
pdf.set_font('Helvetica', size=11)
pdf.ln(tinggi)

w = tinggi * (banyak_kolom * (banyak_pilihan + 2) - 1)
h = tinggi * banyak_baris

pdf.cell(w=15, h=tinggi, txt='Nama')
pdf.cell(w=60, h=tinggi, txt=':')
pdf.cell(w=30, h=tinggi, txt='Mata Pelajaran')
pdf.cell(h=tinggi, txt=':')
pdf.ln(tinggi)

pdf.cell(w=15, h=tinggi, txt='Kelas')
pdf.cell(w=60, h=tinggi, txt=':')
pdf.cell(w=30, h=tinggi, txt='Kode Soal')
pdf.cell(h=tinggi, txt=':')
pdf.ln(tinggi)
pdf.set_font('Helvetica', size=8)

pdf.set_line_width(1)

pdf.rect(tinggi, tinggi * 4, w, h)
# untuk lingkaran di tiap pilihan
pdf.set_line_width(0)
skala = 3/6
jari = skala * tinggi

for baris in range(banyak_baris):
    y_lingkaran = (4 + baris) * tinggi + (tinggi - jari)/2

    for kolom in range(banyak_kolom):
        nomor = baris + kolom * banyak_baris + 1
        if nomor <= banyak_soal:
            pdf.cell(tinggi, tinggi, txt=f'{nomor}.', align='R')

            for i in range(banyak_pilihan):
                x_lingkaran = (2 + i + kolom * (banyak_pilihan + 2)) * \
                    tinggi + (tinggi - jari)/2
                pdf.cell(tinggi, tinggi, txt=abc[i], align='C')
                pdf.circle(x_lingkaran, y_lingkaran, jari)
            pdf.cell(tinggi, tinggi, '')
    pdf.ln(tinggi)
pdf.ln(tinggi)

# uraian
pdf.set_font_size(11)
pdf.cell(tinggi, tinggi, txt='Uraian')
pdf.ln(tinggi)
pdf.set_font_size(11)
# ~ pdf.multi_cell(pdf.epw, tinggi, txt='.'*2300)
pdf.image('kotak.png', x=0, y=0, w=pdf.w, h=pdf.h)

namafile = f'LJK-{sekarang}.pdf'
pdf.output(namafile)
print(f'File Lembar jawab sudah jadi dengan nama LJK-{sekarang}.pdf')
print('di folder yang sama dengan program ini.')

input('Tekan Enter untuk keluar program ;)')
