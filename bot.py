from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime

TOKEN = "8560377315:AAFzNlPEKZSg8Ir6BuXfYTKDNwCGrSfsQfA"
ADMIN_ID = 8021746509
ADMIN_USERNAME = "@SWH1x"

keyboard = [
    ["Deposit 💰", "Withdraw 💵"],
    ["Contact Admin 📞"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

user_state = {}
user_data = {}

# ---------- Time Check ----------
def is_working_time():
    now = datetime.now().hour
    return 6 <= now < 26   # 6AM to 12AM

# ---------- Start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ 🙏\n\n"
        "SWH 1xBet Service\n"
        "⏰ Service Time - 6:00AM to 12:00AM\n\n"
        "Service ကိုရွေးပါ။",
        reply_markup=markup
    )

# ---------- Text ----------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # 🔴 Auto Reply (Closed Time)
    if not is_working_time():
        await update.message.reply_text(
            "⏰ Service Closed\n\n"
            "🕕 6AM မှာ ပြန်ဖွင့်ပါမယ်\n"
            "📩 Message ကိုလက်ခံထားပါတယ် 🙏"
        )
        return

    # 💰 Deposit
    if text == "Deposit 💰":
        user_state[user_id] = "waiting_id"
        await update.message.reply_text(
            "Deposit 💰\n\n"
            "KBZPay / WavePay : 09679636831\n\n"
            "👉 1xBet ID ပို့ပါ။"
        )

    elif user_state.get(user_id) == "waiting_id":
        user_data[user_id] = {"xbet_id": text}
        user_state[user_id] = "waiting_screenshot"
        await update.message.reply_text("📷 Screenshot ပို့ပါ")

    # 💵 Withdraw
    elif text == "Withdraw 💵":
        user_state[user_id] = "waiting_withdraw"
        await update.message.reply_text(
            "Withdraw 💵\n\n"
            "👉 Withdraw Code + Phone Number ပို့ပါ\n"
            "Example: 123456 - 09xxxxxxxx"
        )

    elif user_state.get(user_id) == "waiting_withdraw":
        await update.message.reply_text(
            "✅ Request Received\nAdmin စစ်ဆေးပါမည်"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"WITHDRAW\nUser: {user_id}\n{text}"
        )

        user_state[user_id] = None

    # 📞 Contact
    elif text == "Contact Admin 📞":
        await update.message.reply_text(
            f"Admin → {ADMIN_USERNAME}"
        )

# ---------- Photo ----------
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_state.get(user_id) == "waiting_screenshot":
        photo = update.message.photo[-1].file_id
        xbet_id = user_data[user_id]["xbet_id"]

        await update.message.reply_text(
            "✅ Deposit Received\nAdmin စစ်ဆေးပါမည်"
        )

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=f"DEPOSIT\nUser: {user_id}\nID: {xbet_id}"
        )

        user_state[user_id] = None

# ---------- Run ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot running...")
app.run_polling()