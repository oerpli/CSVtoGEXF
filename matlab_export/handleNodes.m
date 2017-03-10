function [ t ] = handleNodes( id, label, varargin )
node_columns = cell(1,nargin);
t = table(id,label);
for m = 1:length(varargin)
    n = table(varargin{m});
    n.Properties.VariableNames = cellstr(inputname(m+2));
    t = [t n];
end
end