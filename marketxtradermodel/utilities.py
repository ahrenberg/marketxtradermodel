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
import types as _types

def populate_graph(graph, inplace = True, **trader_init_arguments):
    """ Substitude nodes in an existing graph with traders.

    Takes an existing graph and changes all nodes in-place to traders by 
    substituting a new Trader object for each.

    Parameters
    ----------
    graph : networkx graph
        A general networkx graph; modified by function.
    inplace : bool
        If true the provided graph will be update in place, otherwise a copy is
        createdfirst.
    **trader_init_arguments : one or more named keywords for Trader.__init__
        If the value of a parameter is a generator then that generator will be
        used to produce a new parameter value for each new trader created.
        For any other types the parameter value is passed as is to the Trader.
        See Trader for list of arguments.

    Returns
    -------
    graph : networx graph
        Copy of the updated input parameter graph.
    node_map : dict 
        Lookup dictionary from original graph nodes to newly created trader nodes.

    See Also
    --------
    Trader : For documentation on parameters.
   
    """

    # Check arguments provided to separate out the ones requireing special treatment.
    w_graph = graph
    if inplace == False:
        w_graph = graph.copy()
        
    trader_const_arguments = {}
    trader_gen_arguments = {}
    
    for k,v in trader_init_arguments.items():
        if isinstance(v,_types.GeneratorType):
            trader_gen_arguments[k] = v
        else:
            trader_const_arguments[k] = v

    # The construction of the trader arguments is quite a dense piece of code.
    # First the trader arguments which are 'const' i.e. the same for each trader
    # are inserted in an empty dict. Then it is updated with the generated arguments
    node_map = dict(zip(w_graph.nodes.keys(),
                        (_Trader(name = nk, **trader_const_arguments,
                                 **{k:v.__next__() for k,v in trader_gen_arguments.items()})
                         for nk in w_graph.nodes.keys())))
    # Then relabel the nodes.
    _nx.relabel_nodes(w_graph, node_map, copy=False)

    # Return the map, might be of use to caller.
    return w_graph, node_map
