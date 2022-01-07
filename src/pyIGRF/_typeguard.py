# -*- coding: utf-8 -*-

import os
import warnings

if os.environ.get('PYIGRF_DEBUG', '0') == '1':
    from typeguard import typechecked
    warnings.warn("running in debug mode with activated run-time type checks", RuntimeWarning)
else:
    typechecked = lambda x: x
