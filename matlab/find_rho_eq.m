function [rho_2, dl1_eq, dl2_eq, F1_eq, F2_eq] = find_rho_eq(k1, k2, a1, a2, x_eq, rho_1, m, g)
%quick calculation of the equilibrium point for a 2-cable spring system
% k is spring const, a_i is anchor point, x_eq is point to stabilize
% around, and since this is a surface (underdetermined), need to specify
% some input for cable 1 and then solve for cable 2. 
% On 2018-11-5, added gravity to this pretension calculation.

% based on Drew's notebook derivation,
% was:
%rho_2 = -(1/k2) * (x_eq*(k1 + k2) -k1*a1 -k2*a2 -k1*rho_1);
% and with gravity, is:
rho_2 = -(1/k2) * (x_eq*(k1 + k2) -k1*a1 -k2*a2 -k1*rho_1 -m*g);

% where the cable stretch is then
dl2_eq = x_eq - a2 - rho_2;
dl1_eq = a1 - x_eq - rho_1;

% and the pretension forces at those points are
F1_eq = k1*dl1_eq;
F2_eq = k2*dl2_eq;

end

