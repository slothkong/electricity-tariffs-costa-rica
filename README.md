# Electricity Tariffs of Costa Rica
Costa Rica's ["Authoridad Reguladora de los Servicios Publicos" (ARASEP)](https://aresep.go.cr/) publishes historical records and charts on electricity pricing.
Although while said data is of relative good quality, it is somewhat hard to work with, when using open-source analytics tooling. Some of the main hurdles are:
* **Proprietary format**: Published as an Excel workbook
* **Non-standard structure**: Data from each distribution company spreads across multiple worksheets. Futhermore, tariff data is framed within tables of variable column count (i.e. months as columns/metrics)
* **Buggy and/or misleading visualization**: As of June 2026, the PowerBI visualizations embedded on the [ARASEP's website](https://aresep.go.cr/electricidad/tarifas/) does not properly reflect average tariff prices per distribution company or across years

This repository contains the tooling used to produce and maintain the ["Electricy Tariffs of Costa Rica" Kaggle Dataset](https://www.kaggle.com/datasets/slothkong/electricity-tariffs-costa-rica), which aims at addressing the aforementioned challenges by converting ARESEP's published workbook into a more convenient data structures.


**Before**

Multiple tales of variable width:

```
T-RE              Enero  Febrero  Marzo  Abril  Mayo  Junio  Julio  Agosto  Septiembre  Octrubre  Noviembre  Deciembre   
Primeros 200 KWh  72     72       72     72     72    78     75     75      75          65        63         63 
kWh adicional     93     93       93     101    101   101    97     97      97          84        82         82
```

**After**

Single standard wide table of fix width (i.e. 4 dimensions and 1 metric):
```
annio_mes  distribuidor  tipo_de_tarifa  bloque_de_tarifa  colones_por_kwh
2013-01    CAR           T-RE            Primeros 200 KWh  72
2013-01    CAR           T-RE            kWh adicional     93
...        ...           ...             ...               ...
2013-12    CAR           T-RE            Primeros 200 KWh  63
2013-12    CAR           T-RE            kWh adicional     82
```

## Usage

Install the required `python` libraries:
```bash
pip install -r requirements.txt
```

Optionally, override the local paths for input/output files:
```bash
export WORKBOOK_PATH="./kaggle/input/datasets/slothkong/electricity-tariffs-costa-rica/Cuadro E-8 Tarifas electricas final.xlsx"
export CONFIG_PATH="./kaggle/working/cfgs.yaml"
export DATAFRAME_PATH="./kaggle/working/electricity-tariffs-costa-rica.csv"
```

Run the main data processing script:
```bash
python main.py
```

## Configuration

To properly parse the contents of Excel workbooks, this tooling relias on user-provider configuration about which cell ranges are processed.
The configuration follows the schemae:
```yaml
worksheets:
  <name of a worksheet>:         # Example: "CNFL 2023"
    ranges:
      <name above an specific cell range>: # Example: "T-RE" (i.e. acronym of residential tariff)
        range: <specifc cell range>        # Example: "A9:M11"
```
Checkout the [cfgs.yaml](./kaggle/working/cfgs.yaml) file to see the complete configuration.










