from activations import sigmoid

def test_sigmoid():
    assert sigmoid(-1000) == 0
    assert sigmoid(0) == 0.5
    assert sigmoid(1000) == 1