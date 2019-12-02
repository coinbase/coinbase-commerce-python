try:
    import aiohttp  # noqa: F401
except ImportError:
    import warnings

    warnings.warn(
        'Please install extras_require "aio" for using this module',
        ImportWarning
    )

from .api_resources import *  # noqa: F403
from .client import *  # noqa: F403

__all__ = (
        api_resources.__all__  # noqa: F405,W503
        + client.__all__  # noqa: F405,W503
)
