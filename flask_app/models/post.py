from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

#Creation of the class of Post
class Post:
    db_name='beltExam' # Our database name in the workbench
    def __init__(self,data):
        self.id = data['id'],
        self.description = data['description'],
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
    def getPostLikes(cls,data):
        query= 'SELECT  COUNT(likes.id) as nrLikes FROM likes WHERE likes.post_id=%(post_id)s GROUP BY likes.post_id;'
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        if results:
            return results[0]
        return False

    @classmethod
    def create_post(cls,data):
        query = 'INSERT INTO posts ( description, user_id) VALUES ( %(description)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_post(cls,data):
        query = 'UPDATE posts SET description=%(description)s, user_id=%(user_id)s WHERE posts.id=%(post_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_post_by_id(cls, data):
        query= 'SELECT * FROM posts LEFT JOIN users on posts.user_id=users.id WHERE posts.id = %(post_id)s;'
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
        if len(post['description']) < 2:
            flash("Thought must not be empty!", 'description')
            is_valid = False
        return is_valid