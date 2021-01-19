import pandas

excel_path = "/Users/pablo/"
dataframe = pandas.read_excel(excel_path, sheet_name='Dataset')

metadata_dataframe = dataframe.iloc[3:16, 0:3]

metadata_dataframe = metadata_dataframe.rename(index=metadata_dataframe.iloc[:, 0], columns=metadata_dataframe.iloc[0,:]).iloc[1:, 1:]

print(metadata_dataframe.at['#DATASET TITLE', 'Value'])
print(metadata_dataframe.at['#PMID:', 'Value'])