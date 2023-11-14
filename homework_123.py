import datetime as dt

date_format = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, next_record: 'Record ') -> None:
        """Добавление новой записи."""
        self.records.append(next_record)

    def get_today_stats(self) -> float:
        """Сколько потрачено сегодня."""
        d_today = dt.date.today()
        return sum([record.amount
                    for record in self.records
                    if record.date == d_today])

    def get_week_stats(self) -> float:
        """Сколько потрачено за 7 дней."""
        d_today = dt.date.today()
        date_week_ago = d_today - dt.timedelta(days=7)
        return float(sum([record.amount
                          for record in self.records
                          if date_week_ago < record.date <= d_today]))

    def get_today_remained(self) -> float:
        """Cколько еще можно потратить."""
        spent_today = self.get_today_stats()
        return self.limit - spent_today


class CashCalculator(Calculator):
    USD_RATE = 73.0
    EURO_RATE = 88.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency: str) -> str:
        """Сколько денег можно еще потратить."""
        all_currency = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE),
        }

        if currency not in all_currency:
            raise ValueError('Валюта введена некорректно')
        currency_name, currency_course = all_currency[currency]
        spent_today = self.get_today_remained()
        if spent_today == 0:
            return 'Денег нет, держись'

        today_spent_currency = round(abs(spent_today / currency_course), 2)
        if spent_today > 0:
            return(f'На сегодня осталось {today_spent_currency} '
                   f'{currency_name}')
        else:
            return(f'Денег нет, держись: твой долг - '
                   f'{today_spent_currency} {currency_name}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        """Сколько можно еще съесть."""
        spent_today = round(self.get_today_remained())
        if spent_today > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {spent_today} кКал')
        else:
            return 'Хватит есть!'


class Record:
    """Создание записи."""
    def __init__(self, amount: float, comment: str, date: str = None):
        self.amount = float(amount)
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.date.today()
