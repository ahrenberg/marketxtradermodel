""" 
Utility functions for trading simulation.

"""
# Copyright 2017 Lukas Ahrenberg <lukas@ahrenberg.se>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import networkx as _nx
from .trader import Trader as _Trader

def populate_graph(graph,**trader_init_arguments):
    """ Substitude nodes in an existing graph with traders.

    Takes an existing graph and changes all nodes in-place to traders by 
    substituting a new Trader object for each.

    Parameters
    ----------
    graph : networkx graph
        A general networkx graph; modified by function.
    \**trader_init_arguments : one or more named keywords for Trader.__init__
        See Trader

    Returns
    -------
    dict from original nodes to newly created trader nodes
        Provided for convenience.

    See Also
    --------
    Trader : For documentation on parameters.
   
    """
    # First build the dictionary from the old graph nodes to a set of new ones.
    node_map = dict(zip(graph.nodes_iter(),
                        (_Trader(**trader_init_arguments) \
                         for n in range(graph.number_of_nodes()))))
    # Then relabel the nodes.
    _nx.relabel_nodes(graph, node_map, copy=False)

    # Return the map, might be of use to caller.
    return node_map
