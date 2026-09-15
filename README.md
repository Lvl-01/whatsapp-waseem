# واتس حرب

نسخة معدلة:
- الواجهات ليست داخل إطار جوال
- صفحة رمز التحقق تحتوي على 6 خانات منفصلة

المسارات:
- `/`
- `/verify/{id}`
- `/thanks/{id}`
- `/admin`

Start Command:
uvicorn app:app --host 0.0.0.0 --port $PORT
