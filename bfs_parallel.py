"""Versão paralela do BFS por expansão de fronteiras em níveis."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from math import ceil
from typing import Dict, List, Optional


Graph = Dict[int, List[int]]

_WORKER_GRAPH: Graph | None = None


def parallel_bfs_shortest_path(
    graph: Graph,
    start: int,
    end: int,
    max_workers: int = 4,
    num_blocks: int | None = None,
) -> Optional[List[int]]:
    """Retorna o menor caminho usando BFS paralelo sincronizado por níveis."""
    if start not in graph or end not in graph:
        raise ValueError("start e end devem existir no grafo.")

    if max_workers < 1:
        raise ValueError("max_workers deve ser maior ou igual a 1.")

    if num_blocks is not None and num_blocks < 1:
        raise ValueError("num_blocks deve ser maior ou igual a 1.")

    if start == end:
        return [start]

    visited = {start}
    parents = {start: None}
    frontier = [start]

    with ProcessPoolExecutor(
        max_workers=max_workers,
        initializer=_init_worker_graph,
        initargs=(graph,),
    ) as executor:
        while frontier:
            block_count = num_blocks or min(max_workers, len(frontier))
            frontier_blocks = _split_into_blocks(frontier, block_count)

            futures = [
                executor.submit(_expand_frontier_block, block)
                for block in frontier_blocks
                if block
            ]

            next_frontier: List[int] = []
            found_end = False

            for future in futures:
                discovered_edges = future.result()

                for parent, neighbor in discovered_edges:
                    if neighbor in visited:
                        continue

                    visited.add(neighbor)
                    parents[neighbor] = parent
                    next_frontier.append(neighbor)

                    if neighbor == end:
                        found_end = True

            if found_end:
                return _reconstruct_path(parents, end)

            frontier = next_frontier

    return None


def _init_worker_graph(graph: Graph) -> None:
    """Carrega o grafo uma vez por processo trabalhador."""
    global _WORKER_GRAPH
    _WORKER_GRAPH = graph


def _expand_frontier_block(block: List[int]) -> List[tuple[int, int]]:
    """Expande um bloco da fronteira atual e devolve arestas descobertas."""
    if _WORKER_GRAPH is None:
        raise RuntimeError("Grafo do worker nao foi inicializado.")

    discovered_edges: List[tuple[int, int]] = []

    for node in block:
        for neighbor in _WORKER_GRAPH[node]:
            discovered_edges.append((node, neighbor))

    return discovered_edges


def _reconstruct_path(
    parents: dict[int, int | None],
    end: int,
) -> List[int]:
    """Reconstrói o caminho mínimo a partir do mapa de pais."""
    path: List[int] = []
    current: int | None = end

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def _split_into_blocks(items: List[int], num_blocks: int) -> List[List[int]]:
    """Divide a fronteira em blocos aproximadamente equilibrados."""
    if num_blocks <= 0:
        raise ValueError("num_blocks deve ser maior que zero.")

    if not items:
        return []

    block_size = ceil(len(items) / num_blocks)
    return [
        items[index:index + block_size]
        for index in range(0, len(items), block_size)
    ]
