"""
Script to generate resource files - split MIAPPE Check List tsv file into
different data model file - i.e. Investigation_model.tsv, Study_model.tsv, etc
"""

import yaml
import pandas as pd

METADATA_FILE = "metadata.yaml"
SOURCE_TSV_FILE = "MIAPPE_Checklist-Data-Model-v1.1.tsv"
FIELD_COL = "MIAPPE Check list"
OUTPUT_COLS = ['MIAPPE Check list', 'Definition', 'Example', 'Format',
               'Cardinality']

# Load yaml files
with open(METADATA_FILE, "r") as file:
    metadata = yaml.safe_load(file)

# Read csv file
df = pd.read_csv(SOURCE_TSV_FILE, sep='\t')

# Index dictionary
mapping = {item: df[df[FIELD_COL] == item].index.item() for item in metadata['Item']}
mapping['END'] = len(df) + 1

# Create tsv files
keys = list(mapping.keys())

sub_df = {}
for i in range(len(keys) - 1):
    print(keys[i])
    sub_df[keys[i]] = df.loc[mapping[keys[i]] + 1:mapping[keys[i + 1]] - 1, OUTPUT_COLS]
    sub_df[keys[i]].to_csv(f"{keys[i]}_model.tsv", sep='\t', index=False)
