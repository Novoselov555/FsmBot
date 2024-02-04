from aiogram import F, Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message)

from config_data.config import load_config, Config
from database.database import BotDB
from lexicon.lexicon import LEXICON
from states.states import FSMFillForm, FSMFirstTest

router = Router()
BotDB = BotDB('my_database.db')
config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

bot = Bot(BOT_TOKEN)


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON['/cancel'])


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext, bot: Bot):
    await message.answer(text=LEXICON['/cancel_state'])
    try:
        # Все сообщения, начиная с текущего и до первого (message_id = 0)
        for i in range(message.message_id, 0, -1):
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        # Если сообщение не найдено (уже удалено или не существует),
        # код ошибки будет "Bad Request: message to delete not found"
        if ex.message == "Bad Request: message to delete not found":
            print("Все сообщения удалены🙂")
    BotDB.del_row(message.from_user.id)
    await state.clear()


@router.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    await message.answer(text=LEXICON['surname'])
    await state.set_state(FSMFillForm.fill_surname)


@router.message(StateFilter(FSMFillForm.fill_surname), F.text.isalpha())
async def process_surname_sent(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    button_7 = InlineKeyboardButton(
        text='7 класс',
        callback_data='grade_7'
    )
    button_11 = InlineKeyboardButton(
        text='11 класс',
        callback_data='grade_11'
    )
    keyboard: list[list[InlineKeyboardButton]] = [[button_7], [button_11]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(
        text=LEXICON['grade'],
        reply_markup=markup
    )
    await state.set_state(FSMFillForm.fill_grade)


@router.message(StateFilter(FSMFillForm.fill_surname))
async def warning_not_surname(message: Message):
    await message.answer(text=LEXICON['not_surname'])


@router.callback_query(StateFilter(FSMFillForm.fill_grade),
                       F.data.in_(['grade_7', 'grade_11']))
async def process_grade_pass(callback: CallbackQuery, state: FSMContext):
    await state.update_data(grade=callback.data)
    button_first_test_true = InlineKeyboardButton(
        text='Да',
        callback_data='pass_first_test'
    )
    button_first_test_false = InlineKeyboardButton(
        text='Нет',
        callback_data='not_pass_first_test'
    )
    keyboard: list[list[InlineKeyboardButton]] = [[button_first_test_true], [button_first_test_false]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await callback.message.edit_text(
        text=LEXICON['first_test'],
        reply_markup=markup
    )

    await state.set_state(FSMFillForm.fill_first_test)


@router.message(StateFilter(FSMFillForm.fill_grade))
async def warning_not_grade(message: Message):
    await message.answer(
        text=LEXICON['not_grade'])


@router.callback_query(StateFilter(FSMFillForm.fill_first_test), F.data.in_(['pass_first_test', 'not_pass_first_test']))
async def process_first_test_pass(callback: CallbackQuery, state: FSMContext):
    await state.update_data(first_test=callback.data)
    if callback.data == 'pass_first_test':
        data = await state.get_data()
        surname = data.get("surname")
        grade = int(data.get("grade").split('_')[-1])
        first_test = data.get("first_test")
        BotDB.add_data(surname, grade, first_test, 0, 0, 1, 0, 0, 0, callback.from_user.id)

        await callback.message.edit_text(
            text='Спасибо! Ваши данные сохранены!✔'
        )

        a_button_1 = InlineKeyboardButton(
            text='a)',
            callback_data='a_but_1'
        )
        b_button_1 = InlineKeyboardButton(
            text='b)',
            callback_data='b_but_1'
        )
        c_button_1 = InlineKeyboardButton(
            text='c)',
            callback_data='c_but_1'
        )
        keyboard: list[list[InlineKeyboardButton]] = [[a_button_1, b_button_1, c_button_1]]
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await callback.message.answer(
            text=LEXICON['first_question'],
            reply_markup=markup
        )
        await state.set_state(FSMFirstTest.first_question)
    else:
        BotDB.del_row(callback.from_user.id)
        await callback.message.edit_text(
            text='Ну вот, а я думал, что вы захотите участвовать в моем тесте(((\n\n'
                 'Может, попробуем еще раз?🙃\n'
                 'Для этого введите команду /fillform'
        )
        await state.clear()


@router.message(StateFilter(FSMFillForm.fill_first_test))
async def warning_not_first_test(message: Message):
    await message.answer(
        text=LEXICON['not_first_test'])
