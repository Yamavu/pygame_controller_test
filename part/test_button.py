from .button import GenericButton, Button, Shape
import pytest


def test_cannot_instantiate_button_protocol():
    """
    Verifies that the abstract Button class cannot be instantiated directly.
    """
    msg = r"Protocols cannot be instantiated"
    with pytest.raises(TypeError, match=msg):
        GenericButton("Protocol", (0, 0))


@pytest.fixture
def button():
    b = Button("A", (0, 0), shape=Shape.Round, radius=15.0)
    return b


def test_radius(button):
    assert button.radius == 15


def test_activate(button):
    assert not button.active
    button.pressed()
    assert button.active
    button.released()
    assert not button.active
