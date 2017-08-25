marketxtradermodel
==================

A python package providing an implementation of the graph-based market model described in [BHKR09].

It specifies a trader model and includes functions to adapt NetworkX_ directed graphs into trader networks and to evolve these systems over time.

Note that this is not the code used to produce the results in [BHKR09], but a re-implementation of that model.

.. _NetworkX: http://networkx.github.io

Example
-------
>>> import marketxtradermodel as mxtm
>>> import networkx as nx
>>> G = nx.fast_gnp_random_graph(1000,0.0025,directed=True) # Build a random graph.
>>> _ = mxtm.utilities.populate_graph(G) # Change integer nodes to Traders
>>> prices = mxtm.simulate_prices(G,range(10)) # Run 10 simulation steps, measuring market price.

License
-------
Released under Apache 2 license (See LICENSE)::

   Copyright 2017 Lukas Ahrenberg <lukas@ahrenberg.se>

References
----------
.. [BHKR09] A social network model of investment behaviour in the stock market
   by L Bakker, W Hare, H Khosravi, B Ramadanovic - 
   Physica A: Statistical Mechanics and its Applications, 2010,
   https://doi.org/10.1016/j.physa.2009.11.013

