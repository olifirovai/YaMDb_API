import random
import string
from Api.models import User

'''Создать Новый файл utils.py + полностью скопировать код'''
def random_code_generator(size=30,
                          chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_confrm_code_generator():
    confirmation_code = random_code_generator()
    qs_exists = User.objects.filter(
        confirmation_code=confirmation_code).exists()
    if qs_exists:
        return random_code_generator()
    return confirmation_code
