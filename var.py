CREATE_PARQUET_FILES = False
PROCESS_PARQUET_FILES = True
PROCESS_CSV_FILES = True
READ_PARQUET_FILES = True
SHOW_DIFFERENCE_BETWEEN_PARQUET_CSV_FILES = True

# Range de anos da coleta dos dados
ANOS = [
    2009, 
    2010, 
    2011, 
    2012, 
    2013, 
    2014, 
    2015, 
    2016, 
    2017, 
    2018, 
    2019, 
    2020
]

# Classificação CNAE para Computação
CNAE_CLASS = [
    '1830003',
    '2621300',
    '2622100',
    '4651601',
    '4651602',
    '4751201',
    '6190601',
    '6201502',
    '6190602',
    '6201501',
    '6202300',
    '6203100',
    '6204000',
    '6209100',
    '6311900',
    '6319400',
    '6391700',
    '6399200',
    '8599603',
    '9511800'
]

'''
# Classificação CBO para Computação
cboClass = [
    '212205',
    '212210',
    '212215',
    '212305',
    '212310',
    '212315',
    '212320',
    '212405',
    '212410',
    '212415',
    '212420',
    '317105',
    '317110',
    '317115',
    '317120',
    '317205',
    '317210'
]
'''

MESES = [
    '01',
    '02',
    '03',
    '04',
    '05',
    '06',
    '07',
    '08',
    '09',
    '10',
    '11',
    '12'
]

INEP_COLUMNS = [
    'INEP_CURSO_QUANTIDADE_MATRICULADOS', 
    'INEP_CURSO_QUANTIDADE_INGRESSANTES',
    'INEP_CURSO_QUANTIDADE_CONCLUINTES',
    'INEP_CURSO_QUANTIDADE_VAGAS_NOVAS',
    'INEP_CURSO_QUANTIDADE_VAGAS_TOTAL',
    'INEP_CURSO_QUANTIDADE_INSCRITOS_VAGAS_NOVAS',
    'INEP_CURSO_QUANTIDADE_INSCRITOS_TOTAL',
    'INEP_CURSO_QUANTIDADE_ALUNOS_SITUACAO_TRANCADA',
    'INEP_CURSO_QUANTIDADE_ALUNOS_SITUACAO_TRANSFERIDO',
    'INEP_CURSO_QUANTIDADE_ALUNOS_APOIO_SOCIAL',
    'INEP_CURSO_QUANTIDADE_ALUNOS_SITUACAO_FALECIDO',
    'INEP_CURSO_PERCENTUAL_DOCENTE_POR_ALUNO',
    'INEP_CURSO_QUANTIDADE_ALUNOS_DEFICIENTES',
    'INEP_CURSO_EVASAO',
    'INEP_CURSO_PERMANENCIA',
    'INEP_CURSO_QUANTIDADE_VETERANOS',
    'INEP_CURSO_PERCENTUAL_CONCLUINTES',
    'INEP_CURSO_PERCENTUAL_NAO_CONCLUINTES',
    'INEP_CURSO_CONCORRENCIA_VAGAS',
    'INEP_CURSO_DIFERENCA_VAGAS_ANO_ANTERIOR',
    'INEP_CURSO_PERCENTUAL_DIFERENCA_VAGAS_ANO_ANTERIOR',
    'INEP_CURSO_QUANTIDADE_ANOS_CENSO',
    
    'INEP_IES_QUANTIDADE_ALUNOS_DEFICIENTES',
    'INEP_IES_QUANTIDADE_DOCENTES',
    'INEP_IES_QUANTIDADE_DOCENTES_SUPERIOR',
    'INEP_IES_QUANTIDADE_DOCENTES_MESTRADO',
    'INEP_IES_QUANTIDADE_DOCENTES_DOUTORADO',
    'INEP_IES_QUANTIDADE_DOCENTES_EXERCICIO',
    'INEP_IES_QUANTIDADE_DOCENTES_EXERCICIO_GRADUACAO',
    'INEP_IES_QUANTIDADE_DOCENTES_EXERCICIO_MESTRADO',
    'INEP_IES_QUANTIDADE_DOCENTES_EXERCICIO_DOUTORADO',
    'INEP_IES_QUANTIDADE_LIVROS_ELETRONICOS',
]

IBGE_COLUMNS = [
    'IBGE_MUNICIPIO_PIB', 
    'IBGE_MUNICIPIO_POP',
    'IBGE_MUNICIPIO_PIBPERCAPTA',
]

CAGED_COLUMNS = [
    'CAGED_MUNICIPIO_ADMISSOES', 
    'CAGED_MUNICIPIO_DESLIGAMENTOS',
    'CAGED_MUNICIPIO_SALARIO',
    'CAGED_MUNICIPIO_ADMISSOES_IDADE',
    'CAGED_MUNICIPIO_DESLIGAMENTOS_IDADE',
    'CAGED_MUNICIPIO_HORA_CONTRATO',
    'CAGED_MUNICIPIO_SALARIO_MINIMO',
    'CAGED_MUNICIPIO_SALDO',
    'CAGED_MUNICIPIO_DIFERENCA_ADMISSAO',
]

LABELS = {
    # Censo - cursos
    'INEP_CURSO_QUANTIDADE_MATRICULADOS': 'Matriculados' ,
    'INEP_CURSO_QUANTIDADE_INGRESSANTES': 'Ingressantes',
    'INEP_CURSO_QUANTIDADE_CONCLUINTES': 'Concluintes',
    'INEP_CURSO_QUANTIDADE_VAGAS_NOVAS': 'Vagas novas',
    'INEP_CURSO_QUANTIDADE_VAGAS_TOTAL': 'Vagas totais',
    'INEP_CURSO_QUANTIDADE_INSCRITOS_VAGAS_NOVAS': 'Inscritos\nvagas novas',
    'INEP_CURSO_QUANTIDADE_INSCRITOS_TOTAL': 'Inscritos totais',
    'INEP_CURSO_QUANTIDADE_ALUNOS_SITUACAO_TRANCADA': 'Alunos trancados',
    'INEP_CURSO_QUANTIDADE_ALUNOS_SITUACAO_TRANSFERIDO': 'Alunos transferidos',
    'INEP_CURSO_QUANTIDADE_ALUNOS_APOIO_SOCIAL': 'Alunos apoio social',
    'INEP_CURSO_QUANTIDADE_ALUNOS_SITUACAO_FALECIDO': 'Alunos falecidos',
    'INEP_CURSO_PERCENTUAL_DOCENTE_POR_ALUNO': 'Percentual docente por aluno',
    'INEP_CURSO_QUANTIDADE_ALUNOS_DEFICIENTES': 'Alunos\ndeficientes',
    'INEP_CURSO_EVASAO': 'Evasão',
    'INEP_CURSO_PERMANENCIA': 'Permanência',
    'INEP_CURSO_QUANTIDADE_VETERANOS': 'Veteranos',
    'INEP_CURSO_PERCENTUAL_CONCLUINTES': 'Concluintes',
    'INEP_CURSO_PERCENTUAL_NAO_CONCLUINTES': 'Não concluintes',
    'INEP_CURSO_CONCORRENCIA_VAGAS': 'Concorrência\nvagas',
    'INEP_CURSO_DIFERENCA_VAGAS_ANO_ANTERIOR': 'Diferença vagas\nano anterior',
    'INEP_CURSO_PERCENTUAL_DIFERENCA_VAGAS_ANO_ANTERIOR': 'Percentual diferença\nvagas ano anterior',
    'INEP_CURSO_QUANTIDADE_ANOS_CENSO': 'Quantidade de anos do censo',
    
    # Censo - ies
    'INEP_IES_QUANTIDADE_ALUNOS_DEFICIENTES': 'Alunos deficientes',
    'INEP_IES_QUANTIDADE_DOCENTES': 'Docentes',
    'INEP_IES_QUANTIDADE_DOCENTES_SUPERIOR': 'Docentes superior',
    'INEP_IES_QUANTIDADE_DOCENTES_MESTRADO': 'Docentes mestrado',
    'INEP_IES_QUANTIDADE_DOCENTES_DOUTORADO': 'Docentes doutorado',
    'INEP_IES_QUANTIDADE_DOCENTES_EXERCICIO': 'Docentes\nexercício',
    'INEP_IES_QUANTIDADE_DOCENTES_EXERCICIO_GRADUACAO': 'Docentes em exercício graduação',
    'INEP_IES_QUANTIDADE_DOCENTES_EXERCICIO_MESTRADO': 'Docentes em exercício mestrado',
    'INEP_IES_QUANTIDADE_DOCENTES_EXERCICIO_DOUTORADO': 'Docentes em exercício doutorado',
    'INEP_IES_QUANTIDADE_LIVROS_ELETRONICOS': 'Livros eletrônicos',

    # Caged
    'CAGED_MUNICIPIO_ADMISSOES': 'Admissões',
    'CAGED_MUNICIPIO_DESLIGAMENTOS': 'Desligamentos', 
    'CAGED_MUNICIPIO_SALARIO': 'Salário (em R$)', 
    'CAGED_MUNICIPIO_ADMISSOES_IDADE': 'Idade\nadmissão',
    'CAGED_MUNICIPIO_DESLIGAMENTOS_IDADE': 'Idade\ndesligamento',
    'CAGED_MUNICIPIO_HORA_CONTRATO': 'Horas de contrato',
    'CAGED_MUNICIPIO_SALARIO_MINIMO': 'Salário mínimo',
    'CAGED_MUNICIPIO_DIFERENCA_ADMISSAO': 'Diferença\nadmissões e\ndesligamentos',
    'CAGED_MUNICIPIO_SALDO': 'Diferença\ndesligamentos e\nadmissões',
    
    # Ibge
    'IBGE_MUNICIPIO_PIB': 'PIB',
    'IBGE_MUNICIPIO_POP': 'População',
    'IBGE_MUNICIPIO_PIBPERCAPTA': 'PIB per capita',
    'IDHM': 'IDHM',
}

CURSOS = [
        "Ciência da computação",
        # "Sistemas de informação",
        # "Engenharia de computação (DCN Computação)",
        # "Engenharia de computação (DCN Engenharia)",
        # "Sistemas para internet",
        # "Jogos digitais",
        # "Segurança da informação",
        # "Redes de computadores",
        # "Engenharia de software",
        # "Banco de dados",
        # "Engenharia de informação",
        # "Sistemas embarcados",
        # "Defesa cibernética",
        # "Ciência de dados",
        # "Inteligência artificial",
        # "Internet das coisas",
        # "Agrocomputação",
        # "Redes de telecomunicações",
        # "Sistemas de telecomunicações",
        # "Computação formação de professor",
        # "Programas interdisciplinares abrangendo computação e Tecnologias da Informação e Comunicação (TIC)",
        # "Computação e Tecnologias da Informação e Comunicação (TIC) em biociências e saúde",
]