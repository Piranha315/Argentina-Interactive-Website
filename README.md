# Argentina Trade Atlas

An illustrated, interactive map of Argentina's economy, built for the EC 391 (International Trade) country project. The map shows where Argentina's main exports are produced, and a sourced "Civilopedia" below it covers the country profile, trade, comparative advantage, value chains, foreign investment, trade policy and a case study.

- **Live site:** https://piranha315.github.io/Argentina-Interactive-Website/
- **Also on claude.ai:** https://claude.ai/artifact/Wdapxc3nfTBc2QNLQhxMMm
- **Run it locally:** open `index.html` in a browser. It is a single self-contained file; only the fonts load from Google Fonts.

## What's on the map

- **Resources:** shale oil and gas (Vaca Muerta), lithium, soymeal and soy oil, wheat and maize, beef, wine, motor vehicles, gold and silver, Patagonian shrimp, and Tierra del Fuego electronics. Each opens a panel with the headline figure, sourced statistics and the course model it illustrates.
- **Highlights and cities:** Buenos Aires (capital), the Malvinas / Falkland Islands dispute, the sea-lane ship covering Argentina's balancing act between China and the US, and 12 cities with province census data and their role in the trade story.
- **Neighbours:** Brazil, Chile, Uruguay, Paraguay and Bolivia, with 2024 bilateral trade.
- **Navigation:** scroll or pinch to zoom, drag or two-finger swipe to move, a minimap while zoomed, a full-map mode, and keyboard controls (+ / − / arrows / 0). Below 1,180 px wide, details open in a bottom sheet over the map.

## Chapters

The chapters follow the course guidelines:

| Chapter | Topic |
|---|---|
| I | Country profile |
| II | Macroeconomy, business climate and institutions |
| III | Openness and trade patterns, including a gravity regression |
| IV | Specialization and comparative advantage (RCA, Heckscher-Ohlin, Nunn) |
| V | Position in global value chains |
| VI | Foreign direct investment |
| VII | Trade policy and major agreements |
| IX | Case study: Tierra del Fuego as an infant industry (Ch. 8) |

## Data sources

All statistics come from government or intergovernmental sources, except the Corruption Perceptions Index, which the course guidelines require.

- [World Bank, World Development Indicators](https://data.worldbank.org/country/argentina): GDP, growth, inflation, trade openness, BoP goods and services, FDI, tariffs, LPI, social indicators, urban population
- [World Bank, Worldwide Governance Indicators](https://www.worldbank.org/en/publication/worldwide-governance-indicators): six governance scores, 2025 release
- [UN Comtrade](https://comtradeplus.un.org/): exports and imports by HS chapter and partner, product lines for RCA
- [INDEC, Censo 2022 (final results)](https://redatam.indec.gob.ar/redarg/CENSOS/CPV2022/Docs/Redatam_control_de_universos.pdf): province populations
- [Banco Central de la República Argentina](https://www.bcra.gob.ar/): *Informe sobre Inversión Extranjera Directa al 31/12/2023*
- [U.S. Energy Information Administration](https://www.eia.gov/todayinenergy/): crude output, Vaca Muerta
- [U.S. Geological Survey, Mineral Commodity Summaries 2026: Lithium](https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-lithium.pdf)
- [USDA Foreign Agricultural Service](https://fas.usda.gov/): soy and beef trade
- [UNDP Human Development Report 2025](https://hdr.undp.org/)
- [OECD Economic Surveys: Argentina 2019](https://www.oecd.org/en/publications/oecd-economic-surveys-argentina-2019_0c7f002c-en/full-report/component-5)
- [World Trade Organization](https://www.wto.org/english/thewto_e/countries_e/argentina_e.htm), UN Decolonization Committee, UK Ministry of Defence, Falkland Islands Government
- Legal texts via the [Boletín Oficial](https://www.boletinoficial.gob.ar/): Ley 19.640, Decree 727/2021, Ley 27.742 (RIGI), Decree 423/2026, Ley 26.659
- [Transparency International, CPI 2025](https://www.transparency.org/en/cpi) (NGO, required by the guidelines)
- Map outlines: [Natural Earth](https://www.naturalearthdata.com/) (public domain). The painted terrain is illustrative.

### Still to collect

These are marked in red on the page. They need a manual export because the sites block automated download:

- OECD TiVA foreign value-added share and forward participation
- World Bank B-READY score
- UNCTAD non-tariff measure counts and the investment-treaty count
- INDEC provincial employment for the Tierra del Fuego test

## Methods

- **Revealed comparative advantage:** RCA = (X<sub>ik</sub> / X<sub>i</sub>) ÷ (X<sub>Wk</sub> / X<sub>W</sub>), where the world total sums 167 Comtrade reporters for 2023.
- **Gravity regression:** OLS of ln(exports to partner, 2024) on ln(partner GDP) and ln(distance between capitals), with N = 145. GDP 1.155 (s.e. 0.063), distance −1.448 (s.e. 0.223), R² 0.70.
- **Concentration:** Herfindahl index over all partner shares.
- **Distances:** great-circle distances between World Bank capital coordinates.

## Repository layout

```
index.html                 the site (generated by scripts/build.py)
src/atlas.src.html         page template: markup, styles and scripts
data/geo.json              projected map outlines (from scripts/geo.py)
data/data.json             chart series, WGI and gravity results (from scripts/prep.py)
data/data2.json            export mix, partners, import chapters (from scripts/prep2.py)
data/raw/                  raw downloads: World Bank, UN Comtrade, WGI, BCRA report text
scripts/                   data preparation and build scripts
```

## Rebuilding

Requires Python 3 and no extra packages.

```bash
./scripts/fetch_naturalearth.sh   # only needed to regenerate map outlines
python3 scripts/geo.py            # data/geo.json
python3 scripts/prep.py           # data/data.json
python3 scripts/prep2.py          # data/data2.json
python3 scripts/build.py          # index.html
```

To change text or design, edit `src/atlas.src.html` and run `python3 scripts/build.py`.

## Credits

Built for EC 391 International Trade, Boston University, Fall 2026. The fonts are IM Fell English and Alegreya Sans from Google Fonts (SIL Open Font License).
