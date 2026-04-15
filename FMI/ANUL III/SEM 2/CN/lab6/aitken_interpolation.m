function f_interp = aitken_interpolation(x_nodes, f_nodes, x, epsilon)
    m = length(x_nodes) - 1;

    % Sort nodes based on distance to x
    [~, indices] = sort(abs(x - x_nodes));
    x_nodes = x_nodes(indices);
    f_nodes = f_nodes(indices);

    % Initialize divided difference table
    f_table = zeros(m+1, m+1);
    f_table(:,1) = f_nodes(:);

    for i = 1:m
        for j = 0:(i-1)
            y_ij = x_nodes(i+1) - x_nodes(j+1);
            f_table(i+1, j+2) = ((x - x_nodes(j+1)) * f_table(i+1, j+1) - (x - x_nodes(i+1)) * f_table(j+1, j+1)) / y_ij;
        end

        % Convergence criterion
        if abs(f_table(i+1, i+1) - f_table(i, i)) <= epsilon
            f_interp = f_table(i+1, i+1);
            return;
        end
    end

    f_interp = f_table(m+1, m+1);
end
