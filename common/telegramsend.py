from telegram import Bot


# 填写你的 Telegram Bot Token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def send_telegram_message(chat_id, message):

    """向指定聊天 ID 发送消息"""
    # 创建一个 Bot 实例
    bot = Bot(token=TOKEN)

    # 发送消息
    bot.send_message(chat_id=chat_id, text=message)
