try:
    from ..src.entities.sprite import Sprite
except (ModuleNotFoundError, ImportError):
    from entities.sprite import Sprite
except ModuleNotFoundError:
    import os
    print(os.getcwd())
import pytest

def test_rect():
    sprite = Sprite('assets/HUD/Heart.png', 50, 50)
    assert (sprite.rect.x and sprite.rect.y >= 0), "Invalid position"
