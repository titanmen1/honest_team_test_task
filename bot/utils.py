# Функция для извлечения ID сообщения и ID канала из ссылки
import re


def extract_ids(link):
    match = re.search(r't.me/([^/]+)/(\d+)', link)
    if match:
        channel = match.group(1)
        message_id = int(match.group(2))
        return channel, message_id
    return None, None