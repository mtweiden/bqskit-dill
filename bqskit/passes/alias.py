"""This module implements the PassAlias class."""
from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from bqskit.compiler.basepass import BasePass
from bqskit.compiler.workflow import Workflow

if TYPE_CHECKING:
    from bqskit.compiler.passdata import PassData
    from bqskit.ir.circuit import Circuit


class PassAlias(BasePass):
    """A pass that is an alias for another pass or sequence of passes."""

    @abc.abstractmethod
    def get_passes(self) -> list[BasePass]:
        """Return the passes that should be run, when this alias is called."""

    async def run(self, circuit: Circuit, data: PassData) -> None:
        """Perform the pass's operation, see :class:`BasePass` for more."""
        await Workflow(self.get_passes()).run(circuit, data)
