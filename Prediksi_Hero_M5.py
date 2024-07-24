import pickle
import streamlit as st
from sklearn.preprocessing import LabelEncoder

# Memuat model dan label encoder
model = pickle.load(open('prediksi.sav', 'rb'))
label_encoder = pickle.load(open('label_encoder.pkl', 'rb'))

# Judul
st.title('Prediksi M5')

# Menambahkan deskripsi aplikasi
st.write("""
Aplikasi ini memprediksi performa M5 berdasarkan beberapa parameter yang diinputkan. 
Silakan masukkan data pada kolom-kolom yang disediakan di sebelah kiri dan tekan tombol Submit untuk melihat hasil prediksi.
""")

# Menggunakan sidebar untuk input
st.sidebar.title('Input Parameter')

# Input dengan keterangan dan tipe numerik
hero_names = label_encoder.classes_
Hero_Encoded = st.sidebar.selectbox('Nama Hero', hero_names, help="Pilih hero yang ingin diprediksi")
T_Picked = st.sidebar.text_input('Total Pick', help="Masukkan total pick untuk hero ini")
BS_Picked = st.sidebar.text_input('BS Pick', help="Masukkan jumlah pick di Battle State")
RS_Picked = st.sidebar.text_input('RS Pick', help="Masukkan jumlah pick di Ranking State")
T_Banned = st.sidebar.text_input('T Ban', help="Masukkan total ban untuk hero ini")
T_PicksBans = st.sidebar.text_input('Total Pick Ban', help="Masukkan total pick dan ban untuk hero ini")

prediksi_tim = ''

if st.sidebar.button('Submit'):
    try:
        # Konversi nama hero menjadi kode
        Hero_Encoded = label_encoder.transform([Hero_Encoded])[0]
        
        # Konversi input lainnya menjadi float
        T_Picked = float(T_Picked)
        BS_Picked = float(BS_Picked)
        RS_Picked = float(RS_Picked)
        T_Banned = float(T_Banned)
        T_PicksBans = float(T_PicksBans)
        
        # Lakukan prediksi
        MSE = model.predict([[Hero_Encoded, T_Picked, BS_Picked, RS_Picked, T_Banned, T_PicksBans]])

        # Asumsi: Normalisasi hasil prediksi jika berada dalam rentang 0 hingga 1000
        prediksi_persen = (MSE[0] / 1000) * 100

        # Tampilkan hasil prediksi dengan penjelasan
        st.write(f"Prediksi: {prediksi_persen:.2f}%")
        st.write("""
        Hasil prediksi menunjukkan estimasi performa M5 berdasarkan parameter-parameter yang telah dimasukkan.
        Nilai prediksi ini dapat digunakan untuk memahami potensi performa hero dalam pertandingan mendatang.
        """)
    except ValueError:
        st.error('Harap masukkan nilai numerik yang valid.')
    except Exception as e:
        st.error(f'Error: {str(e)}')

# Menambahkan footer
st.markdown("""
<style>
footer {
    visibility: hidden;
}
footer:after {
    content:'Dibuat dengan Streamlit'; 
    visibility: visible;
    display: block;
    position: relative;
    padding: 5px;
    top: 2px;
}
</style>
""", unsafe_allow_html=True)