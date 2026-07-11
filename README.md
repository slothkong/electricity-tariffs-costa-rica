# Electricity Tariffs Costa Rica

[ARASEP](https://en.wikipedia.org/wiki/Autoridad_Reguladora_de_Servicios_P%C3%BAblicos), the regularity institution of Costa Rica's energy prices,  publishes historical records and charts on the country's electricity pricing. Although said data is of relative good quality, it is also somewhat difficult to work with when using open-source analytics tooling:

- **Proprietary format:** Published as an Excel workbook
- **Non-standard structure:** Data from each distribution company spreads across multiple worksheets. Furthermore, tariff data is framed within tables of variable column count (i.e. months as columns/metrics)
- **Buggy and region-locked visualization:** As of June 2026, the PowerBI visualizations embedded on the [ARASEP's website](https://aresep.go.cr/electricidad/tarifas/) does not properly reflect average tariff prices per distribution company or across years. The site appears to be also reachable only form national IP addresses.


This repository includes tooling is used to create/update/visualize the ["Electricity Tariffs Costa Rica" Kaggle Dataset](https://www.kaggle.com/datasets/slothkong/electricity-tariffs-costa-rica), in an attempt to address the aforementioned challenges.

## Features 

Enables conversion of ARESEP's published worksheets into a more convenient data structures, essentially going from multiple tales of variable width:

```
T-RE              Enero  Febrero  Marzo  Abril  Mayo  Junio  Julio  Agosto  Septiembre  Octrubre  Noviembre  Deciembre   
Primeros 200 KWh  72     72       72     72     72    78     75     75      75          65        63         63 
kWh adicional     93     93       93     101    101   101    97     97      97          84        82         82
```

to single standard wide table of fix width (i.e. 6 dimensions and 1 metric):
```
annio_mes  annio  mes  distribuidor  tipo_de_tarifa  bloque_de_tarifa  colones_por_unidad_de_cobro
2013-01    2013   01   CAR           T-RE            Primeros 200 KWh  72
2013-01    2013   01   CAR           T-RE            kWh adicional     93
...        ...    ...  ...           ...             ...               ...
2013-12    2013   12   CAR           T-RE            Primeros 200 KWh  63
2013-12    2013   12   CAR           T-RE            kWh adicional     82
```

## Usage

Install the required `python` libraries:
```bash
pip install -r requirements.txt
```

Optionally, override the local paths for input/output files:
```bash
export WORKBOOK_PATH="./kaggle/input/datasets/slothkong/electricity-tariffs-costa-rica"
export CONFIG_PATH="./kaggle/working/cfgs.yaml"
export DATAFRAME_PATH="./kaggle/working/electricity-tariffs-costa-rica.csv"
```

Run the main data processing script:
```bash
python main.py
```

## Configuration

> **NOTE**: As of version `0.0.1`, configured cell ranges INCLUDE ONLY residential tariff data.

To properly parse the contents of Excel workbooks, this tooling relies on user-provider configuration about which cell ranges are processed.
The configuration follows the schema:
```yaml
workbooks:
  - uri: https://aresep-my.sharepoint.com/:x:/g/personal/multimedia_aresep_go_cr/ET6L4k-QyphAgLpEwSYeNegBbLvOGM7mF0n2vZxId_SGeQ?e=YGhFZr&download=1
    filename: Cuadro E-8 Tarifas electricas final.xlsx
    worksheets:
      <name of a worksheet>:                   # Example: "CNFL 2023"
        ranges:
          <name above an specific cell range>: # Example: "T-RE" (i.e. acronym of residential tariff)
            range: <specifc cell range>        # Example: "A9:M11"
```
Checkout the [cfgs.yaml](./kaggle/working/cfgs.yaml) file to see the complete configuration.










