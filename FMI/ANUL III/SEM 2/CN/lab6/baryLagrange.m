function interpolated_values = baryLagrange(x, y, xx)

  num_nodes = length(x);
  barycentric_weights = ones(1, num_nodes)

  for j = 1:num_nodes
      other_node_indices = [1:j-1, j+1:num_nodes];

      barycentric_weights(j) = prod(x(j) - x(other_node_indices));
  end

  barycentric_weights = 1./barycentric_weights;

  numerator = zeros(size(xx));
  denominator = zeros(size(xx));

  exact_node_match_idx = zeros(size(xx));

  for j = 1:num_nodes

      xdiff = xx - x(j);

      weighted_term = barycentric_weights(j) ./ xdiff;

      numerator = numerator + weighted_term * y(j);
      denominator = denominator + weighted_term;
      exact_node_match_idx(xdiff == 0) = j;
  end

  interpolated_values = numerator ./ denominator;

  indices_with_exact_match = find(exact_node_match_idx);

  interpolated_values(indices_with_exact_match) = y(exact_node_match_idx(indices_with_exact_match));

end
