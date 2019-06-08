import requests


def telegram_bot_sendtext(bot_message):
    bot_token = '816519526:AAGdiWlEIAvsJfBXklyn92fE9l3yFZuQFKw'
    bot_chatID = '451429199'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=html&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def telegram_bot_sendphoto(photo):
    bot_token = '816519526:AAGdiWlEIAvsJfBXklyn92fE9l3yFZuQFKw'
    bot_chatID = '451429199'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendPhoto?chat_id=' + bot_chatID + '&parse_mode=html&photo=' + photo
    response = requests.get(send_text)
    return response.json()


def reader_bot_sendtext(bot_message):
    bot_token = '804490733:AAH2z-ytvwlYyDu5F1n282vgMb99qFT0Qhw'
    bot_chatID = '451429199'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=html&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def reader_bot_sendphoto(photo):
    bot_token = '804490733:AAH2z-ytvwlYyDu5F1n282vgMb99qFT0Qhw'
    bot_chatID = '451429199'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendPhoto?chat_id=' + bot_chatID + '&parse_mode=html&photo=' + photo
    response = requests.get(send_text)
    return response.json()
