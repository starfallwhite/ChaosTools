function [x,time] = RungeSolve_electrooptic_intensity_feedback_chaos(T1,xin,h,N,beta,phi,tou,xita)

x = zeros(1,N);

x_0 = xin(1);
y_0 = xin(2);
n1 = floor(T1/h);

m=1;

for j = 1:N
    time(m)=j*h;
    
    if (j<=n1)
        %x_delay = x(1);
         x_delay = (rand(1)-0.5);
    elseif(j>n1) 
         x_delay = x(j-n1);

    end
    
    
       k11 = -(1/tou)*x_0-(1/(xita*tou))*y_0+(beta/tou)*(cos(x_delay-phi))^2;
       k21 = x_0;
       
       k12 = -(1/tou)*(x_0+0.5*h*k11)-(1/(xita*tou))*(y_0+0.5*h*k21)+(beta/tou)*(cos(x_delay-phi))^2;
       k22 = x_0+0.5*h*k11;
       
       k13 = -(1/tou)*(x_0+0.5*h*k12)-(1/(xita*tou))*(y_0+0.5*h*k22)+(beta/tou)*(cos(x_delay-phi))^2;
       k23 = x_0+0.5*h*k12;
       
       k14 = -(1/tou)*(x_0+h*k13)-(1/(xita*tou))*(y_0+h*k23)+(beta/tou)*(cos(x_delay-phi))^2;
       k24 = x_0+h*k13;
 
       x_0 = x_0+h*(k11+2*k12+2*k13+k14)/6;
       y_0 = y_0+h*(k21+2*k22+2*k23+k24)/6;
       
 
       x(j)=x_0;
       y(j)=y_0;
       
       
       x_Delay(j) = x_delay;
       m=m+1;
end    
end