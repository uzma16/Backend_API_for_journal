from mindfulness.settings import push_service


def send_notification(user_token, title, body, notification_type):
    data_message = {
        'title': title,
        'body': body,
        'notification_type': notification_type
    }
    result = push_service.notify_single_device(registration_id=user_token, data_message=data_message)
    return result

def calculate_coins(entry_type, entry_length):
    if not entry_length:
        return 0
    if entry_type == 'text':
        if 10 <= entry_length <= 50:
            return 5
        elif 51 <= entry_length <= 200:
            return 10
        elif entry_length > 200:
            return 15
    elif entry_type == 'audio':
        if 30 <= entry_length <= 60:
            return 5
        elif 61 <= entry_length <= 180:
            return 10
        elif entry_length > 180:
            return 15
    return 0