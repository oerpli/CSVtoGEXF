function [ t ] = handleNodes( id, label, varargin )
node_columns = cell(1,nargin);
node_columns{1} = 'id';
node_columns{2} = 'label';
for m = 3:nargin
    node_columns{m} = inputname(m);
end
t = table(id,label);
for m = 1:length(varargin)
    n = table(varargin{m});
    n.Properties.VariableNames = node_columns(m+2);
    t = [t n];
end
end