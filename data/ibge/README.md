# Coleta e Organização dos Dados do Instituto Brasileiro de Geografia e Estatística (IBGE)

A coleta e a correta organização dos dados do IBGE é essencial para o bom funcionamento do algoritmo. Abaixo, você encontrará um guia detalhado sobre como obter e estruturar os conjuntos coletados. 

## Conjuntos de Dados

Foram coletados dois conjuntos de dados do IBGE para este projeto:

1. **PIB (Produto Interno Bruto):** Este conjunto contém informações econômicas relevantes para a análise. Os dados foram obtidos por meio da consulta ao Sistema IBGE de Recuperação Automática (SIDRA) e podem ser encontrados aqui: [PIB - SIDRA](https://sidra.ibge.gov.br/tabela/5938).

2. **POPULAÇÃO:** Este conjunto compreende dados demográficos essenciais para as análises. Os dados também foram obtidos por meio do SIDRA e podem ser acessados aqui: [POPULAÇÃO - SIDRA](https://sidra.ibge.gov.br/tabela/6579).

## Procedimentos de Coleta

Ao gerar os conjuntos de dados do SIDRA, certifique-se de seguir os seguintes passos:

- Selecionar os anos desejados para a coleta.
- Escolha os dados específicos referentes ao código e ao nome do município no conjunto gerado.
- Opte por obter todos os dados disponíveis para uma análise completa.
- Selecione o formato 'CSV' durante o processo de geração.
- Com os dados gerados, edite o arquivo a ponto que a primeira linha fique apenas com o nome das colunas referentes ao código do município ('Cód'), nome do município ('Município') e os anos escolhidos.

## Organização dos Dados

Para manter a integridade e a clareza dos dados, é recomendável organizar cada conjunto em pastas distintas, como demonstrado abaixo:

```
ibge/
├── pib/
│   └── data.csv
└── populacao/
    └── data.csv
```

## Contato

Para esclarecimentos adicionais ou dúvidas, não hesite em entrar em contato:

**Nome:** Alisson
**Email:** alisson.v3@hotmail.com

A abordagem organizada na coleta e organização dos dados do IBGE não apenas facilita as análises futuras, mas também contribui para a eficácia do projeto como um todo. Certifique-se de seguir essas diretrizes para garantir o sucesso contínuo do projeto.