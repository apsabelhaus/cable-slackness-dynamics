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
% But make it a bit more "out" so we see the +- 1.5 labels
%xmin = -1.5;
%xmax = 1.5;
xmin = -1.7;
xmax = 1.7;

% Add a line along the x-axis and y-axis.
% Adapted from: https://www.mathworks.com/matlabcentral/answers/97996-is-it-possible-to-add-x-and-y-axis-lines-to-a-plot-in-matlab
colorAxisLine = 'k';
linestyleAxisLine = '-';

% To use latex characters in the plots,
set(0, 'defaulttextinterpreter', 'latex');

% Adjusting the text size - set a variable here to use everywhere below.
fontsize = 14;

%% Plot 1 and 1.5: F = k \delta x
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
ylabel('$F$, applied force');
xlabel('$\Delta \ell$, cable stretch');

% Next, also plot the piecewise-continuous rectified function.
% Just zero out the less-than-zero terms:
F_rect = (F >= 0).*F;

% make the plot!
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);
% Make the line thick and black.https://www.sharelatex.com/project/591c89f19af743d90acc8102
plot(dx, F_rect,'k');


handle = gca;
% Plot the lines:
line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);

% Axis labels:
ylabel('$F$, applied force');
xlabel('$\Delta \ell$, cable stretch');

%% Plot 2: Logistic function
% This plot will show one logistic function, for reference.

% For the logistic barrier function, declare two constants that control
% its form and location.
% See below for more information about what these are and what they do.
% Take a look at the Wikipedia page about analytic approximations to 
% the step function:
% https://en.wikipedia.org/wiki/Heaviside_step_function#Analytic_approximations
logistic_k = 8; % was 5, looked nicer that way.
logistic_x0 = 0;

% TO-DO: look at more general sigmoid functions. Is there one that goes
% "negative" and then doesn't let a cable "push"?
% Ideas include: 
% (1) multiply the logistic(x)*F(x) by logistic(x) again. Since l(x)F(x)
% "goes negative" maybe we can use that?
% (2) what happens if we use another of the smooth sigmoid curves under
% that wikipedia page?
% (3) maybe we do logisitic(x) - small constant, and adjust the offset x0
% accordingly so that it's still l(x)=0 at x=0? Motivation is that since
% F(x) is negative less than zero, and then logistic(x) - small const is
% also negative less than zero, then the product must be greater than or
% equal to zero. BUT, we'd need a way to send the +x part back up to 1 in
% the limit, otherwise we can't claim that this approximates the step
% function (the limit will be off by the small constant.)

% The logistic function in dx looks like
% f(x) = 1 / (1 + exp( -k*(x-x0)))

% To-do: do we need pointwise multiplication here?
logistic_func = 1 ./ (1 + exp(-logistic_k*(dx - logistic_x0)));
% some small constant... BUT still need to adjust x0 probably??
%logistic_func = 1 ./ (1 + exp(-logistic_k*(dx - logistic_x0))) - 0.1;
% Result: doesn't work. The "negativeness" of the logistic - small const
% accumulates, so the spring force actually really pulls more in x < 0,
% e.g., we again cannot claim that the limits match the heaviside step
% function.

% Plot this on a new graph.
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);
% But make it a bit more "out" so we see the +- 1.5 labels
%eps = 0.2;
%xlim([xmin-eps, xmax+eps]);
%ylim([xmin-eps, xmax+eps]);


% Plot the logistic.
plot(dx, logistic_func, 'b', 'LineWidth', 2);

handle = gca;
% Plot the lines:
% line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
% line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
% Add a dashed line at y=1 to emphasize the unit-ness
% line( get(handle,'XLim'), [1 1], 'Color', colorAxisLine, 'LineStyle', '--');

% Axis labels:
ylabel('$L(x)$');
xlabel('$x$');
title('Unit Logistic Function (slope of $\alpha=8$)');

% Move the axes around.
ax = gca;
ax.XAxisLocation = 'origin';
ax.YAxisLocation = 'origin';
%ax.XRuler.FirstCrossoverValue  = 0; % X crossover with Y axis
%ax.XRuler.SecondCrossoverValue  = 0; % X crossover with Y axis
%ax.YRuler.FirstCrossoverValue  = 0; % Y crossover with X axis
%ax.YRuler.SecondCrossoverValue  = 0; % X crossover with Y axis

% Make the text bigger
set(gca, 'fontsize', fontsize);


% In comparison, also do the heaviside step function:
% Plot this on a new graph.
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);
% luckily MATLAB already has the heaviside step built-in
plot(dx, heaviside(dx), 'b.', 'LineWidth', 2);
% also add a point at zero, but big.
plot(0, heaviside(0), 'b.', 'MarkerSize', 20);
% 

% Axis labels:
ylabel('$H(x)$');
xlabel('$x$');
title('Heaviside Step Function');

% Move the axes around.
ax = gca;
ax.XAxisLocation = 'origin';
ax.YAxisLocation = 'origin';

% Make the text bigger
set(gca, 'fontsize', fontsize);

return;

%% Plot 3: Cable force multiplied by logisitic function

% Given that the previous two sections were run, we can calculate the total force of
% the logistically-smoothed cable at a point:

smoothed_F = F.*logistic_func;

% note that this is a pointwise multiplication of two (column?) vectors.

% Plot this on a new graph.
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);

% Plot the smoothed force.
plot(dx, smoothed_F, 'k');

handle = gca;
% Plot the lines:
line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);

% Axis labels:
ylabel('$F_a(\Delta \ell)$');
xlabel('$\Delta \ell$');

%% Plot 3.5: Cable force (rectified) multiplied by the logistic function

% This is a model for a "heavy" cable that always pulls in a bit even
% after it's slack. Cite the civil engineering folks here.

smoothed_F_heavy = F_rect.*logistic_func;

% Plot this on a new graph.
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);

% Plot the smoothed force.
plot(dx, smoothed_F_heavy, 'k');

handle = gca;
% Plot the lines:
line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);

% Axis labels:
ylabel('$F_a(\Delta \ell)$');
xlabel('$\Delta \ell$');
title('Heavier cable, non smooth');

% ...actually, this isn't right either. We need a function that exists
% in quadrants 1 and 2. Let's hack it together for now. Do the logistically
% smoothed version for values greater than zero, and just the logistic
% function for values less than zero. 

F_heavy = smoothed_F_heavy;
% adjust upwards all the positive entries. That's length/2 + 1 to end.
% Hack: it's 0.5.
logistic_offset = 0.5;
F_heavy(length(F_heavy)/2 + 1 : end) = F_heavy(length(F_heavy)/2 + 1 : end) + logistic_offset;
% Sub in the logistic function for the negative values.
F_heavy(1: length(F_heavy)/2) = logistic_func(1 : length(logistic_func)/2);

% Plot.
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);

% Plot the smoothed force.
plot(dx, F_heavy, 'k');

handle = gca;
% Plot the lines:
line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);

% Axis labels:
ylabel('$F_a(\Delta \ell)$');
xlabel('$\Delta \ell$');
title('Heavier cable, non passive');

%% Plot 4: comparison of piecewise function and logistically smoothed function

% Plot this on a new graph.
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);

handle = gca;
% Plot the lines:
line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);

% Rectified force: plot in red
plot(dx, F_rect, 'r', 'LineWidth', 3);
% Smoothed force: blue
plot(dx, smoothed_F, 'b', 'LineWidth', 3);
% Heavier cable: magenta
plot(dx, F_heavy, 'm', 'LineWidth', 3);



% Axis labels:
ylabel('$F_a(\ell$)', 'FontSize',14);
xlabel('$F_c(\ell)$','FontSize',14);

title('Cable Dynamics: Piecewise vs. Smooth');










