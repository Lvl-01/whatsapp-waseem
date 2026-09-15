# واتس حرب

واجهة تدريبية بصفحات:
- `/` إدخال رقم الجوال
- `/verify/{id}` إدخال رمز التحقق
- `/thanks/{id}` رسالة النجاح
- `/admin` لوحة التحكم

## التشغيل محليًا
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

ثم افتح:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin

## النشر على Render
المشروع يحتوي على:
- `render.yaml`
- `requirements.txt`

ارفع الملفات إلى GitHub ثم أنشئ Web Service على Render.
