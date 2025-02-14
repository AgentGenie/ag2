# Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
#
# SPDX-License-Identifier: Apache-2.0

import subprocess
from functools import lru_cache
from logging import getLogger
from typing import Callable, TypeVar

from ...import_utils import patch_object

logger = getLogger(__name__)

__all__ = ["require_jupyter_kernel_gateway_installed", "skip_on_missing_jupyter_kernel_gateway"]


@lru_cache()
def is_jupyter_kernel_gateway_installed() -> bool:
    """Check if jupyter-kernel-gateway is installed."""
    try:
        subprocess.run(
            ["jupyter", "kernelgateway", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning(
            "jupyter-kernel-gateway is required for JupyterCodeExecutor, please install it with `pip install ag2[jupyter-executor]`"
        )
        return False


T = TypeVar("T")


def require_jupyter_kernel_gateway_installed() -> Callable[[T], T]:
    """Decorator to handle optional module dependencies

    Args:
        modules: Module name or list of module names required
        dep_target: Target name for pip installation (e.g. 'test' in pip install ag2[test])
    """
    if is_jupyter_kernel_gateway_installed():

        def decorator(o: T) -> T:
            return o
    else:

        def decorator(o: T) -> T:
            return patch_object(o, missing_modules=[], dep_target="jupyter-executor")

    return decorator


def skip_on_missing_jupyter_kernel_gateway() -> Callable[[T], T]:
    """Decorator to skip a test if an optional module is missing

    Args:
        module: Module name
        dep_target: Target name for pip installation (e.g. 'test' in pip install ag2[test])
    """

    if is_jupyter_kernel_gateway_installed():

        def decorator(o: T) -> T:
            return o
    else:

        def decorator(o: T) -> T:
            import pytest

            return pytest.mark.skip(
                reason="jupyter-kernel-gateway is required for JupyterCodeExecutor, please install it with `pip install ag2[jupyter-executor]`"
            )(o)  # type: ignore[return-value]

    return decorator
