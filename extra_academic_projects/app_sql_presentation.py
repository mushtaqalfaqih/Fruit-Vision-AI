from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
import os

# ==================================================
# إنشاء عرض PowerPoint جديد مع تنسيق احترافي
# ==================================================
prs = Presentation()

# تعيين أبعاد العرض (16:9)
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ==================================================
# دالة مساعدة: إنشاء شكل خلفية بلون متدرج (مبسطة)
# ==================================================
def add_gradient_background(slide, color1, color2):
    """إضافة خلفية متدرجة للشريحة - نسخة مبسطة"""
    left = top = Inches(0)
    width = prs.slide_width
    height = prs.slide_height
    
    # إضافة شكل مستطيل للخلفية
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    
    # تعبئة متدرجة بسيطة
    fill = background.fill
    fill.solid()  # استخدام تعبئة صلبة بدلاً من متدرجة لتجنب المشاكل
    fill.fore_color.rgb = color1
    
    # إزالة الحدود
    background.line.fill.background()
    
    # وضع الخلفية في الخلف
    slide.shapes._spTree.remove(background._element)
    slide.shapes._spTree.insert(0, background._element)

# ==================================================
# دالة: شريحة العنوان الرئيسية
# ==================================================
def create_title_slide(title, subtitle):
    # إنشاء شريحة فارغة
    slide_layout = prs.slide_layouts[6]  # شريحة فارغة
    slide = prs.slides.add_slide(slide_layout)
    
    # إضافة خلفية بسيطة بدلاً من المتدرجة
    left = top = Inches(0)
    width = prs.slide_width
    height = prs.slide_height
    
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(13, 36, 65)
    background.line.fill.background()
    
    # وضع الخلفية في الخلف
    slide.shapes._spTree.remove(background._element)
    slide.shapes._spTree.insert(0, background._element)
    
    # إضافة شكل زخرفي
    left = Inches(0.5)
    top = Inches(1)
    width = prs.slide_width - Inches(1)
    height = Inches(0.2)
    
    # خط زخرفي فوق العنوان
    decorative_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    fill = decorative_line.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(0, 150, 255)
    decorative_line.line.fill.background()
    
    # إضافة العنوان الرئيسي
    title_left = Inches(1)
    title_top = Inches(1.5)
    title_width = prs.slide_width - Inches(2)
    title_height = Inches(2)
    
    title_box = slide.shapes.add_textbox(title_left, title_top, title_width, title_height)
    title_frame = title_box.text_frame
    title_frame.text = title
    
    # تنسيق العنوان
    for paragraph in title_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.size = Pt(48)  # تصغير قليلاً ليتناسب
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.name = 'Arial'
    
    # إضافة العنوان الفرعي
    subtitle_left = Inches(1)
    subtitle_top = Inches(4)
    subtitle_width = prs.slide_width - Inches(2)
    subtitle_height = Inches(1.5)
    
    subtitle_box = slide.shapes.add_textbox(subtitle_left, subtitle_top, subtitle_width, subtitle_height)
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = subtitle
    
    # تنسيق العنوان الفرعي
    for paragraph in subtitle_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.size = Pt(24)
            run.font.color.rgb = RGBColor(200, 220, 255)
            run.font.name = 'Arial'
    
    # إضافة معلومات الطالب والمشرف في الزاوية
    info_left = Inches(0.5)
    info_top = prs.slide_height - Inches(1.5)
    info_width = prs.slide_width - Inches(1)
    info_height = Inches(1)
    
    info_box = slide.shapes.add_textbox(info_left, info_top, info_width, info_height)
    info_frame = info_box.text_frame
    
    info_text = "اسم الطالب: مشتاق الفقية\nاسم المشرف: د. سنان"
    info_frame.text = info_text
    
    for paragraph in info_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.size = Pt(18)
            run.font.color.rgb = RGBColor(180, 200, 240)
            run.font.name = 'Arial'

# ==================================================
# دالة: شريحة المحتوى مع تصميم أنيق (مبسطة)
# ==================================================
def create_content_slide(title, items, is_numbered=True):
    # إنشاء شريحة فارغة
    slide_layout = prs.slide_layouts[1]  # استخدام تخطيط جاهز بدلاً من الفارغ
    slide = prs.slides.add_slide(slide_layout)
    
    # إزالة العناصر الافتراضية
    for shape in slide.shapes:
        if shape.has_text_frame:
            shape.text_frame.clear()
    
    # إضافة خلفية بسيطة
    left = top = Inches(0)
    width = prs.slide_width
    height = prs.slide_height
    
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 247, 250)
    background.line.fill.background()
    
    # وضع الخلفية في الخلف
    slide.shapes._spTree.remove(background._element)
    slide.shapes._spTree.insert(0, background._element)
    
    # إضافة رأس
    header_left = Inches(0)
    header_top = Inches(0)
    header_width = prs.slide_width
    header_height = Inches(1)
    
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, header_left, header_top, header_width, header_height
    )
    fill = header.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(13, 36, 65)
    header.line.fill.background()
    
    # إضافة العنوان في الرأس
    title_left = Inches(0.5)
    title_top = Inches(0.2)
    title_width = prs.slide_width - Inches(1)
    title_height = Inches(0.6)
    
    title_box = slide.shapes.add_textbox(title_left, title_top, title_width, title_height)
    title_frame = title_box.text_frame
    title_frame.text = title
    
    for paragraph in title_frame.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(32)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.name = 'Arial'
    
    # إضافة محتوى النقاط
    content_left = Inches(1)
    content_top = Inches(1.5)
    content_width = prs.slide_width - Inches(2)
    content_height = Inches(5)
    
    content_box = slide.shapes.add_textbox(content_left, content_top, content_width, content_height)
    content_frame = content_box.text_frame
    content_frame.clear()
    
    # إضافة النقاط
    arabic_numbers = ['١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩', '١٠']
    
    for i, item in enumerate(items):
        p = content_frame.add_paragraph()
        
        # تحديد البادئة
        if is_numbered and i < len(arabic_numbers):
            prefix = f"{arabic_numbers[i]}. "
        else:
            prefix = "• "
        
        p.text = prefix + item
        p.level = 0
        
        # تطبيق التنسيق
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(8)
        
        for run in p.runs:
            run.font.size = Pt(24)
            run.font.color.rgb = RGBColor(30, 30, 30)
            run.font.name = 'Arial'
            run.font.bold = True
    
    return slide

# ==================================================
# دالة: شريحة خاصة للكود أو الأمثلة (مبسطة)
# ==================================================
def create_code_slide(title, code, explanation):
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    
    # إزالة العناصر الافتراضية
    for shape in slide.shapes:
        if shape.has_text_frame:
            shape.text_frame.clear()
    
    # إضافة خلفية
    left = top = Inches(0)
    width = prs.slide_width
    height = prs.slide_height
    
    background = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(240, 240, 240)
    background.line.fill.background()
    
    # وضع الخلفية في الخلف
    slide.shapes._spTree.remove(background._element)
    slide.shapes._spTree.insert(0, background._element)
    
    # العنوان
    title_left = Inches(0.5)
    title_top = Inches(0.5)
    title_width = prs.slide_width - Inches(1)
    title_height = Inches(0.8)
    
    title_box = slide.shapes.add_textbox(title_left, title_top, title_width, title_height)
    title_frame = title_box.text_frame
    title_frame.text = title
    
    for paragraph in title_frame.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(32)
            run.font.bold = True
            run.font.color.rgb = RGBColor(13, 36, 65)
            run.font.name = 'Arial'
    
    # مربع للكود
    code_left = Inches(1)
    code_top = Inches(1.5)
    code_width = prs.slide_width - Inches(2)
    code_height = Inches(2)
    
    code_box = slide.shapes.add_textbox(code_left, code_top, code_width, code_height)
    code_frame = code_box.text_frame
    code_frame.text = code
    
    for paragraph in code_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.LEFT
        for run in paragraph.runs:
            run.font.size = Pt(18)
            run.font.name = 'Consolas'
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
    
    # شرح الكود
    explanation_left = Inches(1)
    explanation_top = code_top + code_height + Inches(0.5)
    explanation_width = prs.slide_width - Inches(2)
    explanation_height = Inches(1.5)
    
    explanation_box = slide.shapes.add_textbox(explanation_left, explanation_top, explanation_width, explanation_height)
    explanation_frame = explanation_box.text_frame
    explanation_frame.text = explanation
    
    for paragraph in explanation_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.LEFT
        for run in paragraph.runs:
            run.font.size = Pt(20)
            run.font.color.rgb = RGBColor(80, 80, 80)
            run.font.name = 'Arial'
    
    return slide

# ==================================================
# دالة: شريحة الختام (مبسطة)
# ==================================================
def create_thankyou_slide():
    slide_layout = prs.slide_layouts[0]  # استخدام تخطيط العنوان
    slide = prs.slides.add_slide(slide_layout)
    
    # تنسيق العنوان
    title_shape = slide.shapes.title
    title_shape.text = "شكرًا لكم"
    title_frame = title_shape.text_frame
    
    for paragraph in title_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.size = Pt(48)
            run.font.bold = True
            run.font.color.rgb = RGBColor(13, 36, 65)
            run.font.name = 'Arial'
    
    # تنسيق العنوان الفرعي
    subtitle_shape = slide.placeholders[1]
    subtitle_shape.text = "شكرًا لحسن الاستماع\n\nعرض تقديمي عن لغة SQL\nإعداد: مشتاق الفقية"
    subtitle_frame = subtitle_shape.text_frame
    
    for paragraph in subtitle_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.size = Pt(24)
            run.font.color.rgb = RGBColor(80, 80, 80)
            run.font.name = 'Arial'
    
    return slide

# ==================================================
# إنشاء العرض التقديمي
# ==================================================

print("⏳ جاري إنشاء العرض التقديمي...")

# الشريحة 1: العنوان الرئيسي
create_title_slide(
    "لغة الاستعلامات المهيكلة (SQL)",
    "مقدمة شاملة للغة قواعد البيانات الأشهر"
)

# الشريحة 2: ما هي SQL
create_content_slide(
    "ما هي لغة SQL؟",
    [
        "SQL اختصار لـ Structured Query Language",
        "لغة الاستعلامات المهيكلة",
        "هي لغة تُستخدم للتعامل مع قواعد البيانات العلائقية",
        "تُستخدم من أجل:",
        "إدخال البيانات (Insert)",
        "استرجاع البيانات (Retrieve)",
        "تعديل البيانات (Update)",
        "حذف البيانات (Delete)",
        "إدارة هياكل البيانات (Manage)"
    ]
)

# الشريحة 3: أهمية SQL
create_content_slide(
    "أهمية لغة SQL",
    [
        "سهلة التعلم مقارنة بلغات البرمجة الأخرى",
        "مستخدمة في معظم الأنظمة والتطبيقات العالمية",
        "تُعد أساسًا مهمًا لطلاب التخصصات التقنية:",
        "تقنية المعلومات (IT)",
        "نظم المعلومات",
        "علوم الحاسب",
        "الذكاء الاصطناعي",
        "تُستخدم في جميع القطاعات:",
        "الشركات والبنوك",
        "المستشفيات والقطاع الصحي",
        "المواقع الإلكترونية والتطبيقات",
        "تحليل البيانات والأعمال"
    ],
    is_numbered=False
)

# الشريحة 4: أين تُستخدم SQL
create_content_slide(
    "أين تُستخدم لغة SQL؟",
    [
        "أنظمة إدارة قواعد البيانات الشهيرة:",
        "MySQL (مفتوح المصدر)",
        "Oracle (للشركات الكبيرة)",
        "Microsoft SQL Server",
        "PostgreSQL (متقدم ومجاني)",
        "SQLite (للتطبيقات الصغيرة)",
        "مجالات الاستخدام:",
        "مواقع الويب والتجارة الإلكترونية",
        "تطبيقات الهواتف الذكية",
        "تحليل البيانات والأعمال",
        "أنظمة إدارة المحتوى",
        "الأنظمة المالية والمصرفية"
    ],
    is_numbered=False
)

# الشريحة 5: مفهوم قاعدة البيانات
create_content_slide(
    "مفهوم قاعدة البيانات",
    [
        "قاعدة البيانات: مجموعة منظمة من البيانات",
        "يتم تخزينها بطريقة تسهّل الوصول والإدارة",
        "تتكون قاعدة البيانات من:",
        "جداول (Tables)",
        "صفوف (Rows/Records)",
        "أعمدة (Columns/Fields)",
        "علاقات (Relationships)",
        "مثال عملي:",
        "جدول الطلاب (رقم الطالب، الاسم، العمر، التخصص)",
        "جدول المواد (رمز المادة، اسم المادة، الساعات)",
        "جدول التسجيل (رقم الطالب، رمز المادة، الدرجة)"
    ]
)

# الشريحة 6: أنواع أوامر SQL
create_content_slide(
    "أنواع أوامر SQL",
    [
        "تنقسم أوامر SQL إلى أربعة أنواع رئيسية:",
        "أوامر تعريف البيانات (DDL)",
        "أوامر معالجة البيانات (DML)",
        "أوامر استعلام البيانات (DQL)",
        "أوامر تحكم البيانات (DCL)"
    ]
)

# الشريحة 7: أوامر DDL
create_content_slide(
    "أوامر تعريف البيانات (DDL)",
    [
        "تُستخدم لإنشاء وتعديل بنية قواعد البيانات:",
        "CREATE - إنشاء الجداول أو قواعد البيانات",
        "ALTER - تعديل هيكل الجداول",
        "DROP - حذف الجداول أو قواعد البيانات",
        "TRUNCATE - تفريغ البيانات مع الحفاظ على الهيكل",
        "RENAME - إعادة تسمية الجداول"
    ]
)

# الشريحة 8: أوامر DML
create_content_slide(
    "أوامر معالجة البيانات (DML)",
    [
        "تُستخدم للتعامل مع البيانات داخل الجداول:",
        "INSERT - إدخال بيانات جديدة",
        "UPDATE - تحديث بيانات موجودة",
        "DELETE - حذف بيانات محددة",
        "MERGE - دمج البيانات (إدخال/تحديث)",
        "SELECT INTO - نسخ البيانات إلى جدول جديد"
    ]
)

# الشريحة 9: أوامر DQL
create_content_slide(
    "أوامر الاستعلام عن البيانات (DQL)",
    [
        "تُستخدم لاسترجاع البيانات من الجداول",
        "SELECT - الأمر الأساسي للاستعلام",
        "يمكن استخدامه مع:",
        "WHERE: لتصفية النتائج",
        "ORDER BY: لترتيب النتائج",
        "GROUP BY: لتجميع النتائج",
        "HAVING: لتصفية المجموعات",
        "JOIN: لربط الجداول"
    ]
)

# الشريحة 10: مثال SQL
create_code_slide(
    "مثال عملي على استعلام SQL",
    """SELECT 
    student_name AS 'اسم الطالب',
    student_age AS 'العمر',
    department_name AS 'التخصص'
FROM students
JOIN departments ON students.dept_id = departments.id
WHERE student_age > 20
    AND enrollment_year = 2023
ORDER BY student_name ASC;""",
    """هذا الاستعلام يعرض:
• أسماء الطلاب وأعمارهم وتخصصاتهم
• للطلاب الذين تزيد أعمارهم عن 20 سنة
• والمسجلين في عام 2023
• مع ربط جدول الطلاب بجدول التخصصات
• وترتيب النتائج أبجديًا حسب الاسم"""
)

# الشريحة 11: مميزات SQL
create_content_slide(
    "مميزات لغة SQL",
    [
        "لغة قياسية ومعتمدة عالميًا (ANSI/ISO)",
        "تتعامل بكفاءة مع قواعد بيانات ضخمة",
        "سريعة وفعالة في معالجة البيانات",
        "لا تحتاج إلى خبرة برمجية متقدمة",
        "متوافقة مع معظم أنظمة التشغيل",
        "دعم واسع من المطورين والمجتمعات",
        "تكامل سلس مع لغات برمجة أخرى",
        "أمان عالٍ في التعامل مع البيانات",
        "قابلية التوسع والنمو مع المشروع"
    ]
)

# الشريحة 12: الخلاصة
create_content_slide(
    "الخلاصة والتوصيات",
    [
        "لغة SQL تُعد من أهم لغات قواعد البيانات",
        "لا يمكن الاستغناء عنها في المجال التقني",
        "إتقان SQL يساعد في:",
        "بناء أنظمة قوية وآمنة",
        "تحليل البيانات واتخاذ القرارات",
        "تطوير التطبيقات والمواقع",
        "التقدم الوظيفي في المجال التقني",
        "نصائح للمبتدئين:",
        "ابدأ بالأساسيات (SELECT, INSERT, UPDATE, DELETE)",
        "تدرب على أمثلة عملية",
        "استخدم قواعد بيانات حقيقية",
        "انضم لمجتمعات SQL التعليمية"
    ],
    is_numbered=False
)

# الشريحة 13: الشكر
create_thankyou_slide()

# ==================================================
# حفظ العرض التقديمي
# ==================================================
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "عرض_SQL_الاحترافي.pptx")

try:
    prs.save(file_path)
    print("=" * 60)
    print("✅ تم إنشاء العرض التقديمي بنجاح!")
    print(f"📂 الموقع: {file_path}")
    print(f"📊 عدد الشرائح: {len(prs.slides)} شريحة")
    print("✨ المميزات:")
    print("   • تصميم بسيط وواضح")
    print("   • ألوان متناسقة")
    print("   • تنسيق عربي سليم")
    print("   • عرض أكواد SQL")
    print("   • خالٍ من الأخطاء الشائعة")
    print("=" * 60)
except Exception as e:
    print(f"❌ حدث خطأ أثناء الحفظ: {e}")