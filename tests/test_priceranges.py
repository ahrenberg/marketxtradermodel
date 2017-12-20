""" 
Test functions for priceranges.

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
from marketxtradermodel.priceranges import *
import numpy as np
import math

def test_creation():
    pr = PriceRanges()
    assert(None == pr.compute_price())
    assert(None == pr.price)
    
def test_insert_one():
    pr = PriceRanges()
    # Sell at 1, buy at -1
    pr.insert(p_s = 1, p_b = -1)
    # Should now have three price ranges.
    assert(3 == len(pr.trade_interval_bounds))
    # With these values
    assert(-1 == pr.trade_interval_bounds[0])
    assert( 1 == pr.trade_interval_bounds[1])
    assert( math.inf == pr.trade_interval_bounds[2])
    # And three value ranges.
    assert(3 == len(pr.trade_interval_values))
    print(pr.trade_interval_values)
    # With these values.
    assert(-1 == pr.trade_interval_values[0])
    assert( 0 == pr.trade_interval_values[1])
    assert( 1 == pr.trade_interval_values[2])
    # Finally, we should get the 0 solution no matter
    # where we ask (which we do by forcefully setting pr.price).
    assert(0 == pr.compute_price() and 0 == pr.price)
    pr.price = 0.1
    assert(0 == pr.compute_price() and 0 == pr.price)
    pr.price = -2
    assert(0 == pr.compute_price() and 0 == pr.price)
    pr.price = 100
    assert(0 == pr.compute_price() and 0 == pr.price)

def test_insert_one_flipped():
    pr = PriceRanges()
    # Sell at -2, buy at 2
    pr.insert(p_s = -2, p_b = 2)
    # Should now have three price ranges.
    assert(3 == len(pr.trade_interval_bounds))
    # With these values
    assert(-2 == pr.trade_interval_bounds[0])
    assert( 2 == pr.trade_interval_bounds[1])
    assert( math.inf == pr.trade_interval_bounds[2])
    # And three value ranges.
    assert(3 == len(pr.trade_interval_values))
    print(pr.trade_interval_values)
    # With these values.
    assert( 1 == pr.trade_interval_values[0])
    assert( 0 == pr.trade_interval_values[1])
    assert(-1 == pr.trade_interval_values[2])
    # Finally, we should get the 0 solution no matter
    # where we ask (which we do by forcefully setting pr.price).
    assert(0 == pr.compute_price() and 0 == pr.price)
    pr.price = 0.1
    assert(0 == pr.compute_price() and 0 == pr.price)
    pr.price = -5
    assert(0 == pr.compute_price() and 0 == pr.price)
    pr.price = 100
    assert(0 == pr.compute_price() and 0 == pr.price)

def test_clear_prices():
    pr = PriceRanges()
    pr.insert(-1,1)
    pr.clear_prices()
    assert(None == pr.compute_price())
    assert(None == pr.price)
    pr.insert(-1,1)
    assert(0 == pr.compute_price())

def test_insert_multiple():
    # Comming up with a sequence of three buy/sell pairs so that
    # there are two solutions.
    # Call them a, b, and c, with associated buy and sell prices
    # a_b, a_s, b_b, b_s, c_b, c_s.
    # Letting a be 'inverted' with a_s < a_b and b and c 'normal'.
    # Choosing values so that b_b < a_s < b_s < c_b < c_s < a_b
    # should produce two zero-areas, in b_b < p < a_s and b_s < p < c_b.
    b_b = 1
    a_s = 2
    b_s = 3
    c_b = 4
    c_s = 5
    a_b = 6
    pr = PriceRanges()
    pr.insert(a_s,a_b)
    pr.insert(b_s,b_b)
    pr.insert(c_s,c_b)
    # Now test.
    # Two solutions found.
    assert(2 == len(pr.known_solutions))
    # They are correct.
    s1 = (b_b + a_s)/2.0
    s2 = (b_s + c_b)/2.0
    assert(s1 in pr.known_solutions)
    assert(s2 in pr.known_solutions)
    # Querying on their far side gives the correspoding solution.
    # The default solution should be the one closest to zero.
    assert(min(abs(s1),abs(s2)) == pr.compute_price())
    pr.price = (b_b + 0.25*(a_s - b_b)/2.0)
    assert(s1 == pr.compute_price())
    pr.price = (b_s + 0.75*(c_b - b_s)/2.0)
    assert(s2 == pr.compute_price())

