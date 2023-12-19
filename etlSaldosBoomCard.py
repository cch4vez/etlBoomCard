import pandas as pd
import re


df_saldos = pd.DataFrame()
df = pd.read_csv('saldosG2_758_20231118_0939.txt', delimiter='\t', header=None)

print(df.info())

merged_column = pd.concat([df[col] for col in df.columns], ignore_index=False)

df_merged = pd.DataFrame(merged_column)


df_merged = df_merged.rename(columns={0:'registro'})
df_merged['tipoRegistro'] = df_merged['registro'].apply(lambda x: str(x)[0:1])
df_merged = df_merged[df_merged['tipoRegistro']=='C'].reset_index(drop=True)
df_merged['filtroNombre'] = df_merged['registro'].apply(lambda x: str(x)[16:19])
df_merged = df_merged[df_merged['filtroNombre']!='SGN'].reset_index(drop=True)
df_merged = df_merged[df_merged['filtroNombre']!='INN'].reset_index(drop=True)

# print(df_merged)


df_saldos['tipoRegistro'] = df_merged['tipoRegistro']
df_saldos['CuentaCredencial'] = df_merged['registro'].apply(lambda x: str(x)[1:10])
df_saldos['nombreCliente'] = df_merged['registro'].apply(lambda x: str(x)[16:50])
df_saldos['FechaLimitePago'] = df_merged['registro'].apply(lambda x: str(x)[266:268]+'/'+str(x)[264:266]+'/'+str(x)[260:264])
df_saldos['PagoParaNoGenerarIntereses'] = df_merged['registro'].apply(lambda x: float(re.sub(r'^0+(?=\d)', '', str(x)[291:302])+'.'+str(x)[302:304]))
df_saldos['PagoMinimo'] = df_merged['registro'].apply(lambda x: float(re.sub(r'^0+(?=\d)', '', str(x)[330:341])+'.'+str(x)[342:344]))


print(df_saldos)

for ind in df_saldos.index:
    document = {
        'CuentaCredencial': df_saldos.at[ind, 'CuentaCredencial'],
        'FechaLimitePago': df_saldos.at[ind, 'FechaLimitePago'],
        'PagoParaNoGenerarIntereses': df_saldos.at[ind, 'PagoParaNoGenerarIntereses'],
        'PagoMinimo': df_saldos.at[ind, 'PagoMinimo']
    }
    print(document)



