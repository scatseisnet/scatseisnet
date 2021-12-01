import subprocess
#minimum python 3.7+

def test_inventory():    
    p = subprocess.run(["scatseisnet", "inventory", "--datapath", "./tests/data/YH.DC06..BH{channel}_{tag}.sac"], capture_output=True, text=True)
    stdout = p.stdout
    stderr = p.stderr

    assert "saved" in stdout
    assert "Error" not in stderr


def test_transform():
    p = subprocess.run(["scatseisnet", "transform"], capture_output=True, text=True)
    stdout = p.stdout
    stderr = p.stderr

    assert "Saved" in stdout
    assert "Error" not in stderr


def test_features():
    p = subprocess.run(["scatseisnet", "features"], capture_output=True, text=True)
    stdout = p.stdout
    stderr = p.stderr

    assert "Saved" in stdout
    assert "Error" not in stderr


def test_linkage():
    p = subprocess.run(["scatseisnet", "linkage"], capture_output=True, text=True)
    stdout = p.stdout
    stderr = p.stderr

    assert "Saved" in stdout
    assert "Error" not in stderr