% linear_spring_damper.m
% Function that applies a cable force as a linear spring/damper.
% To be used for testing out a cable.
function force = linear_spring_damper( input )
% inputs:
%   input = a scalar. We're looking for something like F = kx - c \dot x,
%       so 'input' is going to be kx - c \dot x. See the 'C' matrix
%       of the linear system.
%   output = the force value. Here, same as input. 
%       For other spring models, will have smoothing terms.

force = input;

end