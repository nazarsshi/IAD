import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as plx
import plotly.io as plio
from pandas import ExcelWriter

options = ['1) Morbidity dynamics` visualization', '2) Areas` comparison', '3) Show areas`s situation on map',
           '4) Exit']

data_set_translations = {'new_confirm': 'Нещодавньо підтверджені', 'new_susp': 'Нещодавньо запідозрені',
                         'new_recover': 'Нещодавньо одужавші', 'new_death': 'Нещодавньо померлі',
                         'active_confirm': 'Хворі'}

series_translations = {'std': 'Стандартне відхилення', 'mean': 'Середнє значення', 'min': 'Мінімум', 'max': 'Максимум',
                       'count': 'Кількість'}

data_from_csv = pd.read_csv(
    'covid19_by_settlement_dynamics.csv', sep=',',
    skiprows=0,
    parse_dates=['zvit_date'],
    index_col='zvit_date')


def group_by_property(data_frame, column):
    return data_frame.groupby(column).sum()


def filter_by_area(data_frame, area):
    return data_frame[data_frame['registration_area'] == area]


def linear_transform(column):
    return [sum(column[:i + 1]) for i in range(len(column))]


def visualize_corona_dynamics(dataframe):
    area = input('Choose area from data set: ')
    filtered = filter_by_area(dataframe, area)
    data = group_by_property(filtered, 'zvit_date')
    plt.plot(data.index, data['new_confirm'], color="red", label='Підтверджені')
    plt.plot(data.index, data['new_susp'], color='orange', label='Підозрювані')
    plt.plot(data.index, data['new_recover'], color="green", label='Одужавші')
    plt.plot(data.index, data['new_death'], color="black", label='Загиблі')
    plt.xlabel('Дата (рр-мм)')
    plt.ylabel('Кількість випадків')
    plt.title('Графік динаміки захворювань')
    plt.legend(loc='best')
    plt.show()

    # f = lambda d: [sum(d[:i + 1]) for i in range(len(d))]
    plt.plot(data.index, linear_transform(data['new_confirm']), color="red", label='Підтверджені')
    plt.plot(data.index, linear_transform(data['new_susp']), color='orange', label='Підозрювані')
    plt.plot(data.index, linear_transform(data['new_recover']), color="green", label='Одужавші')
    plt.plot(data.index, linear_transform(data['new_death']), color="black", label='Загиблі')
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

    first_area = input("Enter first area: ")
    second_area = input("Enter second area: ")

    copy = data_frame
    first_area_ = filter_by_area(copy, first_area)
    second_area_ = filter_by_area(copy, second_area)

    first_data = group_by_property(first_area_, 'zvit_date')
    second_data = group_by_property(second_area_, 'zvit_date')

    fig, (ax1, ax2) = plt.subplots(2)

    ax1.plot(first_data.index, linear_transform(first_data['new_confirm']), color="red", label='Підтверджені')
    ax1.plot(first_data.index, linear_transform(first_data['new_susp']), color='orange', label='Підозрювані')
    ax1.plot(first_data.index, linear_transform(first_data['new_recover']), color="green", label='Одужавші')
    ax1.plot(first_data.index, linear_transform(first_data['new_death']), color="black", label='Загиблі')
    ax1.set_xlabel('Дата (рр-мм)')
    ax1.set_ylabel('Кількість випадків')
    ax1.set_title(first_area + ' область')
    ax1.legend(loc='best')

    ax2.plot(second_data.index, linear_transform(second_data['new_confirm']), color="red", label='Підтверджені')
    ax2.plot(second_data.index, linear_transform(second_data['new_susp']), color='orange', label='Підозрювані')
    ax2.plot(second_data.index, linear_transform(second_data['new_recover']), color="green", label='Одужавші')
    ax2.plot(second_data.index, linear_transform(second_data['new_death']), color="black", label='Загиблі')
    ax2.set_xlabel('Дата (рр-мм)')
    ax2.set_ylabel('Кількість випадків')
    ax2.set_title(second_area + ' область')
    ax2.legend(loc='best')

    plt.tight_layout()
    plt.show()

    df_ = data_frame.rename(columns=data_set_translations)
    criteria = input('Enter criteria: ')
    with ExcelWriter('data.xlsx') as ew:
        for i in np.unique(data_frame['registration_area']):
            # data_ = df_[df_['registration_area'] == i].groupby('zvit_date')[criteria].sum().describe().drop(
            # labels=['count', '25%', '50%', '75%']).rename(series_translations)
            stats_ = df_[df_['registration_area'] == i].groupby('zvit_date')[criteria].sum()
            stats_.to_excel(ew, i)


def show_corona_situation_on_map(df):
    geo_data = json.load(open('ukraine_al4.geojson', 'r', encoding='utf-8'))
    df = df.groupby('registration_area').sum()
    for i in range(np.size(np.array(geo_data['features']))):
        value = geo_data['features'][i]['properties']['localname']
        if value != 'Київ':
            geo_data['features'][i]['properties']['localname'] = value.replace(" область", "")
        else:
            geo_data['features'][i]['properties']['localname'] = "м. " + value
    state_id_map = {}
    for feature in geo_data['features']:
        feature['id'] = feature['properties']['id']
        state_id_map[feature['properties']['localname']] = feature['id']

    plio.renderers.default = 'browser'
    val = pd.DataFrame(np.array(df.index.values), columns=['tick'])

    df['id'] = val['tick'].apply(lambda x: state_id_map[x]).values

    settlement_data = pd.read_csv(
        'covid19_by_settlement_actual.csv')

    print('Choose color for scattermapplot: total_susp,total_confirm,total_death,total_recover')
    color1 = input()
    settlement_data[color1 + ' koef'] = np.log10(settlement_data[color1])

    plot = plx.scatter_mapbox(settlement_data, 'registration_settlement_lat', 'registration_settlement_lng', zoom=6,
                              hover_name="registration_settlement", color=color1 + ' koef',
                              hover_data=["total_susp", "total_confirm", "total_death", "total_recover"])
    plot.update_layout(mapbox_style="carto-positron")

    plot.update_layout(
        mapbox={
            'style': "open-street-map",
            'center': {'lon': 30.52, 'lat': 50.4501},
            'zoom': 5, 'layers': [{
                'source': geo_data, 'type': 'line', 'color': 'green'}]},
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0})
    plot.show()
    #
    print('Choose color for choropleth: new_susp,new_confirm,active_confirm,new_death,new_recover ')
    color2 = input()
    plot = plx.choropleth_mapbox(df, locations='id', geojson=geo_data, color=color2,
                                 hover_name=df.index.values, mapbox_style='carto-positron',
                                 hover_data=['new_death'],
                                 center={'lat': 50.4501, 'lon': 30.5234}, opacity=0.5, zoom=4)
    plot.update_geos(fitbounds='locations', visible=False)

    plot.show()


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
        elif choice == 3:
            show_corona_situation_on_map(data_from_csv)
        else:
            print('Bye!')
            exit(0)
