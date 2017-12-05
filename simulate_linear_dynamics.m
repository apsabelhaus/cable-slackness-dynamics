% simulate_linear_dynamics.m
% A quick Euler integration of a linear system.
% Andrew P. Sabelhaus 2017

function [result] = simulate_linear_dynamics(A, B, u, x_initial, dt, eps)
% Inputs:
%   A, B = system dynamics matrices for state space model
%   u = input to be applied over whole time period (think: zero order hold)
%   x_initial = initial condition for the integration
%   dt = total amount of time to integrate over
%   eps = timestep for integration within 0 to dt. eps < dt, e.g. taking
%       small steps of eps to eventually reach dt.

% quick check
if eps > dt
    disp('epsilon greater than dt, cannot integrate dynamics.');
    return;
    % ...I don't think this is the right MATLAB code. Been doing C++ for so
    % long that I forget how to throw exceptions here.
end
% ...we are trusting that the dimensions of A, B, x, u all work out
% properly. Shame on you if your A matrix isn't the same size as your
% state.

% Loop through epsilon until we reach dt.
result = x_initial;
current_time = 0;
while current_time < dt
    % Integrate forward by epsilon.
    % derivative is:
    x_dot = A*result + B*u;
    % euler integration
    result = result + eps*x_dot;
    % update the counter.
    current_time = current_time + eps;
    % a quick debugging statement
    %disp(strcat('current time is ', num2str(current_time)));
end
