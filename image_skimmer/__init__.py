"""
Image Skimmer
-------------
Visually skim through large numbers of images quickly,
organizing on the fly.

Basic usage:

    >>> pip install -U image_skimmer
    >>> skim -p path/to/images --extensions .png|.jpg|.jpeg

:copyright: (c) 2020 Tobias Reaper.
:license: MIT, see LICENSE for more details.
"""

__title__ = "image_skimmer"
__author__ = "Tobias Reaper"
__license__ = "MIT"
__copyright__ = "Copyright 2020 Tobias Reaper"

from .skimmer import *
from .utils import *
