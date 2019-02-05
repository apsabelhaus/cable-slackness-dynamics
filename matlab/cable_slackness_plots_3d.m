% cable_slackness_plots_3d.m
% Drew (Andrew P.) Sabelhaus
% Berkeley Emergent Space Tensegrities Lab (BEST)
% Copyright 2019

% This script produces the plots for a paper about a logistically-smoothed 
% cable slackness dynamics model for cable-driven robots.

% This file creates a 3D version of the cable slackness plots. In
% particular, this is for comparing models of BOTH spring and damping terms
% together. The two models under consideration are described below.

% Consistent with the literature, the two state variables are
% x1 = position
% x2 = velocity

%% Setup.

% Clear out the workspace.
clear all;
close all;
clc;

% Declare some constants for the model.
% We'll work in N and cm.
% So, the spring constant is in N / cm:
k = 3;
% And for the damper,
c = 2;

% For all the plots, retain the same number of points.
num_pts = 200;

% Let's go for some range in x.
xmin = -1.5;
xmax = 1.5;

% Add a line along the x-axis and y-axis.
% Adapted from: https://www.mathworks.com/matlabcentral/answers/97996-is-it-possible-to-add-x-and-y-axis-lines-to-a-plot-in-matlab
colorAxisLine = 'k';
linestyleAxisLine = '-';


%% Plot 1 and 1.5: F = - k \delta x - c \dot x
% This plot shows the linear function F = - k \delta x - c \dot x.
% But, what we will plot is -Fc here, so that we show both cable forces
% being passive. Our claim will be that -Fs and -Fd are passive.

% Calculate a set of points to plot.
dx = linspace(xmin, xmax, num_pts);
% And for the velocities, do the same.
xdot = linspace(xmin, xmax, num_pts);

% We grid out these points for a 2D plot.
[DX, XDOT] = meshgrid(dx, xdot);
% Then, we can calculate the total force using MATLAB's elementwise
% operation.
Fs = -k * DX;
Fd = -c * XDOT;

% And since these are now planes, we can simply add.
% Here's where we flip the sign.
Fc = -(Fs + Fd);

% And finally, rectify to > 0. This is a nice MATLAB trick:
Fc( Fc <= 0 ) = 0;

% Then, the applied forces will be:
%Fs = -k*dx;
%Fd = -c*xdot;
% ...vectors of size (num_pts)x1.

% Then, we do a 2D grid of points in the space of dx and xdot

% Make a plot!
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);
zlim([xmin, xmax]);
% Set the orientation of the plot
view([10,20]);
% Make the line thick and black.https://www.sharelatex.com/project/591c89f19af743d90acc8102
%plot(dx, F,'k');

% We can use surf to plot.
Fcsurf = surf(DX, XDOT, Fc);
% turn off the weird edges
Fcsurf.EdgeColor = 'none';

handle = gca;
% Plot the lines:
line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], [0 0], get(handle, 'Zlim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);

% Axis labels:
ylabel('\dot \ell, rate of length change');
xlabel('\Delta \ell, cable stretch');
zlabel('-F_c, applied cable force');
title('Original piecewise-differentiable model');

%% Plot 2: Individual rectification. We don't use this version since it can push a slack cable via damping, but needed for reference.
% Specifically, this is:
% Fs = - H(\delta x) * k \delta x
% Fd = - H(\dot x) * c \dot x

% We already have DX, XDOT, Fs, and Fc, 
% so we can just rectify the individual parts,
% noting that we're flipping the sign *after* adding to Fc so it's a
% greater-than-zero here.
Fs_rect = Fs;
Fs_rect( Fs_rect >= 0 ) = 0;
Fd_rect = Fd;
Fd_rect( Fd_rect >= 0 ) = 0;
Fc_rect = -(Fs_rect + Fd_rect);

% Make a plot!
figure();
hold on;
% The plot limits in the F-direction should keep the plot square.
xlim([xmin, xmax]);
ylim([xmin, xmax]);
zlim([xmin, xmax]);
% Set the orientation of the plot
view([10,20]);
% Make the line thick and black.https://www.sharelatex.com/project/591c89f19af743d90acc8102
%plot(dx, F,'k');

% We can use surf to plot.
Fc_rectsurf = surf(DX, XDOT, Fc_rect);
% turn off the weird edges
Fc_rectsurf.EdgeColor = 'none';

handle = gca;
% Plot the lines:
line( get(handle,'XLim'), [0 0], 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], get(handle, 'Ylim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);
line( [0 0], [0 0], get(handle, 'Zlim'), 'Color', colorAxisLine, 'LineStyle', linestyleAxisLine);

% Axis labels:
ylabel('\dot \ell, rate of length change');
xlabel('\Delta \ell, cable stretch');
zlabel('-Fc_{rect}, applied cable force');
title('Individuall-rectified model. NOT PHYSICALLY REALISTIC');












