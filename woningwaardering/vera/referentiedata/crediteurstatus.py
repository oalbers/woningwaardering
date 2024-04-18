from enum import Enum
from woningwaardering.vera.bvg.generated import Referentiedata


class Crediteurstatus(Enum):
    actief = Referentiedata(
        code="ACT",
        naam="Actief",
    )

    alleen_voor_betalen = Referentiedata(
        code="BET",
        naam="Alleen voor betalen",
    )
    """
    Korting
    """

    geblokkeerd = Referentiedata(
        code="GEB",
        naam="Geblokkeerd",
    )
    """
    Toeslag
    """

    voorlopig = Referentiedata(
        code="VRL",
        naam="Voorlopig",
    )

    @property
    def code(self) -> str | None:
        return self.value.code

    @property
    def naam(self) -> str | None:
        return self.value.naam