"""Open-format persistence for experiment records (JSON) and tables (CSV).

Never silently overwrites: :func:`save_record` refuses to clobber an existing
file unless ``overwrite=True``.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .schemas import ExperimentRecord


def save_record(
    record: ExperimentRecord, directory: str | Path, *, overwrite: bool = False
) -> Path:
    """Write an :class:`ExperimentRecord` to ``<directory>/<id>.json``."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{record.experiment_id}.json"
    if path.exists() and not overwrite:
        raise FileExistsError(
            f"{path} exists; refusing to overwrite (pass overwrite=True)"
        )
    path.write_text(json.dumps(record.to_dict(), indent=2, sort_keys=True))
    return path


def load_record(path: str | Path) -> ExperimentRecord:
    """Load an :class:`ExperimentRecord` from a JSON file."""
    data = json.loads(Path(path).read_text())
    return ExperimentRecord.from_dict(data)


def write_table(rows: list[dict], path: str | Path) -> Path:
    """Write a list of flat dict rows to CSV (columns from the first row)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("no rows to write")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path
