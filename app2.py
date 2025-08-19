İçeriğe geç
Sohbet geçmişi

Şunu dedin:
app2.py
Python
bu mevcut yazılımın anlık hali
ChatGPT:
Şu anda paylaştığınız app2.py dosyasının anlık hali şu şekilde çalışıyor:

Başlık: "Yeni YTB Teşvik Robotu" (sayfanın ortasında gösteriliyor).

Arama Alanı: Kullanıcı NACE kodunu veya konu adını yazıyor → eşleşen kodlar listeleniyor → seçilen kod doğrulanıyor.

İl / İlçe Seçimi:

İl ve ilçe seçiliyor.

OSB/Endüstri bölgesi olup olmadığı soruluyor.

Yatırımın öncelikli yatırım listesinde olup olmadığı seçiliyor.

Sorgula Butonu: Tüm seçimler tamamlandıktan sonra çalışıyor. Eksik giriş varsa hata veriyor.

Sonuçlar Bölümü:

Seçilen NACE kodu ve tanımı, il/ilçe bilgisi, bölge numarası.

Yararlanılacak bölge (ilçe, OSB ve öncelik durumuna göre hesaplanıyor).

Öncelikli/Hedef yatırım bilgisi ve varsa özel şartlar.

Teşvik destekleri:

KDV İstisnası, Gümrük Vergisi Muafiyeti, Yatırım Yeri Tahsisi

SGK İşveren ve İşçi Hissesi Destekleri

Vergi İndirimi (öncelikli/ hedef yatırım durumuna göre farklı oranlar)

Faiz Desteği (ayrıntılı üst sınır bilgisiyle)

Makine Desteği (her zaman “Yok”)

Asgari Yatırım Tutarı (bölgeye göre 12 veya 6 Milyon TL)

Ekosistem Geliştirme Planı notu

Alt kısımda uyarı ve mevzuat linki veriliyor.

Yani mevcut yazılım, NACE kodu + İl/ilçe + OSB + Öncelikli yatırım bilgilerini alıp, bölge ve teşvik hesaplamalarını yaparak tablo halinde sonuçları sunuyor.

İstersen sana bu mevcut hali üzerinden bir akış diyagramı ya da özet tablo çıkarabilirim. İster misin?

Şunu dedin:
buna ilaveler eklemem gerekiyor
ChatGPT:

18s boyunca düşündüm

Analiz duraklatıldı
Şunu dedin:
şimdi bu konu yatırım teşvik konusu, bundan bağımsız olarak başka bir hesaplama koymak istiyorum. Ekranın sol tarafında bu olsun, sağ tarafta diğer hesaplama olacak.

Buradaki hesaplamada Firmanın 2021, 2022,2023 ve 2024 için SGK Prim Gün Sayısı ve Net Satış Hasılatı (TL) olarak kullanıcıdan istenecek. Sorgula dedikten sonra Ortalama Büyüme (Prim gün sayısı) ve Ortalama Büyüme (Net Satış Hasılatı) hesaplanacak. 
Bunlar %10dan büyükse yeşil, küçükse kırmızı olacak.
 
ChatGPT:

10s boyunca düşündüm
Harika—istediğin yan paneli ekledim ve iki sütunlu yeni uygulamayı tek dosyada hazırladım. Solda mevcut Yatırım Teşvik akışın, sağda ise Ortalama Büyüme Hesaplama (2021→2024) yer alıyor. Sağ panel:

Kullanıcıdan 2021–2024 için SGK Prim Gün Sayısı ve Net Satış Hasılatı (TL) alır.

CAGR (yıllık bileşik büyüme) hesaplar: (2024 / 2021)^(1/3) − 1.

Sonuçlar >%10 yeşil, aksi kırmızı renkle gösterilir.

Girilen verileri küçük bir tabloyla da görüntüler.

Hazır dosya burada: app2_dual.py’i indir

İstersen büyüme metodunu “ortalama yıllık (aritmetik)” yapacak bir seçenek de ekleyebilirim veya renk eşiğini %15 gibi farklı bir değere ayarlayabilirim. 

Şunu dedin:
Yıllık büyümeyi net satış hasılatı için hesaplarken deflatör uygulanacak. Deflatör sabiti 2021 için 0,18852, 2022 için 0,36950. 2023 için 0,6215, 2024 için 1 olacak ve kullanıcının girdiği rakamlar bu değerlere bölünenerek hesaplanıp sonra büyüme bu rakamlar üzerindne hesaplanacak
ChatGPT:

2m 1s boyunca düşündüm
Süper, net satış hasılatı için deflatör uygulanmış büyüme hesabını sağ panele entegre ettim. Artık kullanıcı 2021–2024 nominal değerlerini giriyor; uygulama önce şu sabitlerle reel değerlere çeviriyor, sonra CAGR’ı bu reel değerler üzerinden hesaplıyor:

2021 → 0,18852

2022 → 0,36950

2023 → 0,6215

2024 → 1,00

Üretilen dosya: app2_dual_deflated.py’i indir

Ne eklendi?

Net satış hasılatı için reel tablo (nominal ve deflatörlü değerleri yan yana görebilirsin).

CAGR = (Reel_2024 / Reel_2021)^(1/3) − 1 ile hesaplanır.

%10 eşiği: > %10 yeşil, aksi kırmızı.

Açıklama kutusunda kullanılan formül ve deflatörler yazıyor.

İstersen:

Eşik değerini (%10) ayarlanabilir yapayım.

CAGR yerine aritmetik ortalama yıllık artış seçeneği ekleyeyim.

Deflatörleri bir input alanına taşıyıp gerektiğinde güncellenebilir hale getireyim.

Şunu dedin:
kanvasta kodu gösterir misin
ChatGPT:
App2 Dual Deflated
· python
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

        # Uyarı & mevzuat
        st.markdown("_⚠️ Bu içerik ön bilgilendirme amaçlıdır; bağlayıcı hükümlere ulaşmak için resmi mevzuat metinlerini inceleyiniz._")
        st.markdown("[İlgili mevzuat metni](https://sanayi.gov.tr/mevzuat/diger/mc0403018201)")

# -------------------------
# RIGHT: Büyüme Hesaplama
# -------------------------
with right:
    st.title("Ortalama Büyüme Hesaplama (2021→2024)")
    st.caption("SGK Prim Gün Sayısı ve Net Satış Hasılatı için **yıllık bileşik büyüme oranı (CAGR)** hesaplanır. >%10 yeşil, aksi kırmızı.")

    with st.form("growth_form"):
        st.subheader("Veri Girişi")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**SGK Prim Gün Sayısı**")
            p2021 = st.number_input("2021", min_value=0.0, step=1.0, key="p2021")
            p2022 = st.number_input("2022", min_value=0.0, step=1.0, key="p2022")
            p2023 = st.number_input("2023", min_value=0.0, step=1.0, key="p2023")
            p2024 = st.number_input("2024", min_value=0.0, step=1.0, key="p2024")

        with c2:
            st.markdown("**Net Satış Hasılatı (TL)**")
            s2021 = st.number_input("2021 ", min_value=0.0, step=1000.0, key="s2021", format="%.2f")
            s2022 = st.number_input("2022 ", min_value=0.0, step=1000.0, key="s2022", format="%.2f")
            s2023 = st.number_input("2023 ", min_value=0.0, step=1000.0, key="s2023", format="%.2f")
            s2024 = st.number_input("2024 ", min_value=0.0, step=1000.0, key="s2024", format="%.2f")

        submitted = st.form_submit_button("Sorgula")

    if submitted:
        # doğrulama
        prim_vals = [p2021, p2022, p2023, p2024]
        satis_vals_nom = [s2021, s2022, s2023, s2024]

        if not (valid_positive_numbers(prim_vals) and valid_positive_numbers(satis_vals_nom)):
            st.error("Lütfen tüm alanları 0 veya daha büyük sayılarla doldurun.")
        else:
            # Deflatör uygulanmış (reel) satışlar
            satis_vals_reel = []
            years = [2021, 2022, 2023, 2024]
            for y, v in zip(years, satis_vals_nom):
                d = DEFLATORS.get(y, 1.0)
                try:
                    satis_vals_reel.append(v / d if d and d > 0 else float("nan"))
                except Exception:
                    satis_vals_reel.append(float("nan"))

            # CAGR (3 yıl aralık: 2021→2024)
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

            # Bilgi amaçlı tablo (Nominal vs Reel)
            df_show = pd.DataFrame({
                "Yıl": years,
                "Prim Gün": prim_vals,
                "Net Satış (Nominal TL)": satis_vals_nom,
                "Deflatör": [DEFLATORS[y] for y in years],
Hazır! Kodu kanvasa yerleştirdim. Sağdaki editörde app2_dual_deflated.py dosyasını görebilirsin ve üzerinde oynayabilirsin.

Şunu dedin:
sadece ekstra eklenecekleri yazar mısın
ChatGPT:

14s boyunca düşündüm
Tabii. Mevcut sol panel/Yatırım Teşvik akışına dokunmadan, sadece eklemeniz gereken parçalar aşağıdaki gibi. (Kopyala‑yapıştır için bölümlendirdim.)

1) Yardımcılar (dosyanın üst kısımlarına, import’ların altına ekleyin)
import pandas as pd  # varsa tekrar eklemeyin

def cagr(v_start: float, v_end: float, years: int) -> float:
    """Yıllık bileşik büyüme (CAGR)"""
    try:
        if v_start <= 0 or v_end <= 0 or years <= 0:
            return float("nan")
        return (v_end / v_start) ** (1.0 / years) - 1.0
    except Exception:
        return float("nan")

def pct_style(value: float) -> str:
    """>%10 yeşil, aksi kırmızı yazı döndürür (HTML)"""
    if pd.isna(value):
        return '<span style="color:#666">—</span>'
    color = "#069f3c" if value > 0.10 else "#c62828"
    return f'<span style="color:{color}; font-weight:700">{value*100:.2f}%</span>'

def valid_positive_numbers(vals):
    try:
        return all(float(v) >= 0 for v in vals)
    except Exception:
        return False

# Net satış hasılatı için deflatör sabitleri
DEFLATORS = {
    2021: 0.18852,
    2022: 0.36950,
    2023: 0.6215,
    2024: 1.0,
}
2) İki sütun düzeni (sol mevcut kod, sağ yeni hesaplama)
Mevcut içeriğiniz sol sütunda kalsın. Eğer hâlâ tek sütundaysa, en üste şunu ekleyip sol içeriği with left: bloğuna alın:

left, right = st.columns([1, 1], gap="large")

with left:
    # ← mevcut Yatırım Teşvik akışınız buraya
    ...
3) SAĞ panel: “Ortalama Büyüme Hesaplama” (dosyanın sonuna ekleyin)
with right:
    st.title("Ortalama Büyüme Hesaplama (2021→2024)")
    st.caption("SGK Prim Gün Sayısı ve Net Satış Hasılatı için CAGR hesaplanır. >%10 yeşil, aksi kırmızı.")

    with st.form("growth_form"):
        st.subheader("Veri Girişi")
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**SGK Prim Gün Sayısı**")
            p2021 = st.number_input("2021", min_value=0.0, step=1.0, key="p2021")
            p2022 = st.number_input("2022", min_value=0.0, step=1.0, key="p2022")
            p2023 = st.number_input("2023", min_value=0.0, step=1.0, key="p2023")
            p2024 = st.number_input("2024", min_value=0.0, step=1.0, key="p2024")

        with c2:
            st.markdown("**Net Satış Hasılatı (TL)**")
            s2021 = st.number_input("2021 ", min_value=0.0, step=1000.0, key="s2021", format="%.2f")
            s2022 = st.number_input("2022 ", min_value=0.0, step=1000.0, key="s2022", format="%.2f")
            s2023 = st.number_input("2023 ", min_value=0.0, step=1000.0, key="s2023", format="%.2f")
            s2024 = st.number_input("2024 ", min_value=0.0, step=1000.0, key="s2024", format="%.2f")

        submitted = st.form_submit_button("Sorgula")

    if submitted:
        prim_vals = [p2021, p2022, p2023, p2024]
        satis_vals_nom = [s2021, s2022, s2023, s2024]

        if not (valid_positive_numbers(prim_vals) and valid_positive_numbers(satis_vals_nom)):
            st.error("Lütfen tüm alanları 0 veya daha büyük sayılarla doldurun.")
        else:
            # Nominal → Reel (deflatörle düzeltilmiş)
            years = [2021, 2022, 2023, 2024]
            satis_vals_reel = []
            for y, v in zip(years, satis_vals_nom):
                d = DEFLATORS.get(y, 1.0)
                satis_vals_reel.append(v / d if d and d > 0 else float("nan"))

            # CAGR (2021→2024 = 3 yıl)
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

            # Bilgi tablosu (Nominal vs Reel)
            df_show = pd.DataFrame({
                "Yıl": years,
                "Prim Gün": prim_vals,
                "Net Satış (Nominal TL)": satis_vals_nom,
                "Deflatör": [DEFLATORS[y] for y in years],
                "Net Satış (Reel TL)": satis_vals_reel,
            })
            st.dataframe(df_show, hide_index=True, use_container_width=True)

            st.info(
                "Net satış reel hesaplanır: **Reel = Nominal / Deflatör**. "
                "Ortalama büyüme **CAGR**: (Reel_2024 / Reel_2021)^(1/3) - 1. "
                "Eşik: > %10 yeşil, aksi kırmızı."
            )
Notlar

Eşik değerini değiştirmek isterseniz pct_style içindeki 0.10 değerini güncellemeniz yeterli.

Deflatörler sabit sözlükte (DEFLATORS) tanımlı; ihtiyaç olursa kullanıcı girişine de açabiliriz.




Dosya seçilmediDosya seçilmedi
ChatGPT hata yapabilir. Önemli bilgileri kontrol edin.
