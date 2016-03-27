function [a11,a12,a13,a21,a22,a23,a31,a32,a33,Kt,Kv,Ra] = compareSystems(opt_out_filename)

global alpha beta J_rotor N
%motor params

syms s;

Kt = 13.4*10^-3; %torque constant
Kv = 1.4*10^-3*2*pi/60; %speed constant
Ra = 1.9; %armature resistance
N = 64; %speed reduction factor
J_rotor = 5.7e-7; %rotor inertia
alpha = 1/2; %length scaling factor
beta = 1/32; %mass scaling factor

k = 20;
%import variables from csv
M = csvread(opt_out_filename);

%scale results to alpha and beta scaling if optimization was at full scale 
%convert to rotor side of geartrain. Also Inverts A.
M = scaledata(M,1,1,1);

t = M(:,1);
dt_source = t(2)-t(1);
f_ssource = 1/dt_source;

n = 20;
Te_2 = M(k,2);
Te_3 = M(k,3);
a11 = M(k,4);
a12 = M(k,5);
a13 = M(k,6);
a21 = M(k,7);
a22 = M(k,8);
a23 = M(k,9);
a31 = M(k,10);
a32 = M(k,11);
a33 = M(k,12);
Tnet_1 = M(k,13);
Tnet_2 = M(k,14);
Tnet_3 = M(k,15);

%find system from simulink model

SYS = linmod('mimo_sim')

Tss = ss(SYS.a,SYS.b,SYS.c,SYS.d);

[n,d] = tfdata(Tss,'v');

T_simulink = tf(n,d);
%state space rep
K = Kt*Kv/Ra;

C = [-K -K -K 0 0 0; 0 0 0 -K -K -K];
D = [Kt/Ra 0 0 0 0; 0 Kt/Ra 0 0 0];

states = {'T21' 'T22' 'T23' 'T31' 'T32' 'T33'};
inputs = {'v1' 'v2' 'Tm1' 'Tm2' 'Tm3'};
outputs = {'Te2', 'Te3'};
  
A = [0 0 0 0 0 0;-K*a22 -K*a22 -K*a22 0 0 0;0 0 0 -K*a23 -K*a23 -K*a23;0 0 0 0 0 0;-K*a32 -K*a32 -K*a32 0 0 0;0 0 0 -K*a33 -K*a33 -K*a33];
    
B = [0 0 a21 0 0;Kt*a22/Ra 0 0 a22 0;0 Kt*a23/Ra 0 0 a23;0 0 a31 0 0;...
        Kt*a32/Ra 0 0 a32 0;0 Kt*a33/Ra 0 0 a33];
    
%transfer functions
sys_mimo = ss(A,B,C,D,'statename',states,...
        'inputname',inputs,...
        'outputname',outputs);
T_symbolic = tf(sys_mimo); %convert to tf object

T_symbolic(2,1)
T_simulink(2,1)
T_symbolic(1,2)
T_simulink(1,2)
end