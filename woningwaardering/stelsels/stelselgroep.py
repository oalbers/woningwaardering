from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date
from typing import Iterator

from woningwaardering.stelsels.utils import is_geldig
from woningwaardering.vera.bvg.generated import (
    EenhedenEenheid,
    WoningwaarderingResultatenWoningwaardering,
    WoningwaarderingResultatenWoningwaarderingCriterium,
    WoningwaarderingResultatenWoningwaarderingGroep,
    WoningwaarderingResultatenWoningwaarderingResultaat,
)
from woningwaardering.vera.referentiedata import (
    Woningwaarderingstelsel,
    Woningwaarderingstelselgroep,
)


class Stelselgroep(ABC):
    @property
    def stelsel(self) -> Woningwaarderingstelsel:
        return self._stelsel

    @stelsel.setter
    def stelsel(self, value: Woningwaarderingstelsel) -> None:
        self._stelsel = value

    @property
    def stelselgroep(self) -> Woningwaarderingstelselgroep:
        return self._stelselgroep

    @stelselgroep.setter
    def stelselgroep(self, value: Woningwaarderingstelselgroep) -> None:
        self._stelselgroep = value

    """Initialiseert een Stelselgroep.

    Args:
        begindatum (date): De begindatum van de geldigheid van de stelselgroep.
        einddatum (date, optional): De einddatum (t/m) van de geldigheid van de stelselgroep.
        peildatum (date, optional): De peildatum voor de waardering".

    Raises:
        ValueError: Als de stelselgroep niet geldig is op de peildatum.
    """

    def __init__(
        self,
        begindatum: date,
        einddatum: date = date.max,
        peildatum: date = date.today(),
    ) -> None:
        self.peildatum = peildatum
        if not is_geldig(begindatum, einddatum, peildatum):
            raise ValueError(
                f"Stelselgroep ({begindatum} - {einddatum}) is niet geldig op peildatum ({peildatum})."
            )

    @abstractmethod
    def bereken(
        self,
        eenheid: EenhedenEenheid,
        woningwaardering_resultaat: (
            WoningwaarderingResultatenWoningwaarderingResultaat | None
        ) = None,
    ) -> WoningwaarderingResultatenWoningwaarderingGroep:
        """Bereken de woningwaardering voor een specifieke eenheid op stelselgroep-niveau.

        Args:
            eenheid (EenhedenEenheid): De eenheid waarvoor de woningwaardering wordt berekend.
            woningwaardering_resultaat (WoningwaarderingResultatenWoningwaarderingResultaat | None, optional): Het resultaat van de woningwaardering.

        Returns:
            WoningwaarderingResultatenWoningwaarderingGroep: Het resultaat van de woningwaardering voor de gehele groep.
        """
        pass  # pragma: no cover

    def criteriumsleutel_resultaten(
        self,
        woningwaardering_groep: WoningwaarderingResultatenWoningwaarderingGroep,
    ) -> Iterator[WoningwaarderingResultatenWoningwaardering]:
        criteriumsleutelpunten: dict[str, float] = defaultdict(float)
        for woningwaardering in woningwaardering_groep.woningwaarderingen or []:
            if (
                woningwaardering.criterium
                and woningwaardering.criterium.bovenliggende_criterium
                and woningwaardering.criterium.bovenliggende_criterium.id
                and isinstance(woningwaardering.punten, float)
            ):
                criteriumsleutelpunten[
                    woningwaardering.criterium.bovenliggende_criterium.id
                ] += woningwaardering.punten

        for id, punten in criteriumsleutelpunten.items():
            yield WoningwaarderingResultatenWoningwaardering(
                criterium=WoningwaarderingResultatenWoningwaarderingCriterium(
                    naam=id.replace("_", " ").capitalize(),
                    id=id,
                ),
                punten=punten,
            )
