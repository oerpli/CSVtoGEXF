function [ t,spells ] = handleNodesDyn( id, label,exists,  varargin )
node_columns = cell(1,nargin);
node_columns{1} = 'id';
node_columns{2} = 'label';

% create static table
t = table(id,label); % create basic node table

spells = createSpells(id(1), exists(1,:)); % create basic nodespell table
for i = 2:length(id)
    spells = [spells; createSpells(id(i), exists(i,:))];
end
% add non-default-attributes
for m = 1:length(varargin)
    if size(varargin{m},2) == 1 % if its constant over time add to n table
        n = table(varargin{m});
        n.Properties.VariableNames = cellstr(inputname(m+3));
        t = [t n];
    else % if it's changing add to spell table
        for i = 1:length(id)
            spells = [spells; createSpells(id(i),varargin{m}(i,:), inputname(m+3))];
        end
    end
end
end

