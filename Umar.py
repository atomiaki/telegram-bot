1.pip3 install -r requirements.txt
sudo apt install screen
screen -S umarbot
python3 Umar.py
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Текст приветствия
START_TEXT = """Здравствуйте! Я — ваш помощник по справочно-правовой системе «Гарант». 
Выберите, пожалуйста, направление, которое вас интересует:"""

# Варианты направлений
DIRECTIONS = {
    "1": "Для юристов",
    "2": "Для бухгалтеров (коммерческие организации)",
    "3": "Для бухгалтеров (организации, финансируемые из бюджетов различных уровней)",
    "4": "Для специалистов по охране труда",
    "5": "Для специалистов по осуществлению закупок (223-ФЗ)",
    "6": "Для специалистов по осуществлению закупок (44-ФЗ)"
}


# Функция для создания клавиатуры с направлениями
def get_directions_keyboard():
    keyboard = [
        [InlineKeyboardButton(text, callback_data=key)]
        for key, text in DIRECTIONS.items()
    ]
    return InlineKeyboardMarkup(keyboard)


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(START_TEXT, reply_markup=get_directions_keyboard())


# Обработчик выбора направления
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    direction = DIRECTIONS[query.data]
    username = query.from_user.username or query.from_user.full_name

    # Формируем сообщение для пересылки в @garantElia
    message_text = (
        f"Новое обращение:\n"
        f"Направление: {direction}\n"
        f"Пользователь: @{username}"
    )

    # Ссылка на аккаунт @garantElia с предзаполненным сообщением
    garant_elia_link = f"https://t.me/garantElia?start={message_text.replace(' ', '_')}"

    await query.edit_message_text(
        text=f"Вы выбрали: {direction}\n\n"
             f"Пожалуйста, перейдите по ссылке для продолжения:\n"
             f"{garant_elia_link}"
    )


# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


def main() -> None:
    # Создаем Application и передаем токен бота
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_error_handler(error_handler)

    # Запускаем бота
    application.run_polling()


if __name__ == "__main__":
    main()