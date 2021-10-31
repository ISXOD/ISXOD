from PIL import Image
import telebot
import os
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files//Tesseract-OCR//tesseract.exe'


def rename_image(image_name, path):
    list_of_coordinates = ((200, 178, 215, 192), (225, 178, 240, 192), (250, 178, 270, 192), (279, 179, 297, 192),
                           (305, 179, 325, 191), (334, 179, 350, 191))
    result = ''
    for number in list_of_coordinates:
        im = Image.open(path + image_name)
        im_crop = im.crop(number)
        im_crop.save('guido_pillow_crop.jpg', quality=95)

        img = cv2.imread('guido_pillow_crop.jpg', cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, None, fx=5, fy=5)
        img = img / 255.0
        im_power = cv2.pow(img, 6)
        cv2.imwrite('new_image.jpg', 255 * im_power)

        img = Image.open('new_image.jpg')
        config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'  # -c tessedit_char_whitelist=0123456789
        result += pytesseract.image_to_string(img, config=config)  # config='outputbase digits'
        print(result)
        os.remove('guido_pillow_crop.jpg')
        os.remove('new_image.jpg')
        result = result.replace(' ', '')
        result = result.replace('\n', '')
        result = result.replace(' ', '')
        result = result.replace('—', '')
    name = path + 'photos/' + result + '.jpg'
    new_name_file = False
    count = 0
    while new_name_file == False:
        try:
            os.rename(path + image_name, name)
            new_name_file = True
        except FileExistsError:
            count += 1
            name = path + 'photos/' + result + '_' + str(count) + '.jpg'
    print(name)
    result = result + '_' + str(count)
    return result


bot = telebot.TeleBot("1667803516:AAGhnboX3D43OJUl4gB9SOdoYONUcR6PHRg", parse_mode=None)


@bot.message_handler(content_types=["photo"])
def handle_docs_photo(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'files/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    name = file_info.file_path
    path = 'C:/Users/Красков/PycharmProjects/Telebot/files/'
    name = rename_image(name, path)
    bot.send_message(message.chat.id, 'Файл сохранён под именем: ' + name)


@bot.message_handler(content_types=["text"])
def send_document(message):
    print(message.text)
    scr = 'files/photos/' + str(message.text) + '.jpg'
    photo = open(scr, 'rb')
    bot.send_photo(message.chat.id, photo)


bot.polling()
