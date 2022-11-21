from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

#Creation of the class of Post
class Post:
    db_name='recipeAssig' # Our database name in the workbench
    def __init__(self,data):
        self.id = data['id'],
        self.namePost = data['name'],
        self.description = data['description'],
        self.instruction = data['instruction'],
        self.date = data['date'],
        self.user_id = data['user_id'],
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    

    @classmethod
    def getAllPosts(cls):
        query= 'SELECT *, COUNT(likes.id) as likesNr, posts.user_id as creator_id, email FROM posts LEFT JOIN users on posts.user_id = users.id LEFT JOIN likes on likes.post_id = posts.id GROUP BY posts.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        posts= []
        for row in results:
            posts.append(row)
        return posts
        
    @classmethod
    def create_post(cls,data):
        query = 'INSERT INTO posts (namePost, description, instruction,date, user_id) VALUES ( %(namePost)s,%(description)s,%(instruction)s,%(date)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_post(cls,data):
        query = 'UPDATE posts SET namePost=%(namePost)s, description=%(description)s, instruction=%(instruction)s,date=%(date)s, user_id=%(user_id)s WHERE posts.id=%(post_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_post_by_id(cls, data):
        query= 'SELECT * FROM posts WHERE posts.id = %(post_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]


    @classmethod
    def get_user_posts(cls, data):
        query= 'SELECT * FROM users LEFT JOIN posts on posts.user_id = users.id WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        posts = []
        for row in results:
            posts.append(row)
        return posts

    @classmethod
    def addLike(cls, data):
        query= 'INSERT INTO likes (post_id, user_id) VALUES ( %(post_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeLike(cls, data):
        query= 'DELETE FROM likes WHERE post_id = %(post_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def destroyPost(cls, data):
        query= 'DELETE FROM posts WHERE posts.id = %(post_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def deleteAllLikes(cls, data):
        query= 'DELETE FROM likes WHERE likes.post_id = %(post_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['namePost']) < 2:
            flash("Recipe name must be at least 2 characters.", 'namePost')
            is_valid = False
        if len(post['description']) < 2:
            flash("Recipe description must be at least 2 characters.", 'description')
            is_valid = False
        if len(post['instruction']) < 2:
            flash("Recipe instruction  must be at least 2 characters.", 'instruction')
            is_valid = False
        if post['date']=='':
            flash("Recipe date must not be empty.", 'date')
            is_valid = False
        return is_valid