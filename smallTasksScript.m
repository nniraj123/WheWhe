% Code to generate mean plot along with 95% confidence interval
temp = m.corr_coeff_timeSeries(:,391:end,1:500);
temp = reshape(temp, [513*123 500]);
temp_upper = quantile(temp,0.95);
temp_lower = quantile(temp,0.05);
plot(t(1:500),avg_autocorr_FF1(1:500),'b-','LineWidth',1.5)
hold on
plot(t(1:500),temp_upper,'b:','LineWidth',1.1)
plot(t(1:500),temp_lower,'b:','LineWidth',1.1)
xlabel('Time(in days)')
ylabel('Correlation coefficient');
title('Mean vs 95% Confidence autocorrelation values in lower far field')