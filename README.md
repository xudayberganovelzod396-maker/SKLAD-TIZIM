# 🏭 SKLAD TIZIM

**Ombor Boshqaruv Tizimi** - Ombor va ishlab chiqarish uchun mo'ljallangan zamonaviy web-platforma.

## 📋 Imkoniyatlar

- ✅ Mahsulotlarni qo'shish va boshqarish
- ✅ Partiyalarni chiqarish (to'liq va qisman)
- ✅ Ombor joylashuvini vizual ko'rish (A, B, C sektorlar)
- ✅ Qidirish va filtrlash
- ✅ Arxiv va hisobotlar
- ✅ Foydalanuvchi autentifikatsiyasi
- ✅ Xavfsiz ma'lumotlar saqlash

## 🚀 O'rnatish

### 1. Virtual muhit yaratish
```bash
python -m venv venv
```

### 2. Virtual muhitni faollashtirish
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Dasturni ishga tushirish
```bash
python app.py
```

### 5. Brauzerda ochish
```
http://127.0.0.1:5000
```



## 📁 Loyiha tuzilishi

```
SKLAD TIZIM/
├── app.py              # Asosiy Flask ilovasi
├── requirements.txt    # Python kutubxonalari
├── schema.sql          # Ma'lumotlar bazasi sxemasi
├── README.md           # Dokumentatsiya
├── instance/           # SQLite ma'lumotlar bazasi
│   └── sklad.db
├── static/             # Statik fayllar
│   ├── css/           # CSS stillar
│   ├── js/            # JavaScript fayllar
│   └── img/           # Rasmlar
└── templates/          # HTML shablonlar
    ├── index.html     # Bosh sahifa
    ├── login.html     # Kirish sahifasi
    └── 404.html       # Xato sahifasi
```

## 🔧 API Endpoints

### Autentifikatsiya
- `POST /login` - Tizimga kirish
- `GET /logout` - Tizimdan chiqish

### Foydalanuvchi
- `GET /api/user` - Joriy foydalanuvchi ma'lumotlari
- `POST /api/user/password` - Parolni o'zgartirish
- `GET /api/user/activity` - Faoliyat statistikasi

### Partiyalar
- `GET /api/batches` - Barcha partiyalar
- `POST /api/batches` - Yangi partiya qo'shish
- `PUT /api/batches/<id>/remove` - Partiyani chiqarish

### Qidirish
- `GET /api/search?q=<query>` - Oddiy qidirish
- `GET /api/batches/search?q=<query>` - Sahifalash bilan qidirish

### Ombor
- `GET /api/rows_matrix_status` - Ombor matritsa holati

### Arxiv va Hisobot
- `GET /api/archive` - Arxiv ma'lumotlari
- `GET /api/report` - Kirim/chiqim hisoboti

## 🛡️ Xavfsizlik

- Parollar hash qilingan holda saqlanadi
- Sessiya cookie'lari HTTPOnly
- API javoblari keshlanmaydi
- Login talab qiluvchi barcha sahifalar himoyalangan

## 📝 Litsenziya

MIT License

---

**Muallif:** Administrator  
**Versiya:** 2.0  
**Sana:** 2026
