"""
The following class is used to keep track of the intervals in which traders
choose to buy and sell, as well as any known solutions, where the number of
buyers matches the number of sellers.

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

import bisect as _bisect
from math import inf as _Inf

class PriceRanges(object):
    """
    Class to compute possible equilibrium prices from registered trader's buy
    and sell prices.
    
    Attributes
    ----------
    known_solutions: list of float
        List of currently known balancing prices.
    price: float
        Price solution from most recent call to compute_price or None.
    """
    
    def __init__(self):
        self.clear_prices()
        self.price = None

    def _add_interval_value_and_check_solution(self, i_lo, i_hi, p):
        """ Add p to the interval_values where index in range i_lo <= i < i_hi.
        If the resulting value is equal to 0 compute the midpoint from the 
        bounds array and add this to self.known_solutions.

        Parameters
        ----------
        idx_bound : int
            Upper index bound.
        p : float
            Price value to add to interval values. Typically in set {-1,0,1}.
        """
        for i in range(i_lo, i_hi):
            self.trade_interval_values[i] += p
            # Check if solution is found, ingore solutions with infinite prices.
            if 0 == self.trade_interval_values[i] \
               and i > 0 and i+1 < len(self.trade_interval_values):
                self.known_solutions.append((self.trade_interval_bounds[i-1]
                                             + self.trade_interval_bounds[i])
                                            / 2.0)
        
                
    def insert(self, p_s, p_b):
        """ Inserts sell and buy price into ranges.
        
        Parameters
        ----------
        p_s: float
            Sell price.
        p_b: float
            Buy price.

        """
        # Clear known solutions.
        self.known_solutions = []
        # Check inputs
        assert (abs(p_s) != _Inf and abs(p_b) != _Inf), "Buy or sell price can not be infinite"
        # Figure out if the buy or sell price is the lower and
        # create ranges.
        # Assume that buy price is less than sell price.
        p_lo = p_b
        p_lo_val = -1
        p_hi = p_s
        p_hi_val = 1
        # However, if it is swapped, we need to rearrange.
        if p_s < p_b:
            p_lo = p_s
            p_lo_val = 1
            p_hi = p_b
            p_hi_val = -1
        # Find insertion points
        # Note that as upper bound is _Inf, the next value will always exist.
        # Also note that as the inserts are done sequentially in order, the
        # indices remain valid.
        i_lo  = _bisect.bisect_left(self.trade_interval_bounds,p_lo)
        self.trade_interval_bounds.insert(i_lo, p_lo)
        self.trade_interval_values.insert(i_lo,
                                          self.trade_interval_values[i_lo])
        i_hi  = _bisect.bisect_left(self.trade_interval_bounds,p_hi)
        self.trade_interval_bounds.insert(i_hi, p_hi)
        self.trade_interval_values.insert(i_hi,
                                          self.trade_interval_values[i_hi])
        # Now, go over the list, update values and check if any is a solution.
        self._add_interval_value_and_check_solution(0, i_lo+1, p_lo_val)
        self._add_interval_value_and_check_solution(i_lo+1, i_hi+1, 0)
        self._add_interval_value_and_check_solution(i_hi+1,
                                                    len(self.trade_interval_values),
                                                    p_hi_val)

        # Done
        
    def clear_prices(self):
        """Clears price ranges and solutions."""
        self.known_solutions = []
        self.trade_interval_bounds = [_Inf] # Assumed to start at -_Inf
        self.trade_interval_values = [0]
        
    def compute_price(self):
        """ Updates `price` with value from `known_solutions`, or None.
    
        If known_solutions contains multiple values the one closest
        to current value of `price` is chosen, minimizing 
        abs(self.price - p) for p in self.known_solutions.
        
        If self.price is None, the price closest to 0 is picked.
        
        Returns
        -------
        float
            The new value of self.price
        """

        ref = 0 if None == self.price else self.price

        self.price = None if len(self.known_solutions) <= 0 \
                     else min(self.known_solutions,
                              key = lambda p : abs(ref - p))
        return self.price
        
