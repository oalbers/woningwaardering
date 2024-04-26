from enum import Enum
from woningwaardering.vera.bvg.generated import Referentiedata


class Machtigingsoort(Enum):
    doorlopend = Referentiedata(
        code="DOO",
        naam="Doorlopend",
    )

    eenmalig = Referentiedata(
        code="EEN",
        naam="Eenmalig",
    )

    @property
    def code(self) -> str:
        if self.value.code is None:
            raise TypeError("de code van een Referentiedata object mag niet None zijn")
        return self.value.code

    @property
    def naam(self) -> str | None:
        return self.value.naam

    @property
    def parent(self) -> Referentiedata | None:
        return self.value.parent
