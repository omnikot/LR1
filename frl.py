from flask import Flask, render_template, request, redirect, url_for
import telebot
import random
import threading
import datetime

# Создаем Flask приложение
app = Flask(__name__)

# Настройки Telegram бота
BOT_TOKEN = "7874318582:AAFvyiARb3sDf1VyTF6xSVAQ7LcXD7W7m4o"
bot = telebot.TeleBot(BOT_TOKEN)

# Переменные для состояния
greeted_users = set()
fact_timer_active = False
current_chat_id = None

# Чтение данных
with open('greetings.txt', 'r', encoding='utf-8') as file:
    greetings = file.readlines()

with open("phrases.txt", "r", encoding="utf-8") as file:
    phrases = file.readlines()

# Функция отправки сообщений с таймером
def send_message_with_timer():
    global fact_timer_active
    while fact_timer_active:
        if current_chat_id:
            random_phrase = random.choice(phrases)
            bot.send_message(current_chat_id, f'Интересный факт: {random_phrase}')
        threading.Event().wait(20)

# Главная страница
@app.route('/')
def index():
    global fact_timer_active
    return render_template(
        'index.html',
        fact_timer_active=fact_timer_active,
        greeted_users=list(greeted_users),
    )

# Обработчик запуска таймера
@app.route('/start_timer', methods=['POST'])
def start_timer():
    global fact_timer_active, current_chat_id
    current_chat_id = request.form.get('chat_id')
    if not fact_timer_active and current_chat_id:
        fact_timer_active = True
        threading.Thread(target=send_message_with_timer, daemon=True).start()
    return redirect(url_for('index'))

# Обработчик остановки таймера
@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    global fact_timer_active
    fact_timer_active = False
    return redirect(url_for('index'))

# Обработчик отправки приветствия
@app.route('/send_greeting', methods=['POST'])
def send_greeting():
    chat_id = request.form.get('chat_id')
    if chat_id and chat_id not in greeted_users:
        random_greeting = random.choice(greetings)
        bot.send_message(chat_id, random_greeting)
        greeted_users.add(chat_id)
    return redirect(url_for('index'))

# Запуск Flask
if __name__ == "__main__":
    app.run(debug=True)
