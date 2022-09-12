import requests

proxy = {'https_proxy': 'http://127.0.0.1:7890', 'http_proxy': 'http://127.0.0.1:7890','all_proxy': 'socks5://127.0.0.1:7890'}


def telegram_send(message):
    # Telegram_API链接信息配置
    bot_token = '5695810571:AAHUkIGjCwDMFQWLBzADRLN54IWqvtd2Kwg'  # Telegram_bot私钥
    bot_chatID = 'icecola_news'  # 频道名称
    # bot_token = '5321232286:AAGIDNJJZsSJrOFvuBR6tk3zMqn30_qagn0'  # Telegram_bot私钥
    # bot_chatID = 'icecola_new1'  # 频道名称
    # bot_message ="Testing"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=@' + bot_chatID + '&text=' + message
    # print(send_text)
    response = requests.get(send_text,proxies=proxy)  # 发送Telegram消息
    # print(response)

#telegram_send('hello')

