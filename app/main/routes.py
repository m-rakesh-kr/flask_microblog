from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm, EditPostForm
from app.models import User, Post, Like, Comment
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/about')
def about():
    current_year = datetime.now().year
    return render_template('about.html', title="About", current_year=current_year)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!', 'info')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    """
        Here we have used ternary conditional expression" or "ternary operator.
        It's a way to express a conditional check and assign a value based on 
        whether the condition is true or false"
    """
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None

    # Get users that the current user is not following
    unfollowed_users = User.query.filter(User.id != current_user.id).filter(
        ~User.id.in_(current_user.followed.with_entities(User.id))
    ).all()

    current_year = datetime.now().year
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url, unfollowed_users=unfollowed_users, current_year=current_year)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    """
        Here we have used ternary conditional expression" or "ternary operator.
        It's a way to express a conditional check and assign a value based on 
        whether the condition is true or false"
    """
    next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None

    return render_template("index.html", title='Explore',
                           posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    """
        debugging methods and functions...
    """
    # print("POSTTTTTTTTTTTTTTTTTTTTTTTT", dir(posts))
    # print(posts.items)
    # print(help(posts))
    # for post in posts.items:
    #     print(dir(post))
    #     print(vars(post))

    """
        Here we have used ternary conditional expression" or "ternary operator.
        It's a way to express a conditional check and assign a value based on 
        whether the condition is true or false"
    """
    next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None

    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', 'info')
        return redirect(url_for('main.user', username=current_user.username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    # Delete the user's posts (cascades due to the cascade option in User model)
    current_user.posts.delete()

    # Log the user out and delete the user's profile
    db.session.delete(current_user)
    db.session.commit()

    flash('Your profile and all your posts have been deleted.', 'success')
    return redirect(url_for('auth.logout'))  # Redirect to logout or another page


@bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        # You may want to handle unauthorized access here
        flash("Sorry! You cannot edit post of others", 'warning')
        return redirect(url_for('main.index'))

    form = EditPostForm()

    if form.validate_on_submit():
        new_body = form.new_body.data
        post.body = new_body
        db.session.commit()
        return redirect(url_for('main.user', username=post.author.username))

    # Prepopulate the form field with existing post body data
    form.new_body.data = post.body
    return render_template('edit_post.html', title="Edit_Post", form=form, post=post)


@bp.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You don't have permission to delete this post.", 'danger')
        return redirect(url_for('main.index'))

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('main.index'))


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    followers = user.followers.paginate(
        page=page, per_page=current_app.config['FOLLOWERS_PER_PAGE'], error_out=False)
    return render_template('followers.html', user=user, followers=followers)


@bp.route('/following/<username>')
def following(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    following = user.followed.paginate(
        page=page, per_page=current_app.config['FOLLOWERS_PER_PAGE'], error_out=False)
    return render_template('following.html', user=user, following=following)


from flask import jsonify


@bp.route('/unfollowed_users', methods=['GET'])
def get_unfollowed_users():
    unfollowed_users = User.query.filter(User.id != current_user.id).filter(
        ~User.id.in_(current_user.followed.with_entities(User.id))
    ).all()
    return jsonify(users=[user.to_dict() for user in unfollowed_users])


@bp.route('/like_post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the user has already liked the post
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if like:
        db.session.delete(like)
        # flash("You unliked this post")
    else:
        new_like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(new_like)
        # flash("You liked this post")

    db.session.commit()
    return redirect(request.referrer)


@bp.route('/comment_post/<int:post_id>', methods=['POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    comment_body = request.form.get('comment')

    if comment_body:
        new_comment = Comment(body=comment_body, user_id=current_user.id, post_id=post.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been posted.', 'success')
    else:
        flash('Comment body cannot be empty.', 'warning')

    return redirect(url_for('main.index'))  # Change this to wherever you want to redirect after commenting


@bp.route('/view_comments/<int:post_id>')
@login_required
def view_comments(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc()).all()
    # print(comments)
    return render_template('view_comments.html', post=post, comments=comments)
