""" 
Provides a reproduced implementation of the graph-based market model described in [BHKR09].

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

# Read version from pkg_resources and metadata.
try:
    import pkg_resources as _pkgr
    # Note that if someone has an older version installed and simply
    # loads from an updated git repo (or downloaded source dist) without doing
    # a proper setup.py install first, this will yield the old version.
    # Might also be an issue when installed on several places.
    # Probably OK for now though.
    # Also, if installed in editable (developer) mode with pip it will
    # of course show the version number when installed.
    __version__ = _pkgr.get_distribution(__name__).version
    # Throws an exception if no distribution can be found.
except _pkgr.DistributionNotFound as e:
    # Allow to load from directory in this case, but set version to unknown.
    __version__ = "UNKNOWN"

from .simulation import simulate_prices
from .simulation import evolve
from .priceranges import PriceRanges
from .trader import Trader
from . import utilities
