import pytz
from SETTINGS import SETTINGSS

class SEC_SETTINGSS(SETTINGSS):
    def __init__(self) -> None:
        super().__init__()
        self.my_name = 'Николай' # Ваше имя
        # self.my_name = 'Денис' # Ваше имя
        self.veryf_attemts_number = 9 # количество попыток доступа в ваш тг бот после неверно введенного пароля
        self.show_statistic_hour = 21 # время показа дневной статистики (21 - в 9 часов вечера каждого дня)
        self.local_tz = pytz.timezone('Europe/Kiev') # 'Europe/Berlin' -- часовой пояс
        # self.local_tz = pytz.timezone('Europe/Berlin') # 'Europe/Kiev' -- часовой пояс