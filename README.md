# Investigação de Diferenciação e Integração Numéricas

Repositório inicial da atividade de investigação da disciplina de **Cálculo Numérico**.

## Estrutura

```text
investigacao-calculo-numerico/
├── diferencas.py
├── integracao.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── graficos/
└── relatorio/
```

- `diferencas.py`: fórmulas-base de diferenças finitas fornecidas no enunciado.
- `integracao.py`: regras-base de Newton-Cotes, cotas de erro e Gauss-Legendre fornecidas no enunciado.
- `main.py`: arquivo em que as questões, experimentos, tabelas e gráficos serão implementados.
- `graficos/`: saída dos gráficos produzidos durante a investigação.
- `relatorio/`: local para organizar o relatório final em PDF.

## Preparação do ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução

```bash
python3 main.py
```

Neste estado inicial, `main.py` não executa as questões do trabalho; ele contém apenas a organização das seções.
