import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import ExcelWriter

options = ['1) Morbidity dynamics` visualization', '2) Areas` comparison', '3) Exit']

data_set_translations = {'new_confirm': 'Нещодавньо підтверджені', 'new_susp': 'Нещодавньо запідозрені',
                         'new_recover': 'Нещодавньо одужавші', 'new_death': 'Нещодавньо померлі',
                         'active_confirm': 'Хворі'}

series_translations = {'std': 'Стандартне відхилення', 'mean': 'Середнє значення', 'min': 'Мінімум', 'max': 'Максимум',
                       'count': 'Кількість'}

data_from_csv = pd.read_csv(
    'https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_settlement_dynamics.csv', sep=',',
    skiprows=0,
    parse_dates=['zvit_date'],
    index_col='zvit_date')


def group_by_property(data_frame, column):
    return data_frame.groupby(column).sum()


def filter_by_area(data_frame, area):
    return data_frame[data_frame['registration_area'] == area]


def visualize_corona_dynamics(dataframe):
    area = input('Choose area from data set: ')
    filtered = filter_by_area(dataframe, area)
    data = group_by_property(filtered, 'zvit_date')
    plt.plot(data['new_confirm'], color="red", label='Підтверджені')
    plt.plot(data['new_susp'], color='orange', label='Підозрювані')
    plt.plot(data['new_recover'], color="green", label='Одужавші')
    plt.plot(data['new_death'], color="black", label='Загиблі')
    plt.xlabel('Дата (рр-мм)')
    plt.ylabel('Кількість випадків')
    plt.title('Графік динаміки захворювань')
    plt.legend(loc='best')
    plt.show()

    plt.stackplot(data.index, data['active_confirm'], data['new_confirm'], data['new_recover'], data['new_death'],
                  colors=['red', 'orange', 'green', 'black'])
    plt.legend(['Хворі', 'Нещодавньо підтверджені', 'Нещодавньо одужавші', 'Нещодавньо померлі'], loc='upper left')
    plt.title('Графік активних інфікованих')
    plt.xlabel('Дата (рр-мм)')
    plt.ylabel('Кількість випадків')
    plt.show()


def comparison_between_areas(data_frame):
    copy = data_frame
    data = group_by_property(copy, 'registration_area')
    width = 0.5
    fig, ax = plt.subplots()
    dates = np.arange(1, data.shape[0] + 1)
    data = data.sort_values('new_confirm')
    ax.barh(dates + width, data['new_confirm'], width + 0.1, color='red', label='Хворі')
    ax.barh(dates + width, data['new_recover'], width + 0.1, color='green', label='Одужавші')
    ax.barh(dates + width, data['new_death'], width + 0.1, color='black', label='Загиблі')
    plt.title("Графік захворюваності по областях")
    plt.xlabel("Кількість випадків")
    plt.ylabel("Область")
    ax.set(yticks=dates + width, yticklabels=data.index.values)
    ax.legend(loc='best')
    plt.show()

    df_ = data_frame.rename(columns=data_set_translations)
    criteria = input('Enter criteria: ')
    with ExcelWriter('data.xlsx') as ew:
        for i in np.unique(data_frame['registration_area']):
            # data_ = df_[df_['registration_area'] == i].groupby('zvit_date')[criteria].sum().describe().drop(
            # labels=['count', '25%', '50%', '75%']).rename(series_translations)
            stats_ = df_[df_['registration_area'] == i].groupby('zvit_date')[criteria].sum()
            stats_.to_excel(ew, i)


if __name__ == '__main__':
    print(data_from_csv.head(10))
    while True:
        print("\nMENU\n")
        for option in options:
            print(option)
        choice = int(input('\nChoose option, please: '))
        if choice == 1:
            visualize_corona_dynamics(data_from_csv)
        elif choice == 2:
            comparison_between_areas(data_from_csv)
        else:
            print('Bye!')
            exit(0)
