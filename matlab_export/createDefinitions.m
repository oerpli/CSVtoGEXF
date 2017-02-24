function [ definitions ] = createDefinitions( nodetable, edgetable,node_types, edge_types )
deftypes = [node_types' ;  edge_types'];
deftitles = [nodetable.Properties.VariableNames(3:end)' ;  edgetable.Properties.VariableNames(4:end)'];
defedge = [zeros(size(nodetable.Properties.VariableNames(3:end))); ones(size(edgetable.Properties.VariableNames(4:end)))']';
definitions = table(deftitles, defedge, deftypes);
% add correct column labels to all tables
definitions.Properties.VariableNames = {'title','edge','type'};
end

