## Python MIAPPE APIs

A python CLI tool/library to manage and validate metadata that conforms to the [MIAPPE](https://www.miappe.org/)
format. MIAPPE APIs work with metadata stored as xlsx file, similar to this
[MIAPPE example](https://github.com/MIAPPE/MIAPPE/blob/master/MIAPPE_Checklist-Data-Model-v1.1/MIAPPE_templates/MIAPPEv1.1_training_spreadsheet.xlsx)
(you may need to download the xlsx sheet as github does not support viewing xlsx files). 

### To install miappe: 
```commandline
pip install miappe-api
```

### To export MIAPPE metadata schema as Json schema:
```commandline
miappe export --path <schema-path>
```

### To validate MIAPPE xlsx metadata file: 
```commandline
miappe validate <xlsx-file>
```