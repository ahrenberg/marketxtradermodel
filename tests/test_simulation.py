""" 
Test functions for simulation.

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
from marketxtradermodel.simulation import *
import numpy as np

@pytest.fixture
def small_graph_fix():
    G = nx.fast_gnp_random_graph(1000,0.03,directed=True)
    G,_ = mxtm.utilities.populate_graph(G,inplace=True)
    pr = mxtm.PriceRanges()
    return G,pr

def test_time_step(small_graph_fix):
    G,pr = small_graph_fix
    # Do ten steps
    for t in range(10):
        p = time_step(t,G,pr)
        # Check so that the right price is returned.
        assert(p != None)
        assert(0 == sum([n.state[t] for n in G]))
    
