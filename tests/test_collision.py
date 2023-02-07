from ..src.entities.sprite import Sprite
import pytest


def test_rect():
    sprite = Sprite('assets/HUD/Heart.png')

    assert sprite.rect.x >= 0


