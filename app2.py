import streamlit as st
import pandas as pd
import fnmatch
from il_ilce_data import df_il_ilce
from Hangibolge import df_il_bolge
from OncelikliYatirim import oncelikli_yatirim_secim_listesi
from HedefYatirim import df_hedef_yatirim
from NACE import df_nace


def cagr(v_start: float, v_end: float, years: int) -> float:
    """Yıllık bileşik büyüme oranı (CAGR)"""
    try:
        if v_start <= 0 or v_end <= 0 or years <= 0:
            return float("nan")
        return (v_end / v_start) ** (1.0 / years) - 1.0
    except Exception:
        return float("nan")

def pct_style(value: float) -> str:
    if pd.isna(value):
        return '<span style="color:#666">—</span>'
    color = "#069f3c" if value > 0.10 else "#c62828"
    return f'<span style="color:{color}; font-weight:700">{value*100:.2f}%</span>'

def valid_positive_numbers(vals):
    try:
        return all(float(v) >= 0 for v in vals)
    except Exception:
        return False

DEFLATORS = {
    2021: 0.18852,
    2022: 0.36950,
    2023: 0.6215,
    2024: 1.0,
}

left, right = st.columns([1, 1], gap="large")



# Başlığı tam ortalamak için üç sütun
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.title("Yeni YTB Teşvik Robotu")


# 0) Tüm kod–tanım çiftlerini hazırla
faaliyet_options = [
    f"{row['NACE REV. 2.1 KODU']} - {row['NACE REV.2.1 TANIM']}"
    for _, row in df_nace.iterrows()
]

# 1) Arama terimini tek satırda al
search_term = st.text_input(
    "Nace Kodunu veya Konuyu Arayın…",
    placeholder="Örn. kalem, 25.61.07 …"
).strip()

# 2) Aramaya göre filtrele (substring bazlı)
if search_term:
    filtered = [
        opt for opt in faaliyet_options
        if search_term.lower() in opt.lower()
    ]
else:
    # search_term boşken tüm listeyi göstermek yerine hiçbir şey göstermeyebilirsiniz:
    filtered = []

# 3) Eğer eşleşme varsa selectbox’u göster, yoksa uyarı ver
if filtered:
    # Başına isterseniz boş bir değer ekleyebilirsiniz:
    selection = st.selectbox(
        "Eşleşen NACE Kodları:",
        [""] + filtered,
        index=0
    )
    nace_kodu = selection.split(" - ")[0] if selection else ""
    if nace_kodu:
        st.success(f"Seçilen NACE Kodu: {nace_kodu}")
else:
    if search_term:
        st.warning("Eşleşen NACE kodu bulunamadı!")
    # hiçbir şey seçilmedi
    nace_kodu = ""

# 1) İl Seçimi
iller = sorted(df_il_ilce["İl"].unique())
iller_options = [""] + iller
secili_il = st.selectbox("İl Seçin*", iller_options, index=0)

# 2) İlçe Seçimi
ilceler = sorted(df_il_ilce[df_il_ilce["İl"] == secili_il]["İlçe"].unique())
ilceler_options = [""] + ilceler
secili_ilce = st.selectbox("İlçe Seçin*", ilceler_options, index=0)

# 3) OSB veya Endüstri Bölgesi Sorgusu
bolge_secim = st.radio(
    "OSB veya Endüstri Bölgesi mi?*",
    ("Seçiniz...", "Evet", "Hayır"),
    index=0
)
# 4) Öncelikli Yatırım Sorgusu
oncelikli_options = [""] + oncelikli_yatirim_secim_listesi
secim_oncelikli = st.selectbox(
    "Listedeki Öncelikli Yatırımlardan mı?*",
    oncelikli_options,
    index=0
)

col1, col2 = st.columns([3, 1])

with col2:
    # 1) BİRLEŞİK YAZDIRARAK SATIR BOŞLUĞUNU KALDIRMA
    # st.write tek çağrıda “  \n” (iki boşluk + newline) ile satır sonu verir
    st.write("**Kürşat Karapınar**  \n")

# 5) Sorgula

if st.button("Sorgula"):
    # 5.0) Genel alan doldurma kontrolü
    if not secili_il or not secili_ilce or bolge_secim == "Seçiniz..." or secim_oncelikli == "":
        st.error("❌ Lütfen Tüm Alanları (*) Eksiksiz Doldurun!")
        st.stop()
    # 5.1) Geçerlilik kontrolü
    # Geçerlilik kontrolü
    if nace_kodu not in df_nace["NACE REV. 2.1 KODU"].values:
        st.error("❌ Hatalı NACE Kodu girdiniz!")
        st.stop()


    # 5.1) Yatırımın Adı
    yatirim_adi = df_nace.loc[
        df_nace["NACE REV. 2.1 KODU"] == nace_kodu,
        "NACE REV.2.1 TANIM"
    ].squeeze()
    # … geriye kalan tüm kodlar aynı şekilde devam eder …


    # 5.2) İlin Bulunduğu Bölge
    bolge_no = df_il_bolge.loc[
        df_il_bolge["İl"] == secili_il,
        "Kaçıncı Bölge"
    ].iloc[0]
    bolge_yazi = f"{bolge_no}. Bölge"

    # Yararlanılacak Bölge hesapla (önceki mantık)
    yararlanilan_bolge = bolge_no
    if secili_ilce and secili_ilce not in ["Diğer İlçeler", "Tüm İlçeler"]:
        yararlanilan_bolge += 1
    if bolge_secim == "Evet":
        yararlanilan_bolge += 1
    yararlanilan_bolge = min(yararlanilan_bolge, 6)
    yararlanilacak_bolge_yazi = f"{yararlanilan_bolge}. Bölge"


        # Öncelikli/Hedef Yatırım
    oncelikli_flag = "Hayır" if secim_oncelikli in ["Seçiniz...", "Hayır."] else "Evet"
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

    # Eğer hem Öncelikli hem Hedef yatırım hayırsa uyar ve durdur
    if oncelikli_flag == "Hayır" and hedef_flag == "Hayır":
        st.error("Seçtiğiniz NACE Kodu Yatırım Teşvik Belgesi kapsamında desteklenmemektedir.")
        st.stop()

    # Sonuç özeti

    

    # 5.5) Seçim Özeti
    st.subheader("Sonuçlar")
    st.write(f"**NACE Kodu:** {nace_kodu}")
    st.write(f"**Yatırımın Adı:** {yatirim_adi}")
    st.write(f"**İl:** {secili_il}")
    st.write(f"**İlçe:** {secili_ilce}")
    st.write(f"**İlin Olduğu Bölge:** {bolge_yazi}")
    # SGK Hissesi Yararlanılacak Bölge (yeni konum)
    st.write(f"**SGK Hissesi Yararlanılacak Bölge:** {yararlanilacak_bolge_yazi}")
    st.write(f"**OSB/Endüstri Bölgesi:** {bolge_secim}")
    st.write(f"**Öncelikli Yatırım mı?** {oncelikli_flag}")
    st.write(f"**Hedef Yatırım mı?** {hedef_flag}")
    st.write(f"**Yatırımla İlgili Özel Şartlar:** {ozel_sart}")

    # 5.6) KDV, Gümrük ve Yer Tahsisi
    kdv = gumruk = yer_tahsisi = "Yok" if (oncelikli_flag == "Hayır" and hedef_flag == "Hayır") else "Var"
    st.write(f"**KDV İstisnası:** {kdv}")
    st.write(f"**Gümrük Vergisi Muafiyeti:** {gumruk}")
    st.write(f"**Yatırım Yeri Tahsisi:** {yer_tahsisi}")

    # 5.7) SGK İşveren Hissesi Desteği
    sgk_map = {1: "-", 2: "1 Yıl", 3: "2 Yıl", 4: "4 Yıl", 5: "8 Yıl", 6: "12 Yıl"}
    sgk_hibe = sgk_map.get(yararlanilan_bolge, "-")
    st.write(f"**SGK İşveren Hissesi Desteği:** {sgk_hibe}")

    # 5.8) SGK İşçi Hissesi Desteği
    sgk_isci = "10 Yıl" if yararlanilan_bolge == 6 else "Yok"
    st.write(f"**SGK İşçi Hissesi Desteği:** {sgk_isci}")

    # 5.9) Vergi İndirimi
    if oncelikli_flag == "Evet":
        tax_display = "%60, YKO %30"
    elif oncelikli_flag == "Hayır" and hedef_flag == "Evet":
        tax_display = "Yok" if secili_il == "İstanbul" else "%60, YKO %20"
    else:
        tax_display = "Yok"
    st.write(f"**Vergi İndirimi:** {tax_display}")

    # 5.10) Faiz Desteği
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
    st.write(f"**Faiz Desteği:** {faiz_desteği}")

    # 5.11) Makine Desteği
    st.write(f"**Makine Desteği:** Yok")

    # 5.12) Asgari Yatırım Tutarı
    asgari_yatirim = "12 Milyon TL" if bolge_no in [1, 2] else "6 Milyon TL"
    st.write(f"**Asgari Yatırım Tutarı:** {asgari_yatirim}")

    # 5.13) Ekosistem Geliştirme Planı
    st.write("**Ekosistem Geliştirme Planı:** Büyük İşletme veya Yerel Kalkınma Hamlesi ise Evet.")



    # Uyarı
    st.markdown("_⚠️ Bu içerik ön bilgilendirme amaçlıdır; bağlayıcı hükümlere ulaşmak için resmi mevzuat metinlerini inceleyiniz._")

    # İlgili mevzuat metni
    st.markdown("[İlgili mevzuat metni](https://sanayi.gov.tr/mevzuat/diger/mc0403018201)")



import streamlit as st


st.title("KOSGEB ")
st.caption("Kapasite Geliştirme - Küresel Rekabetçilik için büyüme rakamları hesaplama")

with st.form("growth_form"):
    st.subheader("Veri Girişi")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**SGK Prim Gün Sayısı**")
        p2021 = st.number_input("2021", min_value=0, step=1, key="p2021")
        p2022 = st.number_input("2022", min_value=0, step=1, key="p2022")
        p2023 = st.number_input("2023", min_value=0, step=1, key="p2023")
        p2024 = st.number_input("2024", min_value=0, step=1, key="p2024")

    with c2:
        st.markdown("**Net Satış Hasılatı (TL)**")
        s2021 = st.number_input("2021 ", min_value=0, step=1000, key="s2021", format="%d")
        s2022 = st.number_input("2022 ", min_value=0, step=1000, key="s2022", format="%d")
        s2023 = st.number_input("2023 ", min_value=0, step=1000, key="s2023", format="%d")
        s2024 = st.number_input("2024 ", min_value=0, step=1000, key="s2024", format="%d")

    submitted = st.form_submit_button("Sorgula")

if submitted:
    prim_vals = [p2021, p2022, p2023, p2024]
    satis_vals_nom = [s2021, s2022, s2023, s2024]

    if not (valid_positive_numbers(prim_vals) and valid_positive_numbers(satis_vals_nom)):
        st.error("Lütfen tüm alanları 0 veya daha büyük sayılarla doldurun.")
    else:
        # Deflatör uygulanmış (reel) satışlar
        years = [2021, 2022, 2023, 2024]
        satis_vals_reel = [v / DEFLATORS[y] for y, v in zip(years, satis_vals_nom)]

        prim_cagr = cagr(p2021, p2024, 3)
        satis_cagr_reel = cagr(satis_vals_reel[0], satis_vals_reel[-1], 3)

        st.subheader("Sonuçlar")
        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Ortalama Büyüme (Prim Gün Sayısı)**")
            st.markdown(pct_style(prim_cagr), unsafe_allow_html=True)
        with colB:
            st.markdown("**Ortalama Büyüme (Net Satış Hasılatı — Reel)**")
            st.markdown(pct_style(satis_cagr_reel), unsafe_allow_html=True)

        df_show = pd.DataFrame({
            "Yıl": years,
            "Prim Gün": prim_vals,
            "Net Satış (Nominal TL)": satis_vals_nom,
            "Deflatör": [DEFLATORS[y] for y in years],
            "Net Satış (Reel TL)": satis_vals_reel,
        })

       for col in ["Prim Gün", "Net Satış (Nominal TL)", "Net Satış (Reel TL)"]:
    df_show[col] = df_show[col].apply(lambda x: f"{int(x):,}".replace(",", ".") if pd.notnull(x) else x)

        st.dataframe(df_show, hide_index=True, use_container_width=True)

        st.info(
            "Net satış reel hesaplanır: **Reel = Nominal / Deflatör**. "
            "Ortalama büyüme **CAGR**: (Reel_2024 / Reel_2021)^(1/3) - 1. "
            "Eşik: > %10 yeşil, aksi kırmızı."
        )