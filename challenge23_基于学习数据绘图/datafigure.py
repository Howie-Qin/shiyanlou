import json
import pandas as pd
from matplotlib import pyplot as plt



def data_plot():
    df = pd.read_json('user_study.json')
    data = df.groupby('user_id').sum().head(10)


    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')
    ax.set_title('StudyData')

    x = data.index
    y = data.minutes
    ax.plot(x,y)
    plt.show()
    return ax

if __name__ == '__main__':
    data_plot()
