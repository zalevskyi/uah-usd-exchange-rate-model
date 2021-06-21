# UAH-USD Exchange rate model

## Project description

Pet-project developed during [Inoxoft](https://inoxoft.com/) [Data-Focused Programming Bootcamp](https://inoxoft.com/course/data-focused-programming/) [2021](https://dou.ua/calendar/37008/)

### Project task

Model daily UAH-USD exchange rate as outcome of such factors:

- Exchange rates of Ukrainian major economic partners:
  - EUR-USD (EU is the main foreign trade partner for Ukraine)
  - PLN-USD (Poland is the main labour migration marget)
  - RUR-USD (Russia has same exporting goods: steel, wheat)
- Price indexes for key commodities:
  - Steel (one of the major Ukrainian export)
  - Wheat (one of the major Ukrainian export)
  - Oil (one of the major Ukrainian import)
- Sovereigh Bond Index:
  - MVIS EM Sovereign Bond Index (indicator of financial flow into Ukraine as Emerging market)

### Data sources

- National bank of Ukraine [Open API](https://bank.gov.ua/ua/open-data/api-dev) (description only in Ukrainian) for daily currency exchange rates: UAH-USD directly; EUR-USD, PLN-USD, RUR-USD - exchange rate recalculated based on UAH rate
- [Brent Crude Oil Prices](https://www.macrotrends.net/2480/brent-crude-oil-prices-10-year-daily-chart) csv data
- [Wheat Prices](https://www.macrotrends.net/2534/wheat-prices-historical-chart-data) csv data
- [LME Steel Rebar Prices](https://www.lme.com/Market-Data/Reports-and-data/Historical-data-for-cash-settled-futures) xlsx data
- [MVIS EM Sovereign Bond Index](https://www.mvis-indices.com/indices/bond/mvis-em-sovereign-bond-usd-eur) txt data

### Project team

In alphabetical order:

- [Elena Matusova](https://github.com/ElenaMatusova)
- [Volodymyr Zalevskyi](https://github.com/zalevskyi)

### Project structure

#### Install

Some docker files for various use cases:

- GPU Training
- CPU Training
- Deployment (intended to be as lightweight as possible)

#### Data

A home for data downloaders, athena queries etc.

#### Train

A model examples for training (and exporting models)

NOTE: it'll be useful to keep track of system resources while training, try `nvidia-smi` for GPU, `nload` for network, and `htop` for CPU.

#### Deploy

A home for deployable models and test scripts

#### Utils

General purpose scripts (running a shell inside docker quickly etc...)

##### Mac/Linux

- To build a docker image: `source utils/builddocker.sh minimal.Dockerfile`
- To run shell of a docker image: `source utils/runshell.sh`
- To run jupyter-notebook of a docker image: `source utils/runnotebook.sh`

##### Windows

using powershell

- To build a docker image: `./utils/builddocker.ps1`
- To run shell of a docker image: `./utils/runshell.ps1`
- To run jupyter-notebook of a docker image: `./utils/runnotebook.ps1`
