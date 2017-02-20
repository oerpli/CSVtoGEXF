#! /usr/bin/python3
"""FUCK PYLINT"""
import os
import csv
from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET
import vkbeautify as vkb
import argparse


class Attribute():
    Counter = 0
    def __init__(self, title, edge, type):
        self.ID = Attribute.Counter
        Attribute.Counter += 1
        self.Title = title
        self.Type = type
        self.Edge = edge

class Def():
    Arcs = ''
    Attributes = dict()
    Attributes['edge'] = dict()
    Attributes['node'] = dict()
    Keys = {'edge': [], 'node': []}
    Mode = {'edge': 'static', 'node': 'static'}

    @staticmethod
    def GraphMode():
        return sorted(Def.Mode.values())[0] # return dynamic if either of the values is dynamic
    
    @staticmethod
    def xmlAttributes(type, root):
        if(len(Def.Keys[type]) == 0):
            return
        attributes = SubElement(root, 'attributes')
        attributes.set('class',type)
        attributes.set('mode', Def.Mode[type])

        for key in Def.Keys[type]:
            drattrib = SubElement(attributes,'attribute')
            a = Def.Attributes[key]
            drattrib.set('id',str(a.ID))
            drattrib.set('title',a.Title)
            drattrib.set('type',a.Type)

    @staticmethod
    def DeclareAttributes(root):
        Def.xmlAttributes('node',root)
        Def.xmlAttributes('edge',root)
    
    @staticmethod
    def AddAttribute(attribute):
        Def.Keys['edge' if attribute.Edge == '1' else 'node'].append(attribute.Title)
        Def.Attributes[attribute.Title] = attribute

    
    @staticmethod
    def GetID(key):
        return Def.Attributes[key].ID
    @staticmethod
    def GetEdgeKeys():
        return Def.Keys['edge']

    @staticmethod
    def GetNodeKeys():
        return Def.Keys['node']


#
class Spell():
    def __init__(self, start, end, key = None, value = None):
        self.Start = start
        self.End = end
        if key is not None and key != '':
            self.Elem = False
            self.Key = Def.GetID(key)
            self.Value = value
        else:
            self.Elem = True

    def xmlAttribSpell(s, root):
        attv = SubElement(root, 'attvalue')
        attv.set('for', str(s.Key))
        attv.set('value', str(s.Value))
        attv.set('start',str(s.Start))
        attv.set('end',str(s.End))
    def xmlElemSpell(s, root):
        spell = SubElement(root,'spell')
        spell.set('start',str(s.Start))
        spell.set('end',str(s.End))

# Baseclass for Edge and Node - implements common members (how to handle spells and attributes)
class GraphElem():
    def __init__(self, id):
        self.Attributes = dict()
        self.Spells = []
        self.ID = id

    def xmlElement(self, root):
        self.xml(root)
        elem_spells = [x for x in self.Spells if x.Elem]
        if len(elem_spells) > 0:
            spells = SubElement(self.elem, 'spells')
            for s in elem_spells:
                s.xmlElemSpell(spells)
        if len(self.Attributes) > 0:
            att = SubElement(self.elem, 'attvalues')
            attr_spells = [x for x in self.Spells if not x.Elem]
            for key in self.Attributes.keys():
                if len([x for x in attr_spells if x.Key == key]) == 0:
                    attv = SubElement(att, 'attvalue')
                    attv.set('for', str(key))
                    attv.set('value', self.Attributes[key])
            for s in attr_spells:
                s.xmlAttribSpell(att)    

    def addAttribute(self, key, value):
        self.Attributes[Def.GetID(key)] = value

    def AddSpell(self, row):
        self.Spells.append(Spell(row['start'],row['end'],row['key'],row['value']))

    @classmethod
    def Get(cls, key):
        return cls.register[key]
#
class Node(GraphElem):
    register = dict()
    def __init__(self, id, label):
        super(Node,self).__init__(id)
        self.Label = label
        Node.register[id] = self

    def xml(self, root):
        self.elem = SubElement(root, 'node')
        self.elem.set('id', self.ID)
        self.elem.set('label', self.Label)
        
#
class Edge(GraphElem):
    id = 0
    register = dict()
    def __init__(self, source, target, weight):
        super(Edge,self).__init__(Edge.id)
        Edge.id +=1
        self.Source = source
        self.Target = target
        self.Weight = weight
        Edge.register[(source,target)] = self

    def xml(self, root):
        self.elem = SubElement(root, 'edge')
        self.elem.set('id', str(self.ID))
        self.elem.set('source',self.Source)
        self.elem.set('target',self.Target)
        self.elem.set('weight',self.Weight)
#
def readDefinitions(file):
    with open(file, newline = None) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
        for row in reader:
            a = Attribute(row['title'],row['edge'], row['type'])
            Def.AddAttribute(a)

#
def readNodes(file):
    with open(file, newline=None) as csvfile:
        reader = csv.DictReader(csvfile,delimiter='\t', quotechar='"')
        nodes = []
        for row in reader:
            node = Node(row['id'], row['label'])
            for key in Def.GetNodeKeys():
                    node.addAttribute(key, row[key])
            nodes.append(node)

        print("#Nodes: {}".format(len(nodes)))
        return nodes
#
def readEdges(file):
    with open(file, newline=None) as csvfile:
        reader = csv.DictReader(csvfile,delimiter='\t', quotechar='"')
        edges = []
        for row in reader:
            edge = Edge(row['source'], row['target'], row['weight'])
            edges.append(edge)
            for key in Def.GetEdgeKeys():
                edge.addAttribute(key, row[key])
        print("#Edges: {}".format(len(edges)))
        return edges

#
def readEdgeSpells(file):
    with open(file, newline=None) as csvfile:
        reader = csv.DictReader(csvfile,delimiter='\t', quotechar='"')
        for row in reader:
            key = (row['source'], row['target'])
            Edge.Get(key).AddSpell(row)
#
def readNodeSpells(file):
    with open(file, newline=None) as csvfile:
        reader = csv.DictReader(csvfile,delimiter='\t', quotechar='"')
        for row in reader:
            key = row['id']
            Node.Get(key).AddSpell(row)
#

def WriteXML(edges,nodes, out = 'graph'):
    ns = "http://www.w3.org/2001/XMLSchema-instance"
    nsg = "http://www.gexf.net/1.2draft"
    # Configure one attribute with set()
    ET.register_namespace('xsi',ns) #some name
    root = Element('gexf')
    root.set('version', '1.2')
    root.set('xmlns',ns)
    root.set('xmlns:xsi',nsg)

    graph = SubElement(root, 'graph')
    graph.set('mode',Def.GraphMode())
    graph.set('defaultedgetype',Def.Arcs)
    Def.DeclareAttributes(graph)
    nodesE = SubElement(graph,'nodes')
    for node in nodes:
        node.xmlElement(nodesE)
    edgesE = SubElement(graph,'edges')
    for edge in edges:
        edge.xmlElement(edgesE)

    output = './tempgraph123123.xml'
    tree = ET.ElementTree(root)
    out = "{}.gexf".format(out)
    #tree.write("page.xml",xml_declaration=True,encoding='utf-8',method="xml",default_namespace=ns)
    xml = ET.tostring(root).decode("utf-8")
    tree.write(output, encoding="utf-8", xml_declaration=True, default_namespace=None, method="xml")
    vkb.xml(output,out)
    os.remove(output)
    print("Writing graph to {}".format(out))
#

## Parse arguments, read passed edge and node definitions and output gexf file
parser = argparse.ArgumentParser(description='Please provide csv files with edges and nodes as well as an output filename')
parser.add_argument('-e', '--edges', required=True, help='CSV file with edges (source, target, weight, [attributes as defined in definitions])')
parser.add_argument('-n', '--nodes', required=True, help='CSV file with nodes (id, label, [attributes as defined in DEFS])')
parser.add_argument('-d', '--defs', help='CSV file with attribute definitions, title, edge (0/1), type (integer, double, float, boolean, string)')
parser.add_argument('-o', '--output', help='Where to save the graph. Default is ./out.gexf')
parser.add_argument('-se', '--spelledges', help='CSV file with spells of edges (source, target, start, end [, key, value])')
parser.add_argument('-sn', '--spellnodes', help='CSV file with spells of nodes (id, start, end [, key, value])')
parser.add_argument('-a', '--arcs', choices=['undirected','directed','mutual'], help='How to handle edges. Default is directed')

args = parser.parse_args()

if args.defs is not None:
    graph = readDefinitions(args.defs)
edges = readEdges(args.edges)
nodes = readNodes(args.nodes)
if args.spellnodes is not None:
    nodespells = readNodeSpells(args.spellnodes)
    Def.Mode['node'] = 'dynamic'
if args.spelledges is not None:
    edgespells = readEdgeSpells(args.spelledges)
    Def.Mode['edge'] = 'dynamic'
Def.Arcs = args.arcs or 'directed'

WriteXML(edges, nodes, args.output or 'out')

print("Completed")