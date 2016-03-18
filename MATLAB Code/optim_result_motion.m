function optimal_result_impact = optim_result_motion(Y)
global L0 L1 L2 L3 L4 var_array_length

X(:,1) = Y(1:var_array_length);
X(:,2) = Y(var_array_length+1:2*var_array_length);
X(:,3) = Y(2*var_array_length+1:3*var_array_length);
X(:,4) = Y(3*var_array_length+1:4*var_array_length);
X(:,5) = Y(4*var_array_length+1:5*var_array_length);
X(:,6) = Y(5*var_array_length+1:6*var_array_length);
X(:,7) = Y(6*var_array_length+1:7*var_array_length);
X(:,8) = Y(7*var_array_length+1:8*var_array_length);
%% Plotting the fall
for i = 1:var_array_length % Examining the impact time and feasibility of the motion (geometrical constraints on the limb motion/ head and hip height with respect to the ground)
    if X(i,1) > pi || X(i,2) < 0 || X(i,3) >0  || (L0+L1)*sin(X(i,1))+L2*sin(X(i,1)+X(i,2))< 0 || (L0+L1)*sin(X(i,1))+L2*sin(X(i,1)+X(i,2))+(L3+L4)*sin(X(i,1)+X(i,2)+X(i,3)) < 0
        optimal_result_impact = i-1;
        break
    else
        optimal_result_impact = var_array_length;
    end
end

figure
writerObj = VideoWriter('fall.avi');
open(writerObj);
set(gca,'nextplot','replacechildren');
set(gcf,'Renderer','zbuffer');
for i = 1:optimal_result_impact
    plot ([0 (L0+L1)*cos(X(i,1)) (L0+L1)*cos(X(i,1))+L2*cos(X(i,1)+X(i,2)) (L0+L1)*cos(X(i,1))+L2*cos(X(i,1)+X(i,2))+(L3+L4)*cos(X(i,1)+X(i,2)+X(i,3))]...
         ,[0 (L0+L1)*sin(X(i,1)) (L0+L1)*sin(X(i,1))+L2*sin(X(i,1)+X(i,2)) (L0+L1)*sin(X(i,1))+L2*sin(X(i,1)+X(i,2))+(L3+L4)*sin(X(i,1)+X(i,2)+X(i,3)) ],'k');
    hold on
    axis square
    xlabel('X(m)');
    ylabel('Y(m)');
    axis([-(L0+L1+L2+L3+L4)  (L0+L1+L2+L3+L4)  -(L0+L1+L2+L3+L4)  (L0+L1+L2+L3+L4)],'square')
    figure(gcf)
    drawnow
    plot((L0+L1)*cos(X(i,1))+L2*cos(X(i,1)+X(i,2))+(L3+L4)*cos(X(i,1)+X(i,2)+X(i,3))...
         ,(L0+L1)*sin(X(i,1))+L2*sin(X(i,1)+X(i,2))+(L3+L4)*sin(X(i,1)+X(i,2)+X(i,3)),'.k','MarkerSize',40)
    hold off
    pause(0)
    frame = getframe;
    writeVideo(writerObj,frame);
end
close(writerObj);
end
