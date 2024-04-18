from enum import Enum
from woningwaardering.vera.bvg.generated import Referentiedata


class Projectbudgetregelsoort(Enum):
    budget = Referentiedata(
        code="BUD",
        naam="Budget",
    )
    """
    Projectbudgetregel betreft een budgetbedrag
    """

    prognose = Referentiedata(
        code="PRO",
        naam="Prognose",
    )
    """
    Projectbudgetregel betreft een prognose-bedrag
    """

    @property
    def code(self) -> str | None:
        return self.value.code

    @property
    def naam(self) -> str | None:
        return self.value.naam