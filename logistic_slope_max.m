% symbolically calculating the maximum slope of the logistic function. 
% Andrew P. Sabelhaus, 2019

clear all;
close all;
clc;

%% for just the logistic function

% declare the one symbolic variable

syms x

% set up the logistic function
L = 1 / (1 + exp(-x) )

% let's plot it just to see what it looks like
t = linspace(-10, 10, 1000);
L_subbed = eval( subs(L, x, t) );
plot(t, L_subbed);
title('L(x)');

%  its slope is
dLdx = L * (1 - L)

% let's plot this one too
dLdx_subbed = eval( subs(dLdx, x, t) );
figure;
plot(t, dLdx_subbed);
title('dLdx');

% It looks like this function does not have any zeros either.
% So instead, let's try to find is maximum.
% Writing out by hand using the chain rule,
d2Ldx2_analytic = L * (1 - L) * (1 - 2 * L)
pretty( simplify( d2Ldx2_analytic ) )

% A symbolic computation just to be sure I've got this right:
d2Ldx2 = simplify( diff( dLdx ) )
pretty( d2Ldx2 )

% ...OK, all looks good. Let's now plot this function:
d2Ldx2_subbed = eval( subs( d2Ldx2, x, t ) );
figure;
plot(t, d2Ldx2_subbed );
title('d2Ldx2');

% this function definitely looks like it has a zero. Let's find it.
solve( d2Ldx2 == 0 )

% not super surprising, the max is at zero. 
% That's the *location* of the max, so we have to plug back in to dLdx.
max_slope = subs( dLdx, x, 0 )
eval(max_slope) 

% somehow this equals a quarter. So, the maximum slope of L(x) is is 1/4.
% ...write that out in my notebook.

%% Now for x L(x), what we're really interested in.

disp('Now for the cable model itself:');

% set up the logistically-smoothed cable function
xLx = x / (1 + exp(-x) )

% plot of the base function itself
xLx_subbed = eval( subs(xLx, x, t) );
figure;
plot(t, xLx_subbed);
title('xL(x)');

% its slope is
d_xLx_dx = x * L * (1 - L) + L
pretty( simplify(d_xLx_dx) )

% plot this one too
d_xLx_dx_subbed = eval( subs(d_xLx_dx, x, t) );
figure;
plot(t, d_xLx_dx_subbed);
title('d xLx dx');

% Interesting. It looks visually like 
% lim(x -> -inf) = 0, 
% min @ some -x and is less than 1,
% value @ 0 = 0.5,
% max @ some +x and is greater than 1,
% lim(x -> +inf) = 1.

% So, let's do like before, and find the mimima and maxima.
d2_xLx_dx2 = simplify( diff( d_xLx_dx ) )
pretty( d2_xLx_dx2 )

% plot it:
d2_xLx_dx2_subbed = eval( subs( d2_xLx_dx2, x, t ) );
figure;
plot(t, d2_xLx_dx2_subbed );
title('d2 xLx dx2');

% this function definitely looks like it has a zero. Let's find it.
solve( d2_xLx_dx2 == 0 )

% Something around 2.4 (doesn't seem to have an exact answer?)
% Substituting x=2.4 back in to d_xLx_dx ~= 1.1. So, there's probably a
% constant bound here (hooray! that's what we hoped for), but it doesn't
% seem to have a nice value. But maybe the constant itself just can't be
% dealt with by MATLAB's symbolic solver, so see my notebook for an attempt
% to solve d2_xLx_dx2 == 0 by hand.

%% Instead, let's get a bound.

% From the written notes, we need to bound the function
bound1 = x / (exp(x) + 1)

% So let's find the maximum of its derivative, which is in part the
% following (note that I've removed all the other terms that don't
% contribute to the zero (the denominator, for example.) see notes.
% (remember we're just finding the loc of the max right here)
d_bound1_dx = exp(x) + 1 - x * exp(x)

% Solving is
bound1_max_location = solve( d_bound1_dx == 0)

% Then the bound is
bound1_max = subs( bound1, x, bound1_max_location)
eval(bound1_max)

% which then is \alpha = 1 + bound1_max proof, so bound overall is
% ...wait, do I do 1 + 1 + 0.278 or just 1 + 0.278??? maybe mistake.









