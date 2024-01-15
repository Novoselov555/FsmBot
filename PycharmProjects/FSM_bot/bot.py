from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message)

from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

user_dict: dict[int, dict[str, str | int | bool]] = {}


class FSMFillForm(StatesGroup):
    fill_surname = State()
    fill_grade = State()
    fill_first_test = State()
    fill_wish_data = State()


@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Вас приветствует бот по определению уровня'
                              'Вашей финансовой грамотности.\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform'
                         )


@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего, вы еще не начали опрос\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform'
                         )


@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из заполнения анкеты\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте команду /fillform'
                         )

    await state.clear()


@dp.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите вашу фамилию')

    await state.set_state(FSMFillForm.fill_surname)


@dp.message(StateFilter(FSMFillForm.fill_surname), F.text.isalpha())
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
        text='Спасибо!\n\n А теперь выберите класс обучения:',
        reply_markup=markup
    )
    await state.set_state(FSMFillForm.fill_grade)


@dp.message(StateFilter(FSMFillForm.fill_surname))
async def warning_not_surname(message: Message):
    await message.answer(text='То, что вы отправили не похоже на фамилию\n\n'
                              'Пожалуйста, введите вашу фамилию\n\n'
                              'Если вы хотите прервать заполнение анкеты - '
                              'отправьте команду /cancel'
                         )


@dp.callback_query(StateFilter(FSMFillForm.fill_grade),
                   F.data.in_['grade_7', 'grade_11'])
async def process_grade_pass(callback: CallbackQuery, state: FSMContext):
    await state.update_data(grade=callback.data)
    await callback.message.delete()
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
        text='Хотели бы опробовать себя в тесте?',
        reply_markup=markup
    )

    await state.set_state(FSMFillForm.fill_wish_data)


@dp.message(StateFilter(FSMFillForm.fill_grade))
async def warning_not_grade(message: Message):
    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             'при выборе образования\n\nЕсли вы хотите '
             'прервать заполнение анкеты - отправьте '
             'команду /cancel'
    )


@dp.callback_query(StateFilter(FSMFillForm.fill_first_test), F.data.in_['pass_first_test'], ['not_pass_first_test'])
async def process_first_test_pass(callback: CallbackQuery, state: FSMContext):
    await state.update_data(first_test=callback.data)
    yes_data_button = InlineKeyboardButton(
        text='Да',
        callback_data='yes_data'
    )
    no_data_button = InlineKeyboardButton(
        text='Нет',
        callback_data='no_data'
    )
    keyboard: list[list[InlineKeyboardButton]] = [[yes_data_button], [no_data_button]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await callback.message.answer(
        text='Спасибо!\n\n'
             'Остался последний шаг.\n'
             'Хотели бы вы получать новости?',
        reply_markup=markup
    )

    await state.set_state(FSMFillForm.fill_wish_data)


@dp.message(StateFilter(FSMFillForm.fill_first_test))
async def warning_not_first_test(message: Message):
    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             'при выборе образования\n\nЕсли вы хотите '
             'прервать заполнение анкеты - отправьте '
             'команду /cancel'
    )


@dp.callback_query(StateFilter(FSMFillForm.fill_wish_data), F.data.in_['yes_data', 'no_data'])
async def process_fill_data_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(wish_data=callback.data == 'yes_data')
    user_dict[callback.from_user.id] = await state.get_data()
    await state.clear()
    await callback.message.edit_text(
        text='Спасибо! Ваши данные сохранены!\n\n'
             'Вы вышли из опроса'
    )

    await callback.message.answer(
        text='Чтобы посмотреть данные вашей '
             'анкеты - отправьте команду /showdata'
    )


@dp.message(StateFilter(FSMFillForm.fill_wish_data))
async def process_showdata_command(message: Message):
    if message.from_user.id in user_dict:
        await message.answer(
            text=f'Имя: {user_dict[message.from_user.id]["surname"]} \n'
                 f'Класс: {user_dict[message.from_user.id]["grade"]}\n'
            f'Соглашение на тест: {user_dict[message.from_user.id]["first_test"]}\n'
            f'Ваши данные: {user_dict[message.from_user.id]["wish_data"]}\n'
        )
    else:
        await message.answer(
            text='Вы еще не заполняли анкету. '
                 'Чтобы приступить - отправьте '
                 'команду /fillform'
        )


@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, моя твоя не понимать')


if __name__ == '__main__':
    dp.run_polling(bot)