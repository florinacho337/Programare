function [integral_approximation, num_func_evals] = romberg(integrand_func, lower_limit, upper_limit, tolerance, max_iterations)


  % valori implicite
  if nargin < 5
    max_iterations = 10;
  end
  if nargin < 4
    tolerance = 1e-3;
  end

  romberg_table = zeros(max_iterations, max_iterations);

  current_step_size = upper_limit - lower_limit;

  romberg_table(1,1) = current_step_size / 2 * (sum(integrand_func([lower_limit, upper_limit])));
  num_func_evals = 2;

  for k = 2:max_iterations
     new_evaluation_points = lower_limit + ([1:2^(k-2)] - 0.5) * current_step_size;

     romberg_table(k,1) = 0.5 * (romberg_table(k-1,1) + current_step_size * sum(integrand_func(new_evaluation_points)));
     num_func_evals = num_func_evals + length(new_evaluation_points);

     extrapolation_power_of_4 = 4;
     for extrapolation_level = 2:k
        romberg_table(k, extrapolation_level) = ...
            (extrapolation_power_of_4 * romberg_table(k, extrapolation_level-1) - romberg_table(k-1, extrapolation_level-1)) ...
            / (extrapolation_power_of_4 - 1);
        extrapolation_power_of_4 = extrapolation_power_of_4 * 4;
     end

     if (abs(romberg_table(k, k) - romberg_table(k-1, k-1)) < tolerance) && (k > 3)
        integral_approximation = romberg_table(k, k);

        disp('Tabelul Romberg calculat (partial):');
        disp(romberg_table(1:k, 1:k));
        return;
     end

     current_step_size = current_step_size / 2;
  end

  error('Numarul maxim de iteratii a fost atins.');

end

