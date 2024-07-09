import telebot
import os
import string
import random
from reportlab.pdfgen import canvas
from PIL import Image
import pytesseract 

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


Token = ""
bot = telebot.TeleBot(Token)
save_path="NULL"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello, I am Onion Bot, created by Jeet. Send me any image document 🧅")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Get the file ID of the document
    file_id = message.document.file_id
    # Download the document
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    # Save the document to disk
    global res
    res = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
    global save_path
    save_path = res + '.jpeg'
    with open(save_path, 'wb') as f:
        f.write(downloaded_file)
    bot.send_message(message.chat.id, 'Document received. Choose operation to perform')


@bot.message_handler(commands=['convert_to_pdf'])
# Send a message to the user confirming that the document was received
def convert_to_pdf(message):
    if save_path=='NULL':
        bot.send_message(message.chat.id, 'Please send an image document to proceed')
        return
    # Convert image to PDF
    image_to_pdf(save_path, res + '.pdf')
    # Send the PDF file
    with open(res + '.pdf', 'rb') as file:
        bot.send_document(message.chat.id, file)
    # bot.send_message(message.chat.id, 'Thanks for using me 😊')


@bot.message_handler(commands=['scan'])
def scan(message):
    if save_path=='NULL':
        bot.send_message(message.chat.id, 'Please send an image document to proceed')
        return
    # Extract text from the image
    extracted_text = extract_text_from_image(save_path)
    # Send the extracted text
    bot.send_message(message.chat.id, f'Extracted text:\n{extracted_text}')


def image_to_pdf(input_image, output_pdf):
    img = Image.open(input_image)
    pdf = canvas.Canvas(output_pdf, pagesize=img.size)
    pdf.drawInlineImage(input_image, 0, 0)
    pdf.save()


def extract_text_from_image(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"Error: {e}"


bot.polling()
