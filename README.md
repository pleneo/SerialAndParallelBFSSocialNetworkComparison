# Graus de Separação em Rede Social: Serial x Paralelizado

Projeto da disciplina de Computação Paralela Concorrente para comparar uma implementação serial e uma implementação paralela do algoritmo BFS em uma rede social sintética.

## Objetivo

O projeto modela uma rede social como um grafo não direcionado:

- nós representam usuários;
- arestas representam amizades;
- o objetivo é encontrar o menor caminho entre dois usuários, interpretado como os graus de separação.

Foram implementadas duas abordagens:

- serial: BFS clássico em fluxo único;
- paralela: BFS por níveis, com expansão da fronteira em blocos usando `ProcessPoolExecutor`.

Além disso, o projeto mede tempo de execução, calcula speedup, valida os caminhos encontrados e compara dois cenários de benchmark:

- escalabilidade por tamanho do grafo;
- densidade variável com tamanho fixo.

## Requisitos

- Python 3.12 ou superior
- ambiente com suporte a `multiprocessing`
- backend gráfico funcional para `matplotlib`, caso queira abrir os gráficos com `plt.show()`

## Instalação

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como executar

Para rodar o experimento principal:

```bash
python main.py
```

A execução:

- imprime duas tabelas no console;
- plota dois gráficos com `matplotlib`.

## Estrutura do Projeto

- `main.py`: ponto de entrada e configuração dos cenários
- `social_media_graph_gen.py`: geração do grafo sintético
- `bfs_serial.py`: BFS serial para menor caminho
- `bfs_parallel.py`: BFS paralelo por níveis
- `validation.py`: validação dos caminhos
- `benchmark.py`: medição, comparação, tabelas e gráficos

## Metodologia de Comparação

- medição com `time.perf_counter()`;
- 5 repetições por cenário;
- mesmo grafo e mesmo par `start/end` para serial e paralelo;
- pares reprodutíveis e distantes para evitar casos triviais;
- validação por caminho válido e mesma distância mínima.

O speedup é calculado por:

```text
Speedup = Tempo Serial / Tempo Paralelo
```

## Observações

- O fato de a implementação paralela não superar a serial em todos os cenários não invalida o projeto. Esse comportamento faz parte da análise experimental e é explicado pelo overhead de processos, comunicação e sincronização por níveis em Python.
- Em ambientes Linux, o `matplotlib` pode depender de um backend gráfico adequado para abrir a janela dos gráficos.
