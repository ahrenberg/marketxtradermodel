"""
Functions related to running trading simulations on complex networks. 
Based on model described in [BHKR09].

References
----------
.. [BHKR09] A social network model of investment behaviour in the stock market
   by L Bakker, W Hare, H Khosravi, B Ramadanovic - 
   Physica A: Statistical Mechanics and its Applications, 2010

"""
# marketxtradermodel
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
# Need the PriceRanges class.

from .priceranges import PriceRanges as _PriceRanges

def time_step(t, graph, price_range):
    """ Computes a single iteration of the main algorithm.

    Basically imitates algorithm at the end of Section 2 in [BHKR09], updating
    graph state and price_range.

    Parameters
    ----------
    t : Non-negative int
        Time stamp for iteration.
    graph : NetworkX DiGraph with Trader nodes.
        Graph state; will be updated by function.
    price_range : PriceRanges object
        Price ranges; Will be updated by the function.

    Returns
    -------
    float
        The market price at the end of iteration.
    
    """
    # Note: Probably possible to speed up by combining the two loops
    # over all nodes. For now however, keep it simple.
    #
    # Clear the price lists
    price_range.clear_prices()
    # Go over nodes and update epsilon and prices for this time step.
    for n in graph.nodes.keys():
        n.update_epsilon(t)
        (p_s, p_b) = n.compute_price_points(t, graph.neighbors(n))
        price_range.insert(p_s, p_b)
        # Compute the new price
    p = price_range.compute_price()
    # Go over nodes and update states for this time step
    for n in graph.nodes.keys():
        n.update_state(t, p, graph.neighbors(n))
        # For convenience, return price
    return p


def evolve(graph, time_range, price_range):
    """
    Evolve graph model over time, yielding market price at each step.

    Parameters
    -----------
    graph : NetworkX DiGraph with Trader nodes
        A graph with initial state set; will be updated each iteration.
    time_range : iterable of int
        Range of time steps, typical integers 1...N or 0...N-1
    price_range : PriceRanges object
        Initial buy and sell proces; will be updated each iteration.

    Yields
    ------
    int
        Current time
    float
        Market price at t

    """
    for t in time_range:
        yield (t,time_step(t, graph, price_range))

def simulate_prices(graph, time_range, price_range = None):
    """ Evolve model and return a list of market prices.

    This is a convenience function which evolves graph
    over time_range and returns a list of market prices
    at the end of each time step in time_range.

    Parameters
    -----------
    graph : NetworkX DiGraph with Trader nodes
        An graph with initial state set.
    time_range : iterable
        Range of time steps, typical 1...N.
    price_range : PriceRanges object, optional
        A PriceRange object for simulation price if initially calculated 
        externally. If None a new object will be created wiht default initial
        price. If an existing object is provided the initial 
        price will be set to its current price.

    See Also
    --------
    evolve : Generator evolving the model over a number of time steps.
    simulate_and_distill : A more general version allowing.

    Returns
    -------
    list of float
        A list of prices of length len(time_range), contains the market price
        at the end of each iteration.
    
    """
    if price_range == None:
        price_range = _PriceRanges()

    # Accumulate prices here.
    prices = []

    # Loop and compute
    for _, p in evolve(graph, time_range, price_range):
        prices.append(p)
    
    return prices

def simulate_and_distill(graph, time_range, price_range, graph_distiller,
                         price_range_distiller):
    """ Evolve model and return a list of data produced by provided functions.

    This function allows the caller to provide functions acting on the current 
    time step and graph or price_range at each step in the time evolution in 
    order to produce the output data. The call signature should be f(t,x) where
    t is a time from time_range, and x is a NetworkX DiGraph of Trader for
    graph_distiller, or x is a PriceRanges object for price_range_distiller.
    The value returned by a distiler is added to the output data.

    Parameters
    ----------
    graph : NetworkX DiGraph with Trader nodes
        An graph with initial state set.
    time_range : iterable
        Range of time steps, typical 1...N.
    price_range : PriceRanges objec
        Initial buy and sell proces; will be updated each iteration.
    graph_distiller : callable or None
        Function distilling data from the graph at each iteration step.
        This function will be called with the current time and graph as 
        arguments at the end of each iteration step. The returned values are 
        appended to the function output.
        Setting parameter to None skips this step.
    price_range_distiller : callable or None
        Function distilling data from the price_range at each iteration step.
        This function will be called with the current time and price_range as 
        arguments at the end of an iteration step. The returned values are 
        appended to the function output.
        Setting parameter to None skips this step.
        

    Returns
    -------
    list of tuple
        There is one tuple for each time in time_range. The tuples contain the 
        results from calling graph_distiller and price_range_distiller if these
        are not None. Thus, the tuple size is 2 if both distiller functions are
        provided, 1 if either, but not both are None, and 0 if for some reason 
        both are None.

    See Also
    --------
    evolve : Generator evolving the model over a number of time steps.

    Notes
    -----
    This function returns a list of data from all iterations in the simulation.
    If the provided distiller functions are designed to extract a lot of data 
    from the provided graph and prices over many iterations, it may be better
    to consider using the generator evolve instead.
    
    """
    # Output data stored here.
    data = []
    # Evolve system
    for t, _ in evolve(graph, time_range, price_range):
        # Data for this iteration stored here.
        it_data = []
        # If a graph distiller function has been provided append its result to
        # the data.
        if graph_distiller != None:
            it_data.append(graph_distiller(t, graph))
        # Same thing if a range distiller has been provided.
        if price_range_distiller != None:
            it_data.append(price_range_distiller(t, graph))
        # Convert to tuple and append.
        data.append(tuple(it_data))
    
    return data
                           
