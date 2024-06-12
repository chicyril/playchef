#!/usr/bin/env python3
"""This module contains service functions for the app."""
import os
import secrets
from PIL import Image


def save_img(folder, img_obj):
    """Save image in folder in disk."""
    random_hex = secrets.token_hex(16)
    _, ext = os.path.splitext(img_obj.filename)
    recipe_img_filename = f'{random_hex}{ext}'
    recipe_img_path = os.path.join(folder, recipe_img_filename)

    resize = (125, 125)
    img = Image.open(img_obj)
    img.thumbnail(resize)
    img.save(recipe_img_path)

    return recipe_img_filename


def del_img(folder, img_filename):
    """Delete image from disk."""
    recipe_img_path = os.path.join(folder, img_filename)
    try:
        os.remove(recipe_img_path)
    except OSError:
        pass
