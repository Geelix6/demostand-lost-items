from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.inline import start_kb
from state.lost_state import LostState


async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Я помогу найти твою потерянную вещь.",
        reply_markup=start_kb
    )


async def find_callback(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Укажите дату потери в формате ДД.ММ.ГГГГ:")
    await query.answer()
    await state.clear()
    await state.set_state(LostState.date)


async def help_handler(message: types.Message):
    text = (
        "Этот бот поможет найти ваши потерянные вещи\n\n"
        "Список команд:\n"
        "/start — начать поиск: покажет кнопку «Найти пропажу». "
        "Нажмите на эту кнопку, чтобы ввести данные по шагам:\n"
        "1. Дата потери: введите в формате ДД.MM.ГГГГ (например: 01.01.2025)\n"
        "2. Укажите станцию метро\n"
        "3. Опишите пропавшую вещь\n"
        "/cancel — в любой момент отменить ввод и вернуться к старту\n"
        "/help — показать эту справку\n"
    )
    await message.answer(text)
