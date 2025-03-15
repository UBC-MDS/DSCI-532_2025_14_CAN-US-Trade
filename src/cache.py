# file: cache.py
# author: Danish Karlin Isa
# date: 2025-03-18

import os
from flask_caching import Cache

cache = Cache(
    config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'tmp'
    }
)
