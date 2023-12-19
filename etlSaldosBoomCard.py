import pandas as pd
import re


df_saldos = pd.DataFrame()

# Se lee el archivo txt o csv
df = pd.read_csv('saldosG2_758_20231118_0939.txt', delimiter='\t', header=None)

# print(df.info())

# Se hace el merge de todas las columnas del dataframe para tener una sola
merged_column = pd.concat([df[col] for col in df.columns], ignore_index=False)

# Se crea un dataframe a partir de la Serie que se obtuvo del merge
df_merged = pd.DataFrame(merged_column)

# Se renombra la columna, para poder referenciar el mismo y poder hacer los filtros correspondiente
# Cómo solo queremos los movimientos tipo C, agregamos una columna que nos indique el tipo de movimiento df_merged['tipoRegistro'] y después quitamos del df los registros que son diferentes de "C"
# Agregamos una segunda columna para quitar los registros que en el nombre del cliente los 3 primeros caracteres sean 'SGN' e 'INN'

df_merged = df_merged.rename(columns={0:'registro'})
df_merged['tipoRegistro'] = df_merged['registro'].apply(lambda x: str(x)[0:1])
df_merged = df_merged[df_merged['tipoRegistro']=='C'].reset_index(drop=True)
df_merged['filtroNombre'] = df_merged['registro'].apply(lambda x: str(x)[16:19])
df_merged = df_merged[df_merged['filtroNombre']!='SGN'].reset_index(drop=True)
df_merged = df_merged[df_merged['filtroNombre']!='INN'].reset_index(drop=True)

# print(df_merged)

# Aplicamos las operaciones correspondientes para obtener la información conforme el archivo de mapeo que realizó José García

df_saldos['tipoRegistro'] = df_merged['tipoRegistro']
df_saldos['CuentaCredencial'] = df_merged['registro'].apply(lambda x: str(x)[1:10])
df_saldos['nombreCliente'] = df_merged['registro'].apply(lambda x: str(x)[16:50].rstrip())
df_saldos['FechaLimitePago'] = df_merged['registro'].apply(lambda x: str(x)[266:268]+'/'+str(x)[264:266]+'/'+str(x)[260:264])
df_saldos['PagoParaNoGenerarIntereses'] = df_merged['registro'].apply(lambda x: re.sub(r'^0+(?=\d)', '', str(x)[291:302])+'.'+str(x)[302:304])
df_saldos['PagoMinimo'] = df_merged['registro'].apply(lambda x: re.sub(r'^0+(?=\d)', '', str(x)[330:341])+'.'+str(x)[341:343])


print(df_saldos)

for ind in df_saldos.index:
    document = {
        'CuentaCredencial': df_saldos.at[ind, 'CuentaCredencial'],
        'FechaLimitePago': df_saldos.at[ind, 'FechaLimitePago'],
        'PagoParaNoGenerarIntereses': df_saldos.at[ind, 'PagoParaNoGenerarIntereses'],
        'PagoMinimo': df_saldos.at[ind, 'PagoMinimo']
    }
    print(document)



