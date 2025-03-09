import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# Load Dataset
pd.read_csv("dashboard/main_dataset.csv")

# Konfigurasi Tema
st.title("🚴‍♂️ Dashboard Analisis Penyewaan Sepeda")

# Sidebar - Filter Tahun
tahun_pilihan = st.sidebar.selectbox("Pilih Tahun:", df["yr"].unique())

# Data Filter Berdasarkan Tahun
df_filtered = df[df["yr"] == tahun_pilihan]

#Visualisasi 1: Hari Kerja vs Hari Libur
st.subheader("📊 Perbandingan Penyewaan Sepeda:  Hari Libur vs Hari Kerja")
workingday_summary = df_filtered.groupby("workingday")["cnt"].mean().reset_index()
workingday_summary["Kategori"] = workingday_summary["workingday"].map({0: "Hari Libur", 1: "Hari Kerja"})
sns.set_theme(style="whitegrid")
colors = ["#FF0808", "#336699"]
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x="Kategori", y="cnt", hue="Kategori", data=workingday_summary, palette=colors, legend=False)
plt.ylabel("Rata-rata Penyewaan")
plt.xlabel("")
st.pyplot(fig)

#Expander berupa kesimpulan visualisasi data
st.subheader("Perbandingan Penyewaan Sepeda pada Hari Kerja dan Hari Libur")
with st.expander("hasil kesimpulan"):
    st.markdown("""
    Berdasarkan visualisasi yang ditampilkan dalam bar chart, rata-rata penyewaan sepeda pada hari kerja lebih tinggi 
    dibandingkan hari libur. Hal ini menunjukkan bahwa sepeda lebih sering digunakan sebagai moda transportasi untuk 
    aktivitas sehari-hari seperti bekerja atau sekolah, bukan hanya untuk rekreasi. Saat hari libur, pengguna cenderung 
    lebih sedikit karena mereka mungkin memiliki alternatif kegiatan lain atau tidak perlu bepergian sejauh di hari kerja.
    """)

#Visualisasi 2: Pengaruh Cuaca
st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")
weather_summary = df_filtered.groupby("weathersit")["cnt"].sum().reset_index()
weather_labels = {1: "Cerah Berawan", 2: "Mendung Kabut", 3: "Hujan Ringan", 4: "Badai Ekstrem"}
weather_summary["Cuaca"] = weather_summary["weathersit"].map(weather_labels)
weather_colors = ["#99CCFF", "#3399CC", "#006699", "#333366"]
fig, ax = plt.subplots(figsize=(4, 2))
plt.pie(weather_summary["cnt"], labels=weather_summary["Cuaca"], autopct="%1.1f%%", colors=weather_colors, startangle=180)
plt.title("Distribusi Penyewaan Berdasarkan Cuaca")
st.pyplot(fig)

#Expander berupa kesimpulan visualisasi data
st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
with st.expander("hasil kesimpulan"):
    st.markdown("""
    Dari hasil donut chart, terlihat bahwa cuaca memiliki dampak besar terhadap jumlah penyewaan sepeda. Penyewaan sepeda 
    tertinggi terjadi saat cuaca cerah atau berawan, sementara jumlahnya jauh lebih rendah saat kondisi hujan ringan dan 
    badai ekstrem. Hal ini bisa disebabkan oleh kenyamanan pengguna dalam bersepeda saat kondisi cuaca mendukung, sedangkan
    cuaca buruk menghambat aktivitas luar ruangan.
    """)

#Visualisasi 3: Pengguna Terdaftar vs Kasual
st.subheader("👥 Perbandingan Penyewaan: Pengguna Kasual vs Terdaftar")
monthly_user_trend = df_filtered.groupby("mnth")[["casual", "registered"]].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 4))
monthly_user_trend.set_index("mnth").plot(kind="bar", color=["#4682B4", "#DC143C"], edgecolor="black", ax=ax)
plt.xticks(rotation=0)
plt.xlabel("Bulan")
plt.ylabel("Rata-rata Penyewaan")
plt.legend(["Pengguna Kasual", "Pengguna Terdaftar"])
st.pyplot(fig)

#Expander berupa kesimpulan visualisasi data
st.subheader("Perbedaan Jumlah Penyewaan Sepeda antara Pengguna Kasual dan Pengguna Terdaftar")
with st.expander("hasil kesimpulan"):
    st.markdown("""
    Dari bar chart yang menggambarkan tren pengguna sepeda berdasarkan jenisnya, terlihat bahwa pengguna terdaftar lebih 
    mendominasi penyewaan sepeda dibandingkan pengguna kasual. Artinya, pengguna yang telah berlangganan layanan penyewaan 
    cenderung lebih sering menggunakan sepeda dibandingkan pengguna kasual yang hanya menyewa sesekali. Ini bisa mengindikasikan 
    keberhasilan program langganan dalam meningkatkan penggunaan sepeda secara rutin.
    """)

#Visualisasi 4: Perubahan Penyewaan 2011 vs 2012
st.subheader("📈 Tren Penyewaan Sepeda Tahun 2011 vs 2012")
year_trend = df.groupby(["yr", "mnth"])["cnt"].sum().unstack()
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#1E90FF", "#FF4500"]
for i, year in enumerate(year_trend.index):
    plt.plot(year_trend.columns, year_trend.loc[year], marker="o", linestyle="-", linewidth=2, markersize=6, color=colors[i], label=f"Tahun {year}")
plt.xlabel("Bulan")
plt.ylabel("Total Penyewaan")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig)

#Expander berupa kesimpulan visualisasi data
st.subheader("Perubahan Penyewaan Sepeda dari Tahun 2011 ke 2012")
with st.expander("hasil kesimpulan"):
    st.markdown("""
    Berdasarkan line chart, jumlah penyewaan sepeda mengalami peningkatan signifikan pada tahun 2012 dibandingkan 2011. Pola 
    musiman tetap serupa, dengan peningkatan jumlah penyewaan selama musim panas dan penurunan saat mendekati akhir tahun.
    Namun, di setiap bulan, jumlah penyewaan di tahun 2012 selalu lebih tinggi dibandingkan 2011.Hal ini bisa disebabkan oleh 
    meningkatnya popularitas layanan sepeda, perbaikan infrastruktur, atau kampanye promosi yang lebih efektif.
    """)

st.sidebar.header("🔧 Pengaturan Tampilan")
if st.sidebar.checkbox("Tampilkan Data Mentah"):
    st.subheader("📄 Data Mentah Penyewaan Sepeda")
    st.dataframe(df_filtered)

