% symbolically calculating the maximum slope of the logistic function. 

clear all;
close all;
clc;

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







