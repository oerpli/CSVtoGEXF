%% Nodes
nid = 1:15;
nlabel = num2str(nid);

FirstAttribute = exp(1:15); % double attribute
SecondAttribute = nid < 10; % boolean attribute
ThirdAttribute = nid * 2; % integer attribute

node_types = {'double', 'boolean', 'integer'}; % write types of attributes in correct order

% The first two arguments are always id and label - there the variable names don't matter
% Starting from the third argument the variable name will be used as the name of the attribute in the resulting gexf file.
% You can change those names via nodetable.Properties.VariableNames if you want
% nodetable = handleNodes(ids,labels {,arbitrary amount of additional attributes});
nodetable = handleNodes(nid,nlabel,FirstAttribute,SecondAttribute, ThirdAttribute);

%% Edges
g = digraph(rand(15,15));
el = g.Edges.EndNodes;
weight = g.Edges.Weight;

FirstEdgeAttribute = exp(weight);
SecondEdgeAttribute = round(ans);

edge_types = {'double', 'integer'}; % add types of additional columns

% Here the first three arguments are fixed to source, target and weight.
% edgetable = handleEdges(source,target, weight {, arbitrary amount of attributes});
edgetable = handleEdges(el(:,1),el(:,2),weight, FirstEdgeAttribute, SecondEdgeAttribute);


%% Definitions (don't change anything here)
% Just pass the node and edge table as well as the types of the attributes to this function.
definitions = createDefinitions(nodetable,edgetable,node_types, edge_types);

%% Write tab seperated files (python expects those) - maybe adapt paths if necessary
writetable(definitions,'./graph/definitions.txt','Delimiter','\t');
writetable(edgetable,'./graph/edges.txt','Delimiter','\t');
writetable(nodetable,'./graph/nodes.txt','Delimiter','\t');

% run python script
!./../convCSVtoGEXF.py -n ./graph/nodes.txt -e ./graph/edges.txt -d ./graph/definitions.txt -o ./graph/graph



