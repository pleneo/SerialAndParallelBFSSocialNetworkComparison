"""Busca em largura sequencial para menor caminho em grafo não ponderado."""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional


Graph = Dict[int, List[int]]


def bfs_shortest_path(graph: Graph, start: int, end: int) -> Optional[List[int]]:
    """Retorna o menor caminho entre start e end usando BFS."""
    if start not in graph or end not in graph:
        raise ValueError("start e end devem existir no grafo.")

    if start == end:
        return [start]

    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        current = path[-1]

        for neighbor in graph[current]:
            if neighbor in visited:
                continue

            new_path = path + [neighbor]

            if neighbor == end:
                return new_path

            visited.add(neighbor)
            queue.append(new_path)

    return None


def path_distance(path: Optional[List[int]]) -> Optional[int]:
    """Retorna a distância em arestas do caminho."""
    if path is None:
        return None

    return len(path) - 1
