%%%%%%%%%%%%%%%%%%%%%%
%	Description: This function generates 2x2 MIMO PID controlers from the trajectories
%	of the optimized fall, as well as other parameters in opt_out_filename
%
%   Input:     opt_out_filename - name of csv file containing params from
%                   optimization
%              pi_in_filename - name of csv file to write output to  
%   
%   opt_out_filename stucture: 
%   
%   C1: t     - time
%   C2: Te_2  - torque applied at 2nd joint
%   C3: Te_3  - torque applied at 3rd joint 
%   C4: a11   - moment of inertia in terms of state vars at time t
%   C5: a12
%   C6: a13
%   C7: a21
%   C8: a22
%   C9: a23
%   C10: a31
%   C11: a32
%   C12: a33
%   C13: c11  - net torques at each joint
%   C14: c21
%   C15: c31
%
%   pi_in_filename structure:
%
%   C1: t               - time
%   C2: Te_2            - torque applied at 2nd joint
%   C3: Te_3            - torque applied at 3rd joint
%   C4: Te_2_responce   - responce of Te_2 due to load torques
%   C5: Te_3_responce   - responce of Te_3 due to load torques
%   C6: c1              -control matrix
%   C7: c2
%   C8: c3
%   C9: c4
%
%	Author Name: Todd Darcie
%   Student ID: 35296128
%   ENPH 459 Exsoskeleton safe-fall project
%
%%%%%%%%%%%%%%%%%%%%%%

function genControllers(opt_out_filename,pi_in_filename)
%motor params

syms s;

kt = 13.4*10^-3; %torque constant
kv = 1.4*10^-3*2*pi/60; %speed constant
R = 1.9; %armature resistance

%import variables from csv
M = csvread(opt_out_filename);

t = M(:,1);
dt_source = t(2)-t(1);
f_ssource = 1/dt_source;

Te_2 = M(:,2);
Te_3 = M(:,3);
a11 = M(:,4);
a12 = M(:,5);
a13 = M(:,6);
a21 = M(:,7);
a22 = M(:,8);
a23 = M(:,9);
a31 = M(:,10);
a32 = M(:,11);
a33 = M(:,12);
Tnet_1 = M(:,13);
Tnet_2 = M(:,14);
Tnet_3 = M(:,15);

%interpolate optimization data
fs = 1000; %sampling frequency (Hz)
dt = 1/fs;

t_fine = 0:dt:t(length(t));
Te_2 = spline(t,Te_2,t_fine);
Te_3 = spline(t,Te_3,t_fine);
Tnet_1 = spline(t,Tnet_1,t_fine);
Tnet_2 = spline(t,Tnet_2,t_fine);
Tnet_3 = spline(t,Tnet_3,t_fine);

%derived mechanical load torques (includes friction)
Tm_1 = Tnet_1;
Tm_2 = Tnet_2 - Te_2;
Tm_3 = Tnet_3 - Te_3;

%state space rep
C = [-kv/R -kv/R -kv/R 0 0 0; 0 0 0 -kv/R -kv/R -kv/R];
D = [1/R 0 0 0 0; 0 1/R 0 0 0];

states = {'T21' 'T22' 'T23' 'T31' 'T32' 'T33'};
inputs = {'v1' 'v2' 'Tm1' 'Tm2' 'Tm3'};
outputs = {'Te2', 'Te3'};
L1 = length(a11);
T_2x5 = zeros(2,5,L1);
T_2x2 = zeros(2,2,L1);
T_2x3 = zeros(2,3,L1);
C_2x2 = zeros(2,2,L1);
for k = 1:L1
    A = [ 0 0 0 0 0 0 ; -a22(k)*kt*kv/R -a22(k)*kt*kv/R -a22(k)*kt*kv/R 0 0 0 ...
        ; 0 0 0 -a23(k)*kt*kv/R -a23(k)*kt*kv/R -a23(k)*kt*kv/R ; 0 0 0 0 0 0 ...
        ; -a32(k)*kt*kv/R -a32(k)*kt*kv/R -a32(k)*kt* kv/R 0 0 0 ; ...
        0 0 0 -a33(k)*kt*kv/R -a33(k)*kt*kv/R -a33(k)*kt*kv/R];

    B = [0 0 -a21(k) 0 0; a22(k)*kt/R 0 0 -a22(k) 0 ; 0 a23(k)*kt/R 0 0 -a23(k) ...
        ; 0 0 -a31(k) 0 0 ; a32(k)*kt/R 0 0 -a32(k) 0 ; 0 a33(k)*kt/R 0 0 -a33(k)];

    
    ghgh1 = s*eye(6,6)
    ghgh2 = ghgh1-A
    ghgh3 = ghgh2\B
    ghgh4 = C*ghgh3
    ghgh5 = ghgh4+D
    
    %transfer functions
    sys_mimo = ss(A,B,C,D,'statename',states,...
        'inputname',inputs,...
        'outputname',outputs);
    TF = tf(sys_mimo);
    
    T_2x5(:,:,k) = C*((s*eye(6,6)-A)\B)+D;
    T_2x2(:,:,k) = T_2x5(:,1:2,k);
    T_2x3(:,:,k) = T_2x5(:,3:5,k);

    %generate controller
    %C_2x2(:,:,k) = tf_to_C(T_2x2);

    %convert symbolic TF to tf object
    for i = 1:2
        for j = 1:3
            T_2x3(i,j,k)
            [symNum,symDen] = numden(sym(T_2x3(i,j,k))); %get num and den of Symbolic TF
            TFnum = sym2poly(symNum);    %convert Symbolic num to polynomial
            TFden = sym2poly(symDen);    %convert Symbolic den to polynomial
            T_2x3_tf(i,j,k) = tf(TFnum,TFden); %create new tf object
        end
    end
end



%calculate system responce from mechanical load torques
N = 10;
L2 = length(Te_2);
t = -N*dt:dt:N*dt;
Te_2_responce = zeros(size(Te_2));
Te_3_responce = Te_2_responce;
Te_2_adj = Te_2_responce;
Te_3_adj = Te_2_responce;

h = waitbar(0,'Generating system responce...');

for k = 1:L2
    waitbar(k / L2)
    
    %T_2x3_tfd = c2d(T_2x3_tf,0.01);
    
    u = [Tm_1(k-N:k+N) Tm_2(k-N:k+N) Tm_3(k-N:k+N)];
    y = lsim(T_2x3_tf(:,:,floor(k*L1/L2)),u,t); %use transfer function closest to this time
    Te_2_responce(k) = y(N+1,1);
    Te_3_responce(k) = y(N+1,2);
    Te_2_adj(k) = Te_2(k)-Te_2_responce(k);
    Te_3_adj(k) = Te_3(k)-Te_3_responce(k);
end
close(h) 

%write data to csv
C_2x2_p = permute(C_2x2,[3 2 1]);
c1 = C_2x2_p(:,1,1);
c2 = C_2x2_p(:,2,1);
c3 = C_2x2_p(:,1,2);
c4 = C_2x2_p(:,2,2);

M2 = [t Te_2 Te_3 Te_2_responce Te_3_responce c1 c2 c3 c4]
csvwrite(pi_in_filename,M2);

end