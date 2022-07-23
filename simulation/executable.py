import pandas as pd
from simulation.distribution_generator import distribution_generator
from simulation.discrete_time_simulation import DiscreteSimulation
from simulation.plot_simulation_data import plot_simulation_data


# simulation period (5 hours)
period = 5 * 60

# Reading system data
df_system = pd.read_excel('system_data.xlsx', sheet_name='system_data', index_col=0, engine="openpyxl")
df_system.reset_index(drop=True)
df_system = pd.DataFrame(df_system).dropna(how='all')
print(df_system)

# tank output fault distribution
fault_distribution = distribution_generator(period, df_system)
print(fault_distribution)

# Calling class
simulator = DiscreteSimulation(df_system, fault_distribution)

# Collecting simulation data
df_data = simulator.simulator()
print(df_data)

# Plotting data
plot_simulation_data(df_system, df_data)
