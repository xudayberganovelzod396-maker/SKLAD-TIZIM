# SKLAD TIZIMI - ISHGA TUSHIRISH

## 1️⃣ NASIB QILISH (Installation)

```bash
# Python virtual environment yaratish
python -m venv venv

# Activate qilish
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Dependencies o'rnatish
pip install -r requirements.txt
```

## 2️⃣ DASTURNI ISHGA TUSHIRISH (Run)

```bash
# Virtual environment aktiv bo'lishini tekshir
# Keyin:
python app.py
```

## 3️⃣ WEB-SAYTGA KIRISH

Browser-da **http://127.0.0.1:5000** ochish

## 4️⃣ TEST HISOBLAR

### Admin (Hammasini qila oladi):
- Login: **admin**
- Parol: **admin123**

### Ko'ruvchi (Faqat ko'radi):
- Login: **user**
- Parol: **user123**

## 📁 PAPKA TUZILISHI

```
SKLAD INLENE/
├── app.py                    # Flask asosiy fayl
├── requirements.txt          # Python dependencies
├── sklad.db                  # SQLite database (avtomatik yaratiladi)
├── schema.sql               # Database schema
└── templates/
    ├── login.html           # Login sahifasi
    └── index.html           # Bosh sahifa
```

## 🔑 ASOSIY XUSUSIYATLAR

✅ **Admin Panel:**
- Partiya qo'shish
- Partiya o'chirish (slide animation)
- Hammasini ko'rish

✅ **Ko'ruvchi Panel:**
- Faqat ko'rish
- Qidiruv

✅ **Qidiruv:**
- Partiya kodi bo'yicha
- Mahsulot nomi bo'yicha
- Joy bo'yicha (A-1-1)

✅ **Slide Delete Animation:**
- O'ngga surish animatsiyasi
- Status = REMOVED (o'chirilmaydi)

## 🐛 AGAR XATO CHIKSA

Agar `ModuleNotFoundError` chiksa:
```bash
pip install -r requirements.txt
```

Agar database muammo bo'lsa:
```bash
# Database o'chirish va qayta yaratish
rm sklad.db  # Windows: del sklad.db
python app.py
```

## 🚀 KEYINGI QADAM (DEPLOY UCHUN)

Production uchun:
```bash
# requirements.txt-ga qo'shish:
gunicorn==20.1.0

# Running:
gunicorn app:app --bind 0.0.0.0:5000
```

---

**Endi ishga tushdi! 🎉**
