Torque_2_End = 100;
Torque_2_Mid = -150;

Torque_3_End = -50;
Torque_3_Mid = 125;

A = [Torque_2_End];
B = [Torque_2_End];



for i = 2:var_array_length
    
    A(i) = A(i-1) + ( (i < var_array_length/2) - (i > var_array_length/2) ) * (Torque_2_Mid - Torque_2_End)/var_array_length;
    B(i) = B(i-1) + ( (i < var_array_length/2) - (i > var_array_length/2) ) * (Torque_3_Mid - Torque_3_End)/var_array_length;
end

hold on
plot(A)
plot(B)