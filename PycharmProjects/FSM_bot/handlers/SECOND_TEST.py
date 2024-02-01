from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardMarkup, Message)

from database.database import BotDB
from keyboards.kb_abc import keyboard
from lexicon.lexicon import LEXICON
from states.states import FSMSecondTest

router = Router()
BotDB = BotDB('my_database.db')


@router.callback_query(StateFilter(FSMSecondTest.q1), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_first_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q1=callback.data)
    if callback.data == 'c_but_1':
        BotDB.add_scores2(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['q2'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q2)


@router.message(StateFilter(FSMSecondTest.q1))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMSecondTest.q2), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_second_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q2=callback.data)
    if callback.data == 'a_but_1':
        BotDB.add_scores2(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['q3'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q3)


@router.message(StateFilter(FSMSecondTest.q2))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMSecondTest.q3), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_third_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q3=callback.data)
    if callback.data == 'c_but_1':
        BotDB.add_scores2(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['q4'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q4)


@router.message(StateFilter(FSMSecondTest.q3))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMSecondTest.q4), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_fourth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q4=callback.data)
    if callback.data == 'c_but_1':
        BotDB.add_scores2(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['q5'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q5)


@router.message(StateFilter(FSMSecondTest.q4))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMSecondTest.q5), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_fifth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q5=callback.data)
    if callback.data == 'b_but_1':
        BotDB.add_scores2(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['q6'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q6)


@router.message(StateFilter(FSMSecondTest.q5))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMSecondTest.q6), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_sixth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q6=callback.data)
    if callback.data == 'a_but_1':
        BotDB.add_scores2(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['q7'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q7)


@router.message(StateFilter(FSMSecondTest.q6))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMSecondTest.q7), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_seventh_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q7=callback.data)
    if callback.data == 'b_but_1':
        BotDB.add_scores2(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['q8'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q8)


@router.message(StateFilter(FSMSecondTest.q7))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMSecondTest.q8), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_eighth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q8=callback.data)
    if callback.data == 'a_but_1':
        BotDB.add_scores2(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['q9'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q9)


@router.message(StateFilter(FSMSecondTest.q8))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMSecondTest.q9), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_ninth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q9=callback.data)
    if callback.data == 'a_but_1':
        BotDB.add_scores2(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['q10'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q10)


@router.message(StateFilter(FSMSecondTest.q9))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMSecondTest.q10), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_tenth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q10=callback.data)
    if callback.data == 'c_but_1':
        BotDB.add_scores2(callback.from_user.id)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    scores2 = BotDB.get_scores2(callback.from_user.id)
    await callback.message.answer(
        text='Вы закончили заключительный тест!🙌\n\n'
             f'Ваши баллы: {scores2}\n\n'
    )
    if BotDB.get_scores(callback.from_user.id) > BotDB.get_scores2(callback.from_user.id):
        await callback.message.answer(
            text='Да, результат упал, но ничего страшного, Вы все равно молодец!💪'
        )
    elif BotDB.get_scores(callback.from_user.id) < BotDB.get_scores2(callback.from_user.id):
        await callback.message.answer(
            text='Ваш результат увеличился, так держать🤓'
        )
    else:
        await callback.message.answer(
            text='Результаты тестов одинаковы. Стабильность - признак мастерства☺'
        )


@router.message(StateFilter(FSMSecondTest.q10))
async def warning_not_question(message: Message):
    await message.answer(
        text=LEXICON['not_question'])