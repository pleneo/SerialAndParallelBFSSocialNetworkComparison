"""Mede o tempo das execuções serial e paralela."""

from __future__ import annotations

import statistics
import time
from typing import Any, Callable


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
