# Data Transformation

Data processing subroutines to transform the source data into a more convenient data structure.

**Before**

Raw data contains multiple tales of variable width. For example:
```
T-RE              Enero  Febrero  Marzo  Abril  Mayo  Junio  Julio  Agosto  Septiembre  Octrubre  Noviembre  Deciembre   
Primeros 200 KWh  72     72       72     72     72    78     75     75      75          65        63         63 
kWh adicional     93     93       93     101    101   101    97     97      97          84        82         82
```


**After**

Cleaned data aggregates all raw tables into a single standard wide table of fix width (6 dimensions and 1 metric). Continuing with the previous example:
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
export WORKBOOK_PATH="../../kaggle/input/datasets/slothkong/electricity-tariffs-costa-rica"
export CONFIG_PATH="../../kaggle/working/cfgs.yaml"
export DATAFRAME_PATH="../../kaggle/working/electricity-tariffs-costa-rica.csv"
```

Change to the source code directory:
```bash
cd src/
```

Run the main data processing script:
```bash
python main.py
```

## Configuration

> **NOTE**: Shared example configuration INCLUDE ONLY residential tariff data.

To properly parse the contents of Excel workbooks, this tooling relies on user-provider configuration about which cell ranges are processed.
The configuration follows the schema:
```yaml
workbooks:
  - uri: <link to the source Excel workbook>
    filename: <filename of the source Excel workbook>
    worksheets:
      <name of a worksheet>:                   # Example: "CNFL 2023"
        ranges:
          <name above an specific cell range>: # Example: "T-RE" (i.e. acronym of residential tariff)
            range: <specifc cell range>        # Example: "A9:M11"
```
Checkout the [cfgs.yaml](.../../kaggle/working/cfgs.yaml) file to see the complete configuration.
