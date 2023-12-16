
import os
from datetime import datetime
import logging
from stt import STT
import asyncio
from aiogram.filters.command import Command
import g4f
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from keyboards import *
from pathlib import Path
stt = STT()

with open('users.json', encoding='utf-8') as f:
    users = json.load(f)

with open('requests.json', encoding='utf-8') as f:
    req = json.load(f)

with open('questions.json', encoding='utf-8') as f:
    questions = json.load(f)


model = Model(r'vosk/ru')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()



def recognize_speak():
    while True:
        data = stream.read(120000)
        rec.AcceptWaveform(data)
        x=json.loads(rec.Result())
        if x["text"] == "":
            continue
        else:
            return x["text"]


HELP_STR = '''/start - Начало работы
/id - Узнать свой ID
/message СООБЩЕНИЕ - отправить сообщение врачу

/temp <ТЕМПЕРАТУРА_ОТВЕТА> - температура ответа (от 0.01 до 2)
/models - Выбрать модель (GPT)

/help - Помощь
/number_message - Номер сообщения
/time - Время
/ping - Pong
'''



bot = Bot(token="YOUR TOKEN")
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Диспетчер
dp = Dispatcher()
rt = Router()




@dp.message(Command("time"))
async def time(msg: types.Message):
    await bot.send_message(msg.from_user.id, f"⌛ Время: {str(datetime.now())[:]}")

###### ADMINS ##############
@dp.message(Command("off"))
async def time(msg: types.Message):
    if users['users'][str(msg.from_user.id)]['admin']:
        with open('users.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(users, ensure_ascii=False))
        await bot.send_message(msg.from_user.id, f"Завершено!")
        with open('requests.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(req, ensure_ascii=False))
        await bot.send_message(msg.from_user.id, f"Завершено!")
        with open('questions.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(questions, ensure_ascii=False))
        await bot.send_message(msg.from_user.id, f"Завершено!")
    else: await bot.send_message(msg.from_user.id, f"Отказано в доступе!")


@dp.message(Command("message"))
async def time(msg: types.Message):
    print(str(msg.text))
    questions['que'][str(msg.from_user.id)].append(' '.join(str(msg.text).split(' ')[1:]))
    await bot.send_message(msg.from_user.id, 'Вашему врачу'+" доставлено сообщение: "+ ' '.join(str(msg.text).split(' ')[1:]))

######### ADDITIONAL #######################
@dp.message(Command("start"))
async def start(msg: types.Message):
    await bot.send_message(msg.from_user.id, (f"👋 Привет {msg.from_user.full_name}! Это телеграм бот МедГос с помощью его ты можешь списаться с врачём, отправить справки или задать интересующий вопрос ChatGPT!"))

    if not str(msg.from_user.id) in users['users']:
        users['users'][str(msg.from_user.id)] = {"user_full_name":  msg.from_user.full_name, "username": msg.from_user.username, "model": "gpt-3.5-turbo-16k", "temp": 0.7, "admin": False, "msg_left": 10, "msg_used": 0, "mode": ""}
        print('НОВЫЙ ПОЛЬЗОВАТЕЛЬ!', '|', msg.from_user.id, '|', msg.from_user.full_name, '|', msg.from_user.username)
    else: print('Нового пользователя не было созданно, он уже существует')
    if not str(msg.from_user.id) in req['req']:
        req['req'][str(msg.from_user.id)] = []
        print('НОВЫЙ БАЗА ДАННЫХ!', '|', msg.from_user.id, '|', msg.from_user.full_name, '|', msg.from_user.username)
    if not str(msg.from_user.id) in questions['que']:
        questions['que'][str(msg.from_user.id)] = []
        print('НОВЫЙ БАЗА ДАННЫХ!', '|', msg.from_user.id, '|', msg.from_user.full_name, '|', msg.from_user.username)
    else: print('Новой истории диалогов не было созданно, она уже существует')


@dp.message(Command("id"))
async def help(msg: types.Message):
    await bot.send_message(msg.from_user.id, '🪪 Ваш ID: '+str(msg.from_user.id))

@dp.message(Command("help"))
async def help(msg: types.Message):
    await bot.send_message(msg.from_user.id, HELP_STR)

@dp.message(Command("ping"))
async def pong(msg: types.Message):
    await bot.send_message(msg.from_user.id, "⚪ pong")

@dp.message(Command("temp"))
async def number_message(msg: types.Message):
    users['users'][msg.from_user.id]['temp'] = float(str(msg.text).split(' ')[1])
    await bot.send_message(msg.from_user.id, f"*🌡 Температура установлена {users[str(msg.from_user.id)]['temp']}\!*", parse_mode='MarkdownV2')

@dp.message(Command("models"))
async def output(message: types.Message):
    await message.answer(
        f"🧊 Выберите одну из этих моделей:",
        reply_markup=get_keyboard_mini_models()
    )


@dp.message(Command("whoiam"))
async def whoiam(msg: types.Message):
    text = f"👀 Твое имя: {msg.from_user.full_name}, твой ник: {msg.from_user.username}"
    await bot.send_message(msg.from_user.id, text)

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    # Получаем список фотографий в сообщении
    await bot.send_message(message.from_user.id, "Изобаражение получено, врач скоро свяжется с вами")
@dp.message()
async def echo(msg: types.Message):
    if msg.content_type == types.ContentType.VOICE or msg.content_type == types.ContentType.AUDIO or msg.content_type == types.ContentType.DOCUMENT:
        if msg.content_type == types.ContentType.VOICE:
            file_id = msg.voice.file_id
        elif msg.content_type == types.ContentType.AUDIO:
            file_id = msg.audio.file_id
        elif msg.content_type == types.ContentType.DOCUMENT:
            file_id = msg.document.file_id
        else:
            await msg.reply("Формат документа не поддерживается")
            return
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_on_disk = Path("", f"{file_id}.tmp")
        await bot.download_file(file_path, destination=file_on_disk)

        text = stt.audio_to_text(file_on_disk)
        if not text:
            text = "😢 Формат документа не поддерживается"
            return
        os.remove(file_on_disk)  # Удаление временного файла
    else: text=''
    if text: uni_text=text
    else: uni_text=msg.text
    temp = await msg.reply( f"⏰ Сейчас подумаю! ({users['users'][str(msg.from_user.id)]['model']})")
    if users["users"][str(msg.from_user.id)]['mode']:
        try:
            response = await g4f.ChatCompletion.create_async(model=users['users'][str(msg.from_user.id)]['model'],
                                                                     messages=[{"role": "user",
                                                                                "content": uni_text}],
                                                                     tempetarure=users['users'][str(msg.from_user.id)]['temp'])

        except RuntimeError: await bot.send_message(msg.from_user.id, '😢 Похоже генерация не удалась')
    else:
        response = await g4f.ChatCompletion.create_async(model=users['users'][str(msg.from_user.id)]['model'], messages=[{"role": "user", "content": uni_text}], tempetarure=users['users'][str(msg.from_user.id)]['temp'])
    if not 'username' in users['users'][str(msg.from_user.id)]:
        users['users'][str(msg.from_user.id)]['username'] = msg.from_user.username
        users['users'][str(msg.from_user.id)]['user_full_name'] = msg.from_user.full_name

    req['req'][str(msg.from_user.id)].append({uni_text: response})
    await temp.delete()
    await msg.reply(response)







@dp.callback_query(F.data == 'back')
async def set_model_gpt3(callback: types.CallbackQuery):
    await callback.message.delete()


@dp.callback_query(F.data == "gpt-3.5-turbo-16k")
async def set_model_gpt3(callback: types.CallbackQuery):
    print(callback.from_user.id)
    users['users'][str(callback.from_user.id)]['model'] = "gpt-3.5-turbo-16k"
    await callback.message.delete()
    await callback.answer(
        text=f'🧊 Модель gpt-3.5-turbo-16k установлена!',
        show_alert=True)

@dp.callback_query(F.data == "gpt-3.5-turbo-16k-0613")
async def set_model_gpt3(callback: types.CallbackQuery):
    users['users'][str(callback.from_user.id)]['model'] = "gpt-3.5-turbo-16k-0613"
    print(callback.from_user.id)
    await callback.message.delete()
    await callback.answer(
        text=f'🧊 Модель gpt-3.5-turbo-16k-0613 установлена!',
        show_alert=True)

@dp.callback_query(F.data == "gpt-4-0613")
async def set_model_gpt3(callback: types.CallbackQuery):
    users['users'][str(callback.from_user.id)]['model'] = "gpt-4-0613"
    print(callback.from_user.id)
    await callback.message.delete()
    await callback.answer(
        text=f'🧊 Модель gpt-4-0613 установлена!',
        show_alert=True)

@dp.callback_query(F.data == "cancel")
async def set_model_gpt3(callback: types.CallbackQuery):
    await callback.message.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())