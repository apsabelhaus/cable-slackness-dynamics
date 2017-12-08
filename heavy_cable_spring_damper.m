% logistic_smoothed_spring_damper.m
% Cable model that goes slack as per a "heavy cable." Some pull force 
% still applied even when in the slack regime.
function force = heavy_cable_spring_damper( input)

% inputs, outputs same as linear_spring_damper.

% Try to use the tanh function to smooth out something, as in:
% https://www.j-raedler.de/2010/10/smooth-transition-between-functions-with-tanh/

force = input;

end