# Electricity Tariffs Costa Rica
Costa Rica's ["Authoridad Reguladora de los Servicios Publicos" (ARASEP) ](https://aresep.go.cr/electricidad/tarifas/) publishes historical records on electricity pricing.
Although of good quality, said data is somewhat hard to work with when using open-source analytics tooling:
* It is published as an Excel workbook
* Data of each distributor spreads across multiple worksheets
* Tariff data is framed within tables of variable column count (i.e. months as columns/metrics). 

This repository contains programmatic routines for converting the public workbook into a more convenient long-table data structure:

```
annio-mes  distribuidor  tipo_de_tarifa  bloque_de_tarifa  colones_por_kwh
2013-01    CAR           T-RE            Primeros 200 KWh  72
2013-01    CAR           T-RE            kWh adicional     93
...        ...           ...             ...               ...
2013-12    JASEC         T-RE            Primeros 200 KWh  61
2013-12    JASEC         T-RE            kWh adicional     74
```

The result is saved to disk in standard `.csv` format.

## Before You Begin

Install the required `python` libraries:
```bash
pip install -r requirements.txt
```

## Usage

(Optional) override the local paths for input/output files:
```bash
export WORKBOOK_PATH="./kaggle/input/datasets/slothkong/electricity-tariffs-costa-rica/Cuadro E-8 Tarifas electricas final.xlsx")
export CONFIG_PATH="./kaggle/working/cfgs.yaml"
export DATAFRAME_PATH="./kaggle/working/electricity-tariffs-costa-rica.csv"
```

Run the main data processing script:
```bash
python main.py
```

