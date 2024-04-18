from enum import Enum
from woningwaardering.vera.bvg.generated import Referentiedata


class Overeenkomstkoppelingstatus(Enum):
    aangevraagd = Referentiedata(
        code="AAN",
        naam="Aangevraagd",
    )
    """
    Het koppelen van de overeenkomsten is aangevraagd
    """

    afgewezen = Referentiedata(
        code="AFG",
        naam="Afgewezen",
    )
    """
    Het koppelen van de overeenkomsten is afgewezen
    """

    gekoppeld = Referentiedata(
        code="GEK",
        naam="Gekoppeld",
    )
    """
    Het koppelen van de overeenkomsten is gekoppeld
    """

    @property
    def code(self) -> str | None:
        return self.value.code

    @property
    def naam(self) -> str | None:
        return self.value.naam