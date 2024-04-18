from enum import Enum
from woningwaardering.vera.bvg.generated import Referentiedata


class Defectstatus(Enum):
    geinspecteerd = Referentiedata(
        code="INS",
        naam="Geinspecteerd",
    )

    gemeld = Referentiedata(
        code="MEL",
        naam="Gemeld",
    )

    @property
    def code(self) -> str | None:
        return self.value.code

    @property
    def naam(self) -> str | None:
        return self.value.naam