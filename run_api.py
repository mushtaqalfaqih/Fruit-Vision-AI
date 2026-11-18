"""
تشغيل خادم Fruit Vision API
يمكنك تشغيله بالأمر:
python run_api.py
"""
import os
import sys

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(current_dir, "Fruit_Vision_Project")
    sys.path.insert(0, project_dir)
    sys.path.insert(0, os.path.join(project_dir, "yolov5"))

    import uvicorn
    print("=" * 60)
    print("🍎 جاري بدء تشغيل Fruit Vision API...")
    print("🔗 الرابط المحلي: http://127.0.0.1:8000")
    print("📖 التوثيق التفاعلي (Swagger UI): http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run("api:app", app_dir=project_dir, host="0.0.0.0", port=8000, reload=False)
