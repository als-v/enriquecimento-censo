from IPython.display import clear_output
from pathlib import Path 
from tqdm import tqdm
import pandas as pd
import math
import os 

import sys
sys.path.insert(1, '../')
import var as var

salarioAnos = {
    2009: 465,
    2010: 510,
    2011: 545,
    2012: 622,
    2013: 678,
    2014: 724,
    2015: 788,
    2016: 880,
    2017: 937,
    2018: 954,
    2019: 998,
    2020: 1039,
}

def lastDigitIBGE(codigo_6):
   codigo_6 = str(codigo_6)
   
   a = int(codigo_6[0])
   b = (int(codigo_6[1]) * 2) % 10 + (int(codigo_6[1]) * 2) // 10
   c = int(codigo_6[2])
   d = (int(codigo_6[3]) * 2) % 10 + (int(codigo_6[3]) * 2) // 10
   e = int(codigo_6[4])
   f = (int(codigo_6[5]) * 2) % 10 + (int(codigo_6[5]) * 2) // 10
   codigo_7 = (10 - (a + b + c + d + e + f) % 10) % 10
   
   return str(codigo_7)

def resetDic(municipios):
    
    dicAdmissao = {}
    dicDesligamento = {}
    dicSalario = {}
    dicIdadeA = {}
    dicIdadeD = {}
    dicHrContrato = {}
    dicTempoEmprego = {}
    dicSalarioMin = {}

    for municipio in municipios:
        dicAdmissao[municipio] = 0
        dicDesligamento[municipio] = 0
        dicSalario[municipio] = 0
        dicIdadeA[municipio] = 0
        dicIdadeD[municipio] = 0
        dicHrContrato[municipio] = 0
        dicTempoEmprego[municipio] = 0
        dicSalarioMin[municipio] = 0

    return dicAdmissao, dicDesligamento, dicSalario, dicIdadeA, dicIdadeD, dicHrContrato, dicTempoEmprego, dicSalarioMin

def showMessage(index):
    texto = 'Ajustes no(s) ano(s) de '

    if index == 0:
        texto += str(var.ANOS[index])
    else:

        for idx, ano in enumerate(var.ANOS[0:index+1]):
            
            if idx == index:
                texto += ' e ' + str(ano)
            else:
                if idx == 0:
                    texto += str(ano)
                else:
                    texto += ', ' + str(ano)

    texto += ' finalizado!!'

    return texto

def agregacaoDados(dataFrame, doCsv=False, doParquet=False):
    
    if (doCsv and doParquet) or (not doCsv and not doParquet):
        print('Erro: Escolha entre Csv ou Parquet.')
        return

    municipios = dataFrame['CO_MUNICIPIO'].unique().tolist()
    sep = ';'
    municipio6DigColumn = 'Municipio (6)'
    municipio7DigColumn = 'Municipio (7)'
    municipioColumn = 'Município'
    cboColumn = 'CBO 2002 Ocupação'
    cnaeColumn = 'CNAE 2.0 Subclas'
    admissaoColumn = 'Admitidos/Desligados'
    admissaoValue = 1
    desligamentoValue = 2
    salarioColumn = 'Salário Mensal'
    idadeColumn = 'Idade'
    hrContratoColumn = 'Qtd Hora Contrat'
    tempoEmpregoColumn = 'Tempo Emprego'
    grauInstrucaoColumn = 'Grau Instrução'
    salarioMinimoColumn = 'M_SALARIO_MINIMO'

    for ano in var.ANOS:

        clear_output()
        print('Agregando dados de {}.'.format(ano))

        dataFrameAno = pd.DataFrame()

        for mes in var.MESES:

            if ano != 2020:
                encode = 'latin-1'
                filename = f'CAGEDEST_{mes}{ano}'
            else:
                filename = f'CAGEDMOV{ano}{mes}'
                encode = 'utf-8'

            if doCsv: 
                dataCagedAnoMes = pd.read_csv('data/caged/{}/process_{}.csv'.format(ano, filename), sep=sep, encoding=encode, error_bad_lines=False, warn_bad_lines=False, low_memory=False)
            elif doParquet:
                dataCagedAnoMes = pd.read_parquet('data/caged/{}/process_{}.parquet'.format(ano, filename))

            dataCagedAnoMes['ANO'] = ano
            dataCagedAnoMes['MES'] = mes

            dataFrameAno = pd.concat([dataFrameAno, dataCagedAnoMes])


        for municipio in municipios:
            dataFrameMunicipio = dataFrameAno[dataFrameAno[municipio7DigColumn] == municipio]
        
            dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_ADMISSAO'] = dataFrameMunicipio[dataFrameMunicipio[admissaoColumn] == admissaoValue].count()[0]
            dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_DESLIGAMENTO'] = dataFrameMunicipio[dataFrameMunicipio[admissaoColumn] == desligamentoValue].count()[0]
            dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_DIF_ADMISSAO'] = dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_ADMISSAO'] - dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_DESLIGAMENTO']
            dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_SALDO'] = dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_DESLIGAMENTO'] - dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_ADMISSAO']
            
            # dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_SALARIO'] = dataFrameMunicipio[salarioColumn].mean()
            dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_SALARIO'] = dataFrameMunicipio[dataFrameMunicipio[admissaoColumn] == admissaoValue][salarioColumn].mean()

            dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_IDADE_ADMISSAO'] = dataFrameMunicipio[dataFrameMunicipio[admissaoColumn] == admissaoValue][idadeColumn].mean()
            dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_IDADE_DESLIGAMENTO'] = dataFrameMunicipio[dataFrameMunicipio[admissaoColumn] == desligamentoValue][idadeColumn].mean()

            # dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_HORA_CONTRATO'] = dataFrameMunicipio[hrContratoColumn].mean()
            dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_HORA_CONTRATO'] = dataFrameMunicipio[dataFrameMunicipio[admissaoColumn] == admissaoValue][hrContratoColumn].mean()

            # dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_SALARIO_MINIMO'] = dataFrameMunicipio[salarioMinimoColumn].mean()
            dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_MUNICIPIO'] == municipio), 'M_SALARIO_MINIMO'] = dataFrameMunicipio[dataFrameMunicipio[admissaoColumn] == admissaoValue][salarioMinimoColumn].mean()

    return dataFrame

def processData(municipios, doCsv=False, doParquet=False, readParquet=False):
    
    if (not doCsv and not doParquet):
        return None

    info_msg = []
    sep = ';'
    municipio6DigColumn = 'Municipio (6)'
    municipio7DigColumn = 'Municipio (7)'
    municipioColumn = 'Município'
    cboColumn = 'CBO 2002 Ocupação'
    cnaeColumn = 'CNAE 2.0 Subclas'
    admissaoColumn = 'Admitidos/Desligados'
    salarioColumn = 'Salário Mensal'
    idadeColumn = 'Idade'
    hrContratoColumn = 'Qtd Hora Contrat'
    tempoEmpregoColumn = 'Tempo Emprego'
    grauInstrucaoColumn = 'Grau Instrução'
    salarioMinimoColumn = 'M_SALARIO_MINIMO'

    columns = [municipio6DigColumn, municipio7DigColumn, cboColumn, cnaeColumn, admissaoColumn, salarioColumn, idadeColumn, hrContratoColumn, grauInstrucaoColumn, salarioMinimoColumn, tempoEmpregoColumn]

    for idx, ano in enumerate(var.ANOS):
        
        print('\nRealizando ajustes nos dados de {}.'.format(ano))

        for mes in var.MESES:

            print('Mes: {}...'.format(mes))

            if ano != 2020:
                encode = 'latin-1'
                filename = f'CAGEDEST_{mes}{ano}'
            else:
                filename = f'CAGEDMOV{ano}{mes}'
                encode = 'utf-8'
            
            if readParquet:
                dataCagedAnoMes = pd.read_parquet('data/caged/{}/{}.parquet'.format(ano, filename))
            else:
                dataCagedAnoMes = pd.read_csv('data/caged/{}/{}.txt'.format(ano, filename), sep=sep, encoding=encode)

            if ano == 2020:
                dataCagedAnoMes.rename(columns={
                    'município': 'Município',
                    'cbo2002ocupação': 'CBO 2002 Ocupação',
                    'subclasse': 'CNAE 2.0 Subclas',
                    'saldomovimentação': 'Admitidos/Desligados',
                    'valorsaláriofixo': 'Salário Mensal',
                    'idade': 'Idade',
                    'horascontratuais': 'Qtd Hora Contrat',
                    'graudeinstrução': 'Grau Instrução',
                    }, 
                inplace=True)

                dataCagedAnoMes.loc[dataCagedAnoMes[admissaoColumn] == -1, admissaoColumn] = 2
                dataCagedAnoMes[tempoEmpregoColumn] = 0


            # adequacao aos dados
            dataCagedAnoMes = dataCagedAnoMes.rename(columns={municipioColumn: municipio6DigColumn})
            dataCagedAnoMes = dataCagedAnoMes.dropna(axis=0)

            # Tratamento grau instrucao
            dataCagedAnoMes[grauInstrucaoColumn] = dataCagedAnoMes[grauInstrucaoColumn].astype(str)
            dataCagedAnoMes[grauInstrucaoColumn] = dataCagedAnoMes[grauInstrucaoColumn].apply(lambda gi: int(gi) if gi.isnumeric() else 0)
            dataCagedAnoMes = dataCagedAnoMes.loc[dataCagedAnoMes[grauInstrucaoColumn] >= 8]

            # Tratamento codigo cnae
            dataCagedAnoMes[cnaeColumn] = dataCagedAnoMes[cnaeColumn].astype(str)
            dataCagedAnoMes[cboColumn] = dataCagedAnoMes[cboColumn].astype(str)
            # dataCagedAnoMes = dataCagedAnoMes[(dataCagedAnoMes[cnaeColumn].isin(var.CNAE_CLASS)) | (dataCagedAnoMes[cboColumn].isin(cboClass))]
            dataCagedAnoMes = dataCagedAnoMes[(dataCagedAnoMes[cnaeColumn].isin(var.CNAE_CLASS))]

            # Tratamento municipio
            dataCagedAnoMes[municipio6DigColumn] = dataCagedAnoMes[municipio6DigColumn].astype(str)
            dataCagedAnoMes[municipio7DigColumn] = dataCagedAnoMes[municipio6DigColumn].apply(lambda municipio: municipio + lastDigitIBGE(municipio))
            dataCagedAnoMes[municipio6DigColumn] = dataCagedAnoMes[municipio6DigColumn].astype(int)
            dataCagedAnoMes[municipio7DigColumn] = dataCagedAnoMes[municipio7DigColumn].astype(float)
            dataCagedAnoMes = dataCagedAnoMes[dataCagedAnoMes[municipio7DigColumn].isin(municipios)]

            # Tratamento salario
            if ano == 2009:
                dataCagedAnoMes[salarioColumn] = dataCagedAnoMes[salarioColumn].apply(lambda salario: str(salario).replace(',', '.')).astype(float)
            else:
                dataCagedAnoMes[salarioColumn] = dataCagedAnoMes[salarioColumn].apply(lambda salario: salario.replace(',', '.')).astype(float)

            dataCagedAnoMes[salarioMinimoColumn] = dataCagedAnoMes[salarioColumn].apply(lambda salario: salario/salarioAnos[ano])

            # Tratamento idade
            dataCagedAnoMes[idadeColumn] = dataCagedAnoMes[idadeColumn].astype(int)

            if ano == 2020:
                dataCagedAnoMes[hrContratoColumn] = dataCagedAnoMes[hrContratoColumn].apply(lambda hr: str(hr).replace(',', '.')).astype(float)
            else:
                dataCagedAnoMes[hrContratoColumn] = dataCagedAnoMes[hrContratoColumn].astype(float)

            if ano == 2009:
                dataCagedAnoMes[tempoEmpregoColumn] = dataCagedAnoMes[tempoEmpregoColumn].apply(lambda tempo: str(tempo).replace(',', '.')).astype(float)
            elif ano != 2020:
                dataCagedAnoMes[tempoEmpregoColumn] = dataCagedAnoMes[tempoEmpregoColumn].apply(lambda tempo: tempo.replace(',', '.')).astype(float)

            if doCsv:
                dataCagedAnoMes[columns].to_csv(f'data/caged/{ano}/process_{filename}.csv', sep=sep, encoding=encode, index=False)

            if doParquet:
                dataCagedAnoMes[columns].to_parquet(f'data/caged/{ano}/process_{filename}.parquet')

        clear_output()
        print(showMessage(idx))

def get_size(file_path, unit='bytes'):
    file_size = os.path.getsize(file_path)
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def checkDifferentSizes(showAno=False, showMes=False):
    totalTxt = 0
    totalParquet = 0

    for ano in var.ANOS:

        totalAnoTxt = 0
        totalAnoParquet = 0

        if showAno or showMes:
            print('Ano: {}:'.format(ano))

        for mes in var.MESES:

            if ano != 2020:
                filename = f'CAGEDEST_{mes}{ano}'
            else:
                filename = f'CAGEDMOV{ano}{mes}'

            totalMesTxt = Path(f'data/caged/{ano}/{filename}.txt').stat().st_size
            totalAnoTxt += totalMesTxt
            totalTxt += totalMesTxt

            totalMesParquet = Path(f'data/caged/{ano}/{filename}.parquet').stat().st_size
            totalAnoParquet += totalMesParquet
            totalParquet += totalMesParquet

            if showMes:
                reducaoMes = 100 - ((totalMesParquet * 100)/ totalMesTxt)
                print(f'- Mes {mes}: Reducao de {reducaoMes:.2f}%')

                if mes == '12':
                    print('')

        reducaoAno = 100 - ((totalAnoParquet * 100)/ totalAnoTxt)
       
        if showAno:
            print('Total tamanho txt: {}'.format(convert_size(totalAnoTxt)))
            print('Total tamanho parquet: {}\n'.format(convert_size(totalAnoParquet)))
            print(f'Reducao de {reducaoAno:.2f}%\n')

    reducaoTotal = 100 - ((totalParquet * 100)/ totalTxt)
    print(f'** Reducao total de {reducaoTotal:.2f}% **')

def firstAccessData():

    # definição de variáveis
    sep = ';'
    municipioColumn = 'Município'
    cboColumn = 'CBO 2002 Ocupação'
    cnaeColumn = 'CNAE 2.0 Subclas'
    admissaoColumn = 'Admitidos/Desligados'
    salarioColumn = 'Salário Mensal'
    idadeColumn = 'Idade'
    hrContratoColumn = 'Qtd Hora Contrat'
    tempoEmpregoColumn = 'Tempo Emprego'
    grauInstrucaoColumn = 'Grau Instrução'

    columns = [municipioColumn, cboColumn, cnaeColumn, admissaoColumn, salarioColumn, idadeColumn, hrContratoColumn, grauInstrucaoColumn, tempoEmpregoColumn]

    for idx, ano in enumerate(var.ANOS):
        
        print('\nRealizando ajustes nos dados de {}.'.format(ano))

        for mes in var.MESES:

            print('Mes: {}...'.format(mes))

            if ano != 2020:
                encode = 'latin-1'
                filename = f'CAGEDEST_{mes}{ano}'
            else:
                filename = f'CAGEDMOV{ano}{mes}'
                encode = 'utf-8'

            dataCagedAnoMes = pd.read_csv('data/caged/{}/{}.txt'.format(ano, filename), sep=sep, encoding=encode, error_bad_lines=False, warn_bad_lines=False, low_memory=False)
            
            if f'original_{filename}.txt' not in os.listdir(f'data/caged/{ano}/'):
                dataCagedAnoMes.to_csv('data/caged/{}/original_{}.txt'.format(ano, filename))

            if ano == 2020:
                dataCagedAnoMes.rename(columns={
                    'município': 'Município',
                    'cbo2002ocupação': 'CBO 2002 Ocupação',
                    'subclasse': 'CNAE 2.0 Subclas',
                    'saldomovimentação': 'Admitidos/Desligados',
                    'valorsaláriofixo': 'Salário Mensal',
                    'idade': 'Idade',
                    'horascontratuais': 'Qtd Hora Contrat',
                    'graudeinstrução': 'Grau Instrução',
                    }, 
                inplace=True)

                dataCagedAnoMes[tempoEmpregoColumn] = 0

            dataCagedAnoMes[columns].to_csv('data/caged/{}/{}.txt'.format(ano, filename), sep=sep, encoding=encode, index=False)
            dataCagedAnoMes[columns].to_parquet('data/caged/{}/{}.parquet'.format(ano, filename))

        clear_output()
        print(showMessage(idx))

def generateSal(cnaeFilter = False):

    label = ''
    if cnaeFilter:
        label = '_c'

    if f'CAGED_sal{label}.parquet' not in os.listdir('./result/'):
        
        cnaeColumn = 'CNAE 2.0 Subclas'
        dataType = 'txt'

        if var.READ_PARQUET_FILES:
            dataType = 'parquet'
        else:
            dataType = 'csv'

        progress = tqdm(total=(len(var.ANOS)*len(var.MESES))+1)
        dfSalario = pd.DataFrame(columns=['ano', 'municipio', 'salario'])

        for ano in var.ANOS:
            salario = 0
            i = 0

            for mes in var.MESES:

                if ano != 2020:
                    fileName = f'{ano}/CAGEDEST_{mes}{ano}.{dataType}'
                    encode = 'latin-1'
                else:
                    fileName = f'{ano}/CAGEDMOV{ano}{mes}.{dataType}'
                    encode = 'utf-8'

                if var.READ_PARQUET_FILES:
                    data = pd.read_parquet(f'./data/caged/{fileName}')
                    dataFrameAnoMes = pd.DataFrame()
                    dataFrameAnoMes['Salário Mensal'] = data['Salário Mensal']
                    dataFrameAnoMes['Admitidos/Desligados'] = data['Admitidos/Desligados']
                    dataFrameAnoMes['Município'] = data['Município']

                    if cnaeFilter:
                        dataFrameAnoMes[cnaeColumn] = data[cnaeColumn]
                else:

                    if cnaeFilter:
                        columns = ['Admitidos/Desligados', 'Salário Mensal', 'Município', cnaeColumn]
                    else:
                        columns = ['Admitidos/Desligados', 'Salário Mensal', 'Município']
                        
                    dataFrameAnoMes = pd.read_csv(f'./data/caged/{fileName}', usecols=columns, sep=';', encoding=encode)
                
                if cnaeFilter:
                    dataFrameAnoMes[cnaeColumn] = dataFrameAnoMes[cnaeColumn].astype(str)
                    dataFrameAnoMes = dataFrameAnoMes[(dataFrameAnoMes[cnaeColumn].isin(var.CNAE_CLASS))]
            

                dataFrameAnoMes = dataFrameAnoMes.loc[dataFrameAnoMes['Admitidos/Desligados'] == 1]
                dataFrameAnoMes['Salário Mensal'] = dataFrameAnoMes['Salário Mensal'].fillna('0')

                dataFrameAnoMes['Salário Mensal'] = dataFrameAnoMes['Salário Mensal'].str.replace(',', '.')
                dataFrameAnoMes['Salário Mensal'] = dataFrameAnoMes['Salário Mensal'].astype(float)
                dataFrameAnoMes = dataFrameAnoMes.groupby(['Município']).sum().reset_index()

                for municipio in dataFrameAnoMes['Município'].unique().tolist():
                    
                    if len(dfSalario.loc[(dfSalario['ano'] == ano) & (dfSalario['municipio'] == municipio)]) == 0:
                        
                        dfSalario = pd.concat([
                            dfSalario, 
                            pd.DataFrame(
                                columns=['ano', 'municipio', 'salario'], 
                                data=[{
                                    'ano': ano,
                                    'municipio': municipio,
                                    'salario': dataFrameAnoMes[dataFrameAnoMes['Município'] == municipio]['Salário Mensal'].sum()
                                }]
                            )
                        ])

                    else:
                        dfSalario.loc[(dfSalario['ano'] == ano) & (dfSalario['municipio'] == municipio), 'salario'] = dfSalario.loc[(dfSalario['ano'] == ano) & (dfSalario['municipio'] == municipio), 'salario'].values[0] + dataFrameAnoMes.loc[(dataFrameAnoMes['Município'] == municipio), 'Salário Mensal'].sum()
                    
                progress.update(1)

        dfSalario['municipio'] = dfSalario['municipio'].apply(lambda x: str(x) + str(lastDigitIBGE(x)))
        
        dfSalario.to_parquet(f'./result/CAGED_sal{label}.parquet')
        progress.update(1)
        progress.close()
    else:

        progress = tqdm(1)
        dfSalario = pd.read_parquet(f'./result/CAGED_sal{label}.parquet')
        progress.update(1)
        progress.close()

def generateAdmission(cnaeFilter = False):
    
    label = ''
    if cnaeFilter:
        label = '_c'

    if f'CAGED_admissao{label}.parquet' not in os.listdir('./result/') and f'CAGED_desligamento{label}.parquet' not in os.listdir('./result/'):

        cnaeColumn = 'CNAE 2.0 Subclas'
        dataType = 'txt'

        if var.READ_PARQUET_FILES:
            dataType = 'parquet'
        else:
            dataType = 'csv'

        progress = tqdm(total=(len(var.ANOS)*len(var.MESES))+1)

        dfAdmitidos = pd.DataFrame(columns=['ano', 'municipio', 'admitidos'])
        dfDesligados = pd.DataFrame(columns=['ano', 'municipio', 'desligados'])

        for ano in var.ANOS:
            salario = 0
            i = 0

            for mes in var.MESES:

                if ano != 2020:
                    fileName = f'{ano}/CAGEDEST_{mes}{ano}.{dataType}'
                    encode = 'latin-1'
                    admitido = 1
                    desligado = 2
                else:
                    fileName = f'{ano}/CAGEDMOV{ano}{mes}.{dataType}'
                    encode = 'utf-8'
                    admitido = 1
                    desligado = -1

                if var.READ_PARQUET_FILES:
                    data = pd.read_parquet(f'./data/caged/{fileName}')
                    dataFrameAnoMes = pd.DataFrame()
                    dataFrameAnoMes['Admitidos/Desligados'] = data['Admitidos/Desligados']
                    dataFrameAnoMes['Município'] = data['Município']

                    if cnaeFilter:
                        dataFrameAnoMes[cnaeColumn] = data[cnaeColumn]

                else:

                    if cnaeFilter:
                        columns = ['Admitidos/Desligados', 'Salário Mensal', 'Município', cnaeColumn]
                    else:
                        columns = ['Admitidos/Desligados', 'Salário Mensal', 'Município']

                    dataFrameAnoMes = pd.read_csv(f'./data/caged/{fileName}', usecols=columns, sep=';', encoding=encode)

                if cnaeFilter:
                    dataFrameAnoMes[cnaeColumn] = dataFrameAnoMes[cnaeColumn].astype(str)
                    dataFrameAnoMes = dataFrameAnoMes[(dataFrameAnoMes[cnaeColumn].isin(var.CNAE_CLASS))]

                dataFrameAnoMesAdmitidos = dataFrameAnoMes.loc[dataFrameAnoMes['Admitidos/Desligados'] == admitido]
                dataFrameAnoMesDesligados = dataFrameAnoMes.loc[dataFrameAnoMes['Admitidos/Desligados'] == desligado]
                
                for municipio in dataFrameAnoMes['Município'].unique().tolist():

                        if len(dfAdmitidos.loc[(dfAdmitidos['ano'] == ano) & (dfAdmitidos['municipio'] == municipio)]) == 0:

                            dfAdmitidos = pd.concat([
                                dfAdmitidos, 
                                pd.DataFrame(
                                    columns=['ano', 'municipio', 'admitidos'], 
                                    data=[{
                                        'ano': ano,
                                        'municipio': municipio,
                                        'admitidos': len(dataFrameAnoMesAdmitidos[dataFrameAnoMesAdmitidos['Município'] == municipio])
                                    }]
                                )
                            ])

                        else:
                            dfAdmitidos.loc[(dfAdmitidos['ano'] == ano) & (dfAdmitidos['municipio'] == municipio), 'admitidos'] = dfAdmitidos.loc[(dfAdmitidos['ano'] == ano) & (dfAdmitidos['municipio'] == municipio), 'admitidos'].values[0] + len(dataFrameAnoMesAdmitidos.loc[(dataFrameAnoMesAdmitidos['Município'] == municipio)])
                        
                        if len(dfDesligados.loc[(dfDesligados['ano'] == ano) & (dfDesligados['municipio'] == municipio)]) == 0:

                            dfDesligados = pd.concat([
                                dfDesligados, 
                                pd.DataFrame(
                                    columns=['ano', 'municipio', 'desligados'], 
                                    data=[{
                                        'ano': ano,
                                        'municipio': municipio,
                                        'desligados': len(dataFrameAnoMesDesligados[dataFrameAnoMesDesligados['Município'] == municipio])
                                    }]
                                )
                            ])

                        else:
                            dfDesligados.loc[(dfDesligados['ano'] == ano) & (dfDesligados['municipio'] == municipio), 'desligados'] = dfDesligados.loc[(dfDesligados['ano'] == ano) & (dfDesligados['municipio'] == municipio), 'desligados'].values[0] + len(dataFrameAnoMesDesligados.loc[(dataFrameAnoMesDesligados['Município'] == municipio)])
                
                progress.update(1)
        
        dfAdmitidos['municipio'] = dfAdmitidos['municipio'].apply(lambda x: str(x) + str(lastDigitIBGE(x)))
        dfDesligados['municipio'] = dfDesligados['municipio'].apply(lambda x: str(x) + str(lastDigitIBGE(x)))
        dfAdmitidos.to_parquet(f'./result/CAGED_admissao{label}.parquet')
        dfDesligados.to_parquet(f'./result/CAGED_desligamento{label}.parquet')
        progress.update(1)
        progress.close()

    else:
        dfAdmitidos = pd.read_parquet(f'./result/CAGED_admissao{label}.parquet')
        dfDesligados = pd.read_parquet(f'./result/CAGED_desligamento{label}.parquet')

def generateSaldo(cnaeFilter):

    label = ''
    if cnaeFilter:
        label = '_c'

    if f'CAGED_saldo{label}.parquet' not in os.listdir('./result/'):
        
        dfAdmitidosTotal = pd.read_parquet(f'./result/CAGED_admissao{label}.parquet')
        dfDesligadosTotal = pd.read_parquet(f'./result/CAGED_desligamento{label}.parquet')

        progress = tqdm(total=((len(dfAdmitidosTotal['municipio'])))+1)
        dfSaldo = pd.DataFrame(columns=['ano', 'municipio', 'saldo'])

        for ano in dfAdmitidosTotal['ano'].unique():
            dataAnoAdmitidos = dfAdmitidosTotal.loc[dfAdmitidosTotal['ano'] == ano]

            for municipio in dataAnoAdmitidos['municipio'].unique():
                dataAnoDesligados = dfDesligadosTotal.loc[(dfDesligadosTotal['ano'] == ano) & (dfDesligadosTotal['municipio'] == municipio)]

                dfSaldo = pd.concat([
                    dfSaldo, 
                    pd.DataFrame(
                        columns=['ano', 'municipio', 'saldo'], 
                        data=[{
                            'ano': ano,
                            'municipio': municipio,
                            'saldo': dataAnoAdmitidos.loc[(dataAnoAdmitidos['municipio'] == municipio), 'admitidos'].values[0] - dataAnoDesligados['desligados'].values[0]
                        }]
                    )
                ])

                progress.update(1)

        dfSaldo['municipio'] = dfSaldo['municipio'].apply(lambda x: str(x) + str(lastDigitIBGE(x)))
        dfSaldo.to_parquet(f'./result/CAGED_saldo{label}.parquet')
        progress.update(1)
        progress.close()
    else:
        dfSaldo = pd.read_parquet(f'./result/CAGED_saldo{label}.parquet')
