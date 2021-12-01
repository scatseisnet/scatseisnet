import subprocess
import pytest

def test_transform():
    p = subprocess.run(["scatseisnet", "transform", "-x"], capture_output=True, text=True)
    stdout = p.stdout
    stderr = p.stderr

    assert "No such option" in stderr