from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.post import Post
from flask_app.models.user import User


@app.route('/createPost', methods=['POST'])
def createPost():

    if not Post.validate_post(request.form):
        return redirect(request.referrer)
    data = {
        'user_id': session['user_id'],
        'namePost':request.form['namePost'],
        'description':request.form['description'],
        'instruction':request.form['instruction'],
        'date':request.form['date']        
        }
    Post.create_post(data)
    return redirect('/')

@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'post_id': id,
        'user_id': session['user_id']
    }
    Post.addLike(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'post_id': id,
        'user_id': session['user_id']
    }
    Post.removeLike(data)
    return redirect(request.referrer)

@app.route('/delete/<int:id>')
def destroyPost(id):
    data = {
        'post_id': id,
    }
    post = Post.get_post_by_id(data)
    if session['user_id']==post['user_id']:
        Post.deleteAllLikes(data)
        Post.destroyPost(data)
        return redirect(request.referrer)
    return redirect(request.referrer)
    
@app.route('/update/<int:id>')
def updateForm(id):
    data = {
        'post_id': id,
    }
    post = Post.get_post_by_id(data)
    return render_template('update.html', post=post)

@app.route('/updatePost/<int:id>', methods=['POST'])
def updatePost(id):
    data = {
        'post_id': id,
    }
    post = Post.get_post_by_id(data)
    if session['user_id']==post['user_id']:
        if not Post.validate_post(request.form):
            return redirect(request.referrer)
        data2 = {
        'post_id':id,
        'user_id': session['user_id'],
        'namePost':request.form['namePost'],
        'description':request.form['description'],
        'instruction':request.form['instruction'],
        'date':request.form['date']        
        }
        Post.update_post(data2)
        return redirect('/')
    return redirect('/')

@app.route('/post/<int:id>')
def singlePost(id):
    data = {
        'post_id': id,
        'user_id': session['user_id']

    }
    user = User.get_user_by_id(data)
    post = Post.get_post_by_id(data)
    nrLikes=Post.getPostLikes(data)
    return render_template('singlePost.html', post=post, loggedUser=user, nrLikes=nrLikes)