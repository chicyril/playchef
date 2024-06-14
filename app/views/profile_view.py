#!/usr/bin/env python3
"""Contain endpoint definitions for recipe."""
from flask import render_template, url_for, flash, redirect, current_app as app
from flask_login import current_user, login_required
from app.views import app_views
from app.forms.update_profile_form import ProfileUpdateForm
from services import save_img, del_img


@app_views.route('/profile', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def profile():
    """Endpoint for user profile route."""

    form = ProfileUpdateForm(obj=current_user)
    if form.validate_on_submit():
        if form.dp_file.data:
            old_dp_fn = current_user.display_pic
            dir = app.config.get('PROFILE_PIC_DIR')
            current_user.display_pic = save_img(dir, form.dp_file.data)
            if old_dp_fn != 'default.jpg':
                del_img(dir, old_dp_fn)

        current_user.username = form.username.data
        current_user.email = form.email.data
        app.db.commit()
        flash('Your profile has been updated', 'success')
        return redirect(url_for('app_views.profile'))

    return render_template('profile.html', title='Profile', form=form)
