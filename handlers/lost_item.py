from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.inline import retry_kb
from state.lost_state import LostState


async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Операция отменена.", reply_markup=None)
    from handlers.start import start_handler
    await start_handler(message)


async def date_handler(message: types.Message, state: FSMContext):
    text = message.text.strip()
    try:
        date_lost = datetime.strptime(text, "%d.%m.%Y").date()
    except ValueError:
        return await message.answer(
            "Неверный формат даты. Пожалуйста, введите ДД.MM.ГГГГ (например: 01.01.2025):"
        )
    await state.update_data(date_lost=date_lost)
    await state.set_state(LostState.station)
    await message.answer("Укажите станцию метро:")


async def station_handler(message: types.Message, state: FSMContext):
    station = message.text.strip()
    await state.update_data(station=station)
    await state.set_state(LostState.description)
    await message.answer("Опишите пропажу:")


async def description_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    date_lost = data["date_lost"]
    station = data["station"]
    desc = message.text.strip()

    results = [{
        "station": station,
        "date_lost": date_lost,
        "description": desc
    }]

    reply = "Возможные совпадения:\n" + "\n".join(
        f"{item['station']} {item['date_lost']} – {item['description'][:50]}…"
        for item in results
    )
    await message.answer(reply)
    await message.answer(
        "Если вашей вещи нет в похожих, попробуйте поискать ещё раз:",
        reply_markup=retry_kb
    )

    await state.clear()
