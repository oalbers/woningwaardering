from enum import Enum
from woningwaardering.vera.bvg.generated import Referentiedata


class Geslacht(Enum):
    mannelijk = Referentiedata(
        code="M",
        naam="Mannelijk",
    )
    """
    Mannelijk geslacht
    """

    neutraal = Referentiedata(
        code="N",
        naam="Neutraal",
    )
    """
    Gender-neutraal
    """

    vrouwelijk = Referentiedata(
        code="V",
        naam="Vrouwelijk",
    )
    """
    Vrouwelijk geslacht
    """

    @property
    def code(self) -> str | None:
        return self.value.code

    @property
    def naam(self) -> str | None:
        return self.value.naam