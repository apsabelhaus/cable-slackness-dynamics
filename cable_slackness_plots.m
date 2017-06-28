% cable_slackness_plots.m
% Drew (Andrew P.) Sabelhaus
% Berkeley Emergent Space Tensegrities Lab (BEST)
% Copyright 2017

% This script produces the plots for a paper about a logistically-smoothed 
% cable slackness dynamics model for cable-driven robots.

% TO-DO: MAKE THESE PLOTS WITH DAMPING INCLUDED.
% Specifically, something like F = k (\Delta x) + c || \dot \Delta x ||

%% Setup.

% Clear out the workspace.
clear all;
close all;
clc;

% Declare some constants for the model.
% We'll work in N and cm.
% So, the spring constant is in N / cm:
k = 2;

% For all the plots, retain the same number of points.
num_pts = 1000;

% Let's go for some range in x.
xmin = -2;
xmax = 2;

% Add a line along the x-axis and y-axis.
% Adapted from: https://www.mathworks.com/matlabcentral/answers/97996-is-it-possible-to-add-x-and-y-axis-lines-to-a-plot-in-matlab
colorAxisLine = 'k';
linestyleAxisLine = ':';


%% Plot 1: F = k \delta x
% This plot shows the linear function F = k \delta x, 
% without the rectification.

% Calculate a set of points to plot.
dx = linspace(xmin, xmax, num_pts);

% Then, the applied force will be:
F = k*dx;
% ...a vector of size (num_pts)x1.

% Make a plot!
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);
% Make the line thick and black.https://www.sharelatex.com/project/591c89f19af743d90acc8102
plot(dx, F,'k');


handle = gca;
% Plot the lines:
line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);

% Axis labels:
ylabel('F, applied force');
xlabel('\Delta x, cable stretch');

%% Plot 2: Logistic function
% This plot will show one logistic function, for reference.

% For the logistic barrier function, declare two constants that control
% its form and location.
% See below for more information about what these are and what they do.
% Take a look at the Wikipedia page about analytic approximations to 
% the step function:
% https://en.wikipedia.org/wiki/Heaviside_step_function#Analytic_approximations
logistic_k = 5;
logistic_x0 = 0;

% The logistic function in dx looks like
% f(x) = 1 / (1 + exp( -k*(x-x0)))

% To-do: do we need pointwise multiplication here?
logistic_func = 1 ./ (1 + exp(-logistic_k*(dx - logistic_x0)));

% Plot this on a new graph.
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);

% Plot the logistic.
plot(dx, logistic_func, 'k');

handle = gca;
% Plot the lines:
line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);

% Axis labels:
ylabel('L(\Delta x)');
xlabel('\Delta x');

%% Plot 3: Logistic function multiplied by 



