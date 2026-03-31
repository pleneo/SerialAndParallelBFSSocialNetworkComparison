"""
Objetivo do Trabalho:

Em um grafo que represente uma rede social, onde cada nó como vizinho os seus amigos,
implementar um algortimo de Busca em Largura (BFS) que encontre a quantos graus de separação um nó x
estará de um nó z.
Ex: x -> y -> w -> z. Se esse é o menor caminho de x até z, então x está a 3 graus de separação de z.

Essa busca em profundidade será feita de duas maneiras:
    - Serializada: execução sequencial do BFS em um único fluxo de execução.

    - Paralelizada: Multiplos processos de busca se espalharão entre os nós e se aprofundarão no grafo, comparando ao
    final as distancias encontradas e selecionando a melhor **obs: preciso conferir se essa ideia está correta**


Nós são bidirecionais, ou seja, x -> y e y -> x. (x é amigo de y e y é amigo de x).

A busca paralelizada seguirá a Metodologia de Foster para projeção e criação do algoritmo paralelizado, consistindo em:
Particionar, Comunicar, Aglomerar e Mapear.

Para garantir uma comparação justa, as versões serial e paralela serão executadas sobre
o mesmo grafo e os mesmos pares de usuários, com medição de tempo, validação dos caminhos
encontrados e comparação de desempenho.
"""

from __future__ import annotations

from benchmark import (
    format_results_table,
    plot_scalability_results,
    run_scalability_benchmark,
)


GRAPH_SIZES = [10000, 25000, 50000, 75000, 100000]
AVG_FRIENDS = 2
REPEATS = 5
SEED = 42
MAX_WORKERS = 4
NUM_BLOCKS = 4


def main() -> None:
    results = run_scalability_benchmark(
        graph_sizes=GRAPH_SIZES,
        avg_friends=AVG_FRIENDS,
        repeats=REPEATS,
        seed=SEED,
        max_workers=MAX_WORKERS,
        num_blocks=NUM_BLOCKS,
    )

    table = format_results_table(results)
    print(table)
    print()
    plot_scalability_results(results)


if __name__ == "__main__":
    main()
