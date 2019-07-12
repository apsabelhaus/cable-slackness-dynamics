"""
Plot the Lyapunov function results for the 3D cable driven robot tests.
(C) Andrew P. Sabelhaus, 2018
"""

# import everything we need
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# The names for each set of files to load
test_names = ['A','B','C','D']

# creat the filename lists for both the norm error and Lyap results
filenames_lyap = []
filenames_norm_err = []
prefix_lyap = 'lyap_history_3D_'
prefix_norm_err = 'norm_err_3D_'

for name in test_names:
    filenames_lyap.append(prefix_lyap + name + '.npy')
    filenames_norm_err.append(prefix_norm_err + name + '.npy')
    
# load the data files we want
# filenames_lyap = ['lyap_history_A.npy',
#                   'lyap_history_3D_B.npy']

# corrected for path
directory = './results/'
# an easy way 
correct_for_path = 0
if correct_for_path:
    for i in range(len(filenames_lyap)):
        filenames_lyap[i] = directory + filenames_lyap[i]
        filenames_norm_err[i] = directory + filenames_norm_err[i]


# Make a list of strings identifying these files, used
# as a legend later.
# This ABUSES ORDERING! ...because matplotlib assigns legends in order.
datalabels = []
for name in test_names:
    datalabels.append('Initial Condition ' + name)

# datalabels = [r'Initial Condition: $x=5.2$, $\dot x = 0$', \
#              r'Initial Condition: $x=5.5$, $\dot x = 10$', \
#              r'Initial Condition: $x=5.7$, $\dot x = -5$', \
#              r'Initial Condition: $x=6.2$, $\dot x = 0$', \
#              r'Initial Condition: $x=6.9$, $\dot x = 0$', \
#              r'Initial Condition: $x=6.9$, $\dot x = -15$']

# because I don't want to deal with 3D arrays here,
# store all the arrays in a dictionary.
results_lyap = {}
results_norm_err = {}
for name in filenames_lyap:
    results_lyap[name] = np.load(name)
for name in filenames_norm_err:
    results_norm_err[name] = np.load(name)

# recreate the timesteps for plotting. 
# this assumes we chose the same for each simulation
# (which we did, as of 2018-09-16)
t_start = 0.0 
dt = 0.01
num_timesteps = 200
timesteps = np.arange(t_start, dt*(num_timesteps+1), dt)

# Let's plot the results!
figure_size = (5,4)
fontsize = 12

# set up the layout and font size for both plots
plt.rcParams.update({'font.size': fontsize})
plt.rcParams.update({'figure.autolayout': True})

# make latex available
# plt.rc('text', usetex=True)
fig, ax = plt.subplots(figsize=figure_size)

# REMEMBER THAT PYTHON INDEXES FROM 0
# loop over data. Dictionary.
for key in results_lyap:
    # we can shorten the amount of time to plot
    last_timestep = len(timesteps)-1
    ax.plot(timesteps[0:last_timestep], 
            results_lyap[key][0:last_timestep])
# 1D:
#ax.plot(timesteps, pm_state_history[:,0])
# labels
ax.set(xlabel='Time (sec)', ylabel='Lyapunov Function (V) Value', 
    title='Cable-Driven Robot Lyapunov Analysis')
# For the gravity case, and on 2018-11-5,
# we're doing an approx to a rigid bar:
# ax.set(xlabel='Time (sec)', ylabel='Bar CoM Position (m)', 
#     title='Closed-loop slack cable control results')
ax.grid()
# legend
ax.legend(datalabels)
# make a line at the equilibrium position
#ax.axhline(y=6.5, label='Equilibrium position')
plt.show()

# Next, for the norm error:
fig2, ax2 = plt.subplots(figsize=figure_size)

for key in results_norm_err:
    # we can shorten the amount of time to plot
    last_timestep = len(timesteps)-1
    ax2.plot(timesteps[0:last_timestep], 
            results_norm_err[key][0:last_timestep])

ax2.set(xlabel='Time (sec)', ylabel='Total State Error (2-norm)', 
    title='Cable-Driven Robot State Error Analysis')

ax2.legend(datalabels)
ax2.grid()
plt.show()