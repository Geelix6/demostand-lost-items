from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Найти пропажу", callback_data="find_item")]
    ]
)

retry_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Искать ещё раз", callback_data="retry_find")]
    ]
)
