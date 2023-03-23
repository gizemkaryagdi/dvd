import sqlite3

con = sqlite3.connect("dvd_project.db")
cursor = con.cursor()

def bitirici():
    con.commit()
    con.close()

cursor.execute("CREATE TABLE IF NOT EXISTS urunler(urun_ID INT PRIMARY KEY,urun_adi TEXT,urun_turu TEXT,urun_gunluk_fiyat INT,urun_tipi TEXT,urun_durum TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS siparisler(musteri_mail TEXT,siparis_adres TEXT,kiralanan_gun INT, siparis_tarihi INT, urun_ID INT,siparis_id INT PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS musteriler(musteri_ad_soyad TEXT,musteri_sifre TEXT,musteri_tel_no INT,musteri_adres TEXT,musteri_mail TEXT PRIMARY KEY)")

while True :

    print('''
    1 - Müşteri Menüsü
    2 - DVD Menüsü
    3 - Sipariş Menüsü
    0 - Çıkış
    ''')
    islem=int(input("Yapmak istediğiniz işlemi seçiniz: "))

    if islem == 1 :
        
        while True :

            print('''
            1 - Müşteri Oluştur
            2 - Müşteri Sil
            3 - Müşteri Bul
            0 - Çıkış
            ''')
            islem = int(input("Yapmak istediğiniz işlemi seçiniz: "))
            

            if islem == 1 :

                musteri_ad_soyad=input("Adınız Soyadınız: ")
                musteri_sifre=input("Şifreniz: ")
                musteri_tel_no=input("Telefon Numaranız: ")
                musteri_adres=input("Adresiniz: ")
                musteri_mail=input("Mailiniz: ")
                kisi_veri=[(musteri_ad_soyad,musteri_sifre,musteri_tel_no,musteri_adres,musteri_mail)]
                print("Müşteri Başarıyla Eklendi.")
                for i in kisi_veri:
                    cursor.execute("INSERT INTO musteriler VALUES(?,?,?,?,?)",i)
                con.commit()
                

            elif islem == 2 : 

                musteri_mail=input("Silinecek müşterinin mail adresini giriniz : ")
                try:
                  cursor.execute("DELETE FROM musteriler WHERE musteri_mail = ?",(musteri_mail,))
                  con.commit()
                  print("Silme işlemi başarılı.")
                except:
                  print("Silinecek kişi bulunamadı.")


            elif islem == 3 : 

                musteri_mail = input("Bulunacak Müşteri'nin Mail'ini giriniz : ")
                cursor.execute("Select * from musteriler")
                data = cursor.fetchall()
                sayac = 0
                for c in data :
                    if c[4] == musteri_mail :
                        sayac += 1
                        print(c)
                
                if sayac == 0 :
                    print('Mail kayıtlı değil veya hatalı girilmiş ..')
                

            elif islem == 0 : 

                sorgu=input("Müşteri ekranından çıkmak istediğinize emin misiniz (E/H) ?:")

                if sorgu=='E':
                  print("Müşteri ekranından çıkıldı.")
                  break
                  
                else:
                  print("Panele yönlendiriliyorsunuz.")



    elif islem == 2 : 
    
        while True :
            
            print('''
            1 - DVD Ekle
            2 - DVD Sil
            3 - DVD leri Göster
            4 - DVD Bul
            0 - Çıkış
            ''')
            islem = int(input("Yapmak istediğiniz işlemi seçiniz: "))
            
            if islem == 1 :

                urun_ID=int(input("Ürün ID:"))
                urun_adi=input("Ürün Adı:")
                urun_turu=input("Ürün Türü:")
                urun_gunluk_fiyat=input("Ürünün Günlük Fiyatı:")
                urun_tipi=input("Ürün Tipi:")
                urun_durum=input("Ürünün Durumu:")
                try:
                    cursor.execute('INSERT INTO urunler Values(?,?,?,?,?,?)',(urun_ID,urun_adi,urun_turu,urun_gunluk_fiyat,urun_tipi,urun_durum))
                    con.commit()
                    print("DVD başarıyla eklendi.")
                except sqlite3.IntegrityError:
                    print("Aynı DVD'den stokta mevcut.")
            
            
            elif islem == 2 : 

                urun_ID=int(input("Silmek istediğiniz ürün ID:"))
                cursor.execute("DELETE FROM urunler WHERE urun_ID=?",[urun_ID])
                con.commit()
                print("Silme işleminiz başarıyla tamanlandı.")

            
            elif islem == 3 : 

                cursor.execute("SELECT * FROM urunler")
                data=cursor.fetchall()
                for i in data:
                  print("Aradığınız DVD'nin bilgileri : ",i)  

            
            elif islem == 4 :

                dvd_ad = input('Aratılacak olan DVD nin adını giriniz: ')
                cursor.execute('SELECT * FROM urunler')
                data = cursor.fetchall()
                sayac = 0
                for i in data :
                    if i[1] == dvd_ad:
                        sayac += 1
                        print(i)
                
                if sayac == 0 :
                    print('Aradığınız DVD bulunamadı.')
                    
            
            elif islem == 0 : 

                print("DVD ekranından çıkmak istiyor musunuz?")
                cevap=input("Emin misiniz?(E/H)")

                if cevap=="E":
                    print("Programdan çıkılıyor..")
                    break

                else:
                    print("Program çıkışı reddedildi..")



    elif islem == 3 : 
    
        def urun_durumu_degistir():
            a = input("Durumunu değiştirmek istediğiniz ürünün ID'sini giriniz = ")
            b = input("Durumu nasıl değiştirelim (-- Stokta / Stokta_degil --  =)")
            cursor.execute("UPDATE urunler SET urun_durum = ? WHERE urun_durum = ?",(b,a))
            print("Ürün durumu {} olarak degistirildi".format(b))
                
        while True :

            print('''
            1 - Sipariş Oluştur
            2 - Siparişleri Görüntüle
            3 - Sipariş Durum Değiştir
            0 - Çıkış
            ''')
            islem = int(input("Yapmak istediğiniz işlemi seçiniz: "))
            
            if islem == 1 : 
                cursor.execute('SELECT * FROM siparisler')
                data = cursor.fetchall()
                sayac = 0
                for i in data:
                    sayac += 1
                print("Toplam sipariş sayınız {}.".format(sayac))
                siparis_id = sayac+1
                musteri_mail=input("E-posta adresinizi giriniz : ")
                siparis_adres=input("Sipariş adresinizi giriniz : ")
                kiralanan_gun=input("Kaç gün kiralamak istiyorsunuz ?")
                siparis_tarih=input("Sipariş tarihini giriniz : ")
                urun_id=int(input("Eklenecek DVD'nin ID'sini giriniz : "))
                try:              
                    cursor.execute("INSERT INTO siparisler VALUES(?,?,?,?,?,?)",(musteri_mail,siparis_adres,kiralanan_gun,siparis_tarih,urun_id,siparis_id))
                    print("Sipariş başarıyla oluşturuldu.")
                except:
                    print("Sipariş alınmadı bir hata oluştu.") 
                        
            
            elif islem == 2:
            
                 cursor.execute("SELECT * FROM siparisler")
                 data=cursor.fetchall()
                 for i in data:
                    print("Sipariş durumu : ",i)
            

            elif islem==3:
                urun_durumu_degistir()  
              
                
            elif islem == 0:

                print("Sipariş ekranından çıkmak istiyor musunuz?")
                cevap=input("Emin misiniz?(E/H)")

                if cevap=="E":
                    print("Programdan çıkılıyor..")
                    break
                else:
                     print("Program çıkışı reddedildi..")



    elif islem == 0 : 

        print("Programdan çıkmak istiyor musunuz?")
        cevap=input("Emin misiniz?(E/H) :")

        if cevap=="E":
            print("Programdan çıkılıyor..")
            bitirici()
            break
        
        else:
            print("Program çıkışı reddedildi..")