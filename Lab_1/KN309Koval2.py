import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


def make_bar(X):
    labels = np.unique(X)
    sizes = [X[X == p].shape[0] for p in labels]
    plt.figure(num=None, figsize=(24, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.barh([a[0] for a in sorted(zip(labels, sizes), key=lambda x: x[1])],
             [a[1] for a in sorted(zip(labels, sizes), key=lambda x: x[1])])
    plt.xlabel('Count')
    plt.ylabel(X.name)
    plt.title(f'{X.name} bar')
    plt.show()


def visualize_pie_graph(X, top=4):
    labels = np.unique(X)
    sizes = [X[X == x].shape[0] for x in labels]
    t = sorted(zip(labels, sizes), key=lambda x: x[-1])
    sizes = [k[1] for k in t]
    labels = [k[0] for k in t]
    labels = ['Others'] + labels[-top:]
    sizes = [sum(sizes[:-top])] + sizes[-top:]
    plt.figure(num=None, figsize=(5, 5), dpi=80, facecolor='w', edgecolor='k')

    plt.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title(f'{X.name} pie')
    plt.show()


def visualize_hist(X):
    plt.figure(num=None, figsize=(24, 6), dpi=80, facecolor='w', edgecolor='k')

    scale = X.std()
    loc = X.mean()
    x__ = np.linspace(X.min(), X.max(), 1000)
    y__ = norm.pdf(x__, loc, scale)

    plt.hist(X, label=f'{X.name} hist', density=True)
    plt.plot(x__, y__, label=f'Normal({scale:.3f}, {loc:.3f})')
    plt.legend(loc='upper right')
    plt.xlabel(X.name)
    plt.ylabel('Count')
    plt.title(f'{X.name} hist')
    plt.show()


def show_time_series(X, Y):
    plt.figure(num=None, figsize=(24, 6), dpi=80, facecolor='w', edgecolor='k')
    min_ = min(zip(X, Y), key=lambda x: x[1])
    max_ = max(zip(X, Y), key=lambda x: x[1])
    plt.plot(X, Y, label=Y.name)
    plt.scatter(*max_, color='green', label='Max')
    plt.scatter(*min_, color='red', label='Min')
    plt.title(f'{Y.name} time series')
    plt.xlabel(X.name)
    plt.ylabel(Y.name)
    plt.legend(loc='upper left')
    plt.show()


def show_scatter(X, Y):
    plt.figure(num=None, figsize=(24, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.xlabel(X.name)
    plt.ylabel(Y.name)
    plt.title(X.name + "-" + Y.name)
    plt.scatter(X, Y)
    plt.show()


def make_many_scatters(Y, x):
    with plt.style.context('ggplot'):
        n = int(np.ceil(np.sqrt(len(Y))))
        # fig, axes = plt.subplots(nrows=n, ncols=n, figsize=(7, 7))
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(5, 7))
        fig.set_figheight(7)
        fig.set_figwidth(10)
        for i, a in enumerate(axes.flatten()):
            a.scatter(x, Y[i])
            a.set_title(f'{x.name} - {Y[i].name}')
            a.set_ylabel(Y[i].name)
            a.set_xlabel(x.name)
        plt.tight_layout()
        plt.show()
