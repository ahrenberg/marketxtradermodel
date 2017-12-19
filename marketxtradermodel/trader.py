"""
This class represents a trader and will be used as nodes of the graph.

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

import numpy as _np

class Trader(object):
    """
    Describes a trader with state -1 (buy), 0 (hold), 1 (sell), individual
    random distributions, and with a finite, round-robin memory of past states 
    and data.

    Attributes
    ----------
    state : int in set (-1,0,1)
        Current buy/hold/sell state of trader.
    A : float
        Influence by asset price; $A_i$ in [BHKR09].
    B : float
        Influence by percieved change in price; $B_i$ in [BHKR09].
    C : float
        Influence by behaviour of other traders; $C_i$ in [BHKR09].
    D : float
        Innate trading strategy; $D_i$ in [BHKR09].
    eps : RRMem object
        Round-robin memory of current as well as a finite number of previous
        price errors. eps[t], where t is the current time will yield $epsilon_i$
        in [BHKR09].
    epsilon_dist : float or callable returning float.
        Represents either a function sampling the probability distribution of, 
        or a constant value for, the error of the trader's percieved price. 
        ($epsilon_i$ in [BHKR09]).
    perc_price : RRMem object
        Round-robin memory of current as well as a finite number of previous
        prices. perc_price[t], where t is the current time, will yield the
        parameter $p$ in [BHKR09].
    name : str
        Identification string.

    """
    
    # --- Static helper functions ---
    #
    # Compute the state sum [influence] for traders in vector neighiours at integer time t
    _influence = lambda neighbours, t : sum((n.state[t] for n in neighbours))
    # Sample if function provided, return object if not.
    # Note the use of callable below does reportedly not work in Python 3.0 and
    # 3.1, but should work in some versions of 2 and 3.2+. Not tested this
    # claim.
    _sample = lambda v : v() if callable(v) else v 

    # --- Static data ---
    # Buy cutoff threshold
    _b = -1
    # Sell cutoff threshold
    _s = 1
    
    # --- Inner class definition ---
    class RRMem(list):
        """
        Represent a finite memory as a round-robin list.
        Items are looked up at a logical integer time moduolo the capacity (current length). 

        """
        def __getitem__(self, key):
            return super().__getitem__(key % len(self))
        def __setitem__(self, key, val):
            super().__setitem__(key % len(self),val)

    # --- Methods ---
    def __init__(self, 
                 A = 1,
                 B = lambda : _np.random.normal( 0.0, 1.0), 
                 C = lambda : _np.random.normal( 5.0, 2.0),  
                 D = lambda : _np.random.normal(0.0, 1.0),
                 S = lambda : _np.random.choice((-1,0,1)),
                 memory_length = 1,
                 epsilon_dist = lambda : _np.random.normal( 0, 0.33),
                 name = None):
        """
        Init method.
        
        Parameters
        ----------
        A : float or callable returning float, optional
            Influence by asset price, $A_i$ in [BHKR09];
            Default to constant value of 1.
        B : float or callable returning float, optional
            Influence by percieved change in price, $B_i$ in [BHKR09].
            Defaults to callable function sampling from normal distribution of
            mean 0.0 and std. dev. 1.0.
        C : float or function returning float.
            Influence by neigbouring Trader states, $C_i$ in [BHKR09].
            Defaults to callable function sampling from normal distribution of
            mean 5.0 and std. dev. 2.0.
        D : float or function returning float.
            Innate tendency to buy/hold/sell, $D_i$ in [BHKR09].
            Defaults to callable function sampling from normal distribution of
            mean 0.0 and std. dev. 1.0.
        S : int in (-1,0,1), or callable returning int in (-1,0,1), optional
            Initial buy/hold/sell state, $S_i$ in [BHKR09].
            Defaults to callable function choosing one of (-1,0,1) with equal
            probability.
        memory_length : int greater than zero, optional
            Number of previous iterations to "remember".
            Defaults to 1, i.e. remembering one step back.
            Note that this parameter does not change the behaviour of the
            simulation, only the ammount of previous iterations saved in
            the nodes.
        epsilon_dist : float or function returning float.
            Individual trader "error", $\epsilon_i$ in [BHKR09].
            Defaults to callable function sampling from normal distribution of
            mean 0.0 and std. dev. 0.33.
        name : str, optional
            Identification string.

        Notes
        -----
        Parameters A,B,C,D,S, and epsilon_dist may either be constant floats or 
        callables returning a single float (each). If constant, this value is
        used, if it is a callable object this object is called and the returned
        value used instead. The reason is to enable Trader objects sample their
        random variable parameters on creation, so that this does not have to
        be done manually, when creating a large set.
        Tip: If the callables need parameters provided, use a lambdas or bind 
        values using functools.partial. 
        E.g. B = lambda : np.random.normal(0.0, 1.0) will create a callable
        lambda function for parameter B sampling a normal distribution with
        mean 0 and std. dev. 1.0 using numpy.random.normal.
        
        """
        # S(t_m); where t_m = t_l mod len(S), and t_l is a logical clock. t_l = 0,1, 2, 3, 4...
        # Initialize memory to same random number as initially only first value important.
        self.state = Trader.RRMem((Trader._sample(S),)*(memory_length+1))
        # A_i Initialize to a sample or take A if a number.
        self.A = Trader._sample(A)
        # B_i
        self.B = Trader._sample(B)
        # C_i
        self.C = Trader._sample(C)
        # D_i
        self.D = Trader._sample(D)
        # epsilon_i
        self.eps = Trader.RRMem((Trader._sample(epsilon_dist),)*(memory_length+1))
        # Also save the epsilon distribution as this will be used when updating.
        self.epsilon_dist = epsilon_dist
        # Percieved price Also in memory?
        self.perc_price = Trader.RRMem((0,)*(memory_length+1))
        # Set name.
        self.name = name
        
    def update_epsilon(self, t):
        """Update epsilon for time t.

        Parameters
        ----------
        t : Non-negative int
            Time when epsilon should be resampled.
        """
        self.eps[t] = Trader._sample(self.epsilon_dist)
        
    def compute_price_points(self, t, neighbors):
        """ 
        Return buy and sell price points for the Trader at time t 
        given a set of trusted neighbours.
        Computes quantities $p_i^s$ and $p_i^b$ from [BHKR09].
        
        Parameters
        ----------
        t : int
            Time when price points should be calculated.
        neighbours : List of Trader
            List of neighbouring Trader objects influencing this one.

        """
        K = (self.A + self.B) * self.eps[t] \
            - self.B * self.perc_price[t-1] \
            + self.C * Trader._influence(neighbors, t-1) \
            + self.D
        p_s = (Trader._s - K)/(self.A + self.B)
        p_b = (Trader._b - K)/(self.A + self.B)
        if p_b > p_s:
            print("Buy price ({0}) should always be lower than sell price ({1})!".format(p_b, p_s))
            print(" A + B --> {0} [A={1},B={2}]".format(self.A + self.B, self.A, self.B))
        return (p_s, p_b)
    
    def update_state(self, t, price_t, neighbors):
        """
        Updates the state for trader at time t, given the price at time t, and a
        list of trusted neighbours.
        
        Parameters
        ----------
        t : int
            Time when state should be updated.
        price_t : float
            Global market price at time t.
        neighbours : List of Trader
            List of neighbouring Trader objects influencing this one.
        """
        # Perceived price at this time
        self.perc_price[t] = price_t + self.eps[t]
        # Compute L_t
        # L_t = self.A * self.perc_price[t] \
        #       + self.B * (self.perc_price[t] - self.perc_price[t-1]) \
        #       + self.C * Trader._influence(neighbors, t-1) \
        #       + self.D
        K = (self.A + self.B) * self.eps[t] \
            - self.B * self.perc_price[t-1] \
            + self.C * Trader._influence(neighbors, t-1) \
            + self.D
        L_t = (self.A + self.B) * price_t + K
        # Update state
        if L_t < Trader._b:
            self.state[t] = -1
        elif L_t <= Trader._s:
            self.state[t] = 0
        else:
            self.state[t] = 1
            
