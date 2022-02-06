import json
import pandas

# requires 
# pandas

df_excel = pandas.read_excel('excel.xlsx')
df_excel.drop(df_excel.columns[[0]], axis=1,  inplace=True)
df_excel = df_excel.reset_index()
df_excel.drop(df_excel.index[[0]],  inplace=True)

outF = open("es.json", "w")
outF.write("{\n")

columns = df_excel.columns
for row in df_excel.itertuples():
    outF.write('"' + row[2] +'"'+ ":" + '"' +  row[4] + '"' + ",\n")
        
outF.write("}\n")
