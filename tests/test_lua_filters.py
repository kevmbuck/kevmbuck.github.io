from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_filters_do_not_use_unavailable_quarto_yaml_helper():
    for filename in ("publications.lua", "projects.lua"):
        source = (ROOT / "filters" / filename).read_text(encoding="utf-8")
        assert "quarto.utils.read_yaml" not in source
        assert "pandoc.read" in source
        assert "read_yaml_sequence(data_path)" in source
