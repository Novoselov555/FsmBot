from aiogram import Router, F, Bot
from aiogram.filters import StateFilter, Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup)

from database.database import BotDB
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.kb_abc import keyboard as kb
from lexicon.lexicon import LEXICON
from services.file_handling import book
from states.states import FSMCourse, FSMSecondTest
from config_data.config import load_config, Config


router = Router()
BotDB = BotDB('my_database.db')
config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

bot = Bot(BOT_TOKEN)


@router.message(Command(commands='course'), StateFilter(FSMCourse.course))
async def process_course_start(message: Message, state: FSMContext):
    text = book[BotDB.get_page(message.from_user.id)]
    await message.answer(
        text=text,
        parse_mode='HTML',
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{BotDB.get_page(message.from_user.id)}/{len(book)}',
            'forward'
        )
    )
    await state.set_state(FSMCourse.second_test)


@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    if BotDB.get_page(callback.from_user.id) > 1:
        BotDB.backward_page(callback.from_user.id)
        text = book[BotDB.get_page(callback.from_user.id)]
        await callback.message.edit_text(
            text=text,
            parse_mode='HTML',
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{BotDB.get_page(callback.from_user.id)}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    message_id = callback.message.message_id
    chat_id = callback.from_user.id
    BotDB.add_id(chat_id, message_id)
    if BotDB.get_page(callback.from_user.id) < 7:
        BotDB.forward_page(callback.from_user.id)
        text = book[BotDB.get_page(callback.from_user.id)]
        await callback.message.edit_text(
            text=text,
            parse_mode='HTML',
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{BotDB.get_page(callback.from_user.id)}/{len(book)}',
                'forward'
            )
        )
    if BotDB.get_page(callback.from_user.id) == 7 and BotDB.get_last_page(callback.from_user.id) == 0:
        BotDB.get_last_page(callback.from_user.id)
        button_first_test_true = InlineKeyboardButton(
            text='Да✔',
            callback_data='pass_second_test'
        )
        button_first_test_false = InlineKeyboardButton(
            text='Нет❌',
            callback_data='not_pass_second_test'
        )
        keyboard: list[list[InlineKeyboardButton]] = [[button_first_test_true, button_first_test_false]]
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await callback.message.answer(
            text=LEXICON['st'],
            reply_markup=markup
        )
    await callback.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    await callback.answer(text='Любопытный самый?')


@router.callback_query(F.data == 'pass_second_test')
async def process_second_test_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    try:
        chat_id = BotDB.get_ch_id(callback.from_user.id)
        message_id = BotDB.get_msg_id(callback.from_user.id)
        await bot.delete_message(chat_id, message_id)
    except TelegramBadRequest as ex:
        if ex.message == "Bad Request: message to delete not found":
            print("Все сообщения удалены🙂")

    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.edit_text(
        text=LEXICON['q1'],
        reply_markup=markup
    )
    await state.set_state(FSMSecondTest.q1)


@router.callback_query(F.data == 'not_pass_second_test')
async def process_second_test_start(callback: CallbackQuery):
    await callback.answer(
        text='Пожалуй, подожду⏰'
    )
