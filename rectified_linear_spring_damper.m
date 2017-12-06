% rectified_linear_spring_damper.m
% A spring-damper model that rectified cable force to zero if the cable
% goes slack. This is the piecewise model.
% THIS MODEL DOES NOT DO THE ABSOLUTE VALUE of the cable distance.
% e.g. cable goes "infinitely slack" in one direction. We're not doing a
% cable that bounds back once it gets to a certain length "on the other
% side," since that won't ever happen in any of our robots, and is not
% worth modeling as a result.
% Andrew P. Sabelhaus, 2017

function force = rectified_linear_spring_damper( input ) 

% inputs, outputs same as  linear spring damper.

% If input is less than zero, output force is zero.
if input < 0
    force = 0;
else
    force = input;
end