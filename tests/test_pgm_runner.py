import pytest
from click.testing import CliRunner
from pgm.cli.main import main

settings = [('examples/casio3/', 'casio3.yaml'), ('examples/feo/', 'feo.yaml')]


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.mark.parametrize("working_dir, yaml_file", [settings[0]])
def test_casio3_example(cli_runner, working_dir, yaml_file, monkeypatch):
    monkeypatch.chdir(working_dir)
    result = cli_runner.invoke(main, [yaml_file], prog_name="pgm")
    assert result.exit_code == 0
    monkeypatch.undo()


@pytest.mark.parametrize("working_dir, yaml_file", [settings[1]])
def test_feo_example(cli_runner, working_dir, yaml_file, monkeypatch):
    monkeypatch.chdir(working_dir)
    result = cli_runner.invoke(main, [yaml_file], prog_name="pgm")
    assert result.exit_code == 0
    monkeypatch.undo()
