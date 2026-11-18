import tkinter as tk
from tkinter import filedialog, messagebox
import io, sys

# =========================
# قاموس اللغة العربية
# =========================
AR_TO_PY = {
    "اطبع": "print",
    "اذا": "if",
    "وإلا": "else",
    "بينما": "while",
    "و": "and",
    "او": "or",
    "ليس": "not",
    "صحيح": "True",
    "خطأ": "False",
}

# =========================
# أمثلة جاهزة
# =========================
EXAMPLES = {
    "👋 مرحبا": 'اطبع("مرحبا بك 👋")',

    "🔢 متغيرات": '''
x = 10
y = 5
اطبع(x + y)
''',

    "🔁 حلقة": '''
i = 1
بينما i <= 5:
    اطبع("العدد:", i)
    i = i + 1
''',

    "❓ شرط": '''
age = 17
اذا age >= 18:
    اطبع("بالغ")
وإلا:
    اطبع("غير بالغ")
'''
}

# =========================
# تحويل الكود
# =========================
def translate(code):
    for ar, py in AR_TO_PY.items():
        code = code.replace(ar, py)
    return code

# =========================
# تشغيل الكود
# =========================
def run_code():
    output_box.delete("1.0", tk.END)
    code_ar = editor.get("1.0", tk.END)
    code_py = translate(code_ar)

    buffer = io.StringIO()
    sys.stdout = buffer

    try:
        exec(code_py, {})
    except Exception as e:
        output_box.insert(tk.END, f"❌ خطأ:\n{e}")
    finally:
        sys.stdout = sys.__stdout__

    output_box.insert(tk.END, buffer.getvalue())

# =========================
# ملفات
# =========================
def open_file():
    path = filedialog.askopenfilename(filetypes=[("Arabic Code", "*.ar")])
    if path:
        with open(path, "r", encoding="utf-8") as f:
            editor.delete("1.0", tk.END)
            editor.insert(tk.END, f.read())

def save_file():
    path = filedialog.asksaveasfilename(defaultextension=".ar",
                                        filetypes=[("Arabic Code", "*.ar")])
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", tk.END))

# =========================
# نافذة الأمثلة
# =========================
def open_examples():
    win = tk.Toplevel(root)
    win.title("📚 أمثلة جاهزة")
    win.geometry("300x300")
    win.configure(bg="#1e1e1e")

    def insert_example(code):
        editor.delete("1.0", tk.END)
        editor.insert(tk.END, code)
        win.destroy()

    for title, code in EXAMPLES.items():
        btn = tk.Button(
            win, text=title, font=("Arial", 12),
            bg="#2ecc71", fg="black",
            command=lambda c=code: insert_example(c)
        )
        btn.pack(fill="x", padx=10, pady=5)

# =========================
# الواجهة الرئيسية
# =========================
root = tk.Tk()
root.title("🔥 محرر_نصوص.ar — النسخة المتقدمة")
root.geometry("1000x700")
root.configure(bg="#1e1e1e")

# =========================
# شريط القوائم
# =========================
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="📂 فتح", command=open_file)
file_menu.add_command(label="💾 حفظ", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="❌ خروج", command=root.quit)

menu.add_cascade(label="ملف", menu=file_menu)

menu.add_command(label="📚 أمثلة", command=open_examples)
menu.add_command(label="▶ تشغيل", command=run_code)

# =========================
# شريط الأدوات
# =========================
toolbar = tk.Frame(root, bg="#333")
toolbar.pack(fill="x")

tk.Button(toolbar, text="▶ تشغيل", command=run_code,
          bg="#27ae60", fg="white", font=("Arial", 11)).pack(side="left", padx=5, pady=5)

tk.Button(toolbar, text="📚 أمثلة", command=open_examples,
          bg="#f1c40f", fg="black", font=("Arial", 11)).pack(side="left", padx=5)

# =========================
# محرر النصوص
# =========================
editor = tk.Text(
    root, font=("Consolas", 14),
    bg="#1e1e1e", fg="#ffffff",
    insertbackground="white", undo=True
)
editor.pack(expand=True, fill="both", padx=5, pady=5)

editor.insert(tk.END, 'اطبع("🔥 أهلا بك في محرر_نصوص.ar")')

# =========================
# الإخراج
# =========================
output_box = tk.Text(
    root, height=10,
    bg="#000000", fg="#00ff00",
    font=("Consolas", 12)
)
output_box.pack(fill="x", padx=5, pady=5)

root.mainloop()
