from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
class Recipe:
    @staticmethod
    def validate_edit(form):
        is_valid = True
        if len(form['name']) < 2:
            flash("Name must be longer than 2 characters")
            is_valid = False
        if len(form['description']) < 2:
            flash("Description must be longer than 2 characters")
            is_valid = False
        if len(form['instructions']) < 0:
            flash("Instructions must not be blank")
            is_valid = False
        if len(form['description']) < 0:
            flash("Instructions must not be blank")
            is_valid = False
        return is_valid

    def __init__( self , data ):
        self.id = data['id']
        self.users_id = data['users_id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.time_taken = data['time_taken']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
# Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes').query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    
    # @classmethod
    # def search_one(cls,request):
    #     query = f"SELECT * FROM users WHERE email = {request}"
    #     results = connectToMySQL('recipes').query_db(query)
    #     EqualNames = []
    #     for name in results:
    #         EqualNames.append(cls(name))
    #     return EqualNames

    @classmethod
    def add_one(cls,data):
        query = "INSERT INTO recipes ( users_id , name , description, instruction, date_cooked, time_taken ) VALUES ( %(id)s , %(name)s , %(description)s , %(instructions)s, %(datecooked)s, %(underThirty)s);" 
        return connectToMySQL('recipes').query_db(query, data)
    @classmethod
    def edit(cls,data):
        query = "UPDATE recipes Set name = %(name)s, description = %(description)s, instruction = %(instructions)s, date_cooked = %(datecooked)s, time_taken = %(underThirty)s WHERE id = %(ID)s"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE from recipes WHERE id = %(ID)s"
        return connectToMySQL('recipes').query_db(query, data)

