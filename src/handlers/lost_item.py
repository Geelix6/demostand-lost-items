from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.inline import retry_kb
from models.db import SessionLocal
from services.embeddings import get_embedding
from services.search import semantic_search
from state.lost_state import LostState
from utils.md import md_escape


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

    await message.answer("Пожалуйста, подождите... Идёт поиск вещей по вашему описанию 🔍")

    query_emb = get_embedding(desc)
    async with SessionLocal() as session:
        results = await semantic_search(session, query_emb, limit=5)


    if results:
        reply_lines = ["*Найдены возможные совпадения:*\n"]
        for item in results:
            lost_date = item.date_lost.strftime('%d.%m.%Y')
            reply_lines.append(f"*Дата находки:* {md_escape(lost_date)}")
            reply_lines.append(f"*Станция метро:* {md_escape(item.station)}")
            reply_lines.append(f"*Описание вещи:* {md_escape(item.description)}")
            reply_lines.append("")
        reply = "\n".join(reply_lines).strip()
    else:
        reply = "Совпадений не найдено."

    await message.answer(reply, parse_mode="MarkdownV2")
    await message.answer(
        "Если вашей вещи нет в похожих, попробуйте поискать ещё раз:",
        reply_markup=retry_kb
    )

    await state.clear()
