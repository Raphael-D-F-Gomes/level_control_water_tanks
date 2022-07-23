import numpy as np
import pandas as pd
from typing import TypeVar, Tuple

# Dataframe type
PandasDataFrame = TypeVar('pd.core.frame.DataFrame')


def level_update(df_system: PandasDataFrame) -> list:
    """
    params:
            df_system: dataframe with system data
    returns:
            level status
    """

    # Number of buffers
    n_tanks = len(df_system) - 1

    # Building level status array
    level_status = [0] * (n_tanks + 1)

    # Calculating level
    for i in range(1, n_tanks + 1):
        level_status[i] = ((df_system['level_status'][i] * df_system['capacity'][i])
                           + df_system['output_flow_rate'][i - 1] - df_system['output_flow_rate'][i]) \
                          / df_system['capacity'][i]

        # Level can't be negative
        if level_status[i] <= 0:
            level_status[i] = 0

    return level_status
