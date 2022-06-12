import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def all_categories():
        categories_dict = {'categories':{}}
        for category in Category.query.order_by(Category.id).all():
            categories_dict['categories'][str(category.id)] = category.type
 #       print(categories_dict)
        return jsonify(categories_dict)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def all_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        # Retrive categories dict
        dict = all_categories().get_json()

        total_questions = Question.query.count()
        questions = [ question.format() for question in Question.query.all() ]
        if len(questions[start:end]) == 0:
            abort(404)

        # append dict with additional key/pair values
        dict['questions'] = questions[start:end]
        dict['total_questions'] = total_questions
#        dict['current_category'] = 'Sports'
#        print(dict)
        return jsonify(dict)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def del_question(id):
        """deletes a question"""
        question = Question.query.get(id)
        if question is None:
            abort(404)
        question.delete()
        return jsonify({'success': True, 'question_deleted_id':id, 'total_questions': Question.query.count()})

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():
        """creates a new question"""
        try:
            question = Question(**request.get_json())
            question.insert()
            return jsonify({'success': True, 'question_created_id':question.id, 'total_questions': Question.query.count()})
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search_questions', methods=['POST'])
    def search_questions():
        """search for question"""
        try:
            query = request.get_json()['searchTerm']
            results = Question.query.filter(Question.question.ilike('%{}%'.format(query))).all()
            questions = [ question.format() for question in results ]
            dict = {'questions':questions, 'total_questions': len(results)}
#           print(dict)
            return jsonify(dict)
        except:
            abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def category_questions(id):
        """get questions by categories"""
        category = Category.query.get(id)
        if category is None:
            abort(404)
        questions = [ question.format() for question in category.questions ]
        total_questions = len(questions)
        dict = {'questions':questions, 'total_questions':total_questions, 'current_category':category.type}
#        print(dict)
        return jsonify(dict)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
       """returns random questions for the game"""
       req = request.get_json()
       prev_questions = req['previous_questions']
#       print(prev_questions)
       questions = []
       if req['quiz_category']['id'] == 0:
           questions = Question.query.all()
       else:
           category_id = req['quiz_category']['id']
           category = Category.query.get(category_id)
           if category is None:
                abort(404)
           questions = category.questions
       #print(questions)
       for question in list(questions):
           if question.id in prev_questions:
               questions.remove(question)
       if len(questions) != 0:
           rand_question = random.choice(questions)
           return jsonify({'question': rand_question.format()})
       else:
           return jsonify({'question': False})
#       print(request.get_json())
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success":False, "error":"404", "message":"Not found"}), 404

    @app.errorhandler(405)
    def not_allowed_method(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Method not allowed"}),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
            422,
        )

    return app
