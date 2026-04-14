"""
Objetivo do Trabalho:

Em um grafo que represente uma rede social, onde cada nó como vizinho os seus amigos,
implementar um algoritmo de Busca em Largura (BFS) que encontre a quantos graus de separação um nó x
está de um nó z.
Ex: x -> y -> w -> z. Se esse é o menor caminho de x até z, então x está a 3 graus de separação de z.

Essa busca em largura será feita de duas maneiras:
    - Serial: execução sequencial do BFS em um único fluxo de execução.
    - Paralela: expansão da fronteira do BFS por níveis usando múltiplos processos.

Nós são bidirecionais, ou seja, x -> y e y -> x. (x é amigo de y e y é amigo de x).

A busca paralela seguirá a Metodologia de Foster para projeção e criação do algoritmo paralelizado, consistindo em:
Particionar, Comunicar, Aglomerar e Mapear.

Para garantir uma comparação justa, as versões serial e paralela serão executadas sobre
o mesmo grafo e os mesmos pares de usuários, com medição de tempo, validação dos caminhos
encontrados e comparação de desempenho em dois cenários:
    - escalabilidade por tamanho do grafo;
    - variação da densidade com tamanho fixo.
"""

from __future__ import annotations

from benchmark import (
    format_results_table,
    plot_density_results,
    plot_scalability_results,
    run_density_benchmark,
    run_scalability_benchmark,
)


GRAPH_SIZES = [5000, 20000, 40000, 60000, 80000, 100000, 200000]
AVG_FRIENDS = 8
DENSITY_GRAPH_SIZE = 20000
AVG_FRIENDS_VALUES = [4, 8, 12, 16]
REPEATS = 1
SEED = 42
MAX_WORKERS = 4
NUM_BLOCKS = 4


def main() -> None:
    scalability_results = run_scalability_benchmark(
        graph_sizes=GRAPH_SIZES,
        avg_friends=AVG_FRIENDS,
        repeats=REPEATS,
        seed=SEED,
        max_workers=MAX_WORKERS,
        num_blocks=NUM_BLOCKS,
    )

    density_results = run_density_benchmark(
        num_users=DENSITY_GRAPH_SIZE,
        avg_friends_values=AVG_FRIENDS_VALUES,
        repeats=REPEATS,
        seed=SEED,
        max_workers=MAX_WORKERS,
        num_blocks=NUM_BLOCKS,
    )

    print("Cenario 1: Escalabilidade por tamanho")
    print(format_results_table(scalability_results))
    print()
    print("Cenario 2: Densidade variavel com tamanho fixo")
    print(format_results_table(density_results))
    print()

    plot_scalability_results(scalability_results)
    plot_density_results(density_results)


if __name__ == "__main__":
    main()
