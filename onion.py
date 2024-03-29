import telebot
import os
import string
import random
from reportlab.pdfgen import canvas
from PIL import Image

# bot link: https://t.me/i_am_onion_bot

Token = "6553751419:AAFdCcZavXz7VJmGoMHE4lFNrl_Cyirq9Uk"
bot=telebot.TeleBot(Token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello, I am Onion Bot created by Jeet. Send me any image file and I will convert it to pdf in seconds 😉")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Get the file ID of the document
    file_id = message.document.file_id
    # Download the document
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    # Save the document to disk
    res = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    save_path = res+'.jpeg'
    with open(save_path, 'wb') as f:
        f.write(downloaded_file)
    # Send a message to the user confirming that the document was received
    bot.send_message(message.chat.id, 'Document received! I am working on it. Please Wait')

    image_to_pdf(save_path,res+'.pdf')

    file = open(res+'.pdf', 'rb')
    bot.send_document(message.chat.id, file)
    bot.send_message(message.chat.id, 'Thanks for using me 😊')

def image_to_pdf(input_image, output_pdf):
    img = Image.open(input_image)
    pdf = canvas.Canvas(output_pdf, pagesize=img.size)
    pdf.drawInlineImage(input_image, 0, 0)
    pdf.save()




bot.polling()
