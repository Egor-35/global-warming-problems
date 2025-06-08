import telebot  # Импортируем библиотеку для работы с Telegram Bot API
import random  # Импортируем модуль для генерации случайных чисел
import requests  # Импортируем модуль для выполнения HTTP-запросов
from bs4 import BeautifulSoup  # Импортируем библиотеку для парсинга HTML
from telebot import types  # Импортируем типы для работы с кнопками и сообщениями в Telegram
# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на токен вашего бота
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)  # Создаем экземпляр бота с указанным токеном
# Список экологических советов
tips = [
    "Используйте общественный транспорт, езжайте на велосипеде или ходите пешком.",
    "Экономьте электроэнергию: выключайте свет и электроприборы, когда они не используются.",
    "Сократите потребление пластика и сортируйте мусор для рециклинга.",
    "Поддерживайте локальные продукты и уменьшайте транспортировку товаров.",
    "Участвуйте в посадке деревьев и озеленении вашего города.",
    "Отдавайте предпочтение товарам с минимальной упаковкой.",
    "Используйте многоразовые сумки и бутылки вместо одноразовых.",
    "Сократите использование одноразовых посуды и столовых приборов.",
    "Соблюдайте принципы энергосбережения в быту: регулируйте температуру, утепляйте дом.",
    "Поддерживайте и участвуйте в местных экологических инициативах и акциях.",
    "Выбирайте энергоэффективную бытовую технику и оборудование.",
    "Организуйте совместное использование автомобилей (карпулинг) для сокращения количества машин на дорогах.",
    "Покупайте экологически чистые и натуральные продукты, избегая товаров с искусственными добавками.",
    "Используйте альтернативные источники энергии, такие как солнечные батареи или ветровые турбины.",
    "Поддерживайте проекты по защите природы и участвуйте в волонтёрских экологических акциях.",
    "Компостируйте органические отходы для получения натурального удобрения.",
    "Используйте дождевую воду для полива растений и огорода.",
    "Сократите потребление мяса, чтобы уменьшить воздействие на окружающую среду.",
    "Выбирайте экологичные бытовые средства для уборки, избегая химии.",
    "При ремонте дома отдавайте предпочтение натуральным и экологически чистым материалам."
]
# Список вопросов для теста
test_questions = [
    {
        "question": "Какой способ передвижения помогает сократить выбросы углекислого газа?",
        "correct_option": "На общественном транспорте",
        "wrong_option": "На машине",
        "explanation": "Езда на общественном транспорте помогает сократить выбросы углекислого газа и уменьшает нагрузку на дороги."
    },
    # ... (другие вопросы аналогично)
]
# Словарь для хранения состояния теста каждого пользователя
test_states = {}
def send_test_question(chat_id, user_id):
    state = test_states[user_id]  # Получаем состояние теста для пользователя
    q = state["questions"][state["current"]]  # Получаем текущий вопрос
    markup = types.InlineKeyboardMarkup()  # Создаем клавиатуру для ответов
    btn_correct = types.InlineKeyboardButton(q["correct_option"], callback_data=f"test_{state['current']}_correct")  # Кнопка для правильного ответа
    btn_wrong = types.InlineKeyboardButton(q["wrong_option"], callback_data=f"test_{state['current']}_wrong")  # Кнопка для неправильного ответа
    markup.add(btn_wrong, btn_correct)  # Добавляем кнопки на клавиатуру
    bot.send_message(chat_id, q["question"], reply_markup=markup)  # Отправляем вопрос с клавиатурой
@bot.message_handler(commands=['start'])
def start_handler(message):
    # Приветственное сообщение и список доступных команд
    welcome_text = (
        "Привет! Я бот, который помогает бороться с глобальным потеплением.\n"
        "Доступные команды:\n"
        "/tips - получить экологический совет\n"
        "/news - последние новости о климате\n"
        "/donate - способы поддержать экологические проекты\n"
        "/test - пройти тест по экологическим советам"
    )
    bot.send_message(message.chat.id, welcome_text)  # Отправляем приветственное сообщение
@bot.message_handler(commands=['tips'])
def tips_handler(message):
    tip = random.choice(tips)  # Выбираем случайный совет из списка
    bot.send_message(message.chat.id, f"Совет: {tip}")  # Отправляем совет пользователю
@bot.message_handler(commands=['news'])
def news_handler(message):
    url = "https://ria.ru/keyword_globalnoe_poteplenie/"  # URL для получения новостей
    dict_news = {"news": []}  # Словарь для хранения новостей
    response = requests.get(url)  # Выполняем GET-запрос к указанному URL
    bs = BeautifulSoup(response.text, "lxml")  # Парсим HTML-код страницы
    temp = bs.find_all('div', 'list-item')  # Находим все элементы с новостями
    for post in temp:
        dict_news["news"].append(post.find('a', 'list-item__title').text)  # Добавляем заголовки новостей в список
    all_news = ';\n'.join(dict_news["news"])  # Объединяем заголовки в одну строку
    news_text = "Последние новости о глобальном потеплении:\n" + all_news  # Формируем текст с новостями
    bot.send_message(message.chat.id, news_text)  # Отправляем новости пользователю
@bot.message_handler(commands=['donate'])
def donate_handler(message):
    # Сообщение о способах поддержки экологических проектов
    donate_text = (
        "Поддержите борьбу с глобальным потеплением:\n\n"
        "• WWF: https://www.worldwildlife.org/\n"
        "• Greenpeace: https://www.greenpeace.org/\n"
        "• Экопроекты вашего города (найдите информацию на местных ресурсах)!"
    )
    bot.send_message(message.chat.id, donate_text)  # Отправляем информацию о пожертвованиях
@bot.message_handler(commands=['test'])
def test_handler(message):
    user_id = message.chat.id  # Получаем ID пользователя
    test_states[user_id] = {  # Инициализируем состояние теста для пользователя
        "current": 0,  # Индекс текущего вопроса
        "score": 0,  # Счет пользователя
        "questions": test_questions  # Список вопросов для теста
    }
    bot.send_message(user_id, "Начинаем тест! За каждый правильный ответ +1 балл, за неправильный – -1 балл.")  # Сообщение о начале теста
    send_test_question(user_id, user_id)  # Отправляем первый вопрос
@bot.callback_query_handler(func=lambda call: call.data.startswith("test_"))
def test_callback(call):
    user_id = call.message.chat.id  # Получаем ID пользователя
    state = test_states[user_id]  # Получаем состояние теста
    _, q_index, result = call.data.split("_")  # Извлекаем индекс вопроса и результат
    q_index = int(q_index)  # Преобразуем индекс в целое число
    current_q = state["questions"][q_index]  # Получаем текущий вопрос
    if result == "correct":  # Если ответ правильный
        state["score"] += 1  # Увеличиваем счет
        response_text = f"Правильно! {current_q['explanation']}"  # Формируем ответ с объяснением
    else:  # Если ответ неправильный
        state["score"] -= 1  # Уменьшаем счет
        response_text = f"Неправильно. {current_q['explanation']}"  # Формируем ответ с объяснением
    bot.answer_callback_query(call.id)  # Подтверждаем нажатие кнопки
    bot.send_message(user_id, response_text)  # Отправляем ответ пользователю
    state["current"] += 1  # Переходим к следующему вопросу
    if state["current"] < len(state["questions"]):  # Если есть еще вопросы
        send_test_question(user_id, user_id)  # Отправляем следующий вопрос
    else:  # Если вопросы закончились
        bot.send_message(user_id, f"Тест завершён! Ваш итоговый счет: {state['score']}")  # Отправляем итоговый счет
        del test_states[user_id]  # Удаляем состояние теста пользователя
@bot.message_handler(func=lambda message: True)
def catch_all(message):
    # Обработка всех остальных сообщений
    bot.send_message(message.chat.id, "Извините, я не понимаю эту команду. Введите /start, чтобы увидеть список доступных команд.")
print("Бот запущен...")  # Сообщение о запуске бота
bot.infinity_polling(none_stop=True)  # Запускаем бесконечный опрос для обработки сообщений
