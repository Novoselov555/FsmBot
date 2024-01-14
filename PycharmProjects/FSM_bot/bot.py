from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_surname = State()  # Состояние ожидания ввода имени
    fill_grade = State()  # Состояние ожидания выбора образования
    fill_course = State()  # Состояние ожидания выбора получать ли новости


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(
        text='Заполните анкету о себе\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы не начали заполнять анкету\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из заполнения анкеты\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени
@dp.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите вашу фамилию')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_surname)


# Этот хэндлер будет срабатывать, если введена корректная фамилия
# и переводить в состояние ожидания ввода возраста
@dp.message(StateFilter(FSMFillForm.fill_surname), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(surname=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_grade)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_surname))
async def warning_not_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите ваше имя\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать, если выбран класс
# и переводить в состояние согласия на тест
@dp.callback_query(StateFilter(FSMFillForm.fill_grade),
                   F.data.in_(['yes', 'no']))
async def process_education_grade(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные об образовании по ключу "education"
    await state.update_data(grade=callback.data)
    # Создаем объекты инлайн-кнопок
    yes_test_button = InlineKeyboardButton(
        text='Да!',
        callback_data='yes_test'
    )
    no_test_button = InlineKeyboardButton(
        text='Нет, спасибо',
        callback_data='no_test'
    )
    # Добавляем кнопки в клавиатуру в один ряд
    keyboard: list[list[InlineKeyboardButton]] = [
        [yes_test_button, no_test_button]
    ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Редактируем предыдущее сообщение с кнопками, отправляя
    # новый текст и новую клавиатуру
    await callback.message.edit_text(
        text='Спасибо!\n\n'
             'Остался последний шаг.\n'
             'Хотите ли вы поучаствовать в тесте?',
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора получать новости или нет
    await state.set_state(FSMFillForm.fill_course)


# Этот хэндлер будет срабатывать, если во время выбора образования
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_grade))
async def warning_not_grade(message: Message):
    await message.answer(
        text='Пожалуйста, пользуйтесь кнопками '
             'при выборе класса\n\nЕсли вы хотите '
             'прервать заполнение анкеты - отправьте '
             'команду /cancel'
    )


# Этот хэндлер будет срабатывать на выбор получать или
# не получать новости и выводить из машины состояний
@dp.callback_query(StateFilter(FSMFillForm.fill_course),
                   F.data.in_(['yes_test', 'no_test']))
async def process_wish_test_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем данные о получении новостей по ключу "wish_news"
    await state.update_data(test=callback.data == 'yes_test')
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_dict[callback.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    # Отправляем в чат сообщение о выходе из машины состояний
    await callback.message.edit_text(
        text='Спасибо! Ваши данные сохранены!\n\n'
             'Вы вышли из заполнения анкеты'
    )
    # Отправляем в чат сообщение с предложением посмотреть свою анкету
    await callback.message.answer(
        text='Чтобы посмотреть данные вашей '
             'анкеты - отправьте команду /showdata'
    )


# Этот хэндлер будет срабатывать, если во время согласия на получение
# новостей будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_course))
async def warning_not_test_news(message: Message):
    await message.answer(
        text='Пожалуйста, воспользуйтесь кнопками!\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@dp.message(Command(commands='showdata'), StateFilter(default_state))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in user_dict:
        await message.answer(
            text=f'Фамилия: {user_dict[message.from_user.id]["surname"]}\n'
                 f'Класс: {user_dict[message.from_user.id]["grade"]}\n'
                 f'Получить тест: {user_dict[message.from_user.id]["test"]}'
        )
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(
            text='Вы еще не заполняли анкету. '
                 'Чтобы приступить - отправьте '
                 'команду /fillform'
        )


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, моя твоя не понимать')


# Запускаем поллинг
if __name__ == '__main__':
    dp.run_polling(bot)
