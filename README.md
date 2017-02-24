# CSVtoGEXF
Python script that converts CSV files to GEXF files (for gephy).


## Usage
All CSV files must be tab seperated.  Quotechar is `"`. Headers are required
The script requires the following arguments:
* -n (nodes) A list of nodes, columns are: id, label [, whatever is defined in definitions.csv]
* -e (edges) A list of edges, columns are: source, target, weight [, whatever is defined in definitions.csv]

And takes these optional arguments.
* -d (definitions) A list that contains the names of custom columns, a marker to indicate whether the column is for the edge (1) or the node (0) table as well as a datatype. Not required if no additional columns exist
* -es (edgespells) A list of timespans where a edge or an edge attribute exist: source, target, start, end, [attribute name, attribute value]
* -ns (nodespells) A list of timespans where a node or a node attribute exist: id, start, end [attribute name, attribute value]
* -a (arcs) Whether the edges are directed, undirected or mutual (directed but always in both directions). Default is directed.

In the testdata folder there are samples for all the different CSV files. If you have problems contact me on [twitter](https://twitter.com/oerpli)

If neither edgespells or nodespells are given the resulting graph is assumed to be static. If spells are given for attributes any values provided for the same attribute in the node or edge list are discarded (this is because attributes without a start/end declaration must hold at all times and giving spells for those times would result in a critical error in Gephi.


## Matlab support
The matlab export functions are in the folder, depending on the path from where you call them you may need to adapt some paths in the `Export_Example.m` file. 
Also note that currently the types of the optional attributes have to be defined (look at the gexf primer to see what types are allowed). I intend to write some auto detection sometime in the future.

Exporting dynamic graphs does not work currently as I have no idea how people store their dynamic graphs in matlab. If you would like to use this feature drop me a message and I will see what I can do. 
