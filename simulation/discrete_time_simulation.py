import numpy as np
import pandas as pd
from typing import TypeVar
from simulation.output_setups import output_setups_optimization as oso
from simulation.level_update import level_update as lp


class DiscreteSimulation:
    """
    Class designed to simulate the behavior of a plant considering fails in the machines
    to analyse the optimization and decision making of the code
    """
    # Dataframe type
    PandasDataFrame = TypeVar('pd.core.frame.DataFrame')

    def __init__(self, df_system: PandasDataFrame, distribution: PandasDataFrame) -> None:
        """
        params: df_system: dataframe with system data
                distribution: dataframe with fault distribution
        """

        # dataframe with plant, conveyors, levels and scenarios information
        self.df_system = df_system
        self.distribution = distribution

        # number of tanks
        self.n_tanks = len(df_system) - 1

        # distribution period
        self.distribution_period = len(distribution)

    def simulator(self) -> PandasDataFrame:
        """
        returns:
                dataframe with simulation data
        """

        # Lista of tanks
        tanks = list(self.df_system['tanks'])

        # Building dataframe for simulation data
        simulation_data_header = [f'level {tanks[i]}' for i in range(1, self.n_tanks + 1)]
        df_simulation_data = pd.DataFrame(np.ones([self.distribution_period, self.n_tanks]),
                                          columns=simulation_data_header)

        # Generating setups
        for c in range(self.distribution_period):

            # Updating the status (number of machines working in each station)
            self.df_system['output_status'] = self.distribution.loc[c].values

            # Triggering the balance optimization and recovering a list of machines speed
            self.df_system['output_flow_rate'] = oso(self.df_system)

            # Calculating level to the next instant
            self.df_system['level_status'] = lp(self.df_system)

            # Saving levels
            level_status = self.df_system['level_status'].values
            df_simulation_data.loc[c] = level_status[1:self.n_tanks + 1]

        return df_simulation_data
