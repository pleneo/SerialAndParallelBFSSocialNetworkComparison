"""Valida caminhos e compara resultados serial/paralelo."""

from __future__ import annotations

from typing import Dict, List, Optional


Graph = Dict[int, List[int]]


def is_valid_path(
    graph: Graph,
    path: Optional[List[int]],
    start: int,
    end: int,
) -> bool:
    """Verifica se um caminho existe e respeita as arestas do grafo."""
    if path is None or not path:
        return False

    if path[0] != start or path[-1] != end:
        return False

    for current, nxt in zip(path, path[1:]):
        if nxt not in graph.get(current, []):
            return False

    return True


def path_distance(path: Optional[List[int]]) -> Optional[int]:
    """Retorna a quantidade de arestas do caminho."""
    if path is None:
        return None

    return len(path) - 1


def same_distance(
    serial_path: Optional[List[int]],
    parallel_path: Optional[List[int]],
) -> bool:
    """Compara as distâncias encontradas pelas duas abordagens."""
    return path_distance(serial_path) == path_distance(parallel_path)


def validate_both_results(
    graph: Graph,
    start: int,
    end: int,
    serial_path: Optional[List[int]],
    parallel_path: Optional[List[int]],
) -> dict[str, bool]:
    """Resume as validações principais para o experimento."""
    serial_valid = is_valid_path(graph, serial_path, start, end)
    parallel_valid = is_valid_path(graph, parallel_path, start, end)

    return {
        "serial_valid": serial_valid,
        "parallel_valid": parallel_valid,
        "same_distance": same_distance(serial_path, parallel_path),
        "both_found_path": serial_path is not None and parallel_path is not None,
    }
