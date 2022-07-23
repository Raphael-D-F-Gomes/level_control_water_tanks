# Level controle in water tanks in serie 

This repository was created to make available a discrete-time simulation that deal with the level control problem in water tanks in series.

The problem statement is: a serie of tanks are conected in each other, each tank has an input and an output flow rate in (L/min). The flow rate is controled by a water tap that has minumum and maximum limits. This water tap is subject to faults, the fault makes the flow rate null in the respective tap. The challenge is to control the flow rates aiming to approach the tanks levels to a ideal one. 


The file system_data.xlsx is all the data needed to deal with the problem.

* tank capacity (L)
* tank ideal, critical and actual level (%)
* tank minimum, maximum and actual output flow rate (L/min)
* tank output flow rate status (0 or 1)
* tank output flow rate availability (%) - Used to build the faults distribution

The executable.py run the simulation and call the plot method.
