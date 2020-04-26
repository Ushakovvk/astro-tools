def simplification(number: str) -> str:
    number = str(sum([int(i) for i in number]))
    if len(number) > 1:
        number = simplification(number)
    return number


class Client:
    def __init__(self, fio: str, birthday: str):
        self.fio = fio
        self.birthday = birthday
        self.data = {}

    def financial_code(self):
        day, month, year = self.birthday.split('.')
        self.data['число характера'] = simplification(day)
        self.data['число души'] = simplification(month)
        self.data['число года'] = simplification(year)
        self.data['число судьбы'] = simplification(self.data['число характера'] + self.data['число души'] +
                                                   self.data['число года'])
        self.data['финансовый код'] = ''.join([self.data['число характера'], self.data['число души'],
                                               self.data['число года'], self.data['число судьбы']])

    def fio_code(self):
        dict_letter = {"1": ["а", "и", "с", "ъ"],
                       "2": ["б", "й", "т", "ы"],
                       "3": ["в", "к", "у", "ь"],
                       "4": ["г", "л", "ф", "э"],
                       "5": ["д", "м", "х", "ю"],
                       "6": ["е", "н", "ц", "я"],
                       "7": ["ё", "о", "ч"],
                       "8": ["ж", "п", "ш"],
                       "9": ["з", "р", "щ"]}
        fio = self.fio.strip().lower()
        for num, letters in dict_letter.items():
            for letter in letters:
                fio = fio.replace(letter, num)
        self.data['код имени'] = simplification(''.join([simplification(x) for x in fio.split(' ')]))

    def wealth_code(self):
        self.data['код богатства'] = simplification(self.data['код имени'] + self.data['число судьбы'])

    def women_code(self):
        self.data['код женского рода'] = simplification(self.data['код имени'] + self.data['число характера'])

    def men_code(self):
        self.data['код мужского рода'] = simplification(self.data['код имени'] + self.data['число года'])

    def soul_code(self):
        self.data['код денег души'] = simplification(self.data['код имени'] + self.data['число души'])

    def wealth_combination(self):
        self.data['комбинация богатства'] = ''.join([simplification(self.data['финансовый код']),
                                                     self.data['код богатства'],
                                                     self.data['код женского рода'],
                                                     self.data['код мужского рода'],
                                                     self.data['код денег души']])

    def fit(self):
        self.financial_code()
        self.fio_code()
        self.wealth_code()
        self.women_code()
        self.men_code()
        self.soul_code()
        self.wealth_combination()
        return self.data


if __name__ == '__main__':
    con = Client(fio='Дербенцева Азиза Дмитриевна', birthday='02.04.1989')
    data = con.fit()
    for k, v in data.items():
        print(f'{k} - {v}')
