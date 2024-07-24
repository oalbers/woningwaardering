from decimal import Decimal
import warnings

from loguru import logger


from woningwaardering.stelsels import utils
from woningwaardering.stelsels.stelselgroepversie import Stelselgroepversie
from woningwaardering.stelsels.zelfstandige_woonruimten.utils import (
    classificeer_ruimte,
)
from woningwaardering.vera.bvg.generated import (
    EenhedenEenheid,
    WoningwaarderingResultatenWoningwaardering,
    WoningwaarderingResultatenWoningwaarderingCriterium,
    WoningwaarderingResultatenWoningwaarderingCriteriumGroep,
    WoningwaarderingResultatenWoningwaarderingGroep,
    WoningwaarderingResultatenWoningwaarderingResultaat,
)
from woningwaardering.vera.referentiedata import (
    Eenheidklimaatbeheersingsoort,
    Ruimtesoort,
    Ruimtedetailsoort,
    Woningwaarderingstelsel,
    Woningwaarderingstelselgroep,
    Bouwkundigelementdetailsoort,
)
from woningwaardering.vera.utils import heeft_bouwkundig_element


class VerwarmingJan2024(Stelselgroepversie):
    def bereken(
        self,
        eenheid: EenhedenEenheid,
        woningwaardering_resultaat: (
            WoningwaarderingResultatenWoningwaarderingResultaat | None
        ) = None,
    ) -> WoningwaarderingResultatenWoningwaarderingGroep:
        woningwaardering_groep = WoningwaarderingResultatenWoningwaarderingGroep(
            criteriumGroep=WoningwaarderingResultatenWoningwaarderingCriteriumGroep(
                stelsel=Woningwaarderingstelsel.zelfstandige_woonruimten.value,
                stelselgroep=Woningwaarderingstelselgroep.verwarming.value,
            )
        )

        klimaatbeheersing_code = next(
            (
                soort.code
                for soort in eenheid.klimaatbeheersing or []
                if soort.code
                in [
                    Eenheidklimaatbeheersingsoort.individueel.code,
                    Eenheidklimaatbeheersingsoort.collectief.code,
                ]
            ),
            None,
        )

        if klimaatbeheersing_code is None:
            warnings.warn(
                f"Geen klimaatbeheersing van het soort {Eenheidklimaatbeheersingsoort.individueel.naam} of {Eenheidklimaatbeheersingsoort.collectief.naam} is gevonden."
            )
            return woningwaardering_groep

        punten_per_ruimte = VerwarmingJan2024.punten_per_ruimte(klimaatbeheersing_code)

        if punten_per_ruimte is None:
            warnings.warn(
                f"Geen punten per verwarmd ruimte voor klimaatbeheersing van het soort {klimaatbeheersing_code} gevonden."
            )
            return woningwaardering_groep

        logger.debug(
            f"Punten per verwarmd vertrek: {punten_per_ruimte[Ruimtesoort.vertrek.code]}"
        )
        logger.debug(
            f"Punten per verwarmd overige ruimte: {punten_per_ruimte[Ruimtesoort.overige_ruimten.code]}"
        )

        woningwaardering_groep.woningwaarderingen = []
        totaal_punten_overige_ruimten = Decimal("0")

        for ruimte in eenheid.ruimten or []:
            if ruimte.detail_soort is None:
                error_msg = f"ruimte {ruimte.id} heeft geen detailsoort"
                raise TypeError(error_msg)

            ruimtesoort = classificeer_ruimte(ruimte)

            if ruimtesoort is None:
                continue

            if not (
                ruimtesoort.code
                in [Ruimtesoort.overige_ruimten.code, Ruimtesoort.vertrek.code]
                and ruimte.verwarmd
            ):
                logger.debug(
                    f"{ruimte.detail_soort.naam} {ruimte.detail_soort.code} komt niet in aanmerking voor een puntenwaardering onder {Woningwaarderingstelselgroep.verwarming.naam}"
                )
                continue

            woningwaardering = WoningwaarderingResultatenWoningwaardering()

            woningwaardering.criterium = (
                WoningwaarderingResultatenWoningwaarderingCriterium(
                    naam=ruimte.naam,
                )
            )

            punten = Decimal(str(punten_per_ruimte[ruimtesoort.code]))

            if ruimtesoort == Ruimtesoort.overige_ruimten:
                if totaal_punten_overige_ruimten >= Decimal("4.0"):
                    logger.debug(
                        f"De overige ruimten hebben bij elkaar {totaal_punten_overige_ruimten} punten behaald: {ruimte.id} {ruimte.naam} wordt niet meegeteld voor Verwarming."
                    )
                    continue

                # Als de punten de maximum van 4.0 overschrijden, dan wordt het aantal punten dat nog mag worden gegeven voor de ruimte aangepast
                if (totaal_punten_overige_ruimten + punten) >= Decimal("4.0"):
                    logger.debug(
                        f"De maximum punten voor {Ruimtesoort.overige_ruimten.naam} zijn behaald: punten voor {ruimte.id} {ruimte.naam} worden gecorrigeerd."
                    )
                    punten = Decimal("4.0") - totaal_punten_overige_ruimten

                totaal_punten_overige_ruimten += punten
                logger.debug(
                    f"Ruimte {ruimte.id} {ruimte.naam} telt als verwarmde {Ruimtesoort.overige_ruimten.naam} en krijgt {punten} punten."
                )

            else:
                logger.debug(
                    f"Ruimte {ruimte.id} {ruimte.naam} telt als verwarmd {Ruimtesoort.vertrek.naam} en krijgt {punten} punten."
                )

            woningwaardering_groep.woningwaarderingen.append(
                WoningwaarderingResultatenWoningwaardering(
                    criterium=WoningwaarderingResultatenWoningwaarderingCriterium(
                        naam=ruimte.naam,
                    ),
                    punten=punten,
                )
            )

            if (
                ruimte.detail_soort.code
                == Ruimtedetailsoort.woonkamer_en_of_keuken.code
                or ruimte.detail_soort.code
                in [
                    Ruimtedetailsoort.woonkamer.code,
                    Ruimtedetailsoort.woon_en_of_slaapkamer.code,
                    Ruimtedetailsoort.slaapkamer.code,
                ]
                and heeft_bouwkundig_element(
                    ruimte, Bouwkundigelementdetailsoort.aanrecht
                )
            ):
                woningwaardering_groep.woningwaarderingen.append(
                    WoningwaarderingResultatenWoningwaardering(
                        criterium=WoningwaarderingResultatenWoningwaarderingCriterium(
                            naam=f"Open keuken in {ruimte.naam}",
                        ),
                        punten=punten,
                    )
                )

        punten = Decimal(
            sum(
                Decimal(str(woningwaardering.punten))
                for woningwaardering in woningwaardering_groep.woningwaarderingen or []
                if woningwaardering.punten is not None
            )
        )

        woningwaardering_groep.punten = float(punten)
        return woningwaardering_groep

    @staticmethod
    def punten_per_ruimte(
        klimaatbeheersing_code: str,
    ) -> dict[str, float] | None:
        punten_mapping: dict[str, dict[str, float]] = {
            Eenheidklimaatbeheersingsoort.individueel.code: {
                Ruimtesoort.vertrek.code: 2,
                Ruimtesoort.overige_ruimten.code: 1,
            },
            Eenheidklimaatbeheersingsoort.collectief.code: {
                Ruimtesoort.vertrek.code: 1.5,
                Ruimtesoort.overige_ruimten.code: 0.75,
            },
        }

        return punten_mapping[klimaatbeheersing_code]


if __name__ == "__main__":  # pragma: no cover
    logger.enable("woningwaardering")

    verwarmingJan2024 = VerwarmingJan2024()
    with open(
        "tests/data/zelfstandige_woonruimten/input/77795000000.json",
        "r+",
    ) as file:
        eenheid = EenhedenEenheid.model_validate_json(file.read())

        woningwaardering_resultaat = verwarmingJan2024.bereken(eenheid)

        print(
            woningwaardering_resultaat.model_dump_json(
                by_alias=True, indent=2, exclude_none=True
            )
        )

        tabel = utils.naar_tabel(woningwaardering_resultaat)

        print(tabel)
