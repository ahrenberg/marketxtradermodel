"""
The following class is used to hold sorted lists of buy and sell prices 
produced by the traders during a single iteration of a simulation. It also computes
and tracks the current 'balancing' price by a method akin to that described
last in Section 2 of [BHKR09].

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
from numpy import sort as _sort

class PriceRanges(object):
    """
    Class to keep track of sell and buy prices, as well as the current mid price.
    
    Attributes
    ----------
    sell_prices: list of float
        List of current selling prices.
    buy_prices: list of float
        List of current buying prices.
    price : float
        Current market price.

    """
    
    def __init__(self):
        self.sell_prices = []
        self.buy_prices = []
        self.price = 0

    def insert(self, p_s, p_b):
        """ Inserts sell and buy price into ranges.
        
        Parameters
        ----------
        p_s: float
            Sell price.
        p_b: float
            Buy price.

        """
        _bisect.insort(self.sell_prices, p_s)
        _bisect.insort(self.buy_prices, p_b)
        
    def clear_prices(self):
        """Clears sell and buy price ranges."""
        self.sell_prices.clear()
        self.buy_prices.clear()
        
    def compute_price(self):
        """ Computes current market price for current buy and sell price ranges.
        
        After execution the value of the attribute current_price contains the
        computed value. This value is also returned by the function for 
        convenience.

        Returns
        -------
        float
            Current market price.

        Throws
        ------
        AssertionError
            When the number of iterations required is greater than twice the number of sell-prices.
        """
        price_found = False
        current_price = self.price
        n_iters = 0
        n_sell = len(self.sell_prices)
        n_buy = len(self.buy_prices)
        while not price_found:
            sell_idx = _bisect.bisect_left(self.sell_prices, current_price)
            buy_idx = _bisect.bisect_right(self.buy_prices, current_price)
            sell_dist = sell_idx
            buy_dist = len(self.buy_prices) - buy_idx
            if sell_dist > buy_dist:
                # More sell indices, back up towards the list beginning
                # Take up to two closest elements from both sell and buy lists,
                # form a new listand sort it.
                l = _sort(self.sell_prices[max(sell_idx - 2,0):max(sell_idx,1)] \
                         + self.buy_prices[max(buy_idx - 2,0):max(buy_idx,1)])
                # The two largest (last) elements will be the closest ones. Let the new price be their average.
                current_price = (l[-2] + l[-1])/2.0
            elif buy_dist > sell_dist:
                # More sell indices, back up towards the list beginning
                # Take up to two closest elements from both sell and buy lists,
                # form a new listand sort it.
                l = _sort(self.sell_prices[min(sell_idx+1,n_sell-1):min(sell_idx + 3,n_sell)] \
                         + self.buy_prices[min(buy_idx+1,n_buy-1):min(buy_idx + 3,n_buy)])
                # The two smallest (first) elements will be the closest ones. Let the new price be their average.
                current_price = (l[0] + l[1])/2.0
            else:
                # Equal distance, we are done.
                self.price = current_price
                price_found = True
                n_iters += 1
            # The method above should always find a price, but the following if-case
            # is left in to break if running over the full range of prices. This is to
            # catch bugs while developing and avoiding an infinite loop.
            assert n_iters < len(self.sell_prices)*2, \
                  "Lots of step, breaking, something wrong. Phases? Infinite loop?"

        return self.price
