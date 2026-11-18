from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.lib.colors import Color, black, gray
import arabic_reshaper
from bidi.algorithm import get_display

# تسجيل الخطوط العربية
pdfmetrics.registerFont(TTFont('Arabic', 'arial.ttf'))  # تأكد من وجود ملف الخط
pdfmetrics.registerFont(TTFont('ArabicBold', 'arialbd.ttf'))  # الخط العريض

# إعدادات الخطوط
addMapping('Arabic', 0, 0, 'Arabic')
addMapping('Arabic', 1, 0, 'ArabicBold')

# دالة لإعادة تشكيل النص العربي
def arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# إنشاء المستند
doc = SimpleDocTemplate("ملخص_8051.pdf", pagesize=A4,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=72)

# أنماط النصوص
styles = getSampleStyleSheet()

# أنماط مخصصة للعناوين العربية
title_style = ParagraphStyle(
    'ArabicTitle',
    parent=styles['Title'],
    fontName='ArabicBold',
    fontSize=24,
    alignment=TA_RIGHT,
    spaceAfter=30,
    textColor=Color(0, 0, 0.6)  # أزرق داكن
)

heading1_style = ParagraphStyle(
    'ArabicHeading1',
    parent=styles['Heading1'],
    fontName='ArabicBold',
    fontSize=18,
    alignment=TA_RIGHT,
    spaceBefore=20,
    spaceAfter=15,
    textColor=Color(0.2, 0.2, 0.2)
)

heading2_style = ParagraphStyle(
    'ArabicHeading2',
    parent=styles['Heading2'],
    fontName='ArabicBold',
    fontSize=14,
    alignment=TA_RIGHT,
    spaceBefore=15,
    spaceAfter=10,
    textColor=Color(0.3, 0.3, 0.3)
)

# نمط للنص العادي
normal_style = ParagraphStyle(
    'ArabicNormal',
    parent=styles['Normal'],
    fontName='Arabic',
    fontSize=11,
    alignment=TA_RIGHT,
    spaceAfter=8,
    leading=14
)

# نمط للأكواد
code_style = ParagraphStyle(
    'CodeStyle',
    parent=styles['Code'],
    fontName='Courier',
    fontSize=9,
    alignment=TA_LEFT,
    backColor=Color(0.95, 0.95, 0.95),
    borderColor=gray,
    borderWidth=1,
    borderPadding=5,
    leftIndent=20,
    rightIndent=20
)

# قائمة بالعناصر
story = []

# العنوان الرئيسي
title = arabic_text("🧠 خريطة ذهنية: تعليمات التكرار والقفز في متحكم 8051")
story.append(Paragraph(title, title_style))
story.append(Spacer(1, 30))

# الفقرة 1: التكرار
story.append(Paragraph(arabic_text("## 1. **التكرار (Loops) | Looping**"), heading1_style))

# قائمة النقاط
loop_points = [
    arabic_text("**التعريف | Definition:** تكرار تسلسل من التعليمات عدداً محدداً من المرات."),
    arabic_text("**الأهداف | Objectives:**"),
    arabic_text("  • تنفيذ إجراء بشكل متكرر"),
    arabic_text("  • تقليل حجم الكود"),
    arabic_text("  • التحكم في عدد مرات التنفيذ"),
    arabic_text("**المكونات الأساسية | Key Components:**"),
    arabic_text("  • سجل عداد (مثل R0–R7 أو موقع في RAM)"),
    arabic_text("  • تعليمة `DJNZ` (خفض السجل والقفز إذا لم يكن صفراً)"),
    arabic_text("**مثال تطبيقي | Example:**")
]

for point in loop_points:
    story.append(Paragraph(point, normal_style))
    story.append(Spacer(1, 5))

# مثال الكود
code_example = """MOV A,#0       ; A=0
MOV R2,#10     ; R2=10 (عداد)
AGAIN: ADD A,#03 ; أضف 3 إلى A
DJNZ R2,AGAIN ; كرر حتى R2=0
MOV R5,A       ; احفظ الناتج في R5"""
story.append(Paragraph(code_example, code_style))
story.append(Spacer(1, 20))

# الفقرة 2: التكرار المتداخل
story.append(Paragraph(arabic_text("## 2. **التكرار المُتداخل (Nested Loops)**"), heading1_style))

nested_points = [
    arabic_text("**التعريف:** تكرار بداخل تكرار (Loop inside a loop)"),
    arabic_text("**الأهداف:**"),
    arabic_text("  • تنفيذ عمليات تتطلب أكثر من 255 تكراراً"),
    arabic_text("  • زيادة مرونة التحكم في التكرار"),
    arabic_text("**المكونات:**"),
    arabic_text("  • سجلات متعددة للعد (مثل R2، R3)"),
    arabic_text("**مثال تطبيقي:**")
]

for point in nested_points:
    story.append(Paragraph(point, normal_style))
    story.append(Spacer(1, 5))

nested_code = """MOV A,#55H
MOV R3,#10      ; عداد الحلقة الخارجية
NEXT: MOV R2,#70 ; عداد الحلقة الداخلية
AGAIN: CPL A     ; متمم المسجل A
DJNZ R2,AGAIN  ; كرر 70 مرة
DJNZ R3,NEXT   ; كرر الحلقة الخارجية 10 مرات"""
story.append(Paragraph(nested_code, code_style))
story.append(Spacer(1, 20))

# الفقرة 3: القفز الشرطي
story.append(Paragraph(arabic_text("## 3. **القفز الشرطي (Conditional Jumps)**"), heading1_style))

conditional_points = [
    arabic_text("**التعريف:** القفز إلى عنوان محدد إذا تحقق شرط معين"),
    arabic_text("**الأهداف:**"),
    arabic_text("  • اتخاذ قرارات في البرنامج"),
    arabic_text("  • توجيه سير التنفيذ بناءً على الحالة"),
    arabic_text("**أنواع التعليمات | Instruction Types:**"),
    arabic_text("  • **JZ**: القفز إذا كان A = 0"),
    arabic_text("  • **JNZ**: القفز إذا كان A ≠ 0"),
    arabic_text("  • **JC**: القفز إذا كان CY = 1"),
    arabic_text("  • **JNC**: القفز إذا كان CY = 0"),
    arabic_text("  • **JB**: القفز إذا كان البت = 1"),
    arabic_text("  • **JNB**: القفز إذا كان البت = 0"),
    arabic_text("**مثال (JZ):**")
]

for point in conditional_points:
    story.append(Paragraph(point, normal_style))
    story.append(Spacer(1, 5))

conditional_code = """MOV A,R0
JZ OVER     ; إذا كان A=0 اقفز إلى OVER
MOV A,R1
OVER: ..."""
story.append(Paragraph(conditional_code, code_style))
story.append(Spacer(1, 20))

# الفقرة 4: القفز غير الشرطي
story.append(Paragraph(arabic_text("## 4. **القفز غير الشرطي (Unconditional Jumps)**"), heading1_style))

unconditional_points = [
    arabic_text("**التعريف:** نقل التحكم إلى عنوان هدف بشكل غير مشروط"),
    arabic_text("**الأنواع:**"),
    arabic_text("  • **LJMP** (قفز طويل): 3 بايت، يستهدف أي عنوان ضمن 64K"),
    arabic_text("  • **SJMP** (قفز قصير): 2 بايت، مدى -128 إلى +127 بايت من PC الحالي"),
    arabic_text("**الأهداف:**"),
    arabic_text("  • الانتقال إلى أجزاء أخرى من البرنامج"),
    arabic_text("  • تنظيم سير التنفيذ")
]

for point in unconditional_points:
    story.append(Paragraph(point, normal_style))
    story.append(Spacer(1, 5))

story.append(PageBreak())

# الفقرة 5: تعليمات الاستدعاء
story.append(Paragraph(arabic_text("## 5. **تعليمات الاستدعاء (CALL Instructions)**"), heading1_style))

call_points = [
    arabic_text("**التعريف:** استدعاء برنامج فرعي (Subroutine)"),
    arabic_text("**الأهداف:**"),
    arabic_text("  • تنظيم البرنامج إلى وحدات نمطية"),
    arabic_text("  • إعادة استخدام الكود"),
    arabic_text("  • توفير ذاكرة البرنامج"),
    arabic_text("**الأنواع:**"),
    arabic_text("  • **LCALL**: استدعاء طويل (3 بايت)، أي عنوان ضمن 64K"),
    arabic_text("  • **ACALL**: استدعاء مطلق (2 بايت)، نطاق 2K بايت"),
    arabic_text("**مثال (LCALL):**")
]

for point in call_points:
    story.append(Paragraph(point, normal_style))
    story.append(Spacer(1, 5))

call_code = """BACK: MOV A,#55H
      MOV P1,A
      LCALL DELAY   ; استدعاء برنامج التأخير
      MOV A,#0AAH
      MOV P1,A
      LCALL DELAY
      SJMP BACK

DELAY: MOV R5,#0FFH
AGAIN: DJNZ R5,AGAIN
       RET          ; العودة من البرنامج الفرعي"""
story.append(Paragraph(call_code, code_style))
story.append(Spacer(1, 20))

# الفقرة 6: تأخير الزمن
story.append(Paragraph(arabic_text("## 6. **تأخير الزمن (Time Delay)**"), heading1_style))

delay_points = [
    arabic_text("**العناصر المؤثرة | Factors:**"),
    arabic_text("  • تردد الكوارتز (Crystal Frequency)"),
    arabic_text("  • عدد دورات الآلة لكل تعليمة"),
    arabic_text("**حساب وقت التأخير | Delay Calculation:**"),
    arabic_text("  • وقت دورة الآلة = 1 / (تردد الكوارتز / دورات الآلة)"),
    arabic_text("  • زمن التنفيذ = عدد دورات الآلة × وقت دورة الآلة"),
    arabic_text("**مثال (XTAL = 11.0592 MHz):**"),
    arabic_text("دورة الآلة = 1 / (11.0592MHz / 12) = 1.085μs"),
    arabic_text("تعليمة DJNZ تستغرق دورتي آلة → 2 × 1.085 = 2.17μs")
]

for point in delay_points:
    story.append(Paragraph(point, normal_style))
    story.append(Spacer(1, 5))

story.append(Spacer(1, 20))

# الفقرة 7: زيادة التأخير
story.append(Paragraph(arabic_text("## 7. **زيادة التأخير (Increasing Delay)**"), heading1_style))

increase_points = [
    arabic_text("**التقنيات | Techniques:**"),
    arabic_text("  • استخدام حلقات متداخلة (Nested Loops)"),
    arabic_text("  • إضافة تعليمات NOP"),
    arabic_text("**مثال باستخدام NOP:**")
]

for point in increase_points:
    story.append(Paragraph(point, normal_style))
    story.append(Spacer(1, 5))

nop_code = """DELAY: MOV R3,#250
HERE:  NOP
       NOP
       NOP
       NOP
       DJNZ R3,HERE
       RET"""
story.append(Paragraph(nop_code, code_style))
story.append(Spacer(1, 20))

# الفقرة 8: الاختلافات بين إصدارات 8051
story.append(Paragraph(arabic_text("## 8. **الاختلافات بين إصدارات 8051**"), heading1_style))

versions_points = [
    arabic_text("**العوامل المؤثرة على التأخير:**"),
    arabic_text("  1. تردد الكوارتز"),
    arabic_text("  2. عدد دورات الآلة لكل تعليمة (يختلف باختلاف الطراز)"),
    arabic_text("**أمثلة لعدد دورات الآلة:**"),
    arabic_text("  • AT89C51: 12 دورة"),
    arabic_text("  • P89C54X2: 6 دورات"),
    arabic_text("  • DS5000: 4 دورات"),
    arabic_text("  • DS89C4x0: 1 دورة")
]

for point in versions_points:
    story.append(Paragraph(point, normal_style))
    story.append(Spacer(1, 5))

story.append(Spacer(1, 30))

# ملاحظات هامة
story.append(Paragraph(arabic_text("## ✨ **ملاحظات هامة | Key Notes:**"), heading2_style))

notes_points = [
    arabic_text("• كل برنامج فرعي يجب أن ينتهي بـ **RET**"),
    arabic_text("• يمكن استخدام **PUSH/POP** لحفظ واستعادة السجلات في البرامج الفرعية"),
    arabic_text("• القفزات الشرطية كلها **قصيرة المدى** (-128 إلى +127 بايت)"),
    arabic_text("• استخدام **ACALL** بدلاً من **LCALL** يوفر مساحة إذا كان البرنامج الفرعي ضمن نطاق 2K")
]

for point in notes_points:
    story.append(Paragraph(point, normal_style))
    story.append(Spacer(1, 8))

story.append(Spacer(1, 30))

# خاتمة
conclusion = arabic_text("""
هذا الملخص يتبع نفس **الهيكل المنظم** و**التنسيق الواضح** و**الترقيم الهرمي** الذي طلبته، مع الحفاظ على **الجوهر العلمي** و**الاختصار الدقيق** للمعلومات. يمكن تطبيق هذا النموذج على أي مادة أخرى بسهولة.
""")
story.append(Paragraph(conclusion, normal_style))

# إنشاء ملف PDF
try:
    doc.build(story)
    print("تم إنشاء ملف PDF بنجاح: 'ملخص_8051.pdf'")
except Exception as e:
    print(f"حدث خطأ أثناء إنشاء ملف PDF: {e}")