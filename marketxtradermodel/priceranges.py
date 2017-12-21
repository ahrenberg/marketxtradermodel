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
    """
    
    def __init__(self):
        # Contains registered buy and sell prices.
        self._prices = []
        # This attribute contains the result from the most recent call to
        # compute_price, or 0 if no call has been made.
        self._price_ref = 0
        # This is the difference (# buyers) - (# sellers) given the price in
        # _price_ref.
        self._balance = 0
        # Contains the change in _balance when passing each price point in
        # _price, given traversal from lower index to higher.
        self._balance_differences = []
        
                
    def insert(self, p_s, p_b):
        """ Inserts sell and buy price into ranges.
        
        Parameters
        ----------
        p_s: float
            Sell price.
        p_b: float
            Buy price.

        """
        # -1 weight (for balance of buyers - sellers) if rational
        # +1 weight of irrational
        w = -1 if p_b < p_s else 1
        # Insert values.
        i_s = _bisect.bisect_left(self._prices,p_s)
        self._prices.insert(i_s,p_s)
        self._balance_differences.insert(i_s,w)
        i_b = _bisect.bisect_left(self._prices,p_b)
        self._prices.insert(i_b,p_b)
        self._balance_differences.insert(i_b,w)
        # Now check how we are doing compared to the reference price.
        if self._price_ref > p_b and self._price_ref > p_s:
            # If above, subtract one if rational, add one if irrational.
            self._balance += w
        elif self._price_ref < p_b and self._price_ref < p_s:
            # If below, add one if rational, subtract one if irational.
            self._balance -= w

        
    def clear_prices(self):
        """Clears buy and sell prices."""
        self._prices = []
        self._balance_differences = []
        self._balance = 0

    def _search_price(self,start_idx,d):
        """
        Searches for a price balancing the price array.
        
        Parameters
        ----------
        start_idx : int
            Index where to start the search. Should be the result of 
            a bisect_left.
        d : int in -1,1
            Direction of search. -1 means towards lower indicies, +1 towards 
            higher.

        Raises
        ------
        ValueError
            If parameter d not in {-1,1}.
        """
        if d not in set([-1,1]):
            raise ValueError("Search direction must be -1 or 1.")
        idx = start_idx
        b = self._balance
        p = _Inf
        # If going in the positive direction, back up
        # one step due to the while loop checking
        # before add.
        if d  == 1:
            idx -= 1;
        while b != 0 and idx+d >= 0 \
              and idx+d < len(self._balance_differences):
            idx+=d
            b += d*self._balance_differences[idx]
        if b == 0 and idx+d >= 0 and idx+d < len(self._prices):
            p = (self._prices[idx] + self._prices[idx + d])/2.0
        return p
    
    def compute_price(self):
        """ Compute a price point balancing the currently registered prices.
        
        If multiple solutions are avaliable the one closest to the previous
        call to compute_prices are choosen, or to 0 if this is the first call.        

        Returns
        -------
        float
            A price which guarantees an equal number of buyers and sellers
            given the registered prices.

        Throws
        ------
        Exception
            If no prices has been registerd, or if no solution is found.
        """
        # Check if it is ok to call.
        if len(self._prices) <= 0:
            raise Exception("No buy and sell prices registered.")
        # This is the current index
        idx = _bisect.bisect_left(self._prices,self._price_ref)
        p = _Inf
    
        # Check if we are lucky and already at a solution.
        # Then pick it.
        if self._balance == 0:
            p = (self._prices[idx-1] + self._prices[idx])/2.0
        else:
            # Otherwise search
            # Towards lower
            p_lo = self._search_price(idx,-1)
            # And towards higher.
            p_hi = self._search_price(idx, 1)
            # Pick the one closest to the current price.
            p = min(p_lo,p_hi, key = lambda p : abs(p - self._price_ref))
            if p == _Inf:
                raise Exception("No solution found. All registered prices distinct?")
        self._price_ref = p
        return p
