from typing import TypeVar
import pandas as pd
from ortools.sat.python import cp_model
import numpy as np


PandasDataFrame = TypeVar('pd.core.frame.DataFrame')


def output_setups_optimization(df_system: PandasDataFrame) -> list:
    """
    params:
            df_system: dataframe with system data
    returns:
            flow rate setups
    """

    # Number of conveyors
    n_tanks = len(df_system) - 1

    # Critical level safety measure
    for i in range(1, n_tanks + 1):
        if df_system['level_status'][i] >= df_system['critical_level'][i]:
            df_system['output_status'][i - 1] = 0

    # Min and max flow rate limits
    min_flow_rate = list(df_system['output_min_flow_rate'] * df_system['output_status'])
    max_flow_rate = list(df_system['output_max_flow_rate'] * df_system['output_status'])

    # Calling solver
    solver = cp_model.CpModel()

    # Building decision variables
    flow_rate_var = [None] * (n_tanks + 1)
    flow_rate_var[0] = solver.NewIntVar(int(min_flow_rate[0]), int(max_flow_rate[0]), f'v0')

    flow_rate_var[1:n_tanks+1] = [solver.NewIntVar(int(min_flow_rate[j]), int(max_flow_rate[j]), f'v{j}')
                                  for j in range(1, n_tanks + 1)]

    # variable used to min max problem
    z = [solver.NewIntVar(0, int(1e5), f'z{j}') for j in range(n_tanks)]

    for i in range(1, n_tanks + 1):

        # Level in the next instant
        tank_level = int(df_system['level_status'][i] * df_system['capacity'][i])\
                     + flow_rate_var[i - 1] - flow_rate_var[i]

        solver.Add(tank_level - int(df_system['ideal_level'][i] * df_system['capacity'][i]) <= z[i - 1])
        solver.Add(tank_level - int(df_system['ideal_level'][i] * df_system['capacity'][i]) >= -z[i - 1])

    # Minimize the difference between the actual levels and the ideal levels
    solver.Minimize(sum(z))

    # Collecting results
    results = cp_model.CpSolver()
    status = results.Solve(solver)
    results.parameters.enumerate_all_solutions = True

    # Getting arrays with machines speeds and machines that was turned off
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Saving results
        output_setups = [results.Value(flow_rate_var[c]) for c in range(n_tanks + 1)]
    else:
        output_setups = min_flow_rate
        print('infactivel')

    return output_setups
