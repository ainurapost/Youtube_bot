import telebot
import youtube_dl
# import os
from moviepy.editor import *
import glob

TOKEN ='1761734059:AAFpATFnIhevTVmq_fPvUOl9SFBHYjZS_sY'
bot = telebot.TeleBot(TOKEN)

ydl_opts = {'outtmpl': '%(id)s.%(ext)s'}
location = "C:/Users/User/Documents/GitHub/YT_bot/downloads"
os.chdir(location)
files = glob.glob('*.mp?')

@bot.message_handler(commands=['welcome'])
def send_welcome(msg):
    bot.send_message(msg.chat.id, "Welcome to my chat bot")

@bot.message_handler(commands=['download'])
def send_download(msg):
    bot.send_message(msg.chat.id, "Enter type of file: mp3 or mp4: ")

@bot.message_handler(content_types=['text'])
def get_type_file(msg):
    if 'mp3' in msg.text.lower():
        msg2 = bot.send_message(msg.chat.id, "Give me some link to download mp3")
        bot.register_next_step_handler(msg2, get_url_audio)
    elif 'mp4' in msg.text.lower():
        msg2 = bot.send_message(msg.chat.id, "Give me some link to download mp4")
        bot.register_next_step_handler(msg2, get_url_video)
    else:
        msg2 = bot.send_message(msg.chat.id, "mp3 or mp4?? ")
        bot.register_next_step_handler(msg2, get_type_file)

@bot.message_handler(content_types=['text'])
def get_url_audio(message):
    if 'https' in message.text.lower():
        url = message.text
        file_name = download_file(url, ydl_opts)
        if True:
            videoclip = VideoFileClip(file_name[0]+ '.'+ file_name[1])
            audioclip = videoclip.audio
            audio_file = file_name[0] + '.mp3'
            audioclip.write_audiofile(audio_file)
            audioclip.close()
            videoclip.close()
            audio = open(audio_file, 'rb')
            bot.send_audio(message.chat.id, audio)
            audio.close()
            os.unlink(file_name[0] + '.' + file_name[1])
            os.unlink(audio_file)
    else:
        bot.send_message(message.chat.id, "Give me a valid link")

@bot.message_handler(content_types=['text'])
def get_url_video(message):
    if 'https' in message.text.lower():
        url = message.text
        file_name = download_file(url, ydl_opts)
        if True:
            video = open(file_name[0] + '.' + file_name[1], 'rb')
            bot.send_video(message.chat.id, video)
            video.close()
            os.unlink(file_name[0] + '.' + file_name[1])
    else:
        bot.send_message(message.chat.id, "Give me a valid link")

def download_file(url, ydl_opts):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file_info = ydl.extract_info(url, download=True)
        video_id = file_info.get("id", None)
        video_ext = file_info.get('ext', None)
    return video_id, video_ext


# pip install -r requirements.txt
# pip freeze > requirements.txt


bot.polling()




