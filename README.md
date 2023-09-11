# Enriquecimento dos Dados do Censo da Educação Superior

Este repositório contém um guia detalhado para a execução do enriquecimento dos dados do Censo da Educação Superior. Foram utilizadas bases de dados do Cadastro Geral de Empregados e Desempregados (CAGED) e do Instituto Brasileiro de Geografia e Estatística (IBGE) para enriquecer os conjuntos de dados.

## Procedimentos para Execução

Antes de iniciar o processo de enriquecimento, é necessário instalar as dependências do projeto. Para fazer isso, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

Após a instalação das dependências, siga os passos abaixo para cada conjunto de dados:

1. **CAGED:** [Consulte o README correspondente para obter informações sobre como coletar e organizar os dados do CAGED.](./data/caged/README.md)

2. **IBGE:** [Consulte o README correspondente para obter informações sobre como coletar e organizar os dados do IBGE.](./data/ibge/README.md)

Após a coleta e organização dos dados de cada conjunto, você pode executar o script de enriquecimento. \
Os scripts estão divididos em duas partes: um para a organização e pré-processamento dos dados coletados (arquivo com a label `dados`) e outro para a visualização dos dados (arquivo com a label `visualização`).

É obrigatório que o script dos dados do Censo seja executado antes dos demais scripts, onde, após a sua execução, podem seguir qualquer ordem.

Após a conclusão do processo de enriquecimento, pode-se optar por analisar as diferenças nos conjuntos de dados do ponto de vista dos municípios brasileiros e em nível nacional. Para fazer isso, consulte os arquivos de visualização chamados "Visualização Brasil" e "Visualização Municipal".

## Contato

Para esclarecimentos adicionais ou dúvidas, não hesite em entrar em contato:

**Nome:** Alisson