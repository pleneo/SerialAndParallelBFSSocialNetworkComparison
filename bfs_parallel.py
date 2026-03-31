"""Versão paralela do BFS via particionamento da fronteira inicial."""

from __future__ import annotations

from collections import deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from math import ceil
from typing import Dict, List, Optional


Graph = Dict[int, List[int]]


def parallel_bfs_shortest_path(
    graph: Graph,
    start: int,
    end: int,
    max_workers: int = 4,
    num_blocks: int | None = None,
) -> Optional[List[int]]:
    """Busca o menor caminho dividindo os vizinhos iniciais em blocos."""
    if start not in graph or end not in graph:
        raise ValueError("start e end devem existir no grafo.")

    if start == end:
        return [start]

    neighbors = graph[start]
    if not neighbors:
        return None

    if end in neighbors:
        return [start, end]

    block_count = num_blocks or min(max_workers, len(neighbors))
    neighbor_blocks = _split_into_blocks(neighbors, block_count)
    candidate_paths: List[List[int]] = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_search_block, graph, start, end, block)
            for block in neighbor_blocks
            if block
        ]

        for future in as_completed(futures):
            block_paths = future.result()
            candidate_paths.extend(block_paths)

    if not candidate_paths:
        return None

    return min(candidate_paths, key=len)


def _search_block(
    graph: Graph,
    start: int,
    end: int,
    first_neighbors: List[int],
) -> List[List[int]]:
    """Executa buscas independentes para um subconjunto da primeira fronteira."""
    paths: List[List[int]] = []

    for neighbor in first_neighbors:
        partial_path = _bfs_with_forced_first_step(graph, start, neighbor, end)
        if partial_path is not None:
            paths.append(partial_path)

    return paths


def _bfs_with_forced_first_step(
    graph: Graph,
    start: int,
    first_neighbor: int,
    end: int,
) -> Optional[List[int]]:
    """Força o primeiro salto start -> first_neighbor e continua a busca."""
    if first_neighbor == end:
        return [start, end]

    queue = deque([[first_neighbor]])
    visited = {start, first_neighbor}

    while queue:
        path = queue.popleft()
        current = path[-1]

        for neighbor in graph[current]:
            if neighbor in visited:
                continue

            new_path = path + [neighbor]

            if neighbor == end:
                return [start] + new_path

            visited.add(neighbor)
            queue.append(new_path)

    return None


def _split_into_blocks(items: List[int], num_blocks: int) -> List[List[int]]:
    """Divide uma lista em blocos aproximadamente equilibrados."""
    if num_blocks <= 0:
        raise ValueError("num_blocks deve ser maior que zero.")

    block_size = ceil(len(items) / num_blocks)
    return [
        items[index:index + block_size]
        for index in range(0, len(items), block_size)
    ]
