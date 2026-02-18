# Nawa Programming Language

<div align="center">

![Nawa Logo](https://j.top4top.io/p_3701n2bin1.jpg)

## 🌟 نواة - لغة البرمجة العربية المتقدمة

### Nawa - Advanced Arabic Programming Language

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/nawa-lang/nawa.svg)](https://github.com/nawa-lang/nawa/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/nawa-lang/nawa.svg)](https://github.com/nawa-lang/nawa/issues)

[العربية](#عربي) | [English](#english)

</div>

---

<div dir="rtl">

## 🇸🇦 عربي

### 🎯 عن نواة

**نواة** هي لغة برمجة عربية متكاملة مصممة للمبتدئين والمحترفين. تمكنك من بناء:

- 🌐 مواقع ويب كاملة
- 📱 تطبيقات سطح المكتب
- 💾 قواعد بيانات
- 🔌 واجهات API
- 📁 أنظمة ملفات
- 🔐 تطبيقات أمنية

### ✨ المميزات

- **🌍 عربية بالكامل** - كل الكلمات المفتاحية بالعربية
- **📚 سهلة التعلم** - بناء جملة بسيط وواضح
- **🚀 قوية** - دعم كامل للميزات المتقدمة
- **🆓 مجانية** - مفتوحة المصدر للجميع
- **📦 غنية** - مكتبة قياسية شاملة

### 🚀 التثبيت السريع

#### الطريقة 1: عبر pip
```bash
pip install nawa-lang
```

#### الطريقة 2: من المصدر
```bash
git clone https://github.com/nawa-lang/nawa.git
cd nawa
python setup.py install
```

#### الطريقة 3: تشغيل مباشر
```bash
python nawa.py برنامج.nawa
```

### 📝 أمثلة

#### أهلاً وسهلاً
```nawa
اطبع_سطر "أهلاً بك في نواة!"
```

#### متغيرات ودوال
```nawa
متغير اسم = "أحمد"
متغير عمر = 25

دالة ترحيب(اسم) {
    اطبع_سطر "مرحباً "
    اطبع_سطر اسم
}

ترحيب(اسم)
```

#### قواعد بيانات
```nawa
متغير db = قاعدة_بيانات('app.db')
db.نفذ('CREATE TABLE users (id INTEGER, name TEXT)')
db.نفذ('INSERT INTO users VALUES (?, ?)', [1, 'أحمد'])
متغير مستخدمين = db.نفذ('SELECT * FROM users')
```

#### ويب
```nawa
متغير خادم = خادم_ويب(8080)

دالة الرئيسية() {
    ارجع html("<h1>مرحباً!</h1>")
}

خادم.رابط('/', الرئيسية)
خادم.شغل()
```

### 📚 التوثيق الكامل

[اقرأ التوثيق الكامل هنا](README_NAWA.md)

### 🤝 ساهم معنا

نرحب بمساهماتكم! اقرأوا [دليل المساهمة](CONTRIBUTING.md)

### 📞 تواصل معنا

- 📧 Email: nawa.lang@example.com
- 💬 GitHub Issues: [افتح Issue جديد](https://github.com/nawa-lang/nawa/issues)
- 🐦 Twitter: @nawa_lang (قريباً)

### 📄 الترخيص

مرخص تحت [MIT License](LICENSE)

---

## 🇬🇧 English

### 🎯 About Nawa

**Nawa** is a complete Arabic programming language designed for beginners and professionals. It enables you to build:

- 🌐 Full web applications
- 📱 Desktop applications
- 💾 Databases
- 🔌 API integrations
- 📁 File systems
- 🔐 Security applications

### ✨ Features

- **🌍 Arabic Keywords** - All keywords in Arabic
- **📚 Easy to Learn** - Simple and clear syntax
- **🚀 Powerful** - Full support for advanced features
- **🆓 Free** - Open source for everyone
- **📦 Rich** - Comprehensive standard library

### 🚀 Quick Start

#### Method 1: Via pip
```bash
pip install nawa-lang
```

#### Method 2: From source
```bash
git clone https://github.com/nawa-lang/nawa.git
cd nawa
python setup.py install
```

#### Method 3: Direct run
```bash
python nawa.py program.nawa
```

### 📝 Examples

#### Hello World
```nawa
اطبع_سطر "أهلاً بك في نواة!"
```

#### Variables and Functions
```nawa
متغير اسم = "أحمد"
متغير عمر = 25

دالة ترحيب(اسم) {
    اطبع_سطر "مرحباً "
    اطبع_سطر اسم
}

ترحيب(اسم)
```

#### Databases
```nawa
متغير db = قاعدة_بيانات('app.db')
db.نفذ('CREATE TABLE users (id INTEGER, name TEXT)')
db.نفذ('INSERT INTO users VALUES (?, ?)', [1, 'أحمد'])
متغير مستخدمين = db.نفذ('SELECT * FROM users')
```

#### Web
```nawa
متغير خادم = خادم_ويب(8080)

دالة الرئيسية() {
    ارجع html("<h1>مرحباً!</h1>")
}

خادم.رابط('/', الرئيسية)
خادم.شغل()
```

### 📚 Full Documentation

[Read full documentation here](README_NAWA.md)

### 🤝 Contributing

We welcome contributions! Read our [Contributing Guide](CONTRIBUTING.md)

### 📞 Contact Us

- 📧 Email: nawa.lang@example.com
- 💬 GitHub Issues: [Open new Issue](https://github.com/nawa-lang/nawa/issues)
- 🐦 Twitter: @nawa_lang (coming soon)

### 📄 License

Licensed under [MIT License](LICENSE)

</div>

---

<div align="center">

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=nawa-lang/nawa&type=Date)](https://star-history.com/#nawa-lang/nawa&Date)

## 🏆 Contributors

Thanks to all our contributors!

<a href="https://github.com/nawa-lang/nawa/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=nawa-lang/nawa" />
</a>

---

**Made with ❤️ for the Arabic-speaking community**

**صنع بحب ❤️ للمجتمع الناطق بالعربية**

[Website](https://nawa-lang.github.io) | [Documentation](README_NAWA.md) | [Examples](examples/)

</div>
