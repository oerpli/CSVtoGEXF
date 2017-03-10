function [ t ] = handleEdges( target, source, weight, varargin )
edge_columns = cell(1,nargin);
t = table(target, source, weight);
for m = 1:length(varargin)
    n = table(varargin{m});
    n.Properties.VariableNames = cellstr(inputname(m+3));
    t = [t n];
end
end