# UpverterJCLPCB
Contains scripts to convert files exported from Upverter for building PCBs at JLCPCB

This python script (main.py) will massage the output so you can have the boards assembled inexpensively at JCLPCB.
The script will modify the BOM and XYRS exports from Upverter to modify them for compatibility with the JCLPCB assembly processes mapping your MPNs to LCSC part numbers. You may have to tweak a part orientation.

Usage:
    ```python -m main.py [-b <upverter bom> -B <JCLPCB bom>] [-p <upverter pickandplace> -P <JCLPCB pickandplace>]```

The files are all CSV files.
You add your part mappings to LCSC PNs with this dictionary:
  
```python
# populate this dictionary with MPN:LCSC_PNs pairs.
# If a component is not found in this dictionary, a null
# string is returned (due to the dictionary being a defaultdict).
LCSC_crossreference_dict = defaultdict(str,{
'CC0805ZKY5V6BB106':'C15850', #CAP CER 10UF 10V Y5V 0805
'CC0603KRX7R7BB104':'C14663', #CAP CER 0.1UF 16V X7R 0603
'SN74AHCT125DR':'C155176', #SN74AHCT125DR
})
```
