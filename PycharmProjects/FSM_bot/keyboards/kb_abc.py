from aiogram.types import InlineKeyboardButton

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