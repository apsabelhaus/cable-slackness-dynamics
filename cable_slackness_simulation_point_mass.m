%% cable_slackness_simulation_point_mass.m
% Script that runs a simulation of a point mass acted upon by a cable.
% This is going to allow us to test out different controllers for
% cables that go slack.
% Andrew P. Sabelhaus, Berkeley Emergent Space Tensegrities Lab, 2017

%% Set up the simulation.

clear all;
close all;
clc;

% Specify the system model for the point mass.
m = 1; % kg, nominally, I suppose.
k = 100; % N/m
c = 10; % N/m-s

% The state space system is
A = [0 1; 0 0];
B = [0; 1/m];
% Pass through the whole system state. We're looking for the force
% to smooth out the spring-damper part, k - c \dot x.
C = [k, c];

% to-do: need to specify direction of force u1. Maybe we get lazy
% and just test it to see.

% System interconnection.
% Though we really only need the one element for now, let's specify it
% in case we want to be fancier later.
M = [0, -1; 1, 0];

% Length of time to simulate, number of steps, initial condition.
dt = 0.01; % sec
%t_max = 5; % sec
t_max = 10;
% a range of all the times is then
t = 0:dt:t_max;

% Initial condition:
%x0 = [-0.1; -0.1];
%x0 = [ -0.1; 0.1]; % position, velocity
x0 = [-0.1; 0.16]; % seems like 0.16 is stable for logisitic smoothing, 0.17 not stable... hmm I was thinking it would be stable for all? Maybe not?


% For the forward euler integration, let's do smaller steps between
% times in the simulation. Call this epsilon.
eps = 0.001;

% Record the system states.
% Dimension of the state is
num_states = size(A,1);
x_result = zeros(num_states, length(t));
% ...we're using column vectors for states.

% Insert the initial condition into the states matrix.
x_result(:,1) = x0;

%% Forward simulate the system.

% Outer loop: simulation timesteps.
% Let's assign the 'result' to the following timestep. Means we don't
% calculate anything for the length(t)-th step, that's filled in at
% length(t)-1.

for i=1 : (length(t)-1)
    % DEBUGGING
    %disp(strcat('t = ', num2str(t(i))));
    % our input is the output of the cable model.
    % HERE IS WHERE WE'LL FEED BACK THE CABLE MODEL
    % need to pass the linear system output through the cable model, Cx.
    % Be fancier about using M. This is a silly way to get u1 = - y2.
    %u = M(1,2) * linear_spring_damper( C * x_result(:,i) );
    %u = M(1,2) * rectified_linear_spring_damper( C * x_result(:,i) );
    u = M(1,2) * logistic_smoothed_spring_damper( C * x_result(:,i), ...
        5, 0); % last two are beta and beta_0, copied from 'plots' script.
    
    % Call the dynamics simulator
    x_result(:,i+1) = simulate_linear_dynamics(A, B, u, x_result(:,i), ...
           dt, eps);
end

% maybe plot now or something.
figure;
hold on;
plot(t, x_result(1,:));
xlabel('time');
ylabel('position');
title('Position of point mass');

figure;
hold on;
plot(t, x_result(2,:));
xlabel('time');
ylabel('velocity');
title('Velocity of point mass');







