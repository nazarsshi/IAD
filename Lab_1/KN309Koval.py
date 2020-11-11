import pandas as pnds
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.pipeline import make_pipeline

from KN309Koval2 import *

plt.style.use('ggplot')


class DateFormatter(TransformerMixin, BaseEstimator):

    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, y=None):
        data_set = X.copy()

        def formatDate(date):
            day, month = date.split('.')
            dictionary = {'Aug': '08', 'Jul': '07'}
            month = dictionary[month]
            return f'{day}.{month}.2019'

        data_set[self.columns] = data_set[self.columns].applymap(formatDate)
        return data_set

    def fit(self, X, y=None):
        return self


class TemperatureTransformer(TransformerMixin, BaseEstimator):

    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, y=None):
        X[self.columns] = X[self.columns].applymap(lambda x: ((x - 32) * 5) / 9)
        return X

    def fit(self, X, y=None):
        return self


class TimeFormatter(TransformerMixin, BaseEstimator):

    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, y=None):
        def formatTime(time):
            time, daypart = time.split(' ')
            hour, minute = map(int, time.split(':'))

            return f'{hour}:{minute}' if daypart == 'AM' else f'{(hour + 12) % 24}:{minute}'

        X[self.columns] = X[self.columns].applymap(formatTime)
        return X

    def fit(self, X, y=None):
        return self


class PercentageTransformer(TransformerMixin, BaseEstimator):

    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, y=None):
        X[self.columns] = X[self.columns].applymap(lambda x: float(x[:-1]) / 100)
        return X

    def fit(self, X, y=None):
        return self


class SpeedTransformer(TransformerMixin, BaseEstimator):

    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, y=None):
        X[self.columns] = X[self.columns].applymap(lambda x: 0.7 * float(x.split()[0]))
        return X

    def fit(self, X, y=None):
        return self


class DateTimeConcatenator(TransformerMixin, BaseEstimator):

    def __init__(self, dateColumn, timeColumn):
        self.dateColumn = dateColumn
        self.timeColumn = timeColumn

    def transform(self, X, y=None):
        X['DateTime'] = pnds.to_datetime(X[self.dateColumn] + ' ' + X[self.timeColumn], infer_datetime_format=True)
        return X.drop(columns=[self.dateColumn, self.timeColumn])

    def fit(self, X, y=None):
        return self


def format_data(data):
    pipeline = make_pipeline(
        DateFormatter(['day/month']),
        TemperatureTransformer(['Temperature']),
        TimeFormatter(['Time']),
        PercentageTransformer(['Humidity']),
        SpeedTransformer(['Wind Speed', 'Wind Gust']),
        DateTimeConcatenator(dateColumn='day/month', timeColumn='Time'))

    formatted_data = pipeline.fit_transform(data).sort_values(by='DateTime')
    return formatted_data


def select_numeric_column():
    cols = ['Wind Speed',
            'Humidity',
            'Dew Point',
            'Wind Gust',
            'Temperature',
            'Pressure', ]

    print()
    for i, col in enumerate(cols):
        print(f'\t\t{i + 1} - {col}')

    return cols[int(input()) - 1]


def select_categorical_column():
    cols = ['Condition',
            'Wind']

    print()
    for i, col in enumerate(cols):
        print(f'\t\t{i + 1} - {col}')

    return cols[int(input()) - 1]


if __name__ == "__main__":

    data = format_data(pnds.read_csv("DATABASE.csv", sep=';'))

    print(data.head(5))

    options = ['Exit', 'Time series', 'Hist', 'Bar', 'Scatter', 'Pie chart']
    while True:
        print('MENU:')
        for i, option in enumerate(options):
            print(f'\t{i} - {option}')
        option = input()

        if option == '0':
            exit(0)
        if option == '1':
            col = select_numeric_column()
            show_time_series(data['DateTime'], data[col])
        if option == '2':
            col = select_numeric_column()
            visualize_hist(data[col])
        if option == '3':
            col = select_categorical_column()
            make_bar(data[col])
        if option == '4':
            col0 = select_numeric_column()
            col1 = select_numeric_column()
            col2 = select_numeric_column()
            make_many_scatters([data[col1], data[col2]], data[col0])
        if option == '5':
            col = select_categorical_column()
            visualize_pie_graph(data[col])
