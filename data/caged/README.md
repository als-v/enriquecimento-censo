# Coleta e Organização dos Dados do Cadastro Geral de Empregados e Desempregados (CAGED)

A coleta e a correta organização dos dados do CAGED é essencial para o bom funcionamento do algoritmo. Abaixo, você encontrará um guia detalhado sobre como obter e estruturar os conjuntos coletados. 

## Fonte dos Dados

Os conjuntos de dados do CAGED são disponibilizados no formato TXT por meio de um servidor FTP (Protocolo de Transferência de Arquivos). Para acessar esses dados, siga as instruções fornecidas no seguinte endereço: [http://pdet.mte.gov.br/microdados-rais-e-caged](http://pdet.mte.gov.br/microdados-rais-e-caged). 

## Organização dos Dados

A fim de garantir a integridade dos dados e permitir o processamento eficiente pelo algoritmo, é essencial que os arquivos estejam organizados de acordo com a estrutura de pastas a seguir. Este exemplo demonstra a organização para os dados do ano de 2009:

```
caged/
└── 2009/
    ├── CAGEDEST_012009.txt
    ├── CAGEDEST_022009.txt
    ├── CAGEDEST_032009.txt
    ├── CAGEDEST_042009.txt
    ├── CAGEDEST_052009.txt
    ├── CAGEDEST_062009.txt
    ├── CAGEDEST_072009.txt
    ├── CAGEDEST_082009.txt
    ├── CAGEDEST_092009.txt
    ├── CAGEDEST_102009.txt
    ├── CAGEDEST_112009.txt
    └── CAGEDEST_122009.txt
```
**Observação:** Cada ano coletado compreende 12 conjuntos distintos de dados, cada um representando um mês do ano.

**Importante:** Certifique-se de estender esse procedimento para todos os anos dos dados coletados do CAGED, e dos outros conjuntos coletados.

## Contato

Para eventuais dúvidas ou esclarecimentos adicionais, sinta-se à vontade para entrar em contato:

Nome: Alisson

Email: alisson.v3@hotmail.com