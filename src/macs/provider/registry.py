from typing import Callable
from macs.provider.base import BaseProvider
from macs.core.registry import Registry

PROVIDER_REGISTRY = Registry[Callable[[], BaseProvider]]()
