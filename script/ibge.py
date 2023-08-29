import pandas as pd

def agregacaoDadosIBGE(dataFrame):
    
    dataPib = pd.read_csv(f'data/ibge/pib/data.csv', encoding='utf-8', sep=';')
    dataPop = pd.read_csv(f'data/ibge/populacao/data.csv', encoding='utf-8', sep=';')

    dataFrame['M_PIB'] = 0
    dataFrame['M_POP'] = 0
    dataFrame['M_PIB_POP'] = 0

    for municipio in dataFrame['CO_MUNICIPIO'].unique().tolist():
        dataPibMunicipio = dataPib[dataPib['Cód.'] == municipio]
        dataPopMunicipio = dataPop[dataPop['Cód.'] == municipio]

        # Iteração pelos anos que ambos possuem dados
        for ano in (set(dataPib.columns.tolist()) & set(dataPop.columns.tolist())):
            
            if ano in['Cód.', 'Município']:
                continue
            
            pib = float(str(dataPibMunicipio[str(ano)].values[0]).replace(',', '.'))
            pop = float(str(dataPopMunicipio[str(ano)].values[0]).replace(',', '.'))
            dataFrame.loc[(dataFrame['CO_MUNICIPIO'] == municipio) & (dataFrame['ANO'] == ano), 'M_PIB'] = pib
            dataFrame.loc[(dataFrame['CO_MUNICIPIO'] == municipio) & (dataFrame['ANO'] == ano), 'M_POP'] = pop
            dataFrame.loc[(dataFrame['CO_MUNICIPIO'] == municipio) & (dataFrame['ANO'] == ano), 'M_PIB_POP'] = float(str(dataPibMunicipio[str(ano)].values[0]).replace(',', '.'))/float(str(dataPopMunicipio[str(ano)].values[0]).replace(',', '.'))

    return dataFrame
    