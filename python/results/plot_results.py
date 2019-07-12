"""
Plot an initial round of simulations for the 1D cable slackness controller.
(C) Andrew P. Sabelhaus, 2018
"""

# import everything we need
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# load the data files we want
filenames = ['1D_p5pt2_v0.npy', '1D_p5pt5_v10.npy', \
            '1D_p5pt7_vminus5.npy', '1D_p6pt2_v0.npy', \
            '1D_p6pt9_v0.npy', '1D_p6pt9_vminus15.npy']
# corrected for path
directory = './results/'
# an easy way 
correct_for_path = 1
if correct_for_path:
    for i in range(len(filenames)):
        filenames[i] = directory + filenames[i]


# Make a list of strings identifying these files, used
# as a legend later.
datalabels = [r'Initial Condition: $x=5.2$, $\dot x = 0$', \
             r'Initial Condition: $x=5.5$, $\dot x = 10$', \
             r'Initial Condition: $x=5.7$, $\dot x = -5$', \
             r'Initial Condition: $x=6.2$, $\dot x = 0$', \
             r'Initial Condition: $x=6.9$, $\dot x = 0$', \
             r'Initial Condition: $x=6.9$, $\dot x = -15$']

# because I don't want to deal with 3D arrays here,
# store all the arrays in a dictionary.
results = {}
for name in filenames:
    results[name] = np.load(name)

# recreate the timesteps for plotting. 
# this assumes we chose the same for each simulation
# (which we did, as of 2018-09-16)
t_start = 0.0 
dt = 0.01
num_timesteps = 1000
timesteps = np.arange(t_start, dt*(num_timesteps+1), dt)

# Let's plot the results!
# make latex available
plt.rc('text', usetex=True)
fig, ax = plt.subplots()
# REMEMBER THAT PYTHON INDEXES FROM 0
# loop over data. Dictionary.
for key in results:
    # we can shorten the amount of time to plot
    last_timestep = 500;
    ax.plot(timesteps[0:last_timestep], 
            results[key][0:last_timestep,0])
# 1D:
#ax.plot(timesteps, pm_state_history[:,0])
# labels
ax.set(xlabel='Time (sec)', ylabel='Mass position (m)', 
    title='Closed-loop slack cable control results')
# For the gravity case, and on 2018-11-5,
# we're doing an approx to a rigid bar:
ax.set(xlabel='Time (sec)', ylabel='Bar CoM Position (m)', 
    title='Closed-loop slack cable control results')
ax.grid()
# legend
ax.legend(datalabels)
# make a line at the equilibrium position
#ax.axhline(y=6.5, label='Equilibrium position')
plt.show()
