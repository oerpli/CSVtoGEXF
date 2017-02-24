function [ t ] = handleEdges( target, source, weight, varargin )
edge_columns = cell(1,nargin);
edge_columns{1} = 'target';
edge_columns{2} = 'source';
edge_columns{3} = 'weight';
for m = 4:nargin
    edge_columns{m} = inputname(m);
end
t = table(target, source, weight);
for m = 1:length(varargin)
    n = table(varargin{m});
    n.Properties.VariableNames = edge_columns(m+3);
    t = [t n];
end
end