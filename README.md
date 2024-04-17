# Woningwaardering

⌛️ **Work in Progress**

Het Microservices team van Woonstad Rotterdam is in Q1 2024 begonnen met het ontwikkelen met een open-source Python-package waarmee het mogelijk zal zijn om het puntensysteeem van het [woningwaarderingsstelsel](https://aedes.nl/huurbeleid-en-betaalbaarheid/woningwaarderingsstelsel-wws) toe te passen. We gaan hierbij zo veel mogelijk uit van de [VERA-standaard](https://www.coraveraonline.nl/index.php/VERA-standaard) van de corporatiesector. Het doel is om tot een completere woningwaarderingsstelsel-berekening te komen dan die nu beschikbaar zijn via tools zoals bijvoorbeeld die van de [huurcommissie](https://www.huurcommissie.nl/huurders/sociale-huurwoning/maximale-huurprijs-berekenen).

Voor vragen kunt u contact opnemen met de Product Owner van Team Microservices [Wouter Kolbeek](mailto:wouter.kolbeek@woonstadrotterdam.nl) of één van de maintainers van deze repo.

## Inhoudsopgave

1. [Opzet woningwaardering-package](#2-opzet-woningwaardering-package)
2. [Contributing](#3-contributing)
3. [Datamodel uitbreidingen](#4-datamodel-uitbreidingen)
4. [Stelselgroep implementaties, afwijkingen en interpetaties](#5-stelselgroep-implementaties-afwijkingen-en-interpetaties)

## 1. Opzet woningwaardering-package

### Beleidsboek Huurcommissie

Voor het berekenen van een woningwaardering worden de [beleidsboeken van de Nederlandse Huurcommissie](https://www.huurcommissie.nl/huurcommissie-helpt/beleidsboeken) voor de waarderingstelsels voor zelfstandige en onzelfstandige woningen gevolgd.
De beleidsboeken van de Huurcommissie Nederland volgen Nederlandse wet- en regelgeving zoals beschreven in [Artikel 14 van het "Besluit huurprijzen woonruimte"](https://wetten.overheid.nl/BWBR0003237/2024-01-01#Artikel14).

Om berekeningen te maken met betrekking tot een woningwaardering wordt het gepubliceerde beleid vertaald naar Python-code.
Een woningwaardering wordt gemaakt op basis van woningelementen.
De stelselgroepen waarop gescoord wordt, zijn vastgelegd in het [woningwaarderingstelselgroep](https://www.coraveraonline.nl/index.php/Referentiedata:WONINGWAARDERINGSTELSELGROEP) op www.coraveraonline.nl.
Deze worden aangehouden in de opzet van de `woningwaardering`-package.
Voor elke stelselgroep wordt een apart Python-object gemaakt met een naam die overeenkomt met [woningwaarderingstelselgroep](https://www.coraveraonline.nl/index.php/Referentiedata:WONINGWAARDERINGSTELSELGROEP).

De woningwaardering package volgt de [beleidsboeken van de Nederlandse Huurcommissie](https://www.huurcommissie.nl/huurcommissie-helpt/beleidsboeken) en daarmee de nederlandse wet en regelgeving m.b.t. het waarderen van woningen. Tijdens de ontwikkeling van deze package komt het voor dat we inconsistenties in de beleidsboeken vinden of dat er ruimte is voor interpetatie. Daarnaast kan voorkomen dat dat de VERA modellen, met eventuele uitbreidingen, niet toereikend zijn om de stelselgroep voglens eht beleidsboek tot op de letter naukerig te implementeren. In [implementatietoelichting-beleidsboeken](docs/implementatietoelichting-beleidsboeken) onderbouwen wij hoe elk stelselgroep is geïmplementeerd en welke keuzes daarin zijn gemaakt.

Een stelselgroep-object zal een nieuwe versie krijgen wanneer nieuw gepubliceerde wet- en regelgeving, die is opgenomen in de [beleidsboeken van de Nederlandse Huurcommissie](https://www.huurcommissie.nl/huurcommissie-helpt/beleidsboeken), verschilt van de huidige berekening voor dat stelselgroep.

### Repository-structuur

De repository-structuur is ingedeeld volgens de [referentiedata van stelselgroepen van de VERA-standaard](https://www.coraveraonline.nl/index.php/Referentiedata:WONINGWAARDERINGSTELSELGROEP); eerst de stelsels (bijvoorbeeld _zelfstandig_, _onzelfstandig_) en vervolgens de stelselgroepen (bijvoorbeeld _Energieprestatie_, _Wasgelegenheid_).
In de folders van de stelselgroepen bevindt zich de code voor het berekenen van de punten per stelselgroep.

### Design

Het design van de `woningwaardering`-package is zo gekozen dat stelselgroep-objecten en bijbehorende regels modulair zijn.
Dit houdt in dat regels in een stelselgroep-object vervangbaar en inwisselbaar zijn, met als resultaat dat op basis van de gegeven input de woningwaardering berekend wordt met de juiste set aan stelselgroep-objecten en bijbehorende regels.
Ook wanneer een wet verandert met ingang van een bepaalde datum zorgt de modulariteit ervoor dat de juiste regels worden gebruikt voor de stelselgroep.
De `woningwaardering`-package selecteert op basis van een peildatum de juiste set aan regels die volgens de Nederlandse wet gelden voor de desbetreffende peildatum.
Hieronder is het modulaire principe op basis van een peildatum schematisch weergegeven voor het stelselgroep-object `OppervlakteVanVertrekken`.
Voor de duidelijkheid: Onderstaand voorbeeld is niet gebaseerd op een echte verandering in het beleidshandboek.
Het voorbeeld laat zien hoe de berekening van de `OppervlakteVanVertrekken` afhangt van de peildatum.
Op basis van de peildatum wordt voor de bovenste beleidsregel gekozen omdat die berekening geldig is voor de opgegeven peildatum.

![Voorbeeld modulaire oppervlakte van vertrekken](./docs/afbeeldingen/oppervlakte_van_vertrekken.png)

### Lookup tabellen

In lookup tabellen worden constanten en variabelen opgeslagen die nodig zijn in het berekenen van de punten voor een stelselgroep.
In de `woningwaardering` package wordt CSV gebruikt als bestandstype voor het opslaan van een lookup tabel.
De keuze is op CSV gevallen omdat lookup data soms bestaat uit meerdere datarijen waardoor dit vaak minder leesbaar wordt wanneer dit bijvoorbeeld in json of yaml wordt opgeslagen.
Voor VSCode-gebruikers is de extensie Excel Viewer van GrapeCity aan te raden.
Met behulp van deze extensie kunnen CSV-bestanden als tabel weergegeven worden in VSCode.
Hieronder is een voorbeeldtabel te zien zoals deze met Excel Viewer in VSCode wordt weergegeven.

![Excel Viewer](./docs/afbeeldingen/excel_viewer.png)

Door gebruik van CSV-bestanden, wordt het selecteren van de juiste rij of waarde doormiddel van een peildatum vergemakkelijkt.
In de `woningwaardering`-package wordt een peildatum gebruikt om de juiste waarde van bijvoorbeeld een variabele uit een tabel te selecteren.
Dit kan worden gedaan opbasis van de `Begindatum` en de `Einddatum` kolommen in een CSV-bestand.
Wanneer er geen `Begindatum` of `Einddatum` is gespecificeerd, dan is deze niet bekend.
Dit betekent niet dat er geen werkabre en geldige rij geselecteerd kan worden.
Wel zou het kunnen dat er door het ontbreken van een `Begindatum` of `Einddatum` meerdere rijen geldig zijn voor een peildatum.
In dit geval zal de `woningwaardering`-package een error geven die duidelijk maakt dat er geen geldige rij gekozen kan worden op basis van de peildatum voor het desbtreffende CSV-bestand.

## 3. Contributing

### Setup

Om de woningwaardering-package en de daarbij behorende developer dependencies te installeren, run onderstaand command:

```
git clone https://github.com/WoonstadRotterdamTemp/woningwaardering.git
cd woningwaardering
pip install -e ".[dev]"
```

### Naamgeving van classes

Voor de naamgeving van de classes in de woningwaardering module volgen we de VERA referentiedata. Deze referentiedata is gedefinieerd in de referentiedata enums, te vinden onder [woningwaardering/vera/referentiedata](woningwaardering/vera/referentiedata).

#### Stelsels

De namen voor de stelsels zijn te vinden in de `Woningwaarderingstelsel` Enum. Bijvoorbeeld: het stelsel voor zelfstandige woonruimten wordt aangeduid als `Woningwaarderingstelsel.zelfstandige_woonruimten`. De implementatie van dit `Stelsel` bevindt zich in [woningwaardering/stelsels/zelfstandige_woonruimten/zelfstandige_woonruimten.py](woningwaardering/stelsels/zelfstandige_woonruimten/zelfstandige_woonruimten.py).
De begin- en einddatum van de geldigheid van een stelsel wordt vastgelegd in de configuratie `.yml` van het betreffende stelsel. Bijvoorbeeld: voor zelfstandige woonruimten is dit [woningwaardering/stelsels/config/zelfstandige_woonruimten.yml](woningwaardering/stelsels/config/zelfstandige_woonruimten.yml)

#### Stelselgroepen

De namen voor de stelselgroepen zijn te vinden in de `Woningwaarderingstelselgroep` Enum. Bijvoorbeeld: de stelselgroep voor oppervlakte van vertrekken wordt aangeduid als `Woningwaarderingstelselgroep.oppervlakte_van_vertrekken`. De implementatie van deze `Stelselgroep` bevindt zich in [woningwaardering/stelsels/zelfstandige_woonruimten/oppervlakte_van_vertrekken/oppervlakte_van_vertrekken.py](woningwaardering/stelsels/zelfstandige_woonruimten/oppervlakte_van_vertrekken/oppervlakte_van_vertrekken.py).
De begin- en einddatum van de geldigheid van een stelselgroep wordt vastgelegd in de configuratie `.yml` van het betreffende stelsel.

#### Stelselgroepversies

De daadwerkelijke implementatie van een stelselgroep is een `Stelselgroepversie`. Voor stelselgroepversies wordt de naam van de stelselgroep gevolgd door het jaar waarin de versie van de stelselgroep in gebruik gaat. Bijvoorbeeld: de implementatie van de `Stelselgroepversie` voor oppervlakte van vertrekken die in gaat in het jaar 2024 bevindt zich in [woningwaardering/stelsels/zelfstandige_woonruimten/oppervlakte_van_vertrekken/oppervlakte_van_vertrekken_2024.py](woningwaardering/stelsels/zelfstandige_woonruimten/oppervlakte_van_vertrekken/oppervlakte_van_vertrekken_2024.py).
Omdat het lastig is met terugwerkende kracht te achterhalen in welk jaar een versie van een stelselgroep ingegaan is, gebruiken we voor de eerste versie van een stelselgroep het jaar van de implementatie van de stelselgroep in deze module. Wanneer de berekening van een stelselgroep in een bepaald jaar niet wijzigt, wordt er geen nieuwe stelselgroepversie aangemaakt. De begin- en einddatum van de geldigheid van een stelselgroepversie wordt vastgelegd in de configuratie `.yml` van het betreffende stelsel.

### Testing

Voor het testen van code wordt het [pytest framework](https://docs.pytest.org/en/8.0.x/index.html) gebruikt. Meer informatie is te vinden over het framework.
Passende tests worden altijd met de nieuw geschreven code opgeleverd.
Er zijn verschillende "test-scopes" te bedenken, zoals het testen van details en specifieke functies.
Daarnaast is het testen van een hele keten of stelselgroep-object ook vereist.
Bij het opleveren van nieuwe code moet aan beide test-scopes gedacht worden.

#### Conventies voor tests

Tests worden toegevoegd aan de `tests`-folder in de root van de repository.
Voor de structuur in de `tests`-folder wordt dezelfde structuur aangehouden als die in de `woningwaardering`-folder.
De naam van het bestand waarin de tests staan geschreven is `test_<file_name>.py`.
Elke testfunctie in file begint met `test_`, gevolgd door de naam van de functie of class die getest wordt, bijvoorbeeld `def test_<functie_naam>()` of `def test_<ClassNaam>()`.
Hierin wordt de naam de van de functie of class exact gevolgd.
Voor pytest is `test_` een indicator om de functie te herkennen als een testfunctie.

Stel dat de functionaliteiten van `woningwaardering/stelsels/zelfstandige_woonruimten/oppervlakte_van_vertrekken/oppervlakte_van_vertrekken.py` getest moeten worden, dan is het pad naar het bijbehorende testbestand `tests/stelsels/zelfstandige_woonruimten/oppervlakte_van_vertrekken/test_oppervlakte_van_vertrekken.py`.
In `test_oppervlakte_van_vertrekken.py` worden testfuncties geschreven met bijbehorende naamconventies.
Hieronder is de functienaamconventie en python code weergegeven voor het testen van een losse functie (`def losse_functie`):

```python
def test_losse_functie() -> None:
    assert losse_functie() == True
```

Als er een class getest wordt, bijvoorbeeld `OppervlakteVanVertrekken`, dan is de testfunctie opzet als volgt:

```python

def test_OppervlakteVanVertekken():
    opp_v_v = OppervlakteVanVertekken()
    assert self.opp_v_v.functie_een() == 1
    assert self.opp_v_v.functie_twee() == 2
```

#### Test modellen

Om de woningwaardeering-package zo naukeurig mogelijk te testen, zijn er eenheid modellen (in .json format) toegevoegd in `tests/data/input/...`. De modellen volgens vanzelfspreken de VERA standaard en diennen als een test inputs voor de geschreven tests. Omdat er gewerkt wordt met peildatums en de berekening van een stelselgroep per jaar kan veranderen worden de ouptut modellen per jaar opgeslagen. Zie bijvorbeeld de folder `tests/data/output/zelfstandige_woonruimten/peildatum/2024-01-01`. Deze bevat de output voor de input modellen met als peildatum 2024-01-01 of later. Op deze manier kunnen dezelfde input modellen in tests met verschillende peildata getest worden. De resulterende outputs zijn met de hand berekend om de kwaliteit van de tests te geranderen.

Om heel specifieke regelgeving uit het beleidsboek te testen, kunnen er handmatig test modellen gemaakt worden. Deze test modellen worden opgeslagen in de test folder van een stelselgroep waarvoor de specifieke regelgeving die getest wordt. Zie bijvoorbeeld `tests/stelsels/zelfstandige_woonruimten/oppervlakte_van_vertrekken/data/input/gedeelde_berging.json`: hier is een gedeelde berging gedefinieerd om een specifiek set van regels in oppervlakte_van_vertrekken.

### Datamodellen

De datamodellen in de `woningwaardering` package zijn gebaseerd op de OpenAPI-specificatie van het [VERA BVG domein](https://aedes-datastandaarden.github.io/vera-openapi/Ketenprocessen/BVG.html).

Wanneer je deze modellen wilt bijwerken, zorg er dan voor dat [Task](https://taskfile.dev/installation/) is geïnstalleerd, en dat de dev dependencies zijn geïnstalleerd:

```
pip install -e ".[dev]"
```

Vervolgens kan je met dit commando de modellen in deze repository bijwerken:

```
task genereer-vera-bvg-modellen
```

De classes voor deze modellen worden gegeneerd in `woningwaardering/vera/bvg/generated.py`

#### Datamodellen uitbreiden

Wanneer de VERA modellen niet toereikend zijn om de woningwaardering te berekenen, kan het VERA model uitgebreid worden.

Maak hiervoor altijd eerst een issue aan in de [VERA OpenApi repository](https://github.com/Aedes-datastandaarden/vera-openapi).

Maak vervolgens in de map [woningwaardering/vera/bvg/model_uitbreidingen](woningwaardering/vera/bvg/model_uitbreidingen) een class aan met de missende attributen. De naamgeving voor deze classes is: `_{classNaam}`.

Zet in de class bij het toegevoegde attribuut een comment met een link naar het issue in de VERA OpenApi repository zodat duidelijk is waar de toevoeging voor dient, en we kunnen volgen of de aanpassing is doorgevoerd in de VERA modellen.

Daarnaast neem je in de class een docstring op met uitleg over het gebruik en doel van de uitbreiding.

Bijvoorbeeld: voor het uitbreiden van de class `EenhedenRuimte` maak je een class `_EenhedenRuimte` aan:

```python
from typing import Optional

from pydantic import BaseModel, Field


class _EenhedenRuimte(BaseModel):
    # https://github.com/Aedes-datastandaarden/vera-openapi/issues/44
    gedeeld_met_aantal_eenheden: Optional[int] = Field(
        default=None, alias="gedeeldMetAantalEenheden"
    )
    """
    Het aantal eenheden waarmee deze ruimte wordt gedeeld. Deze waarde wordt gebruikt bij het berekenen van de waardering van een gedeelde ruimte met ruimtedetailsoort berging.
    """
```

De task `genereer-vera-bvg-modellen` zal de body van deze classes samenvoegen met de gelijknamige VERA class en zo de toegevoegde attributen beschikbaar maken.

### Referentiedata

Naast de referentiedata specifiek voor deze package, maken we ook gebruik van de [VERA Referentiedata](https://github.com/Aedes-datastandaarden/vera-referentiedata).

Wanneer je deze referentiedata wilt bijwerken, zorg er dan voor dat [Task](https://taskfile.dev/installation/) is geïnstalleerd

Vervolgens kan je met dit commando de referentiedata in deze repository bijwerken:

```
task genereer-vera-referentiedata
```

De referentiedata wordt gegenereerd in `woningwaardering/vera/referentiedata`

## 4. Datamodel uitbreidingen

Tijdens de ontwikkeling van deze package komen wij tegen dat de VERA modellen niet toerijkend zijn om de punten van het stelselgroep te berekenen. Daarom worden er soms uitbreidingen gemaakt op de VERA modellen wanneer nodig. In deze sectie onderbouwen en documenteren wij deze uitbreidingen. In de sectie Referentiedata wordt uitgelegd hoe het mogelijk is om nieuwe [Datamodellen uitbreiden](#datamodellen-uitbreiden) toe te voegen als contributor van dit project.

### Ruimtedetailsoort kast

Binnen het woningwaarderingsstelsel mag onder bepaalde voorwaarden de oppervlakte van vaste kasten worden opgeteld bij de ruimte waar de deur van de kast zich bevindt. Als hier bij het inmeten geen rekening mee gehouden is, kan het attribuut verbonden_ruimten gebruikt worden om de met een ruimte verbonden vaste kasten mee te laten nemen in de waardering. Hiervoor is de VERA referentiedata binnen deze repository uitgebreid met ruimtedetailsoort `Kast`, code `KAS`.

### Verbonden ruimten

Het attribuut `verbonden_ruimten` bevat de ruimten die in verbinding staan met de ruimte die het attribuut bezit. `verbonden_ruimten` wordt gebruikt bij het berekenen van de waardering van kasten en verwarming van ruimten. `verbonden_ruimten` heeft type `Optional[list[EenhedenRuimte]]` en is een uitbreiding op `EenhedenRuimte`. Voor deze uitbreiding staat een [github issue](https://github.com/Aedes-datastandaarden/vera-openapi/issues/47) open ter aanvulling op het VERA model.

### Gedeeld met aantal eenheden

Het attribuut `gedeeld_met_aantal_eenheden` geeft het aantal eenheden weer waarmee een bepaalde ruimte wordt gedeeld. Dit attribuut wordt gebruikt bij het berekenen van de waardering van een gedeelde ruimte met ruimtedetailsoort berging. `gedeeld_met_aantal_eenheden` heeft als type `Optional[int]`. Er staat een [github issue](https://github.com/Aedes-datastandaarden/vera-openapi/issues/44) open voor deze aanvulling op het VERA model.

### Bouwkundige elementen

In de beleidsboeken wordt soms op basis van een bouwkundig element dat aanwezig is in een ruimte, een uitzondering of nuance op een regel besproken. Deze kan bijvoorbeeld tot gevolg hebben dat er punten in mindering of punten extra gegeven kunnen worden. Zo ook bij de berekening van de oppervlakte van een zolder als vertrek of als overige ruimte is er informatie nodig over de trap waarmee deze zolder te bereiken is. Daartoe is het VERA model `EenhedenRuimte` uitgebreid met het attribute `bouwkundige_elementen` met als type `Optional[list[BouwkundigElementenBouwkundigElement]]`. Er staat een [github issue](https://github.com/Aedes-datastandaarden/vera-openapi/issues/46) open om `bouwkundige_elementen` standaard in het VERA model toe te voegen.

## DEPRECATED 5. Stelselgroep implementaties, afwijkingen en interpetaties

De woningwaardering package volgt de [beleidsboeken van de Nederlandse Huurcommissie](https://www.huurcommissie.nl/huurcommissie-helpt/beleidsboeken) en daarmee de nederlandse wet en regelgeving m.b.t. het waarderen van woningen. Tijdens de ontwikkeling van deze package komt het voor dat we inconsistenties in de beleidsboeken vinden of dat er ruimte is voor interpetatie. Daarnaast kan voorkomen dat dat de VERA modellen, met eventuele uitbreidingen, niet toereikend zijn om de stelselgroep voglens eht beleidsboek tot op de letter naukerig te implementeren. In [implementatietoelichting-beleidsboeken](docs/implementatietoelichting-beleidsboeken) onderbouwen wij hoe elk stelselgroep is geïmplementeerd en welke keuzes daarin zijn gemaakt.

### Oppervlakte van overige ruimten

#### 2024

##### Zolder

Wanneer een zolder als overige ruimte wordt beschouwd, dient te worden gekeken in de `bouwkundige_elementen` of de zolder bereikbaar is via een trap. Wanneer deze bereikbaar is via een vaste trap telt de volledige oppervlakte mee voor de punten berekening van Oppervlakte van Overige ruimten.
Wanneer deze wel bereikbaar is, maar niet via een vaste trap, moeten er 5 punten in mindering worden gebracht omdat de ruimte niet bereikt kan worden met een vaste trap. In onze implementatie hebben wij er voor gekozen om te checken of er dan wel een vlizotrap aanwezig is in de `bouwkundige_elementen`, aangezien dit de enige andere soort trap in het VERA model is waarmee een zolder ruimte bereikt zou kunnen worden.
Daarnaast is het onze keuze om de 5 punten in mindering te brengen door de oppervlakte van ze zolder te corrigeren. Het beleidsboek
geeft aan dat de punten in mindering gebracht moeten worden
op de punten berekend voor deze ruimte. Maar ook dat punten
pas berekend moeten worden wanneer de totale oppervlakte van een eenheid bekend is en afgerond is.
Dit is tegenstrijdig en daarom kiezen wij de implementatie die volgens ons het beleidsboek zo goed mogelijk benadert.
Let op, door de afronding komt deze berekening niet helemaal juist
uit, maar dit is de benadering waar wij nu voor kiezen.
