%%% Generating an array of the initial guess, including all the design
%%% varibales. Governing equations of motion for a triple link inverted
%%% pendulum are discretized and solved using forward differencing method.
%%% A = [a11 a12 a13 ; a21 a22 a23 ; a31 a32 a33]
%%% C = [c11 ; c21 ; c31]
%%% A*ddteta = C and D = inv(A)*C
%%% teta = [teta_1 ; teta_2 ; teta_3 ; dteta_1 ; dteta_2 ; dteta_3]
%%% dteta = [dteta_1 ; dteta_2 ; dteta_3 ; ddteta_1 ; ddteta_2 ; ddteta_3]
%%% dteta = [teta(4) ; teta(5) ; teta(6) ; D(1) ; D(2) ; D(3)]
function generateCSV(Y, stateVariableFileName, controlVariableFileName)
global N J_rotor L0 L1 L2 L3 M1 M2 M3 rCOM_1 rCOM_2 rCOM_3 g rG_1 rG_2 rG_3 dt var_array_length

optimizedData = reshape(Y,[length(Y)/8,8]);
controlMat = zeros(var_array_length, 15);


for i = 2:var_array_length % Generating the initial guess using forward differencing method
    
    kneeTorque = optimizedData(i, 7);
    hipTorque = optimizedData(i, 8);
    
    a11 = M1*rG_1^2*L1^2+M2*(rG_2^2*L2^2+(L0+L1)^2+2*rCOM_2*(L0+L1)*L2*cos(optimizedData(i-1,2)))...
        +M3*(rG_3^2*L3^2+L2^2+(L0+L1)^2+2*rCOM_3*L3*L2*cos(optimizedData(i-1,3))+2*L2*(L0+L1)*cos(optimizedData(i-1,2))+2*rCOM_3*(L0+L1)*L3*cos(optimizedData(i-1,2)+optimizedData(i-1,3)));
    a12 = M2*(rG_2^2*L2^2+rCOM_2*(L0+L1)*L2*cos(optimizedData(i-1,2)))...
        +M3*(rG_3^2*L3^2+L2^2+2*rCOM_3*L3*L2*cos(optimizedData(i-1,3))+L2*(L0+L1)*cos(optimizedData(i-1,2))+rCOM_3*(L0+L1)*L3*cos(optimizedData(i-1,2)+optimizedData(i-1,3)));
    a13 =  M3*(rG_3^2*L3^2+rCOM_3*L3*L2*cos(optimizedData(i-1,3))+rCOM_3*(L0+L1)*L3*cos(optimizedData(i-1,2)+optimizedData(i-1,3)));
    c11 = M3*(2*rCOM_3*L2*L3*sin(optimizedData(i-1,3))*optimizedData(i-1,6)+2*L2*(L0+L1)*sin(optimizedData(i-1,2))*optimizedData(i-1,5)+2*rCOM_3*(L0+L1)*L3*sin(optimizedData(i-1,2)+optimizedData(i-1,3))*(optimizedData(i-1,5)+optimizedData(i-1,6)))*optimizedData(i-1,4)...
        +M3*(2*rCOM_3*L2*L3*sin(optimizedData(i-1,3))*optimizedData(i-1,6)+L2*(L0+L1)*sin(optimizedData(i-1,2))*optimizedData(i-1,5)+rCOM_3*(L0+L1)*L3*sin(optimizedData(i-1,2)+optimizedData(i-1,3))*(optimizedData(i-1,5)+optimizedData(i-1,6)))*optimizedData(i-1,5)...
        +M3*(rCOM_3*L2*L3*sin(optimizedData(i-1,3))*optimizedData(i-1,6)+rCOM_3*(L0+L1)*L3*sin(optimizedData(i-1,2)+optimizedData(i-1,3))*(optimizedData(i-1,5)+optimizedData(i-1,6)))*optimizedData(i-1,6)...
        +M2*(2*rCOM_2*L2*(L0+L1)*sin(optimizedData(i-1,2))*optimizedData(i-1,4)*optimizedData(i-1,5)+rCOM_2*(L0+L1)*L2*sin(optimizedData(i-1,2))*(optimizedData(i-1,5))^2)...
        -rCOM_1*M1*L1*g*cos(optimizedData(i-1,1))-(M2+M3)*(L0+L1)*g*cos(optimizedData(i-1,1))-(rCOM_2*M2+M3)*L2*g*cos(optimizedData(i-1,1)+optimizedData(i-1,2))-rCOM_3*M3*g*L3*cos(optimizedData(i-1,1)+optimizedData(i-1,2)+optimizedData(i-1,3));

    a21 = M2*(rG_2^2*L2^2+rCOM_2*(L0+L1)*L2*cos(optimizedData(i-1,2)))...
        +M3*(rG_3^2*L3^2+L2^2+2*rCOM_3*L2*L3*cos(optimizedData(i-1,3))+(L0+L1)*L2*cos(optimizedData(i-1,2))+rCOM_3*(L0+L1)*L3*cos(optimizedData(i-1,2)+optimizedData(i-1,3)));
    a22 = rG_2^2*M2*L2^2 ...
        +M3*(rG_3^2*L3^2+L2^2+2*rCOM_3*L2*L3*cos(optimizedData(i-1,3))) + N^2*J_rotor;
    a23 = M3*(rG_3^2*L3^2+rCOM_3*L2*L3*cos(optimizedData(i-1,3)));
    c21 = M3*(2*rCOM_3*L3*L2*sin(optimizedData(i-1,3))*optimizedData(i-1,6)+L2*(L0+L1)*sin(optimizedData(i-1,2))*optimizedData(i-1,5)+rCOM_3*(L0+L1)*L3*sin(optimizedData(i-1,2)+optimizedData(i-1,3))*(optimizedData(i-1,5)+optimizedData(i-1,6)))*optimizedData(i-1,4)...
        +M3*2*rCOM_3*L3*L2*sin(optimizedData(i-1,3))*optimizedData(i-1,6)*optimizedData(i-1,5)...
        +M3*rCOM_3*L3*L2*sin(optimizedData(i-1,3))*optimizedData(i-1,6)*optimizedData(i-1,6)...
        +M2*rCOM_2*L2*(L0+L1)*sin(optimizedData(i-1,2))*optimizedData(i-1,4)*optimizedData(i-1,5)...
        -M3*(((L0+L1)*L2*sin(optimizedData(i-1,2))+rCOM_3*(L0+L1)*L3*sin(optimizedData(i-1,2)+optimizedData(i-1,3)))*(optimizedData(i-1,5)+optimizedData(i-1,4))+(rCOM_3*L3*(L0+L1)*sin(optimizedData(i-1,2)+optimizedData(i-1,3))*optimizedData(i-1,6)))*optimizedData(i-1,4)...
        -M2*rCOM_2*L2*(L0+L1)*sin(optimizedData(i-1,2))*optimizedData(i-1,4)*(optimizedData(i-1,4)+optimizedData(i-1,5))...
        -(rCOM_2*M2+M3)*L2*g*cos(optimizedData(i-1,1)+optimizedData(i-1,2))-(rCOM_3*M3)*L3*g*cos(optimizedData(i-1,1)+optimizedData(i-1,2)+optimizedData(i-1,3))...
        +0*kneeTorque;

    a31 = M3*(rG_3^2*L3^2+rCOM_3*L3*L2*cos(optimizedData(i-1,3))+rCOM_3*L3*(L0+L1)*cos(optimizedData(i-1,2)+optimizedData(i-1,3)));
    a32 = M3*(rG_3^2*L3^2+rCOM_3*L3*L2*cos(optimizedData(i-1,3)));
    a33 = M3*rG_3^2*L3^2 + N^2*J_rotor;
    c31 = M3*(rCOM_3*L3*L2*sin(optimizedData(i-1,3))*optimizedData(i-1,6)+rCOM_3*L3*(L0+L1)*sin(optimizedData(i-1,2)+optimizedData(i-1,3))*(optimizedData(i-1,5)+optimizedData(i-1,6)))*optimizedData(i-1,4)...
        +M3*(rCOM_3*L3*L2*sin(optimizedData(i-1,3))*optimizedData(i-1,6))*optimizedData(i-1,5)...
        -M3*rCOM_3*L3*(optimizedData(i-1,4)+optimizedData(i-1,5)+optimizedData(i-1,6))*(optimizedData(i-1,4)*(L2*sin(optimizedData(i-1,3))+(L0+L1)*sin(optimizedData(i-1,2)+optimizedData(i-1,3)))+L2*optimizedData(i-1,5)*sin(optimizedData(i-1,3)))...
        -rCOM_3*M3*g*L3*cos(optimizedData(i-1,1)+optimizedData(i-1,2)+optimizedData(i-1,3))...
        +0*hipTorque;
        
    A = [a11 a12 a13 ; a21 a22 a23 ; a31 a32 a33];
    C = [c11 ; c21+kneeTorque ; c31+hipTorque];
    D = A\C;
    
    tA = A';
    
    optimizedData(i,1) = dt*optimizedData(i-1,4)+ optimizedData(i-1,1); 
    optimizedData(i,2) = dt*optimizedData(i-1,5)+ optimizedData(i-1,2); 
    optimizedData(i,3) = dt*optimizedData(i-1,6)+ optimizedData(i-1,3); 
    optimizedData(i,4) = dt*D(1)+ optimizedData(i-1,4);
    optimizedData(i,5) = dt*D(2)+ optimizedData(i-1,5);
    optimizedData(i,6) = dt*D(3)+ optimizedData(i-1,6);
    optimizedData(i,7) = kneeTorque;
    optimizedData(i,8) = hipTorque;
    
    controlMat(i, 1) = (i-1)*dt;
    controlMat(i, 2) = kneeTorque;
    controlMat(i, 3) = hipTorque;
    controlMat(i, 4:12) = tA(:);
    controlMat(i, 13:15) = C';
    
   
end

csvwrite(stateVariableFileName, [controlMat(:, 1), optimizedData])

controlMat(1,2:end) = controlMat(2,2:end);
csvwrite(controlVariableFileName, controlMat)

end