import cv2
import numpy as np
import tkinter as tk
from tkinter import simpledialog
import os
import time


def kontur_kotak(kontur):
	kotak = []
	for i in kontur:
		area = cv2.contourArea(i)
		# print(area)
		if area > 500:
			keliling = cv2.arcLength(i, True)
			kirakira = cv2.approxPolyDP(i, 0.02*keliling, True)
			# print("Titik pojok:")
			# print(len(kirakira))
			if len(kirakira) == 4:
				kotak.append(i)
	kotak = sorted(kotak, key=cv2.contourArea, reverse=True)
	return kotak

def titik_pojok(kontur):
	keliling = cv2.arcLength(kontur, True)
	kirakira = cv2.approxPolyDP(kontur, 0.02 * keliling, True)
	return kirakira

def reorder(titik):
	titik = titik.reshape((4, 2))
	titik_sekarang = np.zeros((4, 2), np.int32)

	tambah = titik.sum(1)
	titik_sekarang[0] = titik[np.argmin(tambah)] #[0, 0]
	titik_sekarang[2] = titik[np.argmax(tambah)] #[w, h]

	selisih = np.diff(titik, axis=1)
	titik_sekarang[1] = titik[np.argmin(selisih)] #[w, 0]
	titik_sekarang[3] = titik[np.argmax(selisih)] #[0, h]
	return titik_sekarang


def deteksi_jawaban(gb1kolom_th):
	soal_soal = np.vsplit(gb1kolom_th, 30)
	jawaban = []
	coretan = []
	
	for soal in soal_soal:
		abcde = np.hsplit(soal, 5)
		coretan.append([ cv2.countNonZero(a) for a in abcde ])
	
	coretan = np.array(coretan)
	print('coretan:')
	print(coretan)
	batas = 60
	
	for soal in coretan:
		dipilih = ''
		for a in range(5):
			if soal[a] > batas:
				dipilih += 'ABCDE'[a]
		jawaban.append(dipilih)
	print('jawaban:')
	print(jawaban)
	return jawaban

def simpan():
	pass
	
	
w = 400
h = 200

margin = 2
w += margin * 2
h += margin * 2

sel_w = w // 20
sel_h = h // 10

jawaban = []
posisi = []


kode_soal = ''
nilai = ''
salahnya = ''
data_kunci = {}
filename_kunci = 'kunci_kode_12.txt'
if not os.path.exists(filename_kunci):
	peringatan = f'File {filename_kunci} belum ditemukan.\n Silakan kopi paste filenya ke folder yang sama dengan file ini.'
	print(peringatan)
else:
	peringatan = ''
	with open(filename_kunci, 'r') as f:
		
		for line in f:
			line = line.strip()
			if not line:
				continue
			key, arr_str = line.split(":", 1)
			key = int(key)
			arrku = arr_str.replace(", ]", "]")
			arr = eval(arrku)
			data_kunci[key] = arr














root = tk.Tk()
root.withdraw()


kelas = simpledialog.askstring('Masukkan kelas', "Kelas: ")
# ~ kelas = '12MQ'
os.system(f'mkdir -p {kelas}')



port = 0
video = cv2.VideoCapture(port)
# ~ video = cv2.VideoCapture(port, cv2.CAP_GSTREAMER)


while(True):
	ret, gb = video.read()
	
	gb_kontur = gb.copy()
	gb_gray = cv2.cvtColor(gb_kontur, cv2.COLOR_BGR2GRAY)
	gb_blur = cv2.GaussianBlur(gb_gray, (5,5), 1)
	gb_canny = cv2.Canny(gb_blur, 5, 60)
	
	kontur, hirarki = cv2.findContours(gb_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	kotak = kontur_kotak(kontur)
	if len(kotak) > 0:
		titik_pojok_jawaban = titik_pojok(kotak[0])
		titik_pojok_jawaban = reorder(titik_pojok_jawaban)
		# ~ print(titik_pojok_jawaban)

		cv2.drawContours(gb_kontur, kotak[0], -1, (0, 255, 0), 2)

		t1 = np.float32(titik_pojok_jawaban)
		t2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
		matriks = cv2.getPerspectiveTransform(t1, t2)
		# ~ gb_tegak = cv2.warpPerspective(gb_asli, matriks, (w, h))
		gb_tegak = cv2.warpPerspective(gb_gray, matriks, (w, h))
		gb_tegak_bersih = gb_tegak[margin: h - margin, margin: w - margin]
	# ~ print(gb_tegak_bersih.shape)
	# ~ deteksi_jawaban(gb_tegak)
	
	kol1 = gb_tegak_bersih[:,sel_w * 1: 6 * sel_w]
	kol2 = gb_tegak_bersih[:,sel_w * 8: 13 * sel_w]
	kol3 = gb_tegak_bersih[:,sel_w * 15:]
	
	gb1kolom = np.vstack((kol1, kol2, kol3))
	# ~ print(kol1.shape)
	# ~ print(kol2.shape)
	# ~ print(kol3.shape)
	# ~ print('-'*30)
	gb1kolom_th = cv2.adaptiveThreshold(gb1kolom, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 121, 10)
	
	
	# ~ soal_soal = np.vsplit(gb1kolom_th, 30)
	# ~ jawaban = []
	# ~ coretan = []
	
	# ~ for soal in soal_soal:
		# ~ abcde = np.hsplit(soal, 5)
		# ~ coretan.append([ cv2.countNonZero(a) for a in abcde ])
	
	# ~ coretan = np.array(coretan)
	# ~ print('coretan:')
	# ~ print(coretan)
	# ~ batas = 60
	
	# ~ for soal in coretan:
		# ~ dipilih = ''
		# ~ for a in range(5):
			# ~ if soal[a] > batas:
				# ~ dipilih += 'ABCDE'[a]
		# ~ jawaban.append(dipilih)
	# ~ print('jawaban:')
	# ~ print(jawaban)
	
	
	
	
	
	cv2.putText(gb_kontur, salahnya, (10, 15), cv2.FONT_HERSHEY_COMPLEX, .5, (0, 0, 255), 1)
	cv2.putText(gb_kontur, nilai, (500, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
	cv2.putText(gb_kontur, kode_soal, (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
	cv2.putText(gb_kontur, peringatan, (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
	
	
	cv2.imshow('Scan', gb_kontur)
	# ~ cv2.imshow('Tegak', gb_tegak_bersih)
	# ~ cv2.imshow('Kolom 1', kol1)
	# ~ cv2.imshow('Kolom 1 threshold', gb1kolom_th)
	# ~ cv2.imshow('Jadi 1 kolom', gb1kolom)
	# ~ cv2.imshow('Kolom 3', kol3)
	
	
	
	
	
	
	
	
	
	
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q') or key == 27:
		break
	elif key == ord('s'):
		waktu = time.localtime()
		waktu_string = time.strftime("%y%m%d_%H%M%S", waktu)
		cv2.imwrite(f'{kelas}/{kode_soal}_{kelas}_{waktu_string}.png', gb_kontur)
	elif key == ord('k'):
		
		
		kode_str = simpledialog.askstring("Input Kode Soal", "Masukkan kode soal (3 digit):")
		if kode_str and kode_str.isdigit():
			kode = int(kode_str)
			if kode in data_kunci:
				current_kunci = data_kunci[kode]
				kunci = [ 'ABCDE'[i] for i in current_kunci ]
				kode_soal = str(kode)
				print("Kunci soal:", current_kunci)
			else:
				kode_soal = f'{kode_str} tidak ditemukan.'
				print("Kode tidak ditemukan dalam file.")
		else:
			print("Input tidak valid.")
		jawaban_dia = deteksi_jawaban(gb1kolom_th)
		print('kunci:')
		print(kunci)
		nilai_list = [ 1 if (kunci[i] in jawaban_dia[i]) else 0 for i in range(30) ]
		print(nilai_list)
		skor = sum(nilai_list)
		nilai = str(skor)
		
		yang_salah = [ id+1 for id, val in enumerate(nilai_list) if val == 0 ]
		salahnya = str(yang_salah)
	

video.release()
cv2.destroyAllWindows()

