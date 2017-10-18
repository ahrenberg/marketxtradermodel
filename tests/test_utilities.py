""" 
Test functions for utilities.

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
import pytest
import networkx as nx
import marketxtradermodel as mxtm
from marketxtradermodel.utilities import *

@pytest.fixture
def utpop_fix():
    return nx.path_graph(5,create_using=nx.DiGraph())

class TestPopulate:
    def test_no_args(self,utpop_fix):
        """ No error when using default arguments. """
        G = utpop_fix
        # Call function.
        G2,node_map = populate_graph(G)
        # Assert that the keys in node map are exactly the nodes in G2.
        assert(set(G2.nodes()) == set(node_map.values()))
        # Assert that all nodes are Traders.
        assert((isinstance(n,mxtm.Trader) for n in G2.nodes))

    def test_map_const(self,utpop_fix):
        """ Test mapping the same arguments for all Traders. """
        G = utpop_fix
        # Setup some arguments.
        # A will just be set to this value
        A = 1
        # Epsilon dist is special as it will be sampled, so
        # the argument should be this lambda.
        epsilon_dist = lambda : 2
        
        # Call function.
        G2,node_map = populate_graph(G, A = A, epsilon_dist = epsilon_dist)
        # Check all nodes.
        assert(((n.A == A and n.epsilon_dist == epsilon_dist) for n in G2.nodes))

    def test_map_gen(self, utpop_fix):
        """ Test mapping generators. """
        G = utpop_fix
        # Use increasing numbers.
        gen = (v for v in range(len(G)))
        # Call function
        G2,node_map = populate_graph(G, C = gen)
        # Check that the sets of the range and the set
        # of attributes are the same.
        assert(set([v for v in range(len(G))]) == set([n.C for n in G2.nodes]))

    def test_mixed_map(self, utpop_fix):
        """ Test both constant and generator arguments for Trader."""
        G = utpop_fix
        # Use increasing numbers.
        gen1 = (v for v in range(len(G)))
        # A trickier one, returning lambdas
        theLambdas = [lambda : 2*v for v in range(len(G))] 
        gen2 = (l for l in theLambdas)
        # A will just be set to this value
        A = 1
        # Call function
        G2,node_map = populate_graph(G, C = gen1, A = A, epsilon_dist = gen2)
        # Check that the sets of the range and the set
        # of attributes are the same.
        assert(set([v for v in range(len(G))]) == set([n.C for n in G2.nodes])
               and (n.A == A for n in G2.nodes)
               and set(theLambdas) == set([n.epsilon_dist for n in G2.nodes]))

    
