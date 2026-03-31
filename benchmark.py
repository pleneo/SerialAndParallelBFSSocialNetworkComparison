"""Mede o tempo das execuções serial e paralela."""

from __future__ import annotations

import statistics
import time
from typing import Any, Callable


import matplotlib.pyplot as plt

from bfs_parallel import parallel_bfs_shortest_path
from bfs_serial import bfs_shortest_path
from social_media_graph_gen import generate_social_graph, pick_distinct_users
from validation import path_distance, validate_both_results


def measure_execution(
    fn: Callable[..., Any],
    *args: Any,
    repeats: int = 5,
    **kwargs: Any,
) -> dict[str, Any]:
    """Executa uma função várias vezes e resume seus tempos."""
    if repeats < 1:
        raise ValueError("repeats deve ser maior ou igual a 1.")

    times: list[float] = []
    last_result = None

    for _ in range(repeats):
        start_time = time.perf_counter()
        last_result = fn(*args, **kwargs)
        end_time = time.perf_counter()
        times.append(end_time - start_time)

    return {
        "result": last_result,
        "times": times,
        "avg_time": statistics.mean(times),
        "min_time": min(times),
        "max_time": max(times),
        "std_dev": statistics.stdev(times) if len(times) > 1 else 0.0,
    }


def compute_speedup(serial_time: float, parallel_time: float) -> float:
    """Calcula o speedup da execução paralela."""
    if parallel_time <= 0:
        raise ValueError("parallel_time deve ser maior que zero.")

    return serial_time / parallel_time


def compare_executions(
    serial_fn: Callable[..., Any],
    parallel_fn: Callable[..., Any],
    serial_args: tuple[Any, ...],
    parallel_args: tuple[Any, ...],
    repeats: int = 5,
    serial_kwargs: dict[str, Any] | None = None,
    parallel_kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Executa os dois modos e devolve as métricas comparativas."""
    serial_stats = measure_execution(
        serial_fn,
        *serial_args,
        repeats=repeats,
        **(serial_kwargs or {}),
    )
    parallel_stats = measure_execution(
        parallel_fn,
        *parallel_args,
        repeats=repeats,
        **(parallel_kwargs or {}),
    )

    return {
        "serial": serial_stats,
        "parallel": parallel_stats,
        "speedup": compute_speedup(
            serial_stats["avg_time"],
            parallel_stats["avg_time"],
        ),
    }


def run_scalability_benchmark(
    graph_sizes: list[int],
    avg_friends: int,
    repeats: int = 5,
    seed: int = 42,
    max_workers: int = 4,
    num_blocks: int | None = None,
) -> list[dict[str, Any]]:
    """Executa a bateria de escalabilidade em múltiplos tamanhos de grafo."""
    results: list[dict[str, Any]] = []

    for index, num_users in enumerate(graph_sizes):
        graph_seed = seed + index
        pair_seed = seed + 10_000 + index

        graph = generate_social_graph(num_users, avg_friends, graph_seed)
        start, end = pick_distinct_users(graph, pair_seed)

        comparison = compare_executions(
            bfs_shortest_path,
            parallel_bfs_shortest_path,
            serial_args=(graph, start, end),
            parallel_args=(graph, start, end),
            repeats=repeats,
            parallel_kwargs={
                "max_workers": max_workers,
                "num_blocks": num_blocks,
            },
        )

        validation = validate_both_results(
            graph,
            start,
            end,
            comparison["serial"]["result"],
            comparison["parallel"]["result"],
        )

        results.append(
            {
                "num_users": num_users,
                "avg_friends": avg_friends,
                "start": start,
                "end": end,
                "distance": path_distance(comparison["serial"]["result"]),
                "serial_avg_time": comparison["serial"]["avg_time"],
                "parallel_avg_time": comparison["parallel"]["avg_time"],
                "serial_min_time": comparison["serial"]["min_time"],
                "parallel_min_time": comparison["parallel"]["min_time"],
                "serial_max_time": comparison["serial"]["max_time"],
                "parallel_max_time": comparison["parallel"]["max_time"],
                "serial_std_dev": comparison["serial"]["std_dev"],
                "parallel_std_dev": comparison["parallel"]["std_dev"],
                "speedup": comparison["speedup"],
                "serial_path": comparison["serial"]["result"],
                "parallel_path": comparison["parallel"]["result"],
                "serial_valid": validation["serial_valid"],
                "parallel_valid": validation["parallel_valid"],
                "same_distance": validation["same_distance"],
                "both_found_path": validation["both_found_path"],
            }
        )

    return results


def format_results_table(results: list[dict[str, Any]]) -> str:
    """Formata os resultados em tabela de texto."""
    headers = [
        "Nos",
        "GrauMedio",
        "Distancia",
        "SerialMedio(s)",
        "ParaleloMedio(s)",
        "Speedup",
        "Valido",
    ]
    rows = []

    for result in results:
        valid = (
            result["serial_valid"]
            and result["parallel_valid"]
            and result["same_distance"]
            and result["both_found_path"]
        )
        rows.append(
            [
                str(result["num_users"]),
                str(result["avg_friends"]),
                str(result["distance"]),
                f'{result["serial_avg_time"]:.6f}',
                f'{result["parallel_avg_time"]:.6f}',
                f'{result["speedup"]:.3f}x',
                "Sim" if valid else "Nao",
            ]
        )

    widths = [
        max(len(header), *(len(row[index]) for row in rows))
        for index, header in enumerate(headers)
    ]

    def format_row(values: list[str]) -> str:
        return " | ".join(
            value.ljust(widths[index])
            for index, value in enumerate(values)
        )

    separator = "-+-".join("-" * width for width in widths)
    table_lines = [format_row(headers), separator]
    table_lines.extend(format_row(row) for row in rows)
    return "\n".join(table_lines)


def plot_scalability_results(results: list[dict[str, Any]]) -> None:
    """Exibe um gráfico com tempos médios e speedup por tamanho de grafo."""
    graph_sizes = [result["num_users"] for result in results]
    serial_times = [result["serial_avg_time"] for result in results]
    parallel_times = [result["parallel_avg_time"] for result in results]
    speedups = [result["speedup"] for result in results]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(graph_sizes, serial_times, marker="o", label="Serial")
    axes[0].plot(graph_sizes, parallel_times, marker="o", label="Paralelo")
    axes[0].set_title("Tempo medio por tamanho do grafo")
    axes[0].set_xlabel("Numero de usuarios")
    axes[0].set_ylabel("Tempo medio (s)")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(graph_sizes, speedups, marker="o", color="darkgreen")
    axes[1].axhline(1.0, color="gray", linestyle="--", linewidth=1)
    axes[1].set_title("Speedup por tamanho do grafo")
    axes[1].set_xlabel("Numero de usuarios")
    axes[1].set_ylabel("Speedup")
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()


    plt.show()
