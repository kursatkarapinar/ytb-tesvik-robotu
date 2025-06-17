import streamlit as st
import pandas as pd
import fnmatch
from il_ilce_data import df_il_ilce
from Hangibolge import df_il_bolge
from OncelikliYatirim import oncelikli_yatirim_secim_listesi
from HedefYatirim import df_hedef_yatirim
from NACE import df_nace

# Başlığı ortalamak için sütunlar
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.title("Yeni YTB Teşvik Robotu")

# 0) NACE Kodunu veya Tanımını Ara ve Seç
query = st.text_input("NACE REV.2.1 Kodu veya Tanım Ara:")
filtered = df_nace[
    df_nace["NACE REV. 2.1 KODU"].str.contains(query, case=False, na=False) |
    df_nace["NACE REV.2.1 TANIM"].str.contains(query, case=False, na=False)
]
options = [f"{row['NACE REV. 2.1 KODU']} - {row['NACE REV.2.1 TANIM']}" for _, row in filtered.iterrows()]
if options:
    selection = st.selectbox("Önerilen NACE Kodları:", options)
    if selection:
        nace_kodu, yatirim_adi = selection.split(" - ", 1)
else:
    nace_kodu = query.strip()
    yatirim_adi = ""

# 1) İl Seçimi
iller = sorted(df_il_ilce["İl"].unique())
secili_il = st.selectbox("İl Seçin", iller)

# 2) İlçe Seçimi
ilceler = sorted(df_il_ilce[df_il_ilce["İl"] == secili_il]["İlçe"].unique())
secili_ilce = st.selectbox("İlçe Seçin", ilceler)

# 3) OSB veya Endüstri Bölgesi Sorgusu
bolge_secim = st.radio(
    "OSB veya Endüstri Bölgesi mi?",
    ("Evet", "Hayır")
)

# 4) Öncelikli Yatırım Sorgusu
secim_oncelikli = st.selectbox(
    "Listedeki Öncelikli Yatırımlardan mı?",
    oncelikli_yatirim_secim_listesi
)

# 5) Sorgula
if st.button("Sorgula"):
    # 5.0) Geçerlilik kontrolü
    if nace_kodu not in df_nace["NACE REV. 2.1 KODU"].values:
        st.error("❌ Hatalı NACE Kodu girdiniz!")
        st.stop()

    # 5.1) Yatırımın Adı (seçim ile güncellendiğini garanti etmek için tekrar çek)
    yatirim_adi = df_nace.loc[
        df_nace["NACE REV. 2.1 KODU"] == nace_kodu,
        "NACE REV.2.1 TANIM"
    ].squeeze()

    # 5.2) İlin Bulunduğu Bölge
    bolge_no = df_il_bolge.loc[
        df_il_bolge["İl"] == secili_il,
        "Kaçıncı Bölge"
    ].iloc[0]
    bolge_yazi = f"{bolge_no}. Bölge"

    # 5.3) SGK Hissesi Yararlanılacak Bölge
    yararlanilan_bolge = bolge_no
    if secili_ilce != "Diğer İlçeler":
        yararlanilan_bolge += 1
    if bolge_secim == "Evet":
        yararlanilan_bolge += 1
    yararlanilan_bolge = min(yararlanilan_bolge, 6)
    sgk_region = f"{yararlanilan_bolge}. Bölge"

    # 5.4) Öncelikli Yatırım mı?
    oncelikli_flag = "Hayır" if secim_oncelikli in ["Seçiniz...", "z) Hayır."] else "Evet"

    # 5.5) Hedef Yatırım mı? & Özel Şartlar
    matches = df_hedef_yatirim[
        df_hedef_yatirim["NACE KODU"].astype(str)
        .apply(lambda pat: fnmatch.fnmatch(nace_kodu, pat))
    ]
    if not matches.empty:
        hedef_flag = "Evet"
        ozel_sart = matches["Özel Şartlar"].iloc[0]
    else:
        hedef_flag = "Hayır"
        ozel_sart = "Hedef Yatırım Değildir"

    # 5.6) Seçim Özeti Tablo
    st.subheader("Sonuçlar")
    summary = {
        'NACE Kodu': nace_kodu,
        'Yatırımın Adı': yatirim_adi,
        'İl': secili_il,
        'İlçe': secili_ilce,
        'İlin Olduğu Bölge': bolge_yazi,
        'SGK Hissesi Yararlanılacak Bölge': sgk_region,
        'OSB/Endüstri Bölgesi': bolge_secim,
        'Öncelikli Yatırım mı?': oncelikli_flag,
        'Hedef Yatırım mı?': hedef_flag,
        'Yatırımla İlgili Özel Şartlar': ozel_sart
    }
    st.table(pd.DataFrame(list(summary.items()), columns=['Başlık', 'Değer']))

    # 5.7) Destekler Metric Görünümü
    kdv, gumruk, yer_tahsisi = (
        ("Yok", "Yok", "Yok")
        if (oncelikli_flag == "Hayır" and hedef_flag == "Hayır")
        else ("Var", "Var", "Var")
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("KDV İstisnası", kdv)
    col2.metric("Gümrük Muafiyeti", gumruk)
    col3.metric("Yatırım Yeri Tahsisi", yer_tahsisi)

    # 5.8) SGK Hissesi Destekleri
    sgk_map = {1: "-", 2: "1 Yıl", 3: "2 Yıl", 4: "4 Yıl", 5: "8 Yıl", 6: "12 Yıl"}
    sgk_hibe = sgk_map.get(yararlanilan_bolge, "-")
    sgk_isci = "10 Yıl" if yararlanilan_bolge == 6 else "Yok"
    col4, col5 = st.columns(2)
    col4.metric("SGK İşveren Hissesi", sgk_hibe)
    col5.metric("SGK İşçi Hissesi", sgk_isci)

    # 5.9) Finansal Destekler
    if oncelikli_flag == "Evet":
        tax_display = "%60, YKO %30"
    elif oncelikli_flag == "Hayır" and hedef_flag == "Evet":
        tax_display = "Yok" if secili_il == "İstanbul" else "%60, YKO %20"
    else:
        tax_display = "Yok"
    if oncelikli_flag == "Evet":
        faiz_desteği = (
            "Var. Faiz oranı TCMB bir hafta vadeli REPO faiz oranının %25 ile 12,5 puandan küçük olanı geçemez. "
            "Faiz tutarı sabit yatırım tutarının %10'u ile 24 Milyon TL'den küçük olanı geçemez."
        )
    elif oncelikli_flag == "Hayır" and hedef_flag == "Evet":
        faiz_desteği = (
            "Var. Faiz oranı TCMB bir hafta vadeli REPO faiz oranının %25 ile 12,5 puandan küçük olanı geçemez. "
            "Faiz tutarı sabit yatırım tutarının %10'u ile 12 Milyon TL'den küçük olanı geçemez."
        )
    else:
        faiz_desteği = "Yok"
    st.subheader("Finansal Destekler")
    st.write(f"**Vergi İndirimi:** {tax_display}")
    st.write(f"**Faiz Desteği:** {faiz_desteği}")

    # 5.10) Diğer Destekler
    col6, col7 = st.columns(2)
    col6.metric("Makine Desteği", "Yok")
    asgari_yatirim = "12 Milyon TL" if bolge_no in [1, 2] else "6 Milyon TL"
    col7.metric("Asgari Yatırım Tutarı", asgari_yatirim)

    # 5.11) Ekosistem Geliştirme Planı
    st.write("**Ekosistem Geliştirme Planı:** Büyük İşletme veya Yerel Kalkınma Hamlesi ise Evet.")

# Boş alt satır için placeholder
st.write(" ")
