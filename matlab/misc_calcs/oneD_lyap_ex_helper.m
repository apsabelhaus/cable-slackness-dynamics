% oneD_lyap_ex_helper.m
% Andrew P. Sabelhaus
% 2018-11-4

clear all;
close all;
clc;

% A quick script to symbolically solve for parts of various Lyapunov
% candidates for the 1D, 1 bar, 2 cable system.

% declare the constants in the problem.
%syms k1 k2 a b;

% we assume we've specified an equilibrium point, that it's valid, etc.
%syms xeq;

% actually, we need to specify specific values here, so we can know this is
% true for our specific case. Might be able to be better about this for a
% general case, but for now, say:
k1 = 300;
k2 = 100;
b = 8;
a = 0.5;
xeq = 4;

% the lengths of each cable are functions of x.
% we will be able to find the equilibrium length of each cable directly
% from the equilibrium position.
% Here we're doing that l_j_hat from Drew's notes.
l1_eq = b - a - xeq;
l2_eq = xeq - a;

% the control inputs are
% (note, for right now, assumed to be constant - lots of conditions on
% integrals and whatnot, so we're simplifying.)
% These could be functions of time, since it's a ratio of one to the other,
% but we can call them a constant for now.
% Symbolically specify a rho1, then calc rho2.
syms rho1;
force1 = k1*(l1_eq - rho1);
% it's easier to do this:
syms rho2;
force2 = k2*(l2_eq - rho2);
% then solve for rho2.
rho2_soln = solve(force1 == force2, rho2);
% looks right. and now reassign.
rho2 = rho2_soln;

% Now, the value of our proposed Lyapunov function at xeq.
% We're looking to see if (informally) our Lyap function zero point does
% indeed correspond to the equilibrium. It has yet to be seen if this is
% the only one - not a 1-to-1 on cables vs. body states.

% page 16 for 2018-11-4 in Drew's notebook:
syms s;
% ...(for "sigma")
RHS = k1*(0.5*s^2 - rho1*s);
LHS = k2*(0.5*s^2 - rho2*s);

% Plug in the limits for each evaluation of the integral.
lim1_top = b - a;
lim1_bot = l1_eq;
lim2_top = l2_eq;
lim2_bot = -a;

% symbolically plug in.
RHS_top = subs(RHS, s, lim1_top);
RHS_bot = subs(RHS, s, lim1_bot);
LHS_top = subs(LHS, s, lim2_top);
LHS_bot = subs(LHS, s, lim2_bot);

% the sum is
RHS_tot = RHS_top - RHS_bot;
LHS_tot = LHS_top - LHS_bot;

% To check, we need to plug in a concrete equilibrium point, and make a
% choice for rho1.
% We know that (given the tension constraint isn't violated) we can always
% find a rho2 that satisfies these conditions. This is the same as the
% nonzero null space condition for the force density inverse kinematics
% calculation.

% let's say equilbrium is at x_eq = b/2. Nice and symmetric.
%xeq_star = b/2;
% and rho1 is whatever.
%rho1_star = 1;

% substitute.
%RHS_tot_sub = subs(RHS_tot, xeq, xeq_star);
%RHS_tot_sub = subs(RHS_tot_sub, rho1, rho1_star);
%LHS_tot_sub = subs(LHS_tot, xeq, xeq_star);
%LHS_tot_sub = subs(LHS_tot_sub, rho1, rho1_star);


% doesn't work, not super surprising, considering I did this really fast
% and probably has bugs.

% Or, alternatively, this Lyap function doesn't work. That wouldn't be
% surprising either, to see that the equilibrium is not at a unique
% minimum.
% We could always redefine the variable of the Lyap function by a constant
% offset though...





