import pandas as pd


def main():
    print('Сладенькие котики!')
    name = input('Введите имя: ')
    birthday = input('Введите дату и время рождения: ')
    sity = input('Введите город рождения: ')
    title = ' '.join([name, birthday, sity])
    helps = ['[1]-Овен', '[2]-Телец', '[3]-Близнецы', '[4]-Рак','[5]-Лев','[6]-Дева','[7]-Весы',
    '[8]-Скорпион','[9]-Стрелец','[10]-Козерог','[11]-Водолей','[12]-Рыбы']
    print(' '.join(helps))
    znak = input(f"Введите знак:")
    dom = input(f"Введите дом:")
    aspekts = input(f"Введите аспекты через пробел: ")
    print('Поехали...')

    actions = pd.read_excel('Солнцезажигающие действия.xlsx', sheet_name='Действия')
    select_actions = actions.loc[actions['Дом'].str.contains(f' {znak} ') | actions['Дом'].str.contains(f' {dom} '), 'Действие']
    if aspekts:
        aspekts_list = aspekts.split(' ')
        for aspekt in aspekts_list:
            select_actions = select_actions.append(actions.loc[actions['Дом'].str.contains(f' {aspekt} ') & actions['Аспект'].str.contains('Главный'), 'Действие'])
    select_actions = select_actions.drop_duplicates()
    select_actions = select_actions.to_list()
    print('\n'.join(select_actions))
    
    with open(f'СЗД_{name}.txt', 'w') as f:
        f.write(title + '\n')
        n = 10
        k = 1
        for i in range(0, len(select_actions), n):
            f.write(f'----------Страница {k}----------' + '\n')
            f.write('\n'.join(select_actions[i:i + n]) + '\n')
            k += 1


if __name__ == "__main__":
    main()
