from datetime import date


from woningwaardering.stelsels.stelsel import Stelsel
from woningwaardering.stelsels import utils
from woningwaardering.vera.bvg.generated import (
    EenhedenEenheid,
)
from woningwaardering.vera.referentiedata import (
    Woningwaarderingstelsel,
)


class ZelfstandigeWoonruimten(Stelsel):
    def __init__(self, peildatum: date = date.today()) -> None:
        super().__init__(
            stelsel=Woningwaarderingstelsel.zelfstandige_woonruimten,
            peildatum=peildatum,
        )


if __name__ == "__main__":
    zelfstandige_woonruimten = ZelfstandigeWoonruimten()
    file = open(
        "./tests/data/input/zelfstandige_woonruimten/41123000005.json",
        "r+",
    )
    eenheid = EenhedenEenheid.model_validate_json(file.read())
    woningwaardering_resultaat = zelfstandige_woonruimten.bereken(eenheid)
    print(
        woningwaardering_resultaat.model_dump_json(
            by_alias=True, indent=2, exclude_none=True
        )
    )

    tabel = utils.naar_tabel(woningwaardering_resultaat)

    print(tabel)