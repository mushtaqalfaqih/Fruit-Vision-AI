"""
Fruit Vision API - خادم فحص وتصنيف جودة الفواكه
يدعم:
1. التصنيف الثنائي (Fresh vs Rotten) عبر ResNet-18
2. الكشف الموضعي وتحديد الأصناف المتعددة عبر YOLOv5
"""

import os
import io
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from contextlib import asynccontextmanager

# ==============================================================================
# إعداد التطبيق والمسارات
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 بدء تشغيل خادم Fruit Vision API على الجهاز: {DEVICE}")
    load_resnet()
    load_yolo()
    yield

app = FastAPI(
    title="Fruit Vision API 🍎🍌",
    description="واجهة برمجية للرؤية الحاسوبية لفحص جودة الفواكه وتحديد مواقعها وحالتها (Fresh / Rotten)",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# مسارات النماذج
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
RESNET_MODEL_PATH = os.path.join(MODELS_DIR, "classification_model.pth")
YOLO_DIR = os.path.join(CURRENT_DIR, "yolov5")
# مسار أوزان YOLO الموحد
YOLO_WEIGHTS_PATH = os.path.join(MODELS_DIR, "yolov5_best.pt")
# مسار بديل لأوزان يولو في حال عدم توفر الأول
YOLO_ALT_WEIGHTS = os.path.join(YOLO_DIR, "runs", "train", "exp", "weights", "best.pt")

# فئات التصنيف
CLASSIFICATION_CLASSES = ["fresh", "rotten"]

# تحويلات الصور لنموذج ResNet
resnet_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# متغيرات تحميل النماذج
resnet_model = None
yolo_model = None

# ==============================================================================
# دوال تحميل النماذج
# ==============================================================================
def load_resnet():
    global resnet_model
    if not os.path.exists(RESNET_MODEL_PATH):
        print(f"⚠️ تحذير: ملف أوزان ResNet18 غير موجود في: {RESNET_MODEL_PATH}")
        return False
    try:
        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, 2)
        state_dict = torch.load(RESNET_MODEL_PATH, map_location=DEVICE)
        model.load_state_dict(state_dict)
        model.to(DEVICE)
        model.eval()
        resnet_model = model
        print("✅ تم تحميل نموذج التصنيف ResNet-18 بنجاح.")
        return True
    except Exception as e:
        print(f"❌ خطأ أثناء تحميل ResNet-18: {e}")
        return False

def load_yolo():
    global yolo_model
    weights = YOLO_WEIGHTS_PATH if os.path.exists(YOLO_WEIGHTS_PATH) else YOLO_ALT_WEIGHTS
    if not os.path.exists(weights):
        print(f"⚠️ تحذير: لم يتم العثور على أوزان YOLO في {weights}")
        return False
    try:
        model = torch.hub.load(YOLO_DIR, "custom", path=weights, source="local")
        model.to(DEVICE)
        model.eval()
        yolo_model = model
        print("✅ تم تحميل نموذج الكشف YOLOv5 بنجاح.")
        return True
    except Exception as e:
        print(f"❌ خطأ أثناء تحميل YOLOv5: {e}")
        return False

# تم استبدال startup_event بـ lifespan الحديث


# ==============================================================================
# مسارات الـ API (Endpoints)
# ==============================================================================
@app.get("/")
def root():
    return {
        "message": "مرحبًا بك في خادم Fruit Vision API 🚀",
        "device": str(DEVICE),
        "models_status": {
            "resnet18_classification": resnet_model is not None,
            "yolov5_detection": yolo_model is not None
        },
        "endpoints": {
            "web_ui": "/ui (واجهة بصرية سهلة للاستخدام)",
            "health": "/health",
            "classify": "POST /predict/classify (تصنيف جودة الفاكهة)",
            "detect": "POST /predict/detect (كشف وتحديد مواقع الفواكه)",
            "inspect": "POST /predict/inspect (فحص شامل كشف + تصنيف)",
            "docs": "/docs"
        }
    }

@app.get("/ui", response_class=HTMLResponse)
def web_dashboard():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍎 فاحص جودة الفواكه الذكي | Fruit Vision</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --success: #16a34a;
            --danger: #dc2626;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --border: #334155;
            --text: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: var(--bg); color: var(--text); min-height: 100vh; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { max-width: 950px; width: 100%; }
        header { text-align: center; margin-bottom: 25px; padding: 20px; background: var(--card-bg); border-radius: 16px; border: 1px solid var(--border); box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
        h1 { font-size: 26px; color: #38bdf8; margin-bottom: 8px; display: flex; align-items: center; justify-content: center; gap: 10px; }
        p.subtitle { color: var(--text-muted); font-size: 14px; }
        .main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .main-grid { grid-template-columns: 1fr; } }
        .card { background: var(--card-bg); border-radius: 16px; padding: 20px; border: 1px solid var(--border); }
        .dropzone { border: 2px dashed #475569; border-radius: 12px; padding: 30px 15px; text-align: center; cursor: pointer; transition: all 0.3s; background: rgba(255,255,255,0.02); }
        .dropzone:hover { border-color: var(--primary); background: rgba(37,99,235,0.05); }
        .dropzone input { display: none; }
        .dropzone-icon { font-size: 40px; margin-bottom: 10px; }
        .btn-group { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
        button.btn { padding: 12px 16px; border-radius: 10px; border: none; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; color: white; }
        button.btn-primary { background: var(--primary); }
        button.btn-primary:hover { background: var(--primary-hover); }
        button.btn-success { background: #059669; }
        button.btn-success:hover { background: #047857; }
        button.btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .preview-box { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 250px; background: #0b1120; border-radius: 12px; border: 1px solid var(--border); overflow: hidden; position: relative; }
        canvas#previewCanvas { max-width: 100%; max-height: 380px; object-fit: contain; }
        .results-box { margin-top: 15px; padding: 15px; border-radius: 10px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); display: none; }
        .badge { display: inline-block; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 14px; }
        .badge-fresh { background: rgba(22, 163, 74, 0.2); color: #4ade80; border: 1px solid #16a34a; }
        .badge-rotten { background: rgba(220, 38, 38, 0.2); color: #f87171; border: 1px solid #dc2626; }
        .progress-bar { width: 100%; height: 8px; background: #334155; border-radius: 4px; overflow: hidden; margin-top: 6px; }
        .progress-fill { height: 100%; background: #38bdf8; width: 0%; transition: width 0.5s; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
        th, td { padding: 8px 10px; text-align: right; border-bottom: 1px solid #334155; }
        th { color: #38bdf8; }
        .spinner { display: inline-block; width: 18px; height: 18px; border: 3px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: white; animation: spin 0.8s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🍎 Fruit Vision Dashboard 🍌</h1>
            <p class="subtitle">فحص جودة وصلاحية الفواكه والكشف عن أصنافها ومواقعها بالذكاء الاصطناعي</p>
        </header>

        <div class="main-grid">
            <!-- جانب الرفع والتحكم -->
            <div class="card">
                <div class="dropzone" id="dropzone" onclick="document.getElementById('fileInput').click()">
                    <div class="dropzone-icon">📷</div>
                    <strong>اضغط هنا لاختيار صورة فاكهة</strong>
                    <p style="color: var(--text-muted); font-size: 13px; margin-top: 5px;">أو اسحب وأفلت ملف الصورة هنا (JPG, PNG)</p>
                    <input type="file" id="fileInput" accept="image/*">
                </div>

                <div class="btn-group">
                    <button class="btn btn-primary" id="btnClassify" onclick="runTask('classify')" disabled>
                        🍏 فحص الجودة (طازجة أم تالفة - ResNet18)
                    </button>
                    <button class="btn btn-success" id="btnDetect" onclick="runTask('detect')" disabled>
                        🔍 كشف وتحديد أماكن الفواكه (YOLOv5)
                    </button>
                </div>

                <div style="margin-top: 15px; font-size: 12px; color: var(--text-muted); text-align: center;">
                    💡 نصيحة: يمكنك تجربة صورة <code style="color:#38bdf8; background:#0b1120; padding:2px 6px; border-radius:4px;">apple.png</code> المتوفرة في المجلد.
                </div>
            </div>

            <!-- جانب العرض والنتائج -->
            <div class="card">
                <div class="preview-box">
                    <p id="placeholderText" style="color: var(--text-muted); font-size: 14px;">لم يتم اختيار صورة بعد</p>
                    <canvas id="previewCanvas"></canvas>
                </div>

                <div class="results-box" id="resultsBox">
                    <div id="resultsContent"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedFile = null;
        let originalImage = new Image();
        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('fileInput');
        const btnClassify = document.getElementById('btnClassify');
        const btnDetect = document.getElementById('btnDetect');
        const canvas = document.getElementById('previewCanvas');
        const ctx = canvas.getContext('2d');
        const placeholderText = document.getElementById('placeholderText');
        const resultsBox = document.getElementById('resultsBox');
        const resultsContent = document.getElementById('resultsContent');

        fileInput.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                handleFile(e.target.files[0]);
            }
        });

        dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.style.borderColor = '#2563eb'; });
        dropzone.addEventListener('dragleave', () => { dropzone.style.borderColor = '#475569'; });
        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.style.borderColor = '#475569';
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                handleFile(e.dataTransfer.files[0]);
            }
        });

        function handleFile(file) {
            selectedFile = file;
            btnClassify.disabled = false;
            btnDetect.disabled = false;
            resultsBox.style.display = 'none';

            const reader = new FileReader();
            reader.onload = (e) => {
                originalImage.onload = () => {
                    placeholderText.style.display = 'none';
                    canvas.width = originalImage.width;
                    canvas.height = originalImage.height;
                    ctx.drawImage(originalImage, 0, 0);
                };
                originalImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }

        async function runTask(taskType) {
            if (!selectedFile) return;

            const endpoint = taskType === 'classify' ? '/predict/classify' : '/predict/detect';
            const btn = taskType === 'classify' ? btnClassify : btnDetect;
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span class="spinner"></span> جاري الفحص...';
            btnClassify.disabled = true;
            btnDetect.disabled = true;

            const formData = new FormData();
            formData.append('file', selectedFile);

            try {
                const response = await fetch(endpoint, { method: 'POST', body: formData });
                const data = await response.json();

                // إعادة رسم الصورة الأساسية
                ctx.drawImage(originalImage, 0, 0);
                resultsBox.style.display = 'block';

                if (taskType === 'classify') {
                    const isFresh = data.fruit_condition === 'fresh';
                    resultsContent.innerHTML = `
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span>حالة الفاكهة:</span>
                            <span class="badge ${isFresh ? 'badge-fresh' : 'badge-rotten'}">
                                ${isFresh ? '✅ طازجة (Fresh)' : '❌ فاسدة / تالفة (Rotten)'}
                            </span>
                        </div>
                        <div style="font-size:13px; margin-top:8px;">
                            <span>نسبة الثقة: <strong>${data.confidence}%</strong></span>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${data.confidence}%; background: ${isFresh ? '#22c55e' : '#ef4444'};"></div>
                            </div>
                        </div>
                    `;
                } else if (taskType === 'detect') {
                    const detections = data.detections || [];
                    if (detections.length === 0) {
                        resultsContent.innerHTML = '<p style="color:#f59e0b;">لم يتم كشف أي فواكه واضحة بالصورة.</p>';
                    } else {
                        // رسم الصناديق على Canvas
                        ctx.lineWidth = Math.max(3, Math.round(canvas.width / 250));
                        ctx.font = `bold ${Math.max(16, Math.round(canvas.width / 40))}px Arial`;

                        let tableRows = '';
                        detections.forEach((d) => {
                            const isRotten = d.name.toLowerCase().includes('rotten');
                            const boxColor = isRotten ? '#ef4444' : '#22c55e';

                            // رسم المربع
                            ctx.strokeStyle = boxColor;
                            ctx.strokeRect(d.bbox.xmin, d.bbox.ymin, d.bbox.xmax - d.bbox.xmin, d.bbox.ymax - d.bbox.ymin);

                            // رسم النص فوق المربع
                            const label = `${d.name} (${d.confidence}%)`;
                            ctx.fillStyle = boxColor;
                            const textWidth = ctx.measureText(label).width;
                            const textHeight = Math.max(16, Math.round(canvas.width / 40));
                            ctx.fillRect(d.bbox.xmin, Math.max(0, d.bbox.ymin - textHeight - 4), textWidth + 8, textHeight + 6);
                            ctx.fillStyle = '#ffffff';
                            ctx.fillText(label, d.bbox.xmin + 4, Math.max(textHeight, d.bbox.ymin - 4));

                            tableRows += `
                                <tr>
                                    <td style="color:${boxColor}; font-weight:bold;">${d.name}</td>
                                    <td>${d.confidence}%</td>
                                </tr>
                            `;
                        });

                        resultsContent.innerHTML = `
                            <p style="margin-bottom:8px;">تم كشف <strong>${detections.length}</strong> عنصر في الصورة:</p>
                            <table>
                                <thead><tr><th>الصنف والحالة</th><th>نسبة الثقة</th></tr></thead>
                                <tbody>${tableRows}</tbody>
                            </table>
                        `;
                    }
                }
            } catch (err) {
                resultsBox.style.display = 'block';
                resultsContent.innerHTML = `<p style="color:#ef4444;">حدث خطأ أثناء الاتصال بالخادم: ${err.message}</p>`;
            } finally {
                btn.innerHTML = originalText;
                btnClassify.disabled = false;
                btnDetect.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "resnet_loaded": resnet_model is not None,
        "yolo_loaded": yolo_model is not None
    }

@app.post("/predict/classify")
async def classify_fruit(file: UploadFile = File(...)):
    """
    تصنيف جودة الفاكهة في الصورة بالكامل (طازجة أو فاسدة) باستخدام ResNet-18.
    """
    if resnet_model is None:
        if not load_resnet():
            raise HTTPException(status_code=500, detail="نموذج ResNet-18 غير متوفر أو تعذر تحميله.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="الملف المرفوع ليس صورة صالحة.")

    input_tensor = resnet_transform(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        output = resnet_model(input_tensor)
        probabilities = torch.softmax(output, dim=1)
        conf, pred = torch.max(probabilities, 1)

    predicted_class = CLASSIFICATION_CLASSES[pred.item()]
    confidence_score = round(conf.item() * 100, 2)

    return {
        "fruit_condition": predicted_class,
        "confidence": confidence_score,
        "is_fresh": predicted_class == "fresh",
        "probabilities": {
            "fresh": round(probabilities[0][0].item() * 100, 2),
            "rotten": round(probabilities[0][1].item() * 100, 2)
        }
    }

@app.post("/predict/detect")
async def detect_fruits(file: UploadFile = File(...)):
    """
    كشف جميع الفواكه الموجودة بالصورة وتحديد مربعات الإحاطة (Bounding Boxes) وأصنافها عبر YOLOv5.
    """
    if yolo_model is None:
        if not load_yolo():
            raise HTTPException(status_code=500, detail="نموذج YOLOv5 غير متوفر أو تعذر تحميله.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="الملف المرفوع ليس صورة صالحة.")

    results = yolo_model(image)
    df = results.pandas().xyxy[0]

    detections = []
    for _, row in df.iterrows():
        detections.append({
            "name": row["name"],
            "class_id": int(row["class"]),
            "confidence": round(float(row["confidence"]) * 100, 2),
            "bbox": {
                "xmin": round(float(row["xmin"]), 2),
                "ymin": round(float(row["ymin"]), 2),
                "xmax": round(float(row["xmax"]), 2),
                "ymax": round(float(row["ymax"]), 2)
            }
        })

    return {
        "total_detected": len(detections),
        "detections": detections
    }

@app.post("/predict/inspect")
async def inspect_full(file: UploadFile = File(...)):
    """
    فحص شامل: يدمج الكشف الموضعي وتصنيف الحالة.
    """
    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="الملف المرفوع ليس صورة صالحة.")

    # 1. تصنيف الصورة بالكامل عبر ResNet
    classify_result = None
    if resnet_model or load_resnet():
        input_tensor = resnet_transform(image).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            output = resnet_model(input_tensor)
            probs = torch.softmax(output, dim=1)
            conf, pred = torch.max(probs, 1)
        classify_result = {
            "condition": CLASSIFICATION_CLASSES[pred.item()],
            "confidence": round(conf.item() * 100, 2)
        }

    # 2. كشف العناصر عبر YOLO
    detections = []
    if yolo_model or load_yolo():
        results = yolo_model(image)
        df = results.pandas().xyxy[0]
        for _, row in df.iterrows():
            detections.append({
                "label": row["name"],
                "confidence": round(float(row["confidence"]) * 100, 2),
                "box": [round(float(row["xmin"]), 1), round(float(row["ymin"]), 1),
                        round(float(row["xmax"]), 1), round(float(row["ymax"]), 1)]
            })

    return {
        "status": "success",
        "global_classification": classify_result,
        "detected_objects_count": len(detections),
        "detections": detections
    }

# ==============================================================================
# نقطة نهاية للتوافق مع الإصدار السابق (Backward Compatibility)
# ==============================================================================
@app.post("/predict-image")
async def predict_image_legacy(file: UploadFile = File(...)):
    return await classify_fruit(file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
