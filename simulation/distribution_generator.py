import pandas as pd
import math
import numpy as np
import random as rd
from typing import TypeVar


# Dataframe type
PandasDataFrame = TypeVar('pd.core.frame.DataFrame')


def distribution_generator(period: int, df_system: PandasDataFrame) -> PandasDataFrame:
    """
    Method designed to create a discrete time distribution
    params: period: The input parameter is the sample period for the discrete time distribution
            df_system: plant data
    return: machines_distribution: returns a dataframe with the discrete time distribution
    """

    # Considering one working day, time step in minutes
    time_step = 1

    # Number of tanks
    n_tanks = len(df_system['availability'])

    # Array of small, medium and large fails
    faults = [np.zeros(math.ceil(2 / time_step)), np.zeros(math.ceil(3 / time_step)),
              np.zeros(math.ceil(4 / time_step))]

    # Number of time-steps on each fault
    n_instant_fault = [len(faults[0]), len(faults[1]), len(faults[2])]

    # Array of the discrete time distribution
    distribution = [[] for _ in range(n_tanks)]
    n_fault = np.zeros(3).astype(int)

    for j in range(n_tanks):

        # Number of zeros by the availability of each machine
        n_zeros = math.ceil((1 - df_system['availability'].values[j]) * period)

        # Ordering the faults
        if n_zeros - n_instant_fault[2] >= 0:
            n_zeros -= n_instant_fault[2]
            n_fault[2] = 1
        if n_zeros - n_instant_fault[1] >= 0:
            n_zeros -= n_instant_fault[1]
            n_fault[1] = 1

        # Number of small faults
        n_fault[0] = math.ceil(n_zeros / n_instant_fault[0])

        # Number of zeros re-adapted
        n_zeros = n_fault[2] * n_instant_fault[2] + n_fault[1] * n_instant_fault[1] + n_fault[0] * n_instant_fault[0]

        # Random position of medium and big faults
        pos_fault = [rd.randint(1, (period - 1 - n_zeros)), rd.randint(1, (period - 1 - n_zeros))]

        # Creating the distribution and adding the faults
        distribution[j] = np.ones(period - n_zeros)
        if n_fault[2] == 1:
            distribution[j] = np.insert(distribution[j], pos_fault[1], faults[2])
        if n_fault[1] == 1:
            distribution[j] = np.insert(distribution[j], pos_fault[0], faults[1])

        for i in range(n_fault[0]):
            pos_small_fault = rd.randint(1, len(distribution[j]) - 1)
            distribution[j] = np.insert(distribution[j], pos_small_fault, faults[0])

    # List of the machines names
    tanks_list = [m for m in df_system['tanks'].values]

    # Adapting the distribution for the problem
    distribution_adapted = []
    for i in range(period):
        distribution_adapted.append([distribution[j][i] for j in range(n_tanks)])

    # Saving distribution in another dataframe to visual effect
    faults_distribution = pd.DataFrame(np.array(distribution_adapted), columns=tanks_list)

    with pd.ExcelWriter("distribution.xlsx") as writer:
        faults_distribution.to_excel(writer, sheet_name="distribution")

    return faults_distribution
