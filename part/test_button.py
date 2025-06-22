from .button import Button, Button1
import pytest


def test_cannot_instantiate_abstract_button():
    """
    Verifies that the abstract Button class cannot be instantiated directly.
    """
    msg = "Can't instantiate abstract class Button with abstract method draw"
    with pytest.raises(TypeError, match=msg):
        Button("Abstract", (0, 0))


@pytest.fixture
def button():
    b = Button1("A", (0, 0), radius=15.0)
    return b


def test_radius(button):
    assert button.radius == 15


def test_activate(button):
    assert not button.active
    button.pressed()
    assert button.active
    button.released()
    assert not button.active
