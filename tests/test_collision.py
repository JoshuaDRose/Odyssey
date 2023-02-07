try:
    from src.entities.sprite import Sprite
except ModuleNotFoundError:
    from entities.sprite import Sprite
import pytest

def test_rect():
    sprite = Sprite('assets/HUD/Heart.png', 50, 50)
    assert (sprite.rect.x and sprite.rect.y >= 0), "Invalid position"
