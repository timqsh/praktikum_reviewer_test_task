import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # FIX: оператор not на отдельной строке не соответствует PEP8
        self.date = (
            # IMPROVE: еще можно использовать `dt.date.today()`,
            # но текущий вариант решения тоже подходит.
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # FIX: имя переменной должно начинаться с маленькой буквы. 
        # В текущем варианте затеняется имя класса,
        # что может привести к неочевидным ошибкам.
        for Record in self.records:
            # IMPROVE: стоит вынести вычисление сегодняшней даты за цикл
            if Record.date == dt.datetime.now().date():
                # IMPROVE: тут можно использовать оператор `+=`
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
            # IMPROVE: некритично, но бинарный оператор лучше использовать на следующей строке:
            # https://www.python.org/dev/peps/pep-0008/#should-a-line-break-before-or-after-a-binary-operator
            # IMPROVE: код будет проще читаться, если вынести переменную `days_delta = today = record.date`
            # IMPROVE: а еще можно использовать цепочку операторов сравнения: `0 <= (today - record.date).days < 7`
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # FIX: комментарий, описывающий метод, лучше заменить на docstring
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # FIX: длинную строку можно сделать используя скобки, а не обратный слэш:
            # (
            #   'Very very '
            #   'long string.'
            # )
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # FIX: избыточный else, ведь в блоке if уже есть возврат
        else:
            # FIX: круглые скобки излишни. Выглядит будто `return` используется как функция
            return('Хватит есть!')


class CashCalculator(Calculator):
    # IMPROVE: Курс долларА ;)
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # FIX: избыточные параметры USD_RATE и EURO_RATE.
    # Лучше использовать self.USD_RATE и self.EURO_RATE в теле метода
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # FIX: Эта строчка кода не делает ничего полезного.
            # Она сравнивает `cash_remained` c `1.00` и не использует результат сравнения.
            # Кажется, она просто лишняя.
            cash_remained == 1.00
            currency_type = 'руб'
        # IMPROVE: код будет проще читаться, если в этом месте отделить пустой строчкой
        # два разных блока с условиями. Так они не будут визуально сливаться.
        if cash_remained > 0:
            return (
                # FIX: Форматирование возвращаемых строк нужно сделать единообразно.
                # Сейчас в первом случае используется функция `round`, а во втором форматирование через `:.2f`.
                # Кроме того в первом случае используется f-строка, а во втором - функция `format`.
                # FIX: математические вычисления не стоит делать внутри f-строки.
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # IMPROVE: тут хватит и простого else.
        elif cash_remained < 0:
            # TODO для длинных строк лучше использовать скобки а не обратный слэш.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # FIX: избыточное переопределение наследуемого метода.
    # Если убрать метод, который просто вызывает метод базового класса,
    # то результат не изменится, поскольку будет работать наследование.
    def get_week_stats(self):
        super().get_week_stats()
