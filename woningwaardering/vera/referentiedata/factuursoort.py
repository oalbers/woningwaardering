from enum import Enum
from woningwaardering.vera.bvg.generated import Referentiedata


class Factuursoort(Enum):
    credit_factuur_extern = Referentiedata(
        code="CEX",
        naam="Credit factuur extern",
    )
    """
    Credit factuur extern
    """

    credit_factuur_intern = Referentiedata(
        code="CIF",
        naam="Credit factuur intern",
    )
    """
    Credit factuur intern
    """

    debet_factuur_extern = Referentiedata(
        code="DEX",
        naam="Debet factuur extern",
    )
    """
    Debet factuur extern
    """

    debet_factuur_intern = Referentiedata(
        code="DIF",
        naam="Debet factuur intern",
    )
    """
    Debet factuur intern
    """

    @property
    def code(self) -> str | None:
        return self.value.code

    @property
    def naam(self) -> str | None:
        return self.value.naam