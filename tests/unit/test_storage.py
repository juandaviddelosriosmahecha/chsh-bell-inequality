"""Unit tests: record round-trip and no-silent-overwrite guarantee."""

import pytest

from beyond_chsh.data.schemas import ExperimentRecord, SettingRecord, new_experiment_id
from beyond_chsh.data.storage import load_record, save_record


def _make_record() -> ExperimentRecord:
    return ExperimentRecord(
        experiment_id=new_experiment_id(),
        mode="ideal",
        config={"shots": 100},
        settings=[
            SettingRecord(x=0, y=0, alice_angle=0.0, bob_angle=0.1,
                          counts={"00": 50, "11": 50}, shots=100)
        ],
        seed=42,
    )


def test_record_roundtrip(tmp_path):
    rec = _make_record()
    path = save_record(rec, tmp_path)
    loaded = load_record(path)
    assert loaded.experiment_id == rec.experiment_id
    assert loaded.mode == "ideal"
    assert loaded.settings[0].counts == {"00": 50, "11": 50}
    assert loaded.seed == 42


def test_no_silent_overwrite(tmp_path):
    rec = _make_record()
    save_record(rec, tmp_path)
    with pytest.raises(FileExistsError):
        save_record(rec, tmp_path)
    # Explicit overwrite is allowed.
    save_record(rec, tmp_path, overwrite=True)
