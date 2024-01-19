from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from lexicon.lexicon import LEXICON

router = Router()


@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text=LEXICON['echo'])
