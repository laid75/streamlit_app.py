import streamlit as st
import sqlite3
import pandas as pd
from fpdf import FPDF

# إعداد قاعدة البيانات
conn = sqlite3.connect("qa_db.sqlite")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS qa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT,
    category TEXT
)
""")
conn.commit()

# إضافة سؤال
def add_question(question, answer, category):
    c.execute("INSERT INTO qa (question, answer, category) VALUES (?, ?, ?)", 
              (question, answer, category))
    conn.commit()

# البحث
def search_question(keyword, category=None):
    if category and category != "الكل":
        c.execute("SELECT * FROM qa WHERE question LIKE ? AND category=?", (f"%{keyword}%", category))
    else:
        c.execute("SELECT * FROM qa WHERE question LIKE ?", (f"%{keyword}%",))
    return c.fetchall()

# التصدير PDF
def export_pdf():
    c.execute("SELECT question, answer, category FROM qa")
    data = c.fetchall()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for q, a, cat in data:
        pdf.multi_cell(0, 10, f"Q: {q}\nA: {a}\nCategory: {cat}\n---")

    pdf.output("qa_export.pdf")

st.title("📘 نظام إدارة الأسئلة والأجوبة")

menu = ["إضافة سؤال", "بحث", "عرض الجميع", "تصدير PDF"]
choice = st.sidebar.selectbox("اختر", menu)

if choice == "إضافة سؤال":
    q = st.text_area("السؤال")
    a = st.text_area("الجواب")
    cat = st.selectbox("الفئة", ["رياضيات", "علوم", "طب", "تقنية", "أخرى"])
    if st.button("حفظ"):
        add_question(q, a, cat)
        st.success("تمت الإضافة بنجاح!")

elif choice == "بحث":
    keyword = st.text_input("كلمة البحث")
    cat = st.selectbox("الفئة", ["الكل", "رياضيات", "علوم", "طب", "تقنية", "أخرى"])
    result = search_question(keyword, cat)
    st.write(result)

elif choice == "عرض الجميع":
    c.execute("SELECT * FROM qa")
    st.write(c.fetchall())

elif choice == "تصدير PDF":
    if st.button("تصدير"):
        export_pdf()
        st.success("تم إنشاء ملف PDF!")
