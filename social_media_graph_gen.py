"""Gera uma rede social sintética para os testes de BFS."""

from __future__ import annotations

import random
from typing import Dict, List


Graph = Dict[int, List[int]]


def generate_social_graph(
    num_users: int,
    avg_friends: int,
    seed: int | None = None,
) -> Graph:
    """Gera um grafo não direcionado com conectividade básica.

    Regras:
    - cada usuário é identificado por um inteiro de 0 a num_users - 1;
    - amizades são bidirecionais;
    - não há autoamizade;
    - não há arestas duplicadas;
    - uma estrutura conectada mínima é criada antes de adicionar amizades extras.
    """
    if num_users < 2:
        raise ValueError("num_users deve ser maior ou igual a 2.")

    if avg_friends < 1:
        raise ValueError("avg_friends deve ser maior ou igual a 1.")

    if avg_friends >= num_users:
        raise ValueError("avg_friends deve ser menor que num_users.")

    rng = random.Random(seed)
    adjacency = {user: set() for user in range(num_users)}

    _build_connected_backbone(adjacency, rng)
    _add_random_friendships(adjacency, avg_friends, rng)

    return {
        user: sorted(neighbors)
        for user, neighbors in adjacency.items()
    }


def pick_distinct_users(graph: Graph, seed: int | None = None) -> tuple[int, int]:
    """Escolhe dois usuários distintos do grafo para origem e destino."""
    if len(graph) < 2:
        raise ValueError("O grafo precisa ter pelo menos 2 usuários.")

    rng = random.Random(seed)
    start, end = rng.sample(list(graph.keys()), 2)
    return start, end


def _build_connected_backbone(
    adjacency: dict[int, set[int]],
    rng: random.Random,
) -> None:
    """Cria um caminho aleatório que conecta todos os nós."""
    users = list(adjacency.keys())
    rng.shuffle(users)

    for index in range(1, len(users)):
        left = users[index - 1]
        right = users[index]
        adjacency[left].add(right)
        adjacency[right].add(left)


def _add_random_friendships(
    adjacency: dict[int, set[int]],
    avg_friends: int,
    rng: random.Random,
) -> None:
    """Adiciona amizades aleatórias até atingir a média desejada."""
    num_users = len(adjacency)
    target_edges = max(num_users - 1, (num_users * avg_friends) // 2)
    current_edges = _count_edges(adjacency)

    while current_edges < target_edges:
        user_a = rng.randrange(num_users)
        user_b = rng.randrange(num_users)

        if user_a == user_b:
            continue

        if user_b in adjacency[user_a]:
            continue

        adjacency[user_a].add(user_b)
        adjacency[user_b].add(user_a)
        current_edges += 1


def _count_edges(adjacency: dict[int, set[int]]) -> int:
    """Conta arestas não direcionadas do grafo."""
    return sum(len(neighbors) for neighbors in adjacency.values()) // 2
