% logistic_smoothed_spring_damper.m
% Cable model that goes slack as per the logistically-smoothed model
% we derived.
function force = logistic_smoothed_spring_damper( input, beta, beta_0 )

% inputs, outputs same as linear_spring_damper.
%   beta = "slope" of the logisitic function. This is NOT a control,
%       and is only included as an input to this function for convenience.
%       Looks like we used beta = 5 in previous work.
%   beta_0 = "offset" of the logisitic function, shifing left/right along
%       the 'input' axis. Also NOT a control.

% Logistic function is 
logistic = 1 / (1 + exp(-beta*(input - beta_0)));

% Output a warning message. If input is too negative, then we won't
% actually get a "correct" force. Theoretically, this system should be
% stable, but if the force is way too small, then the simulation won't
% match the theory: if the theory has some insanely long settling time,
% then the simulation will round off to zero, and that time will go to
% infinity (e.g. become unstable.)
if logistic == 0
    disp('WARNING: logistic_smoothed_spring_damper has rounded to zero, maxed out numerical precision. Results are not accurate against theory.');
end

% The applied force is the logisitic smoothing times the input.
% Think: unit step(x) * cable_force(x)
force = input * logistic;

end