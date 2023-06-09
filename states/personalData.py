from aiogram.dispatcher.filters.state import StatesGroup, State


# Shaxsiy ma'lumotlarni yig'sih uchun PersonalData holatdan yaratamiz
class PersonalData(StatesGroup):
    # Foydalanuvchi buyerda 4 ta holatdan o'tishi kerak
    fullName = State() # ism
    manzil = State() # email
    phoneNum = State() # Tel raqami
    dateTime = State() # Vaqt Sana
    NewMessage = State()
    Confirm = State()
