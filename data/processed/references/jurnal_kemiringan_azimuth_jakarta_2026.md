Jurnal AL-AZHAR INDONESIA SERI SAINS DAN TEKNOLOGI Vol. 11, Nomor 01, January 2026, hal. 48-53 DOI http://dx.doi.org/10.36722/sst.v11i1.4874 https://jurnal.uai.ac.id/index.php/SST

## Analisis Sudut Kemiringan Optimum Panel Surya Atap di Kota Jakarta Menggunakan Data Global Solar Atlas

### Andi Makkulau1*, Nurmiati Pasra2, Samsurizal1, Bayu Lanzardi Yahya1,M Abyan Alwan3

1Teknik Elektro, Fakultas Ketenagalistrikan dan Energi Terbarukan, Institut Teknologi PLN, 2Teknik Elektro, Sekolah Vokasi, Institut Teknologi PLN, 3Teknik Tenaga Listrik, Fakultas Ketenagalistrikan dan Energi Terbarukan, Institut Teknologi PLN, Duri Kosambi Jakarta Barat, DKI Jakarta, 11750.

Penulis untuk korespondensi/E-mail: andi.mk@itpln.ac.id

Abstract – The utilization of rooftop solar photovoltaic (PV) systems in urban areas has gained significant momentum as part of the energy transition strategy. Determining the optimum tilt angle of PV panels is crucial in maximizing system output. This study aims to analyze the optimum tilt angle for rooftop PV with multiple linear regression in five administrative cities of Jakarta using solar resource data from the Global Solar Atlas. Annual energy yield data were evaluated at an azimuth of 0° (facing north) with tilt angle variations from 0° to 20° in 1° intervals. The analysis employed a quadratic regression model estimated using Ordinary Least Squares (OLS), with uncertainty assessment conducted through 1000 bootstrap iterations. Results indicate that the optimum tilt angle ranges between 5° and 9°, with intercity variations: West Jakarta (5°), North Jakarta (9°), Central Jakarta (7.5°), East Jakarta (8.2°), and South Jakarta (7°). Energy gains compared to the horizontal orientation (0°) are relatively small, less than 1.1%. These findings suggest that for practical rooftop installations in Jakarta, a tilt angle of 7–9° can be recommended, as performance differences with continuous optimum estimation are negligible.

Abstrak - Pemanfaatan Pembangkit Listrik Tenaga Surya (PLTS) atap di wilayah perkotaan semakin berkembang sebagai bagian dari strategi transisi energi. Penentuan sudut kemiringan panel surya merupakan faktor penting yang memengaruhi daya keluaran sistem. Penelitian ini bertujuan untuk menganalisis sudut optimum panel surya pada PLTS atap dengan menggunakan metode regresi linier berganda di lima wilayah Kota Jakarta dengan menggunakan data potensi energi surya dari Global Solar Atlas. Data keluaran energi tahunan dievaluasi pada azimuth 0° (menghadap utara) dengan variasi sudut kemiringan 0°–20° pada interval 1°. Analisis dilakukan dengan pendekatan regresi kuadratik menggunakan Metode Ordinary Least Squares (OLS) dan ketidakpastian estimasi optimum dihitung dengan bootstrap 1000 iterasi. Hasil penelitian menunjukkan bahwa sudut optimum berada pada rentang 5–9°, dengan variasi antar wilayah: Jakarta Barat (5°), Jakarta Utara (9°), Jakarta Pusat (7.5°), Jakarta Timur (8.2°) dan Jakarta Selatan (7°). Peningkatan energi dibandingkan posisi horizontal (0°) relatif kecil, yaitu kurang dari 1.1%. Temuan ini menyarankan bahwa secara praktis, pemasangan panel surya di Jakarta dapat menggunakan sudut 7–9° tanpa modifikasi besar pada struktur atap, karena perbedaan kinerja energi dengan sudut optimum kontinu sangat tipis.

Keywords - Global Solar Atlas, Jakarta, Optimum Tilt Angle, Quadratic Regression, Rooftop Solar PV.

#### PENDAHULUAN

# K

ebutuhan energi di perkotaan terus meningkat seiring dengan pertumbuhan penduduk dan

aktivitas ekonomi. Salah satu upaya strategis untuk mengurangi ketergantungan pada energi fosil adalah pemanfaatan energi terbarukan, khususnya energi

surya. Pemerintah Indonesia melalui berbagai regulasi, termasuk Peraturan Menteri ESDM No. 26 Tahun 2021 yang diperbarui pada 2024, mendorong adopsi Pembangkit Listrik Tenaga Surya (PLTS) atap [1]-[2]. Jakarta sebagai pusat kegiatan ekonomi memiliki potensi besar dalam penerapan PLTS atap, baik di

Received: 27 September 2025, Accepted: 11 December 2025, Published: 26 January 2026

sektor rumah tangga maupun industri, namun salah satu faktor teknis yang berpengaruh pada performa PLTS adalah sudut kemiringan panel surya. Sudut yang tidak optimal dapat mengurangi potensi energi yang dihasilkan, sehingga diperlukan adanya evaluasi berbasis data yang dapat dijadikan acuan teknis [3]–[5].

Penelitian terdahulu menyoroti pentingnya optimasi sudut panel surya [6]–[13], namun sebagian besar studi dilakukan pada skala nasional atau menggunakan simulasi umum, tanpa membedakan antar wilayah kota besar seperti Jakarta yang memiliki variasi iklim mikro. Oleh karena itu, penelitian ini difokuskan untuk menentukan sudut optimum PLTS atap di lima wilayah Kota Jakarta menggunakan Data Global Solar Atlas.

Tujuan utama penelitian ini adalah untuk menentukan sudut kemiringan optimum panel surya di setiap wilayah Jakarta, mengevaluasi perbedaan energi keluaran antara konfigurasi horizontal dan sudut optimum, serta menyusun rekomendasi praktis bagi implementasi sistem PLTS atap rumah tangga di Jakarta, sehingga hasil penelitian dapat memberikan dasar teknis yang lebih akurat bagi perencanaan dan optimasi pemanfaatan energi surya di kawasan tersebut.

METODE Desain, tempat dan waktu

Desain penelitian merupakan Penelitian Kuantitatif dengan menggunakan Metode Regresi Kuadratik. Penelitian dilakukan di Jakarta dalam jangka waktu Juni – Agustus 2025.

#### Data

Data potensi energi surya tahunan diperoleh dari perangkat Global Solar Atlas untuk lima wilayah di Jakarta yaitu Jakarta Barat, Jakarta Utara, Jakarta Pusat, Jakarta Timur dan Jakarta Selatan. Variasi sudut kemiringan panel yang dianalisis adalah 0° hingga 20° dengan interval 1°, pada orientasi azimuth 0° (menghadap utara) dan data yang didapatkan adalah daya luaran tahunan dari PLTS seperti yang tertera pada gambar 1.

![image 1](<jurnal_kemiringan_azimuth_jakarta_2026_images/imageFile1.png>)

Gambar 1. Diagram Alir Penelitian

Analisis Diskrit Sudut optimum awal ditentukan dengan mencari nilai maksimum energi pada dataset diskrit 0°–20°.

#### Analisis Regresi Kuadratik

Berbagai macam metode regresi linear [14] dapat digunakan untuk menganalisa suatu fenomena dan pada penelitian ini Model kuadratik [15]–[18] digunakan untuk memperkirakan optimum kontinu.

E(β) = aβ2+ bβ + c (1)

dengan:

- • E(β) = energi tahunan (MWh/year),
- • β = sudut kemiringan panel (°),
- • a,b,c = parameter regresi hasil OLS.


Sudut optimum kontinu diperoleh dari:

β ∗= − 2𝑎𝑏 (2)

dengan E(β∗) sebagai energi maksimum hasil estimasi.

#### Bootstrap

Bootstrap resampling sebanyak 1000 iterasi per lokasi digunakan untuk mengestimasi interval kepercayaan (CI) 95% dari distribusi β∗.[19]

#### Perangkat Analisis

Seluruh analisis dilakukan menggunakan Python dengan pustaka pandas, statsmodels, numpy dan matplotlib.

#### HASIL DAN PEMBAHASAN

Hasil data sudut kemiringan optimum panel surya pada lima wilayah administrasi Jakarta ditunjukkan pada gambar 2, gambar menunjukkan hasil penentuan sudut optimasi 0°-20° yang berbanding dengan daya keluaran PLTS di lima wilayah kota Jakarta dengan azimuth tetap menghadap utara 0°.

Hasil Koefisien Kuadratik per Lokasi Persamaan umum: E(t)=a t2+b t+c dengan t = sudut kemiringan (°), E dalam MWh/year.

Jakarta Barat Diketahui: β∗=5.1; E∗=1.306; E0=1.294.

Hitung A= (E0−E∗) / β∗2= − 0.012 / 26.01 = − 0.000461530. Maka ekspansi ke bentuk standar memberi:

- a = A = −0.000461530
- b = −2Aβ∗ = 0.004707
- c = Aβ∗2+ E∗ =1.294000


Persamaan: E(t) = −0.000461530t2 + 0.004707 t + 1.294000

Jakarta Utara Diketahui: β∗ = 9.0; E∗ = 1.342; E0= 1.328. A= −0.014/81 = −0.0001728395. Koefisien:

- a = − 0.000172840
- b = − 2aβ∗ = 0.003111111
- c = 1.328000


Persamaan: E(t) = − 0.000172840 t2 + 0.003111 t + 1.328000

Jakarta Pusat Diketahui:

- β∗ = 7.5; E* = 1.301; E0 = 1.291. A= − 0.010/56.25 = −0.0001777778. Koefisien:

- a = − 0.000177778
- b = − 2aβ*= 0.002666667
- c = 1.291000


Persamaan: E(t) = − 0.000177778t2 + 0.002666667 t + 1.291000

Jakarta Timur Diketahui:

- β∗ = 8.2; E∗ = 1.287; E0= 1.275 Koefisien:


- a = − 0.000178444
- b = − 2aβ∗ = 0.002925
- c = 1.275000


Persamaan: E(t) = − 0.000178444 t2 + 0.002925 t + 1.275000

#### Jakarta Selatan

Kasus khusus: E0= E∗=1.281E_ sehingga A dari t=0 akan nol, untuk memperoleh koefisien yang lebih representatif peneliti menggunakan titik t = 20 (E20 = 1.263) bersama β∗=7.0 dan E∗ = 1.281.

Gunakan A= (E20−E∗) / (20−β∗)2 = − 0.018/169

= − 0.0001065089. Koefisien:

- a = − 0.000106509
- b = − 2aβ∗ = 0.001491124
- c = Aβ∗2+ E∗ = 1.275781 (hasil ini sedikit berbeda dari E0 karena pemilihan titik t = 20 untuk penentuan A)


Persamaan (aproksimasi): E(t) = − 0.000106509 t2+ 0.001491124 t + 1.275781

![image 2](<jurnal_kemiringan_azimuth_jakarta_2026_images/imageFile2.png>)

Gambar 2. Kurva 3D Sudut Kemiringan vs Daya Keluaran PLTS Atap di Lima Wilayah Jakarta Tabel 1. Sudut optimum PLTS atap di lima wilayah Jakarta

R2 Jakarta Barat

Lokasi Sudut_opt (diskrit)

Daya_max (MWh/th)

Daya_0° (MWh/th)

% Gain dari 0°

Betaa_opt (OLS, °)

CI 95% ( ° )

5 1.306 1.294 +0.93% 5.1 4.6 - 5.7 0.999 Jakarta Utara

9 1.342 1.328 +1.05% 9.0 8.4 - 9.7 0.999 Jakarta Pusat

7-10 1.301 1.291 +0.77% 7.5 6.9 - 8.2 0.999

Jakarta Timur

8-10 1.287 1.275 +0.94% 8.2 7.6 - 8.9 0.999

Jakarta Selatan

0 & 7-10 1.281 1.281 ≈0.00% 7.0 6.2 - 7.8 0.998

Hasil analisis menunjukkan bahwa setiap wilayah Jakarta memiliki variasi sudut kemiringan optimum yang relatif rendah yaitu berada pada kisaran 5° hingga 9°. Perbedaan daya keluaran antara sudut horizontal (0°) dan sudut optimum kontinu relatif kecil, dengan peningkatan maksimum kurang dari 1.1%. Ringkasan hasil analisis sudut optimum PLTS atap di lima wilayah Jakarta disajikan pada tabel 1.

Hasil menunjukkan optimum praktis berada di rentang 5–9°. Peningkatan energi dibandingkan posisi horizontal relatif kecil (<1.1%). Perbedaan paling besar terjadi di Jakarta Utara, sementara di Jakarta Selatan energi optimum hampir sama dengan kondisi datar. Hal ini mengindikasikan bahwa modifikasi sudut yang signifikan tidak selalu diperlukan.

Temuan ini konsisten dengan posisi geografis Jakarta (lintang ≈ 6° LS), di mana sudut optimum

panel cenderung mendekati lintang lokal [20], [21]. Dalam implementasinya rekomendasi sudut 7–9° dianggap memadai, selain itu juga membantu mengurangi akumulasi debu dan air hujan di panel.

Selain ditampilkan dalam bentuk tabulasi, hasil analisis juga divisualisasikan untuk memperjelas perbedaan antar wilayah. Gambar 2 menyajikan kurva hubungan antara variasi sudut kemiringan panel (0–20°) dengan daya keluaran tahunan pada lima wilayah Jakarta, serta perbandingan langsung antara daya pada posisi horizontal (0°) dan daya pada sudut optimum.

#### KESIMPULAN

Hasil penelitian menunjukkan bahwa sudut kemiringan optimum panel surya di lima wilayah Jakarta berada pada rentang 5°–9°, dengan

perbedaan yang relatif tipis antar wilayah. Penerapan sudut optimum tersebut menghasilkan peningkatan energi keluaran yang relatif kecil, yakni kurang dari 1,1% dibandingkan konfigurasi horizontal, sehingga secara praktis tidak terdapat penalti energi yang signifikan apabila terjadi deviasi kecil dari sudut ideal. Berdasarkan analisis Global Solar Atlas dan konsistensi pola radiasi antarwilayah, rekomendasi umum yang paling relevan untuk implementasi PLTS atap rumah tangga di Jakarta adalah penggunaan sudut kemiringan 7°–9°. Dengan demikian, rekomendasi ini dapat diterapkan secara luas tanpa memerlukan penyesuaian spesifik antarwilayah di Jakarta.

#### UCAPAN TERIMA KASIH

Penulis menyampaikan penghargaan yang setinggitingginya kepada Institut Teknologi PLN dan Kementerian Pendidikan Tinggi, Sains, dan Teknologi atas dukungan pendanaan melalui hibah Kementerian Pendidikan Tinggi Sain dan Teknologi tahun 2025 dengan Nomor Kontrak Internal: 004/PDP/B08/2025 serta Kontrak Turunan: 0923/LL3/AL.04/2025. Ucapan terima kasih juga disampaikan kepada LPPM ITPLN yang telah memfasilitasi dan memberikan dukungan penuh dalam pelaksanaan penelitian ini. Berkat kolaborasi dan dukungan tersebut, penelitian ini dapat diselesaikan dan ditulis dalam bentuk naskah ilmiah. Harapannya, hasil penelitian ini tidak hanya menjadi rujukan bagi penelitian selanjutnya, tetapi juga memberikan kontribusi nyata dalam memperkaya wawasan dan pengetahuan para pembaca.

#### REFERENSI

- [1] Menteri ESDM, “Peraturan Menteri Energi Dan Sumber Daya Mineralrepublik Indonesianomor 2 Tahun 2024 Tentang Pembangkit Listrik Tenaga Surya Atap Yang Terhubung Pada Jaringan Tenaga Listrik Pemegang Izin Usaha Penyediaan Tenaga Listrik Untuk Kepentingan Umum,” Mentri Energi dan Sumber Daya Miner., vol. 2024, pp. 1–35, 2024, [Online]. Available: https://jdih.esdm.go.id/storage/document/Perm en ESDM Nomor 2 Tahun 2024.pdf.
- [2] Kementerian ESDM RI, Peraturan Menteri ESDM no 26 tahun 2021. 2021.
- [3] A. Makkulau and Christiono; Samsurizal, “Characteristics of Temperature Changes Measurement on Photovoltaic Surfaces Against Quality of Output Current on Solar Power


- Plants,” in 2019 International Conference on Technologies and Policies in Electric Power and Energy, TPEPE 2019, 2019, pp. 20–23, doi: 10.1109/IEEECONF48524.2019.9102630.
- [4] R. Samsurizal, Afrianda and A. Makkulau, “Optimizing the Potential of Solar Energy PT PJB UP Muara Karang Rooftop Area Using HelioScope,” Elkha J. Tek. Elektro, vol. 14, no. 1, pp. 1–6, 2022, doi: http://dx.doi.org/10.26418/elkha.v14i1.49910.
- [5] M. A. Samsurizal, Christiono, “Evaluasi Sudut Kemiringan Terhadap Pengaruh Irradiance Pada Array Photovoltaic Jenis Monocristalline,” J. Ilm. Setrum, vol. 8, no. 1, pp. 28–34, 2019, doi: http://dx.doi.org/10.36055/setrum.v8i1.5135.
- [6] N. P. Sartono, E. Ridwan, and H. Mohammad, “Pengaruh Perbedaan Posisi Sudut Kemiringan Panel Surya 120 Watt Peak Terhadap Peningkatan Efisiensi,” Pros. Semin. Nas., pp. 246–253, 2021.
- [7] T. M. A. Pandria, M. Muzakir, E. Mawardi, S. Samsuddin, M. Munawir, and M. Mukhlizar, “Penentuan Sudut Kemiringan Optimum Berdasarkan Energi Keluaran Panel Surya,” J. Serambi Eng., vol. 6, no. 1, pp. 1655–1661, 2021, doi: 10.32672/jse.v6i1.2665.
- [8] D. Hendrawati and N. F. A. S. Nadella Penny, “Analisis Perhitungan Optimasi Daya Panel Surya Ditinjau Dari Sudut Kemiringan Peneerimaan Iradiasi Panel Surya,” vol. 1, no. November, pp. 846–855, 2021.
- [9] Samsurizal, M. Andi, and Christiono, “Analisis Pengaruh Sudut Kemiringan Terhadap Arus Keluaran Pada Photovoltaic Dengan Menggunakan Regretion Quadratic Method,” Energi & Kelistrikan, vol. 10, no. 2, pp. 137– 144, 2018.
- [10] A. Makkulau, Samsurizal, and M. Fikri, “Pengaruh Intensitas Matahari Terhadap Karakteristik Sel Surya Jenis Polycristaline Menggunakan Regresi Linear,” vol. 10, no. 1, pp. 69–76, 2021, doi: 10.33322/kilat.v10i1.994.
- [11] N. Mukisa and R. Zamora, “Optimal tilt angle for solar photovoltaic modules on pitched rooftops: A case of low latitude equatorial region,” Sustain. Energy Technol. Assessments, vol. 50, no. October 2021, 2022, doi: 10.1016/j.seta.2021.101821.
- [12] M. Nfaoui and K. El-Hami, “Extracting the maximum energy from solar panels,” Energy Reports, vol. 4, pp. 536–545, 2018, doi: 10.1016/j.egyr.2018.05.002.
- [13] M. Alaikal Huda and A. Makkulau, “Evaluasi Sudut Kemiringan Pada Panel Surya Untuk


- Mendapatkan Nilai Irradiance Terbaik Dengan Arus Tertinggi,” Institut Teknologi PLN, 2022.
- [14] S. Hidayat, W. N. Tanjung, C. A. Marthayodha, and D. Rachmawaty, “Analisis Model Rantai Pasok Universitas Al Azhar Indonesia Bagian II - Bidang Penelitian,” Jurnal Al-Azhar Indonesia Seri Sains dan Teknologi., vol. 3, no. 1, p. 23, 2017, doi: 10.36722/sst.v3i1.180.
- [15] A. F. M. S. Makkulau, “Pengaruh Iradiasi Matahari Terhadap Arus Keluaran Pada Permukaan Modul Surya Dengan Menggunakan Simulasi Matlab,” 2022, pp. 38– 42, [Online]. Available: https://eng.unhas.ac.id/electrical/sneti/prosidin g/prosiding.html.
- [16] D. Dahliya, S. Samsurizal, and N. Pasra, “Efisiensi Panel Surya Kapasitas 100 Wp Akibat Pengaruh Suhu Dan Kecepatan Angin,” Sutet, vol. 11, no. 2, pp. 71–80, 2021, doi: 10.33322/sutet.v11i2.1551.
- [17] N. R. Budhianti and T. Widiharih, “D-Optimal Design For 3rd Degree Polynomial Regression With Heteroscedastisity,” J. gaussian, vol. 2, no. April, pp. 129–135, 2013.


- [18] H. Qu, H. Zhao, W. Wang, and J. Zhang, “Experimental study on the losses of dusty PV modules considering irradiance levels and tilt angles,” Energy Reports, vol. 13, no. October 2024, pp. 2844–2854, 2025, doi: 10.1016/j.egyr.2025.02.011.
- [19] E. W. Steyerberg, F. E. Harrell, G. J. J. M. Borsboom, M. J. C. Eijkemans, Y. Vergouwe, and J. D. F. Habbema, “Internal validation of predictive models: Efficiency of some procedures for logistic regression analysis,” J. Clin. Epidemiol., vol. 54, no. 8, pp. 774–781, 2001, doi: 10.1016/S0895-4356(01)00341-9.
- [20] A. Martial, E. A. Akata, D. Njomo, B. Agrawal, A. Mackpayen, and A. M. Ali, “Tilt Angle and Orientation Assessment of Photovoltaic Thermal ( PVT ) System for Sub-Saharan Tropical Regions : Case Study Douala , Cameroon,” 2022.
- [21] B. Rinchi, R. Dababseh, M. Jubran, S. Aldahidi, M. E. B. Abdalla, and O. Ayadi, “Global prediction of optimal solar panel tilt angles via machine learning,” vol. 382, no. October 2024, 2025.


