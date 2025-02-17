from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# 🔹 تنظیم کلید API (باید API Key خودتو جایگزین کنی)
openai.api_key = "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"

# 🔹 ذخیره اطلاعات چت کاربر
user_sessions = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id")  # شناسایی کاربر
    user_message = data.get("message")

    # اگر کاربر جدید است، ازش درس رو می‌پرسیم
    if user_id not in user_sessions:
        user_sessions[user_id] = {"subject": None}
        return jsonify({"reply": "دانش‌آموز عزیز، در چه درسی مشکل داری؟ 📚"})

    # ذخیره موضوع درس انتخابی
    if user_sessions[user_id]["subject"] is None:
        user_sessions[user_id]["subject"] = user_message
        return jsonify({"reply": f"خیلی خوب! حالا سوالت درباره‌ی {user_message} رو بپرس. 😊"})

    # 🔹 درخواست به OpenAI API برای دریافت پاسخ
    subject = user_sessions[user_id]["subject"]
    prompt = f"یک معلم حرفه‌ای که سوالات دانش‌آموزان درباره‌ی {subject} را به زبان ساده توضیح می‌دهد.\n\nدانش‌آموز: {user_message}\nمعلم:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "تو یک معلم حرفه‌ای هستی که به سوالات درسی پاسخ می‌دهی."},
                  {"role": "user", "content": prompt}]
    )

    bot_reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": bot_reply})



@app.route("/", methods=["GET"])
def home():
    return "API is running!"



if __name__ == "__main__":
    app.run(debug=True)
