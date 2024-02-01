from aiogram.filters.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    fill_surname = State()
    fill_grade = State()
    fill_first_test = State()
    fill_wish_data = State()


class FSMFirstTest(StatesGroup):
    first_question = State()
    second_question = State()
    third_question = State()
    fourth_question = State()
    fifth_question = State()
    sixth_question = State()
    seventh_question = State()
    eighth_question = State()
    ninth_question = State()
    tenth_question = State()


class FSMCourse(StatesGroup):
    course = State()
    second_test = State()


class FSMSecondTest(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
