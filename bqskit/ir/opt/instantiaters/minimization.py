"""This module implements the Minimization class."""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from bqskit.ir.opt.cost.functions.hilbertschmidt import HilbertSchmidtGenerator
from bqskit.ir.opt.cost.generator import CostFunctionGenerator
from bqskit.ir.opt.instantiater import Instantiater
from bqskit.ir.opt.minimizer import Minimizer
from bqskit.ir.opt.minimizers.lbfgs import LBFGSMinimizer
from bqskit.qis.state.state import StateVector
from bqskit.qis.unitary.unitarymatrix import UnitaryMatrix

if TYPE_CHECKING:
    from bqskit.ir.circuit import Circuit


class Minimization(Instantiater):
    """The Minimization circuit instantiater."""

    def __init__(
        self,
        cost_fn_gen: CostFunctionGenerator = HilbertSchmidtGenerator(),
        minimizer: Minimizer | None = None,
    ) -> None:
        """
        Construct and configure a Minimization Instantiater.

        Args:
            cost_fn_gen (CostFunctionGenerator): This generator creates cost
                functions that are minimized.
                (Default: HilbertSchmidtGenerator())

            minimizer (Minimizer | None): The minimizer to use. If left as
                None, attempts to select best one.
        """

        if not isinstance(cost_fn_gen, CostFunctionGenerator):
            raise TypeError(
                'Expected CostFunctionGenerator, got %s.' % type(cost_fn_gen),
            )

        if minimizer is not None and not isinstance(minimizer, Minimizer):
            raise TypeError('Expected Minimizer, got %s.' % type(minimizer))

        self.cost_fn_gen = cost_fn_gen
        self.minimizer = minimizer

    def instantiate(
        self,
        circuit: Circuit,
        target: UnitaryMatrix | StateVector,
        x0: np.ndarray,
    ) -> np.ndarray:
        """Instantiate `circuit`, see Instantiater for more info."""
        cost = self.cost_fn_gen.gen_cost(circuit, target)

        if self.minimizer is None:
            return LBFGSMinimizer().minimize(cost, x0)
        else:
            return self.minimizer.minimize(cost, x0)

    @staticmethod
    def is_capable(circuit: Circuit) -> bool:
        """Return true if the circuit can be instantiated."""
        return True

    @staticmethod
    def get_violation_report(circuit: Circuit) -> str:
        """
        All circuits can be instantiated with minimization.

        See Instantiater for more info.
        """
        raise ValueError('Circuit can be instantiated.')

    @staticmethod
    def get_method_name() -> str:
        """Return the name of this method."""
        return 'minimization'