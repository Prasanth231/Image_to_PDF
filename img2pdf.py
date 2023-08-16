#################################################################################
import os
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import cv2
import pytesseract
import warnings
from docx import Document
from docx2pdf import convert
import time
from time import sleep
#################################################################################
def receive_image(update, context):
    pythoncom.CoInitialize()
    
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    #print("level 1")

    if update.message.photo:

        photo_file_id = update.message.photo[-1].file_id

        photo_file = context.bot.get_file(photo_file_id)
        filename = f"{message_id}.jpeg"
        photo_file.download(filename)
        print("downloaded")
        context.bot.send_message(chat_id=chat_id, text="Thanks for the image!")
    else:
        def error(update, context):
            logger.error('Update "%s" caused error "%s"', update, context.error)
            context.bot.send_message(chat_id=chat_id, text='An error occurred. Please try again later.')

    pytesseract.pytesseract.tesseract_cmd=r'C:\\Users\\family\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
    img= cv2.imread(filename)
    imgtext= pytesseract.image_to_string(filename)
    context.bot.send_message(chat_id=chat_id, text=imgtext)
    doc_file= 'Text.docx'
    document = Document()
    document.add_paragraph(imgtext)
    document.save(doc_file)
    with open(doc_file, 'rb') as f:
        context.bot.send_document(chat_id=chat_id, document=f, filename='Text.docx')
    pdf_file= "Text.pdf"
    #pdf_file = doc_path.replace(".docx", ".pdf")
    #convert(doc_file)
    convert(doc_file, pdf_file)
    with open(pdf_file, 'rb') as f:
        context.bot.send_document(chat_id=chat_id, document=f,filename='Text.pdf')
    time.sleep(5)
    if os.path.isfile(doc_file):
        os.remove(doc_file)
    if os.path.isfile(pdf_file):
        os.remove(pdf_file)
    if os.path.isfile(filename):
        os.remove(filename)        
#################################################################################
bot_token = "6211989392:AAFdsfs3IP0fKeacWm-mPnLrLqORRWg9fQ" #bot Token
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher
image_handler = MessageHandler(Filters.photo, receive_image)
dispatcher.add_handler(image_handler)
updater.start_polling()
updater.idle()
#################################################################################
