import numpy as np
import matplotlib.pyplot as plt
from typing import TypeVar


# Dataframe type
PandasDataFrame = TypeVar('pd.core.frame.DataFrame')


def plot_simulation_data(df_system: PandasDataFrame, df_simulation_data: PandasDataFrame) -> None:

    # list and number of tanks
    tanks = list(df_simulation_data)
    n_tanks = len(list(df_simulation_data))

    # Adapting data to plot
    df_simulation_data = df_simulation_data * 100

    # Critical and ideal level data
    critical_level = [df_system['critical_level'].values * 100] * len(df_simulation_data)
    critical_level = np.transpose(critical_level)
    ideal_level = [df_system['ideal_level'].values * 100] * len(df_simulation_data)
    ideal_level = np.transpose(ideal_level)

    # Plotting simulation data
    for i in range(n_tanks):
        plt.plot(df_simulation_data[tanks[i]])

    plt.plot(critical_level[0], linestyle='--', color='red')
    plt.plot(ideal_level[0], linestyle='--', color='green')

    # Building legend
    legend = [None] * (n_tanks + 2)
    legend[-1] = 'Ideal level'
    legend[n_tanks] = 'Critical level'
    legend[0:n_tanks] = tanks

    plt.legend(legend)
    plt.ylabel('Tanks Level (%)')
    plt.xlabel('Time (min)')
    plt.ylim([0, 100])
    plt.show()
