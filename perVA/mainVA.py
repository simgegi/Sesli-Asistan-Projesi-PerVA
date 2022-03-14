# -*- coding: utf-8 -*-




import urllib.request
import urllib3
import wmi
from currency_converter import CurrencyConverter
import speech_recognition as sr
from datetime import datetime
import webbrowser
from gtts import gTTS
from playsound import playsound
import time
import os
import wikipedia
import random
import pyowm
import re
import locale
import requests as req
import pyautogui
import psutil



urllib3.disable_warnings()
locale.setlocale(locale.LC_CTYPE, 'turkish')



'''tts'''

def answer(text):
    print("Asistan:" + text)
    aud = gTTS(text=text, lang="tr", lang_check=True)
    k = random.randint(1, 25000)
    aud_file = str(k) + "ses.mp3"
    aud.save(aud_file)
    playsound(aud_file)
    os.remove(aud_file)



'''stt'''

def speak():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=8)
        print("...")
    try:
        voice = r.recognize_google(audio, language="tr-TR")
        print("Siz: " + voice)
    except sr.UnknownValueError:
        answer("Söylediğiniz şeyi anlayamadım. Lütfen tekrar deneyin.")
        voice = speak()
    return voice



'''fonks'''


def greet():
    answer_greet = ["Senin için ne yapmamı istersin?", "Nasıl gidiyor?",
                    "Seni gördüğüme sevindim."]
    greet = answer_greet[random.randint(0, len(answer_greet) - 1)]
    current_time = int(datetime.now().hour)
    if current_time<12 and current_time>=0:
        answer("Günaydın. " + greet)
    if current_time>=12 and current_time<18:
        answer("İyi günler. " + greet)
    if current_time>=18 and current_time<21:
        answer("İyi akşamlar. " + greet)
    if current_time>=20 and current_time!=0:
        answer("İyi geceler. " + greet)
    else:
        answer(greet)



def time_t():
    locale.setlocale(locale.LC_CTYPE, 'turkish')
    now_time = datetime.now().strftime('%H:%M:%S')
    answer(str(now_time))


def search_g():
    searchFor = voice
    url = "https://google.com/search?q=" + searchFor
    webbrowser.get().open(url)
    answer(searchFor + "için bulduklarım")


def name():
    answer_name = ["Ben Perva, PERsonal Voice Assistant", "Adım Perva, tanıştığıma sevindim.",
                   "Adım Perva ve sana yardımcı olmak için yaratıldım"]
    name_ans = answer_name[random.randint(0, len(answer_name) - 1)]
    answer(name_ans)

def operation():
    hesap = str(voice)
    opr = hesap.split()[0]
    answer(opr)

def youtube():

    ans_yt = ["Hemen açıyorum", "Youtube açılıyor", "Açtım bile."]
    tube = ans_yt[random.randint(0, len(ans_yt) - 1)]
    answer(tube)
    webbrowser.open("https://www.youtube.com.tr")


def today():
    locale.setlocale(locale.LC_ALL, 'turkish')
    day_tdy = datetime.today().now().strftime("%B %d %A")
    answer("Bugün günlerden: ")
    print (day_tdy)



def wiki():
    language = "tr"
    wikipedia.set_lang(language)
    info = wikipedia.summary(voice, sentences=2)
    answer(info + "için bulduğum sonuçlar")
    print(info)


def harita():
    answer("Harita açılıyor")
    webbrowser.open('https://www.google.com/maps')


def loc():
    location = voice.replace("nerede", "")
    answer(location + "konumu bulunuyor.")
    webbrowser.open("https://www.google.nl/maps/place/" + location + "/&amp;")


def netflix():
    answer("Netflix açılıyor")
    webbrowser.open("https://www.netflix.com/")

def notes():
    answer("Lütfen notunuza ne yazmak istediğinizi söyleyin.")
    notes1 = open("AssistantNotes.txt", 'a')
    note = speak()
    notes1.write(note + "\n")
    notes1.close()
    answer("Notunuz alındı.")
    x = open

def translate():
    if "kelimesini çevir" in voice or "cümlesini çevir":
        trns_b = voice.replace("kelimesini çevir" or "cümlesini çevir", "")
        answer("Çeviri yapılıyor")
        webbrowser.open("https://www.google.com/search?q=" + trns_b + "+%C3%A7evir&ei=")
    else:
        answer("Çevirmek istediğiniz cümleyi söyleyin.")
        trns = speak()
        answer("çeviri yapılıyor")
        webbrowser.open("https://www.google.com/search?q=" + trns + "+%C3%A7evir&ei=")

def currency():
     cr = CurrencyConverter()
     answer("Kaç birim parayı çevirmek istiyorsunuz?")
     val = speak()
     answer("Hangi para biriminden çevirmek istiyorsunuz")
     first_cr = speak()
     if "dolar" in first_cr:
         first_cr = "USD"
     elif "euro" in first_cr:
         first_cr = "EUR"
     elif "pound" in first_cr or "sterlin" in first_cr:
         first_cr = "GBP"
     elif "japon yeni" in first_cr:
         first_cr = "JPY"
     elif "tele" in first_cr or "türk lirası" in first_cr:
         first_cr = "TRY"
     else:
         answer("Geçersiz para birimi")
         return False

     answer("Hangi para birimine çevirmek istiyorsunuz")
     last_cr = speak()
     if "dolar" in last_cr:
         last_cr = "USD"
     elif "euro" in last_cr:
         last_cr = "EUR"
     elif "pound" in last_cr or "sterlin" in last_cr:
         last_cr = "GBP"
     elif "yen" in last_cr:
         last_cr = "JPY"
     elif "tele" in last_cr or "Türk lirası" in last_cr:
         last_cr= "TRY"
     else:
         answer("Geçersiz para birimi")
         return False

     answer("Sonuç=")
     print(cr.convert(val, first_cr, last_cr))


def weather():
    wth = pyowm.OWM("Api key") #Pyowm sitesine üye olup aldığınız api key'i tırnak içine yazmanız gerekiyor
    answer("Neresi için hava durumunu öğrenmek istiyorsun?")
    place = speak()

    loc_own = wth.weather_manager().weather_at_place("{}, TR".format(place))
    wth_loc = loc_own.weather
    wth_temp = int(wth_loc.temperature("celsius")["temp"])
    wth_wind = int(wth_loc.wind()["speed"])

    answer("Bugün "+place+" için hava " + str(wth_temp) + " derece")
    answer("Rüzgar " + str(wth_wind) + " kilometre hızında")


def weather_b():
    wth = pyowm.OWM("Api key")
    answer("Bugün hangi bölgelerde takılacaksın?")
    place = speak()

    loc_own = wth.weather_manager().weather_at_place("{}, TR".format(place))
    wth_loc = loc_own.get_weather()
    wth_temp = int(wth_loc.get_temperature("celsius")["temp"])
    if wth_temp<0:
        answer("Bugün " +place+" bölgesinde hava buz gibi. Sıkı giyinsen iyi edersin.")
    elif wth_temp>0 and wth_temp<10:
        answer("Bugün "+place+" bölgesinde hava soğuk gibi duruyor. Biraz dikkat et giydiklerine de üşütme.")
    elif wth_temp>10 and wth_temp<20:
        answer("Bugün "+place+" bölgesinde hava fena değil. Bahar gelmiş diyebiliriz! Ona göre giyinebilirsin.")
    else:
        answer("Bugün "+place+" "+place+" değil Miami sanki. Tam efil efil giyinmelik.")


def music_yt():
    song = voice
    song = voice.replace("dinle", "")
    song.encode('ascii', 'replace')
    new_song = song.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + new_song)
    video_ids = re.findall("watch\?v=(\S{11})", html.read().decode("UTF-8"))
    webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])

def full():
    pyautogui.hotkey("f")

def pause():
    pyautogui.hotkey("playpause")

def remember():
    note = voice.replace("aklında tut","")
    notes1 = open("Rememberme.txt", 'a')
    notes1.write(note + "\n")
    notes1.close()
    answer("Kaydettim. Hatırlatmamı istediğinde ''hatırlat'' demen yeterli")

def ret_remember():
    notes1 = open("Rememberme.txt", "r")
    answer(notes1.read())

def scholar():
    mak = voice.replace("makale", "")
    url_mak = 'http://google.com/search?q=' + mak
    answer(mak + "hakkında makaleler için bulunanlar")
    webbrowser.open(url_mak)

def my_loc():
    url_myloc = "https://www.google.com/maps/search/Where+am+I+?/"
    answer("Konumunuz bulunuyor.")
    webbrowser.open(url_myloc)

def paint():
    answer("Paint açılıyor.")
    os.startfile("c:\Windows\System32\mspaint.exe")

def calc():
    answer("Hesap makinesi açılıyor")
    os.startfile("C:\Windows\System32\calc.exe")

def my_name():
    f_name = ["Memnun oldum", "Artık arkadaş sayılırız", "Vay ne güzel isim"]
    r_name = f_name[random.randint(0, len(f_name) - 1)]
    answer(r_name)

def news_r(info):
        for i in range(0, 3):
            news = info["articles"][i]["title"]
            x = i + 1
            x = str(x)
            answer(x + ".) " + news)

def news():
        url = 'http://newsapi.org/v2/top-headlines?country=tr&apiKey=APIKEY' #APIKEY yazan yerde siteye üye olup alınan api key yazılmalı
        news = req.get(url)
        info = news.json()
        answer("Bugünün gündemleri:")
        news_r(info)

def battery():
    batt = psutil.sensors_battery().percent
    batt = str(batt)
    answer("Şarjınız %" + batt)

def screen_shot():
    pic = pyautogui.screenshot()
    k = random.randint(1, 50000)
    pic_save = "py" + str(k) + "screenshot.png"
    pic.save(pic_save)
    answer("Ekran görüntüsü alındı.")

def sound_down():
        answer("Sesi biraz mı çok mu azaltmamı istersin?")
        sound = speak()
        if "biraz" in sound:
            for i in range(1, 10):
                pyautogui.hotkey("volumedown")
        elif "çok" in sound:
            for i in range(1, 30):
                pyautogui.hotkey("volumedown")

def sound_up():
    answer("Sesi biraz mı çok mu arttırmamı istersin?")
    sound = speak()
    if "biraz" in sound:
        for i in range(1, 10):
            pyautogui.hotkey("volumeup")
    elif "çok" in sound:
        for i in range(1, 30):
            pyautogui.hotkey("volumeup")

def brght_up():
    brightness = 0
    answer("Çok mu arttırmamı istersiniz az mı?")
    brg = speak()
    if "çok" in brg:
        brightness = 100
    if "az" in brg:
        brightness = 70
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(brightness, 0)

def brght_down():
    brightness = 0
    answer("Çok mu düşürmemi istersiniz az mı?")
    brg = speak()
    if "çok" in brg:
        brightness = 10
    if "az" in brg:
        brightness = 30
    c = wmi.WMI(namespace='wmi')
    methods = c.WmiMonitorBrightnessMethods()[0]
    methods.WmiSetBrightness(brightness, 0)

def dialog_a():
    dia_ans = ["İyiyim, sana yardımcı olabilirsem daha da iyi olacağım.", "Hayat buralarda sakin.", "Sorduğun için teşekkürler. Her şey tıkırında.", "Ben gayet iyiyim. İsteklerini yerine getirmek için bekliyorum."]
    dia_rand = dia_ans[random.randint(0,len(dia_ans)-1)]
    answer(dia_rand)





def response(voice):
    if "Merhaba" in voice or "Açıl" in voice or "Selam" in voice or "merhaba" in voice or "açıl" in voice or "selam" in voice or "hey" in voice or "Hey" in voice:
        greet()

    elif "Benim adım" in voice or "İsmim" in voice or "benim adım" in voice or "ismim" in voice:
        my_name()

    elif "saat kaç" in voice or "saati söyle" in voice or "Saat kaç" in voice or "Saati söyle" in voice :
        time_t()

    elif "Ara" in voice or "Nedir" in voice or "Ne demek" in voice or "Nasıl" in voice or "Niye" in voice or "Niçin" in voice or "Hangi" in voice or "ara" in voice or "nedir" in voice or "ne demek" in voice or "nasıl" in voice or "niye" in voice or "niçin" in voice or "hangi" in voice:
        search_g()

    elif "İsmin ne" in voice or "Adın ne" in voice or "Sen kimsin" in voice or "Adını söyle" in voice or "İsmini söyle" in voice or "ismin ne" in voice or "adın ne" in voice or "sen kimsin" in voice or "adını söyle" in voice or "ismini söyle" in voice:
        name()

    elif "artı" in voice or "eksi" in voice or "çarpı" in voice or "kere" in voice or "bölü" in voice or "üssü" in voice or '+' in voice or '-' in voice or '/' in voice or '*' in voice:
        operation()

    elif "YouTube" in voice or "Youtube'u aç" in voice or "youtube" in voice or "youtube'u aç" in voice:
        youtube()

    elif "Bugün günlerden ne" in voice or "Bugün hangi gün" in voice or "Hangi gündeyiz" in voice or "Hangi gün" in voice or  "bugün günlerden ne" in voice or "bugün hangi gün" in voice or "hangi gündeyiz" in voice or "hangi gün" in voice:
        today()

    elif "vikipedi" in voice or "Vikipedi" in voice:
        voice = voice.replace("vikipedi", "")
        wiki()

    elif "hakkında bilgi" in voice:
        voice = voice.replace("hakkında bilgi", "")
        wiki()

    elif "Haritayı aç" in voice or "Haritayı göster" in voice or "Harita" in voice or "haritayı aç" in voice or "haritayı göster" in voice or "harita" in voice:
        harita()

    elif "nerede" in voice:
        loc()

    elif "Netflix" in voice or "netflix" in voice:
        netflix()

    elif "Paint" in voice or "paint" in voice:
        paint()

    elif "Hesap makinesini aç" in voice or "Hesap makinesi aç" in voice:
       calc()

    elif "Not al" in voice or "Not tut" in voice or "not al" in voice or "not tut" in voice:
        notes()

    elif "Çeviri yap" in voice or "kelimesini çevir" in voice or "cümlesini çevir" in voice or "çeviri yap" in voice:
        translate()

    elif "döviz" in voice or "Döviz" in voice or "Döviz çevir" in voice or "Döviz hesapla" in voice or "döviz çevir" in voice or "döviz hesapla" in voice or "kur" in voice or "Kur hesapla" in voice or "kur hesapla" in voice:
        currency()

    elif "Bugün hava nasıl" in voice or "bugün hava nasıl"  in voice or "hava durumu" in voice or "Hava durumu" in voice or "bugünkü hava" in voice or "Bugünkü hava" in voice or "Bugün kaç derece?" in voice or "bugün kaç derece" in voice or "meteoroloji" in voice:
        weather()

    elif "dinle" in voice:
        music_yt()

    elif "tam ekran" in voice or "Tam ekran" in voice or "ekranı büyüt" in voice or "Ekranı büyüt" in voice:
        full()

    elif "durdur" in voice or "Durdur" in voice or "Duraklat" in voice or "duraklat" in voice:
        pause()

    elif "aklında tut" in voice or "Aklında tut" in voice:
        remember()

    elif "hatırlat" in voice or "Hatırlat" in voice:
        ret_remember()
        os.remove("Rememberme.txt")

    elif "haberler" in voice or "Haberler" in voice or "gündem" in voice or "Gündem" in voice:
        news()

    elif "makale" in voice:
        scholar()

    elif "neredeyim" in voice or "Neredeyim" in voice or "konumum" in voice or "Konumum" in voice or "konum" in voice or "Konum" in voice:
        my_loc()

    elif "kimdir" in voice or "Kimdir" in voice:
        voice = voice.replace("kimdir", "")
        wiki()

    elif "şarjım" in voice or "Şarjım" in voice:
        battery()

    elif "ekran görüntüsü" in voice or "Ekran görüntüsü" in voice or "screenshot" in voice or "Screenshot" in voice:
        screen_shot()

    elif "sesi azalt" in voice or "Sesi azalt" in voice or "sesi alçalt" in voice or "Sesi alçalt" in voice:
        sound_down()

    elif "sesi arttır" in voice or "Sesi arttır" in voice or "Sesi yükselt" in voice or "sesi yükselt" in voice:
        sound_up()

    elif "parlaklığı arttır" in voice or "Parlaklığı arttır" in voice or "Parlaklığı yükselt" in voice or "parlaklığı yükselt" in voice:
        brght_up()

    elif "parlaklığı azalt" in voice or "Parlaklığı azalt" in voice or "parlaklığı düşür" in voice or "Parlaklığı düşür" in voice:
        brght_down()

    elif "bir şey söyle" in voice or "Bir şey söyle" in voice:
        answer("Konuşmak için değil verdiğiniz görevleri yerine getirmek için yaratıldım.")

    elif "naber" in voice or "Naber" in voice or "Nasılsın" in voice or "nasılsın" in voice or "nasıl gidiyor" in voice or "hayat nasıl" in voice or "mutlu musun" in voice:
        dialog_a()

    elif "nerelisin" in voice or "memleket neresi" in voice:
        answer("Bilgisayarında doğup yaşadığıma göre bilgisayarlıyım diyebiliriz.")

    elif "giysem" in voice or "giymeliyim" in voice or "giyinsem" in voice or "kalın mı giyinsem" in voice or "Kalın mı giyinsem" in voice:
        weather_b()

    elif "kapat" in voice or "görüşürüz" in voice or "baybay" in voice or "kapan" in voice or "yeter" in voice or "teşekkürler" in voice or "teşekkür ederim" in voice:
        answer("Görüşmek üzere! Umarım yardımcı olabilmişimdir.")
        exit()

    else:
        web_br = voice
        answer("Söylediğiniz şey için google sonuçları:")
        webbrowser.open("https://www.google.com/search?q=" + web_br)




time.sleep(3)
answer("Merhaba nasıl yardımcı olabilirim")
while 1:
    voice = speak()
    response(voice)
