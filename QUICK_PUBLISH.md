# 🚀 دليل النشر السريع لنواة

## ⚡ طريقة 1: باستخدام السكريبت (الأسهل)

```bash
cd /storage/emulated/0/Download/arabs
chmod +x publish_to_github.sh
./publish_to_github.sh
```

## 📝 طريقة 2: يدوياً

### الخطوة 1: إنشاء المستودع

1. اذهب إلى [github.com](https://github.com)
2. سجل الدخول بحسابك
3. اضغط على **+** في الزاوية
4. اختر **New repository**
5. املأ البيانات:
   - **Repository name**: `nawa`
   - **Description**: `نواة - لغة البرمجة العربية المتقدمة | Nawa - Advanced Arabic Programming Language`
   - **Public**: ✅
   - **Initialize**: ❌ (لا تُفعّل)
6. اضغط **Create repository**

### الخطوة 2: رفع الملفات

افتح Terminal/Command Prompt ونفذ:

```bash
cd /storage/emulated/0/Download/arabs

# تهيئة المستودع
git init

# إضافة كل الملفات
git add .

# إنشاء أول commit
git commit -m "🎉 إطلاق نواة - لغة البرمجة العربية"

# تغيير اسم الفرع
git branch -M main

# إضافة الرابط (استبدل YOUR_USERNAME باسم المستخدم)
git remote add origin https://github.com/tofey-ar/nawa.git

# الرفع
git push -u origin main
```

### الخطوة 3: إعداد GitHub Pages (موقع إلكتروني)

1. اذهب إلى **Settings** في المستودع
2. اختر **Pages** من القائمة الجانبية
3. تحت **Source**، اختر **main** ثم **/ (root)**
4. اضغط **Save**
5. انتظر دقيقة ثم موقعك سيكون على:
   `https://tofey-ar.github.io/nawa/`

### الخطوة 4: إضافة Topics

1. في الصفحة الرئيسية للمستودع
2. اضغط على ⚙️ (Settings) بجانب About
3. أضف Topics:
   - `arabic`
   - `programming-language`
   - `nawa`
   - `interpreter`
   - `education`
   - `open-source`

---

## 🎨 تخصيص المستودع

### إضافة Badge في README

```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/tofey-ar/nawa.svg)](https://github.com/tofey-ar/nawa/stargazers)
```

### إضافة روابط مهمة

في نهاية README.md:

```markdown
## 🔗 روابط مهمة

- 🌐 الموقع: https://tofey-ar.github.io/nawa/
- 📚 التوثيق: [README_NAWA.md](README_NAWA.md)
- 💬 النقاشات: [Discussions](https://github.com/tofey-ar/nawa/discussions)
- 🐛 الإبلاغ عن مشاكل: [Issues](https://github.com/tofey-ar/nawa/issues)
```

---

## 📢 الترويج

### بعد النشر، شارك على:

#### Twitter/X
```
🚀 أطلقتُ نواة - أول لغة برمجة عربية متكاملة!

✅ كلمات عربية
✅ ويب وقواعد بيانات
✅ مجانية ومفتوحة المصدر

جربها: github.com/tofey-ar/nawa

#نواة #برمجة #عربي #تقنية
```

#### LinkedIn
```
فخور بالإعلان عن إطلاق نواة، لغة برمجة عربية متكاملة!

نواة تمكن المطورين الناطقين بالعربية من البرمجة بلغتهم الأم.

الرابط: github.com/tofey-ar/nawa

#Programming #Arabic #OpenSource #Technology
```

#### Facebook Groups
- مجموعات المبرمجين العرب
- مجموعات التعليم التقني
- مجموعات المصدر المفتوح

---

## 📊 تتبع النجاح

### إحصائيات مهمة:
- ⭐ Stars على GitHub
- 🍴 Forks
- 👥 Contributors
- 📥 التحميلات من PyPI

### أدوات مفيدة:
- [GitHub Insights](https://github.com/tofey-ar/nawa/pulse)
- [PyPI Stats](https://pypistats.org/) (بعد النشر على PyPI)

---

## 🔄 التحديثات المستقبلية

### إصدار تحديث:

```bash
# عدّل رقم الإصدار في:
# - setup.py
# - pyproject.toml
# - nawa.py (NAWA_VERSION)

git add .
git commit -m "📦 الإصدار 1.1.0 - ميزات جديدة"
git tag v1.1.0
git push origin main --tags
```

---

## 🆘 حل المشاكل

### مشكلة: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/tofey-ar/nawa.git
```

### مشكلة: "Authentication failed"
1. اذهب إلى: https://github.com/settings/tokens
2. أنشئ Token جديد بصلاحيات **repo**
3. استخدمه بدلاً من كلمة المرور

### مشكلة: "large files"
```bash
# لحذف الملفات الكبيرة
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch PATH/TO/LARGE-FILE' \
  --prune-empty --tag-name-filter cat -- --all
```

---

<div align="center">

**نواة - لغة البرمجة العربية**

🚀 انطلق الآن! 🚀

</div>
