from datetime import date

from prettytable import PrettyTable

from woningwaardering.stelsels.stelsel import Stelsel
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
    zel = ZelfstandigeWoonruimten()
    f = open(
        "./tests/data/input/zelfstandige_woonruimten/41164000002.json",
        "r+",
    )
    eenheid = EenhedenEenheid.model_validate_json(f.read())
    woningwaardering_resultaat = zel.bereken(eenheid)
    print(
        woningwaardering_resultaat.model_dump_json(
            by_alias=True, indent=2, exclude_none=True
        )
    )

    table = PrettyTable()
    table.field_names = ["Groep", "Naam", "Aantal", "Meeteenheid", "Punten"]
    table.align = "l"
    table.align["Aantal"] = "r"
    table.align["Punten"] = "r"

    for woningwaardering_groep in woningwaardering_resultaat.groepen or []:
        for woningwaardering in woningwaardering_groep.woningwaarderingen or []:
            table.add_row(
                [
                    woningwaardering_groep.criterium_groep.stelselgroep.naam,
                    woningwaardering.criterium.naam,
                    woningwaardering.aantal,
                    woningwaardering.criterium.meeteenheid.naam,
                    woningwaardering.punten or "",
                ]
            )
        table.add_row(
            [
                woningwaardering_groep.criterium_groep.stelselgroep.naam,
                "Subtotaal",
                sum(
                    [
                        woningwaardering.aantal
                        for woningwaardering in woningwaardering_groep.woningwaarderingen
                        or []
                        if woningwaardering.aantal is not None
                    ]
                ),
                "",
                woningwaardering_groep.punten,
            ],
            divider=True,
        )
    table.add_row(
        [
            woningwaardering_resultaat.stelsel.naam,
            "Totaal",
            "",
            "",
            woningwaardering_resultaat.punten,
        ],
        divider=True,
    )

    print(table)
