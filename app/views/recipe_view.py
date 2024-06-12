#!/usr/bin/env python3
"""Contain endpoint definitions for recipe."""
from urllib.parse import urlparse
from flask import request, jsonify, current_app, flash, redirect, url_for, render_template
from flask_login import current_user, login_required
from models import Recipe, Category, Ingredient, Step
from app.views import app_views
from app.forms.recipe_form import RecipeForm
from app.forms.csrf_form import CSRFForm
from services import save_img, del_img


@app_views.route('/recipe/create', methods=['GET', 'POST'],
                 strict_slashes=False)
@login_required
def recipe_create():
    """
    This is the endpoint function for handling new recipe creation.
    """

    next = request.args.get('next')

    form = RecipeForm()

    if form.validate_on_submit():
        dir = current_app.config.get('RECIPE_IMG_DIR')
        img = form.image.data
        image_fn = save_img(dir, img) if img else None
        name = form.name.data
        description = form.description.data

        recipe = Recipe(name=name, description=description,
                        user_id=current_user.id, image=image_fn)

        current_app.db.add(recipe)
        current_app.db.commit()

        for ingredient_form in form.ingredients.entries:
            ingredient = Ingredient(name=ingredient_form.form.name.data,
                                    recipe_id=recipe.id)
            current_app.db.add(ingredient)

        for step_form in form.steps.entries:
            step = Step(description=step_form.form.description.data,
                        recipe_id=recipe.id)
            current_app.db.add(step)

        recipe.categories = [Category.query.get(category_id)
                             for category_id in form.categories.data]

        new_category_name = form.new_category.data.strip()
        if new_category_name:
            new_category = Category.query.filter_by(
                name=new_category_name).first()
            if not new_category:
                new_category = Category(name=new_category_name,
                                        user_id=current_user.id)
                current_app.db.add(new_category)
            if new_category not in recipe.categories:
                recipe.categories.append(new_category)

        current_app.db.commit()

        flash('Recipe created successfully!', 'success')

        if next and next != '/None':
            return redirect(next)
        return redirect(request.referrer or url_for('app_views.home'))

    if not next:
        next = urlparse(request.referrer).path
    return render_template('recipe_create.html', form=form,
                           title='Create Recipe', next=next)


@app_views.route('/recipe/edit/<recipe_id>', methods=['GET', 'POST'],
                 strict_slashes=False)
@login_required
def recipe_edit(recipe_id):
    """Endpoint function for recipe editing."""

    recipe = Recipe.query.get(recipe_id)

    if recipe.user != current_user:
        flash('You are not authorized to edit this recipe.', 'danger')
        return redirect(url_for('app_views.home'))

    next = request.args.get('next')

    form = RecipeForm(obj=recipe)
    form.image.label.text = 'Change Image'
    form.submit.label.text = 'Save'

    if form.validate_on_submit():
        if form.image.data:
            old_img_fn = recipe.image
            dir = current_app.config.get('RECIPE_IMG_DIR')
            recipe.image = save_img(dir, form.image.data)
            if old_img_fn != 'recipe_default.jpg':
                del_img(dir, old_img_fn)

        recipe.name = form.name.data
        recipe.description = form.description.data

        recipe.ingredients.clear()
        for ingredient_form in form.ingredients:
            ingredient = Ingredient(name=ingredient_form.form.name.data,
                                    recipe=recipe)
            current_app.db.add(ingredient)

        recipe.steps.clear()
        for step_form in form.steps:
            step = Step(description=step_form.form.description.data,
                        recipe=recipe)
            current_app.db.add(step)

        recipe.categories.clear()
        recipe.categories = [Category.query.get(category_id)
                             for category_id in form.categories.data]

        new_category_name = form.new_category.data.strip()
        if new_category_name:
            new_category = Category.query.filter_by(
                name=new_category_name).first()
            if not new_category:
                new_category = Category(name=new_category_name,
                                        user_id=current_user.id)
                current_app.db.add(new_category)
            if new_category not in recipe.categories:
                recipe.categories.append(new_category)

        current_app.db.commit()

        flash('Recipe updated successfully!', 'success')

        if next and next != '/None':
            return redirect(next)
        return redirect(url_for('app_views.recipe', recipe_id=recipe.id))

    form.categories.data = [c.id for c in recipe.categories]
    if not next:
        next = urlparse(request.referrer).path
    return render_template('recipe_edit.html', recipe=recipe,
                           form=form, next=next)


@app_views.route('/recipe/delete/<recipe_id>', methods=['POST'],
                 strict_slashes=False)
@login_required
def recipe_delete(recipe_id):
    """Endpoint function for recipe deletion."""

    recipe = Recipe.query.get(recipe_id)
    if recipe.user != current_user:
        flash('You are not authorized to delete this recipe.', 'danger')
        return redirect(request.referrer or url_for('app_views.home'))

    csrf_form = CSRFForm()
    if csrf_form.validate_on_submit():
        if recipe.image != 'recipe_default.jpg':
            dir = current_app.config.get('RECIPE_IMG_DIR')
            del_img(dir, recipe.image)
        current_app.db.delete(recipe)
        current_app.db.commit()
        flash('Recipe deleted successfully!', 'success')
        return redirect(request.referrer or url_for('app_views.home'))

    flash('Failed to delete recipe. Invalid CSRF token.', 'danger')
    return redirect(request.referrer or url_for('app_views.home'))


@app_views.route('/recipe/<recipe_id>', strict_slashes=False)
def recipe(recipe_id):
    """Endpoint function for single recipe view."""

    csrf_form = CSRFForm()
    recipe = Recipe.query.get(recipe_id)
    if not current_user.recipes:
        return redirect(url_for('app_views.home'))
    return render_template('recipe.html', recipe=recipe, form=csrf_form)


@ app_views.route('/recipe/filter_recipes', strict_slashes=False)
def filter_recipes():
    """
    Endpoint function for filtering recipes by category in user home.
    """

    category_name = request.args.get('category', 'all')
    if category_name == 'all':
        recipes = Recipe.query.all()
    else:
        category = Category.query.filter_by(name=category_name).first()
        recipes = category.recipes if category else []
    return jsonify({'recipes': [recipe.dicto() for recipe in recipes]})


@app_views.route('/recipe/add_to_favorites/<recipe_id>', methods=['POST'])
@login_required
def add_to_favorites(recipe_id):
    """Endpoint function for add recipes to user favorites."""

    csrf_form = CSRFForm()
    if csrf_form.validate_on_submit():
        recipe = Recipe.query.get(recipe_id)
        current_user.favorites.append(recipe)
        current_app.db.commit()
        flash('Recipe added to favorites!', 'success')
        return redirect(request.referrer or
                        url_for('app_views.recipe', recipe_id=recipe.id))

    flash('Failed to add to favorites.', 'danger')
    return redirect(url_for('app_views.home'))


@app_views.route('/recipe/remove_from_favorites/<recipe_id>', methods=['POST'])
@login_required
def remove_from_favorites(recipe_id):
    """
    Endpoint function for removing recipes from user favorites.
    """

    csrf_form = CSRFForm()
    if csrf_form.validate_on_submit():
        recipe = Recipe.query.get(recipe_id)
        current_user.favorites.remove(recipe)
        current_app.db.commit()
        flash('Recipe removed from favorites!', 'success')
        return redirect(request.referrer or
                        url_for('app_views.recipe', recipe_id=recipe.id))

    flash('Failed to remove from favorites.', 'danger')
    return redirect(url_for('app_views.home'))
