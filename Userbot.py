import asyncio
import random
import datetime
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 24926482  # Buraya kendi API ID'ni yaz
API_HASH = "00bb872c6a01aa3666d84af7b7ed660a"  # Buraya kendi API Hash'ini yaz
SAHIB_ID = 123456789  # Sadece senin ID’n

bot = Client("blayzen_userbot", api_id=API_ID, api_hash=API_HASH)

# Global spam ayarları
spam_durum = False
spam_sure = 2

# Komut Engelleyici
def sadece_sahip(func):
    async def wrapper(client, message: Message):
        if message.from_user.id != SAHIB_ID:
            await message.edit("Bu komutu sadece sahibim kullanabilir.")
            return
        await func(client, message)
    return wrapper

@bot.on_message(filters.command("yardim", "."))
@sadece_sahip
async def yardim(client, message):
    komutlar = """
**Bu Bot Blayzen Tarafından Yazılmıştır.**

Mevcut Komutlar:

.ship - Yanıtlanan kişiyle aşk uyumu
.kurulum - Hesabın kurulum tarihini gösterir
.saka - Rastgele şaka yapar
.fikra - Rastgele fıkra anlatır
.hikaye - Rastgele kısa hikaye yazar
.filmoner - Film önerisi yapar (kategori sorar)
.zarat - 1-6 arası zar atar
.hava <şehir> - Belirtilen şehrin hava durumunu gösterir
.slap - Yanıt verilen kişiye tokat/küfür atar
.spam <yazı> - Belirtilen yazıyı spamlar
.sure <saniye> - Spamlar arası süreyi ayarlar
.dur - Spamlamayı durdurur
"""
    await message.edit(komutlar)

@bot.on_message(filters.command("ship", ".") & filters.reply)
@sadece_sahip
async def ship(client, message):
    ask_orani = random.randint(0, 100)
    kalpler = ['💔', '🖤', '❤️‍🔥', '❤️‍', '❤️', '💕', '💗', '💘', '💞', '💖', '❣️', '💓', '💝']
    kalp = random.choice(kalpler)
    sozler = [
        (0, 20, "Bu iş olmaz, birbirinize hiç uymuyorsunuz."),
        (21, 40, "Zorla güzellik olmaz, belki dost kalırsınız."),
        (41, 60, "Arada bir kıvılcım olabilir."),
        (61, 80, "Gayet uyumlusunuz, şansınızı deneyin!"),
        (81, 100, "Ruh ikizisiniz, birbiriniz için yaratılmışsınız!")
    ]
    yorum = next((s for minv, maxv, s in sozler if minv <= ask_orani <= maxv), "Yorum bulunamadı.")
    cevap = f"**Aşk Uyumu**\n{message.from_user.mention} {kalp} {message.reply_to_message.from_user.mention}\n\n**Uyum Oranı:** %{ask_orani}\n{yorum}"
    await message.edit(cevap)

@bot.on_message(filters.command("kurulum", "."))
@sadece_sahip
async def kurulum(client, message):
    try:
        me = await client.get_me()
        kurulum_tarihi = me.dc_id if me.dc_id else "Bilinmiyor"
        tarih = datetime.datetime.fromtimestamp(me.id >> 32).strftime("%d.%m.%Y")
        await message.edit(f"Hesabın kurulum tarihi: **{tarih}**")
    except Exception as e:
        await message.edit(f"Hata oluştu: {e}")

@bot.on_message(filters.command("saka", "."))
@sadece_sahip
async def saka(client, message):
    sakalar = [
        "Gece yatarken yorganı üstüme çekiyorum... Sabah bakıyorum hala yer çekiyor!",
        "Doktora gittim, 'İnsanları çok seviyorum' dedim. Psikoloğa yönlendirdi.",
        "Dünya yuvarlak ama ben hala köşeye sıkışıyorum.",
        "Bir gün kahve içmeye gittim, fincan bana 'merhaba' dedi.",
        "Paraya ihtiyacım var ama para bana hiç ihtiyaç duymuyor.",
        "Çok çalışırsan ilerde patron olamazsın. Patronlar zengin olur.",
        "Matematik zor bir ders değil, sadece içinde çok sayıda sayı barındırıyor."
    ]
    await message.edit(random.choice(sakalar))

@bot.on_message(filters.command("fikra", "."))
@sadece_sahip
async def fikra(client, message):
    fikralar = [
        "Temel ile Dursun ormanda yürüyormuş. Temel birden bağırmış: 'Ayı geliyor!' Dursun da 'Ben de!' demiş.",
        "Nasreddin Hoca: 'Dün gece rüyamda bir koyun gördüm.' Karısı: 'Kes sesini, uykumda bile yalan söylüyorsun!'",
        "Adam: 'Doktorum bana rüyamda çadır kurduğumu söylüyorlar.' Doktor: 'O zaman gece kamp yapmayı bırak.'",
        "İki bilgisayar konuşuyormuş. Biri diğerine demiş: 'Bugün kendimi çok RAM'siz hissediyorum.'"
    ]
    await message.edit(random.choice(fikralar))

@bot.on_message(filters.command("hikaye", "."))
@sadece_sahip
async def hikaye(client, message):
    hikayeler = [
        "Bir zamanlar küçük bir köyde, yıldızlara dokunmak isteyen bir çocuk yaşarmış.",
        "Issız bir ormanda yalnız yürüyen adam, geçmişin yankılarını duymaya başlamış.",
        "Her sabah tren istasyonunda bekleyen kadın, bir gün geçmişten gelen bir zarf bulmuş.",
        "Yağmurlu bir günde karşılaştılar. İkisi de birbirinin sığınağı oldu."
    ]
    await message.edit(random.choice(hikayeler))

@bot.on_message(filters.command("filmoner", "."))
@sadece_sahip
async def filmoner(client, message):
    await message.edit("Lütfen kategori yazınız: (aksiyon, komedi, dram, bilimkurgu, korku)")
    yanit = await bot.listen(message.chat.id)
    kategori = yanit.text.lower()
    filmler = {
        "aksiyon": ["John Wick", "Mad Max: Fury Road", "Gladiator", "Inception", "The Dark Knight"],
        "komedi": ["Yes Man", "Hangover", "The Mask", "Superbad", "Zombieland"],
        "dram": ["The Shawshank Redemption", "Forrest Gump", "The Green Mile", "A Beautiful Mind"],
        "bilimkurgu": ["Interstellar", "The Matrix", "Blade Runner 2049", "Arrival"],
        "korku": ["The Conjuring", "Hereditary", "It", "Get Out"]
    }
    cevap = random.choice(filmler.get(kategori, ["Bu kategoride film bulunamadı."]))
    await message.edit(f"**Film Önerisi:** {cevap}")

@bot.on_message(filters.command("zarat", "."))
@sadece_sahip
async def zarat(client, message):
    zar = random.randint(1, 6)
    await message.edit(f"Zar atıldı: 🎲 **{zar}**")

@bot.on_message(filters.command("hava", "."))
@sadece_sahip
async def hava(client, message):
    try:
        sehir = message.text.split(maxsplit=1)[1]
    except:
        await message.edit("Lütfen şehir ismi giriniz. Örnek: `.hava İstanbul`")
        return
    try:
        url = f"https://wttr.in/{sehir}?format=3"
        sonuc = requests.get(url).text
        await message.edit(f"Hava durumu: {sonuc}")
    except:
        await message.edit("Hava durumu alınamadı.")

@bot.on_message(filters.command("slap", ".") & filters.reply)
@sadece_sahip
async def slap(client, message):
    hedef = message.reply_to_message.from_user.mention
    slaplar = [
        f"{hedef}'e tava fırlattı!",
        f"{hedef}'e sandalye ile vurdu!",
        f"{hedef}'i bir küfür yağmuruna tuttu!",
        f"{hedef}'e gökten taş yağdırdı!",
        f"{hedef}'i tokat manyağı yaptı!"
    ]
    await message.edit(random.choice(slaplar))

@bot.on_message(filters.command("spam", "."))
@sadece_sahip
async def spam(client, message):
    global spam_durum
    try:
        icerik = message.text.split(maxsplit=1)[1]
    except:
        await message.edit("Spamlamak için bir yazı giriniz.")
        return
    spam_durum = True
    await message.edit("Spam başlatıldı. `.dur` yazarak durdurabilirsin.")
    while spam_durum:
        await message.reply(icerik)
        await asyncio.sleep(spam_sure)

@bot.on_message(filters.command("sure", "."))
@sadece_sahip
async def sure(client, message):
    global spam_sure
    try:
        spam_sure = int(message.text.split()[1])
        await message.edit(f"Spam süresi {spam_sure} saniye olarak ayarlandı.")
    except:
        await message.edit("Lütfen süreyi saniye cinsinden giriniz. Örnek: `.sure 3`")

@bot.on_message(filters.command("dur", "."))
@sadece_sahip
async def dur(client, message):
    global spam_durum
    spam_durum = False
    await message.edit("Spam durduruldu.")

print("Bot başlatılıyor...")
bot.run()
