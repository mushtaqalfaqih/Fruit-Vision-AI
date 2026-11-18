"""
اختبار شامل لكافة نماذج ونقاط نهاية Fruit Vision API
"""
import os
import sys

# إضافة المسارات
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(current_dir, "Fruit_Vision_Project")
sys.path.insert(0, project_dir)
sys.path.insert(0, os.path.join(project_dir, "yolov5"))

from fastapi.testclient import TestClient
from api import app

def run_tests():
    print("=" * 60)
    print("🧪 بدء الاختبارات الآلية لنظام Fruit Vision...")
    print("=" * 60)

    with TestClient(app) as client:
        # 1. اختبار الجذر
        print("\n1️⃣ فحص نقطة البداية (GET /)...")
        res = client.get("/")
        assert res.status_code == 200, f"Failed: {res.text}"
        print("✅ الاستجابة:", res.json())

        # 2. اختبار فحص الصحة
        print("\n2️⃣ فحص صحة النماذج (GET /health)...")
        res = client.get("/health")
        assert res.status_code == 200, f"Failed: {res.text}"
        data = res.json()
        print(f"✅ حالة ResNet18: {'محمّل' if data.get('resnet_loaded') else 'غير محمّل'}")
        print(f"✅ حالة YOLOv5: {'محمّل' if data.get('yolo_loaded') else 'غير محمّل'}")

        # 3. اختبار تصنيف صورة
        image_path = os.path.join(current_dir, "apple.png")
        if os.path.exists(image_path):
            print(f"\n3️⃣ فحص تصنيف الصورة (POST /predict/classify) على: {image_path}...")
            with open(image_path, "rb") as f:
                res = client.post("/predict/classify", files={"file": ("apple.png", f, "image/png")})
            assert res.status_code == 200, f"Failed: {res.text}"
            print("✅ نتيجة التصنيف:", res.json())

            # 4. اختبار كشف YOLOv5
            print(f"\n4️⃣ فحص كشف وتحديد مواقع الأجسام (POST /predict/detect)...")
            with open(image_path, "rb") as f:
                res = client.post("/predict/detect", files={"file": ("apple.png", f, "image/png")})
            assert res.status_code == 200, f"Failed: {res.text}"
            print("✅ نتيجة الكشف:", res.json())

            # 5. اختبار الفحص الشامل المدمج
            print(f"\n5️⃣ فحص الفحص الشامل المدمج (POST /predict/inspect)...")
            with open(image_path, "rb") as f:
                res = client.post("/predict/inspect", files={"file": ("apple.png", f, "image/png")})
            assert res.status_code == 200, f"Failed: {res.text}"
            print("✅ نتيجة الفحص الشامل:", res.json())

    print("\n" + "=" * 60)
    print("🎉 جميع الاختبارات تمت بنجاح وبدون أي أخطاء!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
