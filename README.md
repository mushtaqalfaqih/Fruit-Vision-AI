# 🍎 Fruit Vision AI - نظام الرؤية الحاسوبية لفحص وتصنيف جودة الفواكه

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/YOLOv5-Object%20Detection-00FFFF?logo=yolo&logoColor=black" alt="YOLOv5">
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Accuracy-97%25%20Val-success" alt="Accuracy">
  <img src="https://img.shields.io/badge/Status-Active%20%26%20Ready-brightgreen" alt="Status">
</p>

---

## 🌟 نبذة عن المشروع (Overview)

**Fruit Vision AI** هو نظام ذكاء اصطناعي متكامل للرؤية الحاسوبية (Computer Vision)، يهدف إلى أتمتة فحص وتصنيف جودة الفواكه في خطوط الإنتاج والأسواق والمخازن الذكية. يدمج المشروع بين تقنيتين رائدتين:
1. **تصنيف جودة الفواكه (Quality Classification):** تقييم حالة الفاكهة كطازجة (**Fresh**) أو تالفة/فاسدة (**Rotten**) بدقة تصل إلى **97%** عبر شبكة **ResNet-18** (Transfer Learning).
2. **كشف وتحديد مواقع الفواكه (Object Detection):** التعرف على 28 صنفاً من الفواكه والخضار وتحديد إحداثيات ومربعات الإحاطة (Bounding Boxes) في الوقت الفعلي باستخدام **YOLOv5**.
3. **لوحة تحكم تفاعلية (Interactive Web UI):** واجهة ويب مدمجة لسحب وإفلات الصور وتجربة النماذج وعرض الصناديق ونسب الثقة مباشرة.
4. **خادم REST API فائق السرعة:** مبني باستخدام **FastAPI** لتسهيل التكامل مع تطبيقات الويب والجوال ومعدات الفرز الآلي.

---

## 🚀 المميزات الرئيسية (Key Features)

* **دقة عالية:** تدريب نموذج ResNet-18 على مجموعات بيانات متوازنة محققاً دقة 97% في التحقق.
* **كشف موضعي متعدد:** استخراج موقع كل حبة فاكهة في الصورة وحالتها عبر YOLOv5.
* **واجهة مستخدم بصرية مدمجة:** بدون أي تعقيد، تجربة فورية عبر المتصفح على `/ui`.
* **توثيق برمجيات تفاعلي:** دعم كامل لمواصفات OpenAPI و Swagger UI على `/docs`.
* **بنية برمجية نظيفة:** كود منظم ومختبر بنسبة 100%، وخالٍ من الأخطاء والمسارات المكسورة.

---

## 📁 هيكلية المشروع (Project Architecture)

```text
├── models/                                # أوزان النماذج المُدرّبة
│   ├── classification_model.pth           # أوزان نموذج ResNet-18 (42.7 MB)
│   └── yolov5_best.pt                     # أوزان نموذج YOLOv5 (14.5 MB)
├── Fruit_Vision_Project/
│   ├── api.py                             # خادم FastAPI ولوحة التحكم البصرية (Web UI)
│   ├── check_labelimg_notebook.ipynb      # دفتر التدريب والاختبار (PyTorch + YOLOv5)
│   ├── prepare_yolo_dataset.py            # سكريبت معالجة وتجهيز الـ Dataset
│   ├── fruit.yaml                         # إعدادات وفئات الكشف
│   ├── yolov5/                            # إطار عمل YOLOv5 المخصص
│   └── labelImg/                          # أداة التوسيم المدمجة
├── extra_academic_projects/               # مشاريع وأبحاث أكاديمية إضافية
├── run_api.py                             # سكريبت الإطلاق السريع للخادم
├── test_system.py                         # الاختبارات المؤتمتة لكامل النظام
├── apple.png                              # صورة اختبارية تجريبية
├── requirements.txt                       # حزم ومكتبات المشروع
└── README.md                              # دليل الاستخدام والتوثيق
```

---

## ⚙️ متطلبات التثبيت والتشغيل (Quick Start)

### 1. استنساخ المستودع (Clone):
```bash
git clone https://github.com/mushtaqalfaqih/Fruit-Vision-AI.git
cd Fruit-Vision-AI
```

### 2. تثبيت الحزم المطلوبة:
```bash
pip install -r requirements.txt
```

### 3. اختبار جاهزية النظام والنماذج:
```bash
python test_system.py
```

### 4. تشغيل خادم الـ API ولوحة التحكم:
```bash
python run_api.py
```
* 🌐 **لوحة التحكم البصرية:** [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui)
* 📖 **توثيق Swagger التفاعلي:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 نقاط نهاية الـ API (API Endpoints)

| المسار (Endpoint) | الطريقة (Method) | الوظيفة |
|---|---|---|
| `/ui` | `GET` | لوحة التحكم الرسومية المباشرة لفحص الصور وسحبها |
| `/health` | `GET` | فحص صحة وجاهزية النماذج في الذاكرة |
| `/predict/classify` | `POST` | تصنيف جودة الفاكهة (طازجة Fresh أم فاسدة Rotten) |
| `/predict/detect` | `POST` | كشف وتحديد أماكن الفواكه ومربعات الإحاطة (YOLO) |
| `/predict/inspect` | `POST` | فحص شامل مزدوج (كشف موضعي + تصنيف جودة) |

---

## 📊 أمثلة الاستجابة (Sample Response)

### استدعاء التصنيف (`POST /predict/classify`):
```json
{
  "fruit_condition": "fresh",
  "confidence": 88.56,
  "is_fresh": true,
  "probabilities": {
    "fresh": 88.56,
    "rotten": 11.44
  }
}
```

---

## 👨‍💻 المطوّر (Author)

* **مشتاق الفقيه (Mushtaq Al-Faqih)**
* GitHub: [@mushtaqalfaqih](https://github.com/mushtaqalfaqih)
* الذكاء الاصطناعي وهندسة البيانات 🤖
