import pandas as pd
from io import StringIO

data = """İl,İlçe
Adanam,Aladağ
Adana,Feke
Adana,İmamoğlu
Adana,Karaisalı
Adana,Karataş
Adana,Pozantı
Adana,Saimbeyli
Adana,Tufanbeyli
Adana,Yumurtalık
Afyonkarahisar,Bayat
Afyonkarahisar,Çobanlar
Afyonkarahisar,Evciler
Afyonkarahisar,Hocalar
Afyonkarahisar,İhsaniye
Afyonkarahisar,Kızılören
Afyonkarahisar,Sinanpaşa
Aksaray,Ağaçören
Aksaray,Eskil
Aksaray,Gülağaç
Aksaray,Güzelyurt
Aksaray,Sultanhanı
Amasya,Göynücek
Amasya,Hamamözü
Ankara,Bala
Ankara,Çamlıdere
Ankara,Evren
Ankara,Güdül
Ankara,Haymana
Ankara,Kalecik
Antalya,Akseki
Antalya,Gündoğmuş
Antalya,İbradı
Aydın,Bozdoğan
Aydın,Buharkent
Aydın,Germencik
Aydın,Karacasu
Aydın,Karpuzlu
Aydın,Koçarlı
Aydın,Köşk
Aydın,Kuyucak
Aydın,Sultanhisar
Aydın,Yenipazar
Balıkesir,Balya
Balıkesir,Dursunbey
Balıkesir,Havran
Balıkesir,İvrindi
Balıkesir,Kepsut
Balıkesir,Manyas
Balıkesir,Savaştepe
Balıkesir,Sındırgı
Bilecik,Gölpazarı
Bilecik,İnhisar
Bilecik,Pazaryeri
Bilecik,Yenipazar
Bolu,Dörtdivan
Bolu,Göynük
Bolu,Kıbrıscık
Bolu,Mengen
Bolu,Mudurnu
Bolu,Seben
Burdur,Ağlasun
Burdur,Altınyayla
Burdur,Çavdır
Burdur,Çeltikçi
Burdur,Kemer
Burdur,Tefenni
Burdur,Yeşilova
Bursa,Büyükorhan
Bursa,Harmancık
Bursa,Keles
Bursa,Orhaneli
Çanakkale,Bayramiç
Çanakkale,Yenice
Çankırı,Bayramören
Çankırı,Yapraklı
Çorum,Bayat
Çorum,Boğazkale
Çorum,Dodurga
Çorum,Kargı
Çorum,Laçin
Çorum,Mecitözü
Çorum,Oğuzlar
Çorum,Ortaköy
Çorum,Uğurludağ
Denizli,Babadağ
Denizli,Baklan
Denizli,Bekilli
Denizli,Beyağaç
Denizli,Bozkurt
Denizli,Çal
Denizli,Çameli
Denizli,Çardak
Denizli,Güney
Denizli,Kale
Düzce,Cumayeri
Düzce,Çilimli
Düzce,Gölyaka
Düzce,Yığılca
Edirne,Enez
Edirne,Havsa
Edirne,İpsala
Edirne,Lalapaşa
Edirne,Meriç
Edirne,Süloğlu
Elazığ,Ağın
Erzincan,Çayırlı
Erzincan,Kemah
Erzincan,Otlukbeli
Erzincan,Tercan
Erzincan,Üzümlü
Erzurum,Çat
Erzurum,Hınıs
Erzurum,Karaçoban
Erzurum,Karayazı
Erzurum,Köprüköy
Erzurum,Şenkaya
Erzurum,Tekman
Eskişehir,Alpu
Eskişehir,Beylikova
Eskişehir,Çifteler
Eskişehir,Günyüzü
Eskişehir,Han
Eskişehir,Mahmudiye
Eskişehir,Mihalgazi
Eskişehir,Mihalıççık
Eskişehir,Sarıcakaya
Eskişehir,Seyitgazi
Gaziantep,Karkamış
Gaziantep,Oğuzeli
Gaziantep,Yavuzeli
Giresun,Çamoluk
Isparta,Aksu
Isparta,Atabey
Isparta,Gelendost
Isparta,Senirkent
Isparta,Sütçüler
Isparta,Şarkikaraağaç
Isparta,Yenişarbademli
İzmir,Bayındır
İzmir,Beydağ
İzmir,Kınık
İzmir,Kiraz
Karabük,Eflani
Karabük,Eskipazar
Karabük,Ovacık
Karabük,Yenice
Karaman,Ayrancı
Karaman,Başyayla
Karaman,Ermenek
Karaman,Sarıveliler
Kastamonu,Ağlı
Kastamonu,Araç
Kastamonu,Cide
Kastamonu,Doğanyurt
Kastamonu,Küre
Kastamonu,Pınarbaşı
Kastamonu,Şenpazar
Kayseri,Akkışla
Kayseri,Bünyan
Kayseri,Felahiye
Kayseri,İncesu
Kayseri,Özvatan
Kayseri,Pınarbaşı
Kayseri,Sarıoğlan
Kayseri,Sarız
Kayseri,Tomarza
Kayseri,Yahyalı
Kayseri,Yeşilhisar
Kırıkkale,Balışeyh
Kırıkkale,Çelebi
Kırıkkale,Delice
Kırıkkale,Karakeçili
Kırıkkale,Keskin
Kırıkkale,Sulakyurt
Kırklareli,Demirköy
Kırklareli,Kofçaz
Kırklareli,Pehlivanköy
Kırşehir,Akçakent
Kırşehir,Akpınar
Kırşehir,Boztepe
Kırşehir,Çiçekdağı
Kilis,Elbeyli
Kocaeli,Kandıra
Konya,Ahırlı
Konya,Akören
Konya,Altınekin
Konya,Bozkır
Konya,Çeltik
Konya,Çumra
Konya,Derbent
Konya,Derebucak
Konya,Doğanhisar
Konya,Emirgazi
Konya,Güneysınır
Konya,Hadim
Konya,Halkapınar
Konya,Hüyük
Konya,Kadınhanı
Konya,Sarayönü
Konya,Taşkent
Konya,Tuzlukçu
Konya,Yalıhüyük
Konya,Yunak
Kütahya,Altıntaş
Kütahya,Aslanapa
Kütahya,Çavdarhisar
Kütahya,Domaniç
Kütahya,Dumlupınar
Kütahya,Emet
Kütahya,Hisarcık
Kütahya,Pazarlar
Kütahya,Şaphane
Manisa,Ahmetli
Manisa,Demirci
Manisa,Gölmarmara
Manisa,Gördes
Manisa,Kırkağaç
Manisa,Köprübaşı
Manisa,Sarıgöl
Manisa,Saruhanlı
Manisa,Selendi
Mersin,Aydıncık
Mersin,Bozyazı
Mersin,Çamlıyayla
Mersin,Gülnar
Mersin,Mut
Muğla,Kavaklıdere
Muğla,Seydikemer
Nevşehir,Acıgöl
Nevşehir,Derinkuyu
Nevşehir,Gülşehir
Nevşehir,Hacıbektaş
Niğde,Altunhisar
Niğde,Çiftlik
Ordu,Akkuş
Ordu,Çatalpınar
Ordu,Çaybaşı
Ordu,Gürgentepe
Ordu,İkizce
Ordu,Mesudiye
Osmaniye,Sumbas
Rize,Çamlıhemşin
Rize,Derepazarı
Rize,Güneysu
Rize,Hemşin
Rize,İkizdere
Rize,İyidere
Rize,Kalkandere
Sakarya,Karapürçek
Sakarya,Kaynarca
Sakarya,Kocaali
Sakarya,Taraklı
Samsun,Alaçam
Samsun,Asarcık
Samsun,Ayvacık
Samsun,Kavak
Samsun,Ladik
Samsun,Salıpazarı
Samsun,Terme
Samsun,Vezirköprü
Samsun,Yakakent
Sinop,Dikmen
Sivas,Akıncılar
Sivas,Altınyayla
Sivas,Doğanşar
Sivas,Gölova
Sivas,Hafik
Sivas,İmranlı
Sivas,Koyulhisar
Sivas,Ulaş
Sivas,Yıldızeli
Tekirdağ,Hayrabolu
Tokat,Başçiftlik
Tokat,Sulusaray
Trabzon,Araklı
Trabzon,Çarşıbaşı
Trabzon,Dernekpazarı
Trabzon,Düzköy
Trabzon,Hayrat
Trabzon,Köprübaşı
Trabzon,Şalpazarı
Trabzon,Tonya
Uşak,Banaz
Uşak,Karahallı
Uşak,Sivaslı
Uşak,Ulubey
Yozgat,Aydıncık
Yozgat,Kadışehri
Zonguldak,Kilimli
Adana,Diğer İlçeler
Adıyaman,Tüm İlçeler
Afyonkarahisar,Diğer İlçeler
Ağrı,Tüm İlçeler
Aksaray,Diğer İlçeler
Amasya,Diğer İlçeler
Ankara,Diğer İlçeler
Antalya,Diğer İlçeler
Ardahan,Tüm İlçeler
Artvin,Tüm İlçeler
Aydın,Diğer İlçeler
Balıkesir,Diğer İlçeler
Bartın,Tüm İlçeler
Batman,Tüm İlçeler
Bayburt,Tüm İlçeler
Bilecik,Diğer İlçeler
Bingöl,Tüm İlçeler
Bitlis,Tüm İlçeler
Bolu,Diğer İlçeler
Burdur,Diğer İlçeler
Bursa,Diğer İlçeler
Çanakkale,Diğer İlçeler
Çankırı,Diğer İlçeler
Çorum,Diğer İlçeler
Denizli,Diğer İlçeler
Diyarbakır,Tüm İlçeler
Düzce,Diğer İlçeler
Edirne,Diğer İlçeler
Elazığ,Diğer İlçeler
Erzincan,Diğer İlçeler
Erzurum,Diğer İlçeler
Eskişehir,Diğer İlçeler
Gaziantep,Diğer İlçeler
Giresun,Diğer İlçeler
Gümüşhane,Tüm İlçeler
Hakkari,Tüm İlçeler
Hatay,Tüm İlçeler
Iğdır,Tüm İlçeler
Isparta,Diğer İlçeler
İstanbul,Tüm İlçeler
İzmir,Diğer İlçeler
Kahramanmaraş,Tüm İlçeler
Karabük,Diğer İlçeler
Karaman,Diğer İlçeler
Kars,Tüm İlçeler
Kastamonu,Diğer İlçeler
Kayseri,Diğer İlçeler
Kırıkkale,Diğer İlçeler
Kırklareli,Diğer İlçeler
Kırşehir,Diğer İlçeler
Kilis,Diğer İlçeler
Kocaeli,Diğer İlçeler
Konya,Diğer İlçeler
Kütahya,Diğer İlçeler
Malatya,Diğer İlçeler
Manisa,Diğer İlçeler
Mardin,Tüm İlçeler
Mersin,Diğer İlçeler
Muğla,Diğer İlçeler
Muş,Tüm İlçeler
Nevşehir,Diğer İlçeler
Niğde,Diğer İlçeler
Ordu,Diğer İlçeler
Osmaniye,Diğer İlçeler
Rize,Diğer İlçeler
Sakarya,Diğer İlçeler
Samsun,Diğer İlçeler
Siirt,Tüm İlçeler
Sinop,Diğer İlçeler
Sivas,Diğer İlçeler
Şanlıurfa,Tüm İlçeler
Şırnak,Tüm İlçeler
Tekirdağ,Diğer İlçeler
Tokat,Diğer İlçeler
Trabzon,Diğer İlçeler
Tunceli,Tüm İlçeler
Uşak,Diğer İlçeler
Van,Tüm İlçeler
Yalova,Tüm İlçeler
Yozgat,Diğer İlçeler
Zonguldak,Diğer İlçeler"""

df_il_ilce = pd.read_csv(StringIO(data))
