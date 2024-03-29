from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardMarkup, Message)

from database.database import BotDB
from keyboards.kb_abc import keyboard
from lexicon.lexicon import LEXICON
from states.states import FSMFirstTest, FSMCourse

router = Router()
BotDB = BotDB('my_database.db')
first_test_scores = 0


@router.callback_query(StateFilter(FSMFirstTest.first_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_first_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q1=callback.data)
    if callback.data == 'b_but_1':
        BotDB.add_scores(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['second_question'],
        reply_markup=markup
    )
    await state.set_state(FSMFirstTest.second_question)


@router.message(StateFilter(FSMFirstTest.first_question))
async def warning_not_q1(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMFirstTest.second_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_second_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q2=callback.data)
    if callback.data == 'b_but_1':
        BotDB.add_scores(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['third_question'],
        reply_markup=markup
    )
    await state.set_state(FSMFirstTest.third_question)


@router.message(StateFilter(FSMFirstTest.second_question))
async def warning_not_q2(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMFirstTest.third_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_third_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q3=callback.data)
    if callback.data == 'a_but_1':
        BotDB.add_scores(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['fourth_question'],
        reply_markup=markup
    )
    await state.set_state(FSMFirstTest.fourth_question)


@router.message(StateFilter(FSMFirstTest.third_question))
async def warning_not_q3(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMFirstTest.fourth_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_fourth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q4=callback.data)
    if callback.data == 'a_but_1':
        BotDB.add_scores(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['fifth_question'],
        reply_markup=markup
    )
    await state.set_state(FSMFirstTest.fifth_question)


@router.message(StateFilter(FSMFirstTest.fourth_question))
async def warning_not_q4(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMFirstTest.fifth_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_fifth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q5=callback.data)
    if callback.data == 'b_but_1':
        BotDB.add_scores(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['sixth_question'],
        reply_markup=markup
    )
    await state.set_state(FSMFirstTest.sixth_question)


@router.message(StateFilter(FSMFirstTest.fifth_question))
async def warning_not_q5(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMFirstTest.sixth_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_sixth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q6=callback.data)
    if callback.data == 'b_but_1':
        BotDB.add_scores(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['seventh_question'],
        reply_markup=markup
    )
    await state.set_state(FSMFirstTest.seventh_question)


@router.message(StateFilter(FSMFirstTest.sixth_question))
async def warning_not_q6(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMFirstTest.seventh_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_seventh_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q7=callback.data)
    if callback.data == 'b_but_1':
        BotDB.add_scores(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['eighth_question'],
        reply_markup=markup
    )
    await state.set_state(FSMFirstTest.eighth_question)


@router.message(StateFilter(FSMFirstTest.seventh_question))
async def warning_not_q7(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMFirstTest.eighth_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_eighth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q8=callback.data)
    if callback.data == 'b_but_1':
        BotDB.add_scores(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['ninth_question'],
        reply_markup=markup
    )
    await state.set_state(FSMFirstTest.ninth_question)


@router.message(StateFilter(FSMFirstTest.eighth_question))
async def warning_not_q8(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMFirstTest.ninth_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_ninth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q9=callback.data)
    if callback.data == 'c_but_1':
        BotDB.add_scores(callback.from_user.id)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    await callback.message.answer(
        text=LEXICON['tenth_question'],
        reply_markup=markup
    )
    await state.set_state(FSMFirstTest.tenth_question)


@router.message(StateFilter(FSMFirstTest.ninth_question))
async def warning_not_q9(message: Message):
    await message.answer(
        text=LEXICON['not_question'])


@router.callback_query(StateFilter(FSMFirstTest.tenth_question), F.data.in_(['a_but_1', 'b_but_1', 'c_but_1']))
async def process_tenth_question(callback: CallbackQuery, state: FSMContext):
    await state.update_data(q10=callback.data)
    if callback.data == 'a_but_1':
        BotDB.add_scores(callback.from_user.id)
    text = callback.message.text + '\n\nВаш ответ: {}'.format(callback.data[0])
    await callback.message.edit_text(text=text)
    scores = BotDB.get_scores(callback.from_user.id)
    await callback.message.answer(
        text='Вы закончили тест!🤴\n\n'
             f'Ваши баллы: {scores}\n\n'
             'Переходим к курсу!\n'
             'Нажмите на /course'
    )
    await state.set_state(FSMCourse.course)


@router.message(StateFilter(FSMFirstTest.tenth_question))
async def warning_not_q10(message: Message):
    await message.answer(
        text=LEXICON['not_question'])
