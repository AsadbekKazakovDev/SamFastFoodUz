import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from handlers.users.menu_handlers import show_item

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from data.config import ADMINS, CHANNELS
from keyboards.inline.manage_send import confirmation_keyboard, post_callback
from keyboards.default.location import keyboard
from loader import dp, db, bot
from states.personalData import PersonalData


# /click komandasi uchun handler yaratamiz. Bu yerda foydalanuvchi hech qanday holatda emas, state=None
@dp.callback_query_handler(text="click")
async def enter_test(call: CallbackQuery):
    await call.message.answer(f"<b> 9860190110539391\nAsadbek Kazakov\n\n</b>Bizning hisob raqam. To`lov qilishingiz mumkin!!! \n\n"
                              "To'liq ismingizni kiriting↙️")
    await PersonalData.fullName.set()




@dp.message_handler(state=PersonalData.fullName)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text

    await state.update_data(
        {"name": fullname}
    )

    await message.answer("Manzil kiriting", reply_markup=keyboard)

    # await PersonalData.email.set()
    await PersonalData.next()

@dp.message_handler(state=PersonalData.manzil)
async def answer_email(message: types.Message, state: FSMContext):
    manzil = message.text


    await state.update_data(
        {"manzil": manzil}
    )

    await message.answer("Telefon raqam kiriting", reply_markup=ReplyKeyboardRemove())

    await PersonalData.next()


@dp.message_handler(state=PersonalData.phoneNum)
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.text

    await state.update_data(
        {"phone": phone}
    )

    await message.answer("Sana & Vaqt", reply_markup=ReplyKeyboardRemove())

    await PersonalData.next()

@dp.message_handler(state=PersonalData.dateTime)
async def answer_date(message: types.Message, state: FSMContext):
    datetime = message.text

    await state.update_data(
        {"datetime": datetime}
    )
    # Ma`lumotlarni qayta o'qiymiz
    data = await state.get_data()
    name = data.get("name")
    manzil = data.get("manzil")
    phone = data.get("phone")
    datetime = data.get("datetime")

    msg = f"Quyidagi ma`lumotlar qabul qilindi:\n"
    msg += f"Status - Click\n"
    msg += f"Ismingiz - {name}\n"
    msg += f"Manzil - {manzil}\n"
    msg += f"Telefon: - {phone}\n"
    msg += f"Sana: - {datetime}"

    # await message.text(msg)


    await state.update_data(text=msg, mention=message.from_user.get_mention())
    await message.answer(f"{msg}\n\n Postni tekshirish uchun yuboraymi?",
                         reply_markup=confirmation_keyboard)

    await PersonalData.NewMessage.set()
    await PersonalData.next()



@dp.callback_query_handler(post_callback.filter(action="post"), state=PersonalData.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post Adminga yuborildi")
    await bot.send_message(ADMINS[0], f"Foydalanuvchi {mention} quyidagi postni chop etmoqchi:")
    await bot.send_message(ADMINS[0], text, parse_mode="HTML", reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=PersonalData.Confirm)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post rad etildi.")


@dp.message_handler(state=PersonalData.Confirm)
async def post_unknown(message: Message):
    await message.answer("Chop etish yoki rad etishni tanlang")


@dp.callback_query_handler(post_callback.filter(action="post"), user_id=ADMINS)
async def approve_post(call: CallbackQuery):
    await call.answer("Chop etishga ruhsat berdingiz.", show_alert=True)
    target_channel = CHANNELS[0]
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)


@dp.callback_query_handler(post_callback.filter(action="cancel"), user_id=ADMINS)
async def decline_post(call: CallbackQuery):
    await call.answer("Post rad etildi.", show_alert=True)
    await call.message.edit_reply_markup()