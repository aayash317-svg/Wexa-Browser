"""
Unit tests for Wexa Browser dataset installation and integrity verification.
Validates all 10 installed datasets against manifest, file integrity, and record counts.
"""

import json
from pathlib import Path
import pytest
import pyarrow.parquet as pq

DATASETS_DIR = Path(__file__).resolve().parent.parent / "data" / "datasets"
MANIFEST_PATH = DATASETS_DIR / "manifest.json"


def test_manifest_exists_and_valid():
    assert MANIFEST_PATH.exists(), "Manifest file does not exist"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["total_datasets"] == 10
    assert len(data["datasets"]) == 10
    names = [d["name"] for d in data["datasets"]]
    expected_names = [
        "The Stack",
        "CodeSearchNet",
        "MBPP",
        "HumanEval",
        "SWE-bench",
        "MiniWoB++",
        "WebArena",
        "BrowserGym",
        "Spider",
        "Wexa Custom Dataset"
    ]
    for exp in expected_names:
        assert exp in names, f"Dataset {exp} missing from manifest"


def test_01_the_stack():
    dir_path = DATASETS_DIR / "01_the_stack"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    for fname in ["stack_python_smol.json", "stack_javascript_smol.json", "stack_html_smol.json"]:
        fpath = dir_path / fname
        assert fpath.exists(), f"Missing {fname}"
        assert fpath.stat().st_size > 100_000, f"{fname} is too small"
        with open(fpath, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]
            assert len(lines) > 0
            assert "content" in lines[0]


def test_02_codesearchnet():
    dir_path = DATASETS_DIR / "02_codesearchnet"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    test_parquet = dir_path / "codesearchnet_python_test.parquet"
    val_parquet = dir_path / "codesearchnet_python_val.parquet"
    assert test_parquet.exists() and test_parquet.stat().st_size > 1_000_000
    assert val_parquet.exists() and val_parquet.stat().st_size > 1_000_000
    table = pq.read_table(test_parquet)
    assert table.num_rows > 1000
    assert "func_code_string" in table.column_names or "func_documentation_string" in table.column_names


def test_03_mbpp():
    dir_path = DATASETS_DIR / "03_mbpp"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    mbpp_file = dir_path / "mbpp.jsonl"
    assert mbpp_file.exists()
    with open(mbpp_file, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]
    assert len(records) == 974
    sample = records[0]
    assert "text" in sample and "code" in sample and "test_list" in sample


def test_04_humaneval():
    dir_path = DATASETS_DIR / "04_humaneval"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    he_file = dir_path / "HumanEval.jsonl"
    assert he_file.exists()
    with open(he_file, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]
    assert len(records) == 164
    sample = records[0]
    assert "task_id" in sample and "prompt" in sample and "test" in sample


def test_05_swe_bench():
    dir_path = DATASETS_DIR / "05_swe_bench"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    dev_parquet = dir_path / "swe_bench_lite_dev.parquet"
    test_parquet = dir_path / "swe_bench_lite_test.parquet"
    assert dev_parquet.exists() and dev_parquet.stat().st_size > 50_000
    assert test_parquet.exists() and test_parquet.stat().st_size > 500_000
    table = pq.read_table(dev_parquet)
    assert table.num_rows > 0
    assert "instance_id" in table.column_names
    assert "patch" in table.column_names


def test_06_miniwob():
    dir_path = DATASETS_DIR / "06_miniwob"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    catalog_file = dir_path / "miniwob_tasks_catalog.json"
    assert catalog_file.exists()
    with open(catalog_file, "r", encoding="utf-8") as f:
        tasks = json.load(f)
    assert len(tasks) >= 100
    assert "env_id" in tasks[0]


def test_07_webarena():
    dir_path = DATASETS_DIR / "07_webarena"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    raw_file = dir_path / "test.raw.json"
    assert raw_file.exists()
    with open(raw_file, "r", encoding="utf-8") as f:
        tasks = json.load(f)
    assert len(tasks) == 812
    sample = tasks[0]
    assert "task_id" in sample and "intent" in sample and "start_url" in sample


def test_08_browsergym():
    dir_path = DATASETS_DIR / "08_browsergym"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    schema_file = dir_path / "action_space_schema.json"
    assert schema_file.exists()
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert "action_spaces" in schema
    assert len(schema["action_spaces"]) >= 8


def test_09_spider():
    dir_path = DATASETS_DIR / "09_spider"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    train_parquet = dir_path / "spider_train.parquet"
    val_parquet = dir_path / "spider_validation.parquet"
    assert train_parquet.exists() and train_parquet.stat().st_size > 500_000
    assert val_parquet.exists() and val_parquet.stat().st_size > 50_000
    table = pq.read_table(train_parquet)
    assert table.num_rows > 1000
    assert "query" in table.column_names or "question" in table.column_names


def test_10_wexa_custom():
    dir_path = DATASETS_DIR / "10_wexa_custom"
    assert dir_path.is_dir()
    assert (dir_path / "README.md").exists()
    required_files = [
        "page_understanding.jsonl",
        "editor_detection.jsonl",
        "permissions_and_safety.jsonl",
        "code_insertion.jsonl",
        "recovery.jsonl",
        "wexa_train.jsonl",
        "wexa_eval.jsonl"
    ]
    for rf in required_files:
        p = dir_path / rf
        assert p.exists(), f"Missing custom file {rf}"
        with open(p, "r", encoding="utf-8") as f:
            lines = [l for l in f if l.strip()]
        assert len(lines) > 0, f"File {rf} is empty"
