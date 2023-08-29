import pandas as pd
import sys
sys.path.insert(1, '../')
import var as var

def agregacaoDadosInep():
    dataFrame = pd.DataFrame()

    for ano in var.ANOS:
        dataAno = pd.read_csv(
            'data/censo/{}/MICRODADOS_CADASTRO_CURSOS_{}.CSV'.format(str(ano), str(ano)), 
            sep=';', 
            encoding='latin-1', 
        )

        dataFrame = pd.concat([dataFrame, dataAno])

    print('Total de Cursos: {}'.format(dataFrame.shape[0]))
    print('Total de IES: {}'.format(len(dataFrame['CO_IES'].unique().tolist())))

    return dataFrame

def calculoQuantidadeDocentes(dataFrame, iesList):
    dataFrame['PC_DOC_ALUNO'] = 0

    for ano in dataFrame['NU_ANO_CENSO'].unique().tolist():
        dataAno = dataFrame[dataFrame['NU_ANO_CENSO'] == ano]
        dataAno = dataAno[dataAno['CO_IES'].isin(iesList)]

        dataAnoIes = pd.read_csv(
            'data/censo/{}/MICRODADOS_CADASTRO_IES_{}.CSV'.format(str(ano), str(ano)), 
            sep=';', 
            encoding='latin-1', 
        )

        dataAnoIes = dataAnoIes[dataAnoIes['CO_IES'].isin(iesList)]

        if ano == 2009:
            dataAnoIes.rename(columns={
                'QT_DOCENTE_TOTAL': 'QT_DOC_TOTAL',
                'QT_DOCENTE_EXE': 'QT_DOC_EXE',
                'DOC_EX_GRAD': 'QT_DOC_EX_GRAD',
                'DOC_EX_MEST': 'QT_DOC_EX_MEST',
                'DOC_EX_DOUT': 'QT_DOC_EX_DOUT',
            }, 
            inplace=True)

        for ies in dataAno['CO_IES'].unique().tolist():
            
            dataIes = dataAno[dataAno['CO_IES'] == ies]

            matriculados = dataIes['QT_MAT'].sum()
            docentes = dataAnoIes.loc[dataAnoIes['CO_IES'] == ies, 'QT_DOC_EXE'].sum()
            conta = 0

            if docentes != 0:
                conta = matriculados / docentes

            dataFrame.loc[(dataFrame['NU_ANO_CENSO'] == ano) & (dataFrame['CO_IES'] == ies), 'PC_DOC_ALUNO'] = conta
            dataFrame.loc[(dataFrame['NU_ANO_CENSO'] == ano) & (dataFrame['CO_IES'] == ies), 'IES_TOT_ALUNO_DEFICIENTE'] = dataIes['QT_ALUNO_DEFICIENTE'].sum()

    return dataFrame

def filtroDadosInep(dataFrame):

    dataComputacao = pd.DataFrame()

    for curso in var.CURSOS:

        # restringir apenas aos cursos de computação
        dataCurso = dataFrame.loc[dataFrame['NO_CINE_ROTULO'] == curso]

        # restringir apenas aos cursos de bacharelado e licenciatura
        # dataCurso = dataCurso.loc[(dataCurso['TP_GRAU_ACADEMICO'] == 1) | (dataCurso['TP_GRAU_ACADEMICO'] == 2) | (dataCurso['TP_GRAU_ACADEMICO'] == 4)]
        dataCurso = dataCurso.loc[(dataCurso['TP_GRAU_ACADEMICO'] == 1) | (dataCurso['TP_GRAU_ACADEMICO'] == 2) | (dataCurso['TP_GRAU_ACADEMICO'] == 3) | (dataCurso['TP_GRAU_ACADEMICO'] == 4)]

        # restringir apenas aos cursos presenciais
        dataCurso = dataCurso.loc[dataCurso['TP_MODALIDADE_ENSINO'] == 1]

        print(f'Curso: {curso}: {len(dataCurso)} ocorrências\n')

        dataComputacao = pd.concat([dataComputacao, dataCurso])

    return dataComputacao

def iesFiltradas(dataFrame):

    dataComputacao = pd.DataFrame()

    for curso in var.CURSOS:

        # restringir apenas aos cursos de computação
        dataCurso = dataFrame.loc[dataFrame['NO_CINE_ROTULO'] == curso]

        # restringir apenas aos cursos de bacharelado e licenciatura
        dataCurso = dataCurso.loc[(dataCurso['TP_GRAU_ACADEMICO'] == 1) | (dataCurso['TP_GRAU_ACADEMICO'] == 2) | (dataCurso['TP_GRAU_ACADEMICO'] == 4)]

        # restringir apenas aos cursos presenciais
        dataCurso = dataCurso.loc[dataCurso['TP_MODALIDADE_ENSINO'] == 1]

        dataComputacao = pd.concat([dataComputacao, dataCurso])

    return dataComputacao['CO_IES'].unique().tolist()

def criacaoDadosCurso(dataFrame):
    data = []

    for ano in var.ANOS:

        dataAno = dataFrame.loc[dataFrame['NU_ANO_CENSO'] == ano]
        print('Ano de {}, total de Cursos: {}'.format(ano, dataAno.shape[0]))

        for ies in dataAno['CO_IES'].unique().tolist():
            dataIes = dataAno[dataAno['CO_IES'] == ies]

            for coMunicipio in dataIes['CO_MUNICIPIO'].unique().tolist():
                dataMunicipio = dataIes[dataIes['CO_MUNICIPIO'] == coMunicipio]

                if len(dataMunicipio) == 0:
                    continue

                nomeMunicipio = dataMunicipio['NO_MUNICIPIO'].unique().tolist()[0]

                for value in dataMunicipio['NO_CINE_ROTULO'].unique().tolist():
                    dataNO_CINE = dataMunicipio[dataMunicipio['NO_CINE_ROTULO'] == value]

                    if len(dataNO_CINE) != 1:
                        break

                    data.append([
                        ano,
                        ies,
                        coMunicipio,
                        nomeMunicipio,
                        value,
                        dataNO_CINE['QT_MAT'].sum(),
                        dataNO_CINE['QT_ING'].sum(),
                        dataNO_CINE['QT_CONC'].sum(),
                        dataNO_CINE['QT_VG_NOVA'].sum(),
                        dataNO_CINE['QT_INSC_VG_NOVA'].sum(),
                        dataNO_CINE['SG_UF'].values[0],
                        dataNO_CINE['QT_VG_TOTAL'].sum(),
                        dataNO_CINE['TP_REDE'].values[0],
                        dataNO_CINE['QT_ALUNO_DEFICIENTE'].values[0],
                        dataNO_CINE['QT_SIT_TRANCADA'].values[0],
                        dataNO_CINE['QT_SIT_TRANSFERIDO'].values[0],
                        dataNO_CINE['QT_APOIO_SOCIAL'].values[0],
                        dataNO_CINE['NO_UF'].values[0],
                        dataNO_CINE['CO_UF'].values[0],
                        dataNO_CINE['QT_SIT_FALECIDO'].values[0],
                        dataNO_CINE['QT_INSCRITO_TOTAL'].sum(),
                        dataNO_CINE['PC_DOC_ALUNO'].values[0],
                        dataNO_CINE['IES_TOT_ALUNO_DEFICIENTE'].values[0],
                    ])

    return pd.DataFrame(data, columns=['ANO', 'CO_IES', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'C_NO_CINE_ROTULO', 'C_QT_MAT', 'C_QT_ING', 'C_QT_CONC', 'C_QT_VG_NOVA', 'C_QT_INSC_VG_NOVA', 'C_SG_UF', 'C_QT_VG_TOTAL', 'C_TP_REDE', 'C_QT_ALUNO_DEFICIENTE', 'C_QT_SIT_TRANCADA', 'C_QT_SIT_TRANSFERIDO', 'C_QT_APOIO_SOCIAL', 'C_NO_UF', 'C_CO_UF', 'C_QT_SIT_FALECIDO', 'QT_INSCRITO_TOTAL', 'PC_DOC_ALUNO', 'IES_TOT_ALUNO_DEFICIENTE'])

def adicionaDadosIes(dataCurso):

    for ano in dataCurso['ANO'].unique().tolist():
        dataAno = dataCurso[dataCurso['ANO'] == ano]

        dataAnoIes = pd.read_csv(
            'data/censo/{}/MICRODADOS_CADASTRO_IES_{}.CSV'.format(str(ano), str(ano)), 
            sep=';', 
            encoding='latin-1', 
        )

        print(f'Ano: {ano}, qtd ies: {len(dataAnoIes)}.\n')

        for ies in dataAno['CO_IES'].unique().tolist():
            dataIesAno = dataAnoIes.loc[dataAnoIes['CO_IES'] == ies]

            if ano == 2009:
                dataIesAno.rename(columns={
                    'QT_DOCENTE_TOTAL': 'QT_DOC_TOTAL',
                    'QT_DOCENTE_EXE': 'QT_DOC_EXE',
                    'DOC_EX_GRAD': 'QT_DOC_EX_GRAD',
                    'DOC_EX_MEST': 'QT_DOC_EX_MEST',
                    'DOC_EX_DOUT': 'QT_DOC_EX_DOUT',
                    }, 
                inplace=True)

            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_TEC_TOTAL'] = dataIesAno['QT_TEC_TOTAL'].values[0]
            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_TEC_SUPERIOR_TOTAL'] = dataIesAno['QT_TEC_SUPERIOR_MASC'].values[0] + dataIesAno['QT_TEC_SUPERIOR_FEM'].values[0]
            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_TEC_MESTRADO_TOTAL'] = dataIesAno['QT_TEC_MESTRADO_MASC'].values[0] + dataIesAno['QT_TEC_MESTRADO_FEM'].values[0]
            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_TEC_DOUTORADO_TOTAL'] = dataIesAno['QT_TEC_DOUTORADO_MASC'].values[0] + dataIesAno['QT_TEC_DOUTORADO_FEM'].values[0]
            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_LIVRO_ELETRONICO'] = dataIesAno['QT_LIVRO_ELETRONICO'].values[0]

            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_DOC_TOTAL'] = dataIesAno['QT_DOC_TOTAL'].values[0]
            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_DOC_EXE'] = dataIesAno['QT_DOC_EXE'].values[0]
            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_DOC_EX_GRAD'] = dataIesAno['QT_DOC_EX_GRAD'].values[0]
            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_DOC_EX_MEST'] = dataIesAno['QT_DOC_EX_MEST'].values[0]
            dataCurso.loc[(dataCurso['ANO'] == ano) & (dataCurso['CO_IES'] == ies), 'IES_QT_DOC_EX_DOUT'] = dataIesAno['QT_DOC_EX_DOUT'].values[0]

    return dataCurso

def calculoEvasao(dataFrame):
    dataFrame['C_EVASAO'] = 999999

    for ies in dataFrame['CO_IES'].unique().tolist():
        dataIes = dataFrame.loc[dataFrame['CO_IES'] == ies]


        for coMunicipio in dataIes['CO_MUNICIPIO'].unique().tolist():
            dataMunicipio = dataIes.loc[dataIes['CO_MUNICIPIO'] == coMunicipio]

            for nomeCurso in dataMunicipio['C_NO_CINE_ROTULO'].unique().tolist():
                dataCurso = dataMunicipio.loc[dataMunicipio['C_NO_CINE_ROTULO'] == nomeCurso]
                dataCurso = dataCurso.sort_values(by=['ANO'], ascending=False)
                
                for idx, ano in enumerate(dataCurso['ANO'].unique().tolist()):

                    if len(dataCurso['ANO'].unique().tolist()) - 1 == idx:
                        break

                    if ano == 2009:
                        break

                    if dataCurso['ANO'].unique().tolist()[idx+1] != ano - 1:
                        break
                    
                    matriculados = dataCurso.loc[dataCurso['ANO'] == ano]['C_QT_MAT'].values[0]
                    ingressantes = dataCurso.loc[dataCurso['ANO'] == ano]['C_QT_ING'].values[0]
                    matriculadosAnterior = dataCurso.loc[dataCurso['ANO'] == ano - 1]['C_QT_MAT'].values[0]
                    concluintesAnterior = dataCurso.loc[dataCurso['ANO'] == ano - 1]['C_QT_CONC'].values[0]

                    divisor = matriculados - ingressantes
                    dividendo = matriculadosAnterior - concluintesAnterior

                    if dividendo == 0:
                        permanencia = 0
                    else:
                        permanencia = round(divisor / dividendo, 2)

                    evasao = 1 - permanencia

                    dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicipio) & (dataFrame['C_NO_CINE_ROTULO'] == nomeCurso), 'C_PERMANENCIA'] = permanencia
                    dataFrame.loc[(dataFrame['ANO'] == ano) & (dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicipio) & (dataFrame['C_NO_CINE_ROTULO'] == nomeCurso), 'C_EVASAO'] = evasao
    
    total = dataFrame.shape[0]
    totalEvasao = dataFrame.loc[dataFrame['C_EVASAO'] != 999999].shape[0]
    totalSemEvasao = dataFrame.loc[dataFrame['C_EVASAO'] == 999999].shape[0]

    print('Total de Cursos: {}\nFoi calculado a evasão de {}% dos cursos\nCerca de {}% não foi possivel calcular'.format(total, round((totalEvasao/total)*100, 2), round((totalSemEvasao/total)*100, 2)))

    return dataFrame

def calculoPercentuais(dataFrame):

    for ies in dataFrame['CO_IES'].unique().tolist():
        dataIes = dataFrame[dataFrame['CO_IES'] == ies]

        for coMunicio in dataIes['CO_MUNICIPIO'].unique().tolist():
            dataMunicipio = dataIes[dataIes['CO_MUNICIPIO'] == coMunicio]

            for value in dataMunicipio['C_NO_CINE_ROTULO'].unique().tolist():
                dataNO_CINE = dataMunicipio[dataMunicipio['C_NO_CINE_ROTULO'] == value]
                dataFrame.loc[(dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicio) & (dataFrame['C_NO_CINE_ROTULO'] == value), 'C_QT_ANOS'] = len(dataNO_CINE)

                for ano in dataNO_CINE['ANO'].unique().tolist():
                    dataFrame.loc[dataFrame['ANO'] == ano, 'C_QT_VETERANOS'] = dataFrame.loc[dataFrame['ANO'] == ano, 'C_QT_MAT'] - dataFrame.loc[dataFrame['ANO'] == ano, 'C_QT_ING']
                    
                    dataAno = dataNO_CINE[dataNO_CINE['ANO'] == ano]
                    dataAnoPassado = dataNO_CINE[dataNO_CINE['ANO'] == ano-1]

                    concluintes = dataAno['C_QT_CONC'].values[0]
                    matriculados = dataAno['C_QT_MAT'].values[0]
                    inscritos = dataAno['QT_INSCRITO_TOTAL'].values[0]
                    n_concluintes = (matriculados - dataAno['C_QT_ING'].values[0]) - concluintes
                    vagas = dataAno['C_QT_VG_NOVA'].values[0]

                    calc_concluintes = 0
                    calc_n_concluintes = 0

                    if matriculados > 0:
                        calc_concluintes = round(concluintes/matriculados, 2)
                        calc_n_concluintes = round(n_concluintes/matriculados, 2)

                    dataFrame.loc[(dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicio) & (dataFrame['C_NO_CINE_ROTULO'] == value) & (dataFrame['ANO'] == ano), 'C_PERC_CONC'] = calc_concluintes
                    dataFrame.loc[(dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicio) & (dataFrame['C_NO_CINE_ROTULO'] == value) & (dataFrame['ANO'] == ano), 'C_PERC_NCONC'] = calc_n_concluintes

                    result = 0

                    if vagas != 0:
                        result = round(inscritos/vagas, 2)

                    dataFrame.loc[(dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicio) & (dataFrame['C_NO_CINE_ROTULO'] == value) & (dataFrame['ANO'] == ano), 'C_PERC_VAGA'] = result

                    if len(dataAnoPassado) > 0:
                        matriculadosAnoPassado = dataAnoPassado['C_QT_MAT'].values[0]
                        result = matriculados - matriculadosAnoPassado

                        dataFrame.loc[(dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicio) & (dataFrame['C_NO_CINE_ROTULO'] == value) & (dataFrame['ANO'] == ano), 'C_DIF_VAGA_ANO'] = result

                        if result > 0:
                            dataFrame.loc[(dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicio) & (dataFrame['C_NO_CINE_ROTULO'] == value) & (dataFrame['ANO'] == ano), 'C_PERC_VAGA_ANO'] = round(matriculadosAnoPassado/result, 2)
                        else:
                            dataFrame.loc[(dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicio) & (dataFrame['C_NO_CINE_ROTULO'] == value) & (dataFrame['ANO'] == ano), 'C_PERC_VAGA_ANO'] = 0
                    else:
                        dataFrame.loc[(dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicio) & (dataFrame['C_NO_CINE_ROTULO'] == value) & (dataFrame['ANO'] == ano), 'C_DIF_VAGA_ANO'] = 0
                        dataFrame.loc[(dataFrame['CO_IES'] == ies) & (dataFrame['CO_MUNICIPIO'] == coMunicio) & (dataFrame['C_NO_CINE_ROTULO'] == value) & (dataFrame['ANO'] == ano), 'C_PERC_VAGA_ANO'] = 0
    
    return dataFrame
