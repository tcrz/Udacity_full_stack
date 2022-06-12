import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.new_question = {"question":"What is the nickname of the Ghana men's football team?", "answer":"Black Stars","category": "6", "difficulty":"3"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Test for /categories endpoint
    def test_all_categories(self):
        """test endpoint for categories"""
        response = self.client().get('/categories')
        self.assertTrue(response.json['categories'])
        self.assertEqual(response.status_code, 200)

    def test_wrong_method_on_all_categories(self):
        """test wrong methods on categories endpoint"""
        response = self.client().post('/categories', json={'question':'blah blah blahh?'})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Method not allowed')

    # Test for /questions endpoint
    def test_all_questions(self):
        """test endpoint for questions"""
        response = self.client().get('/questions')
        questions_num = Question.query.count()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['categories'])
#        self.assertTrue(response.json['current_category'])
        self.assertTrue(response.json['total_questions'], questions_num)
        self.assertTrue(response.json['questions'])

    def test_wrong_pagination_request_on_questions(self):
        """test endpoint for page number with no books"""
        response = self.client().get('/questions?page=4356')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Not found')

    # Test for question creation endpoint
    def test_create_question(self):
        """test endpoint for question creation"""
        response = self.client().post('/questions', json=self.new_question)
        questions_num = Question.query.count()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertTrue(response.json['question_created_id'])
        self.assertTrue(response.json['total_questions'], questions_num)

    def test_wrongjson_create_question(self):
        """test wrong json on question creation endpoint"""
        response = self.client().post('/questions', json={"question": "Is this a test"})
        self.assertEqual(response.status_code, 422)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Unprocessable')


    # Test for deletion endpoint
    def test_del_question(self):
        """test endpoint for question deletion"""
        question_id = Question.query.filter_by(answer='Black Stars').first().id
        response = self.client().delete('/questions/' + str(question_id))
        question = Question.query.get(question_id)
        questions_num = Question.query.count()
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(question)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['question_deleted_id'], question_id)
        self.assertTrue(response.json['total_questions'], questions_num)

    def test_wrongrequest_del_question(self):
        """test wrong request and nonexistent question on delete endpoint"""
        response = self.client().get('/questions/1')
        self.assertEqual(response.status_code, 405)
        self.assertFalse(response.json['success'])
        response = self.client().delete('/question/1122')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Not found')

    # Test questions search endpoint
    def test_search_question(self):
        """test endpoint for searching questions"""
        response = self.client().post('/search_questions', json={'searchTerm':'title'})
        results = response.json['questions']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['questions'])
        self.assertEqual(response.json['total_questions'], len(results))

    def test_wrongrequest_search_question(self):
        """test wrong request method on search endpoint"""
        response = self.client().get('/search_questions')
        self.assertEqual(response.status_code, 405)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Method not allowed')

    # Test categories-questions endpoint
    def test_category_questions(self):
        """test retrieving questions by their categories"""
        response = self.client().get('/categories/6/questions')
        category_name = Category.query.get(6).type
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['questions'])
        self.assertTrue(response.json['total_questions'])
        self.assertEqual(response.json['current_category'], category_name)

    def test_wrongid_category_questions(self):
        """test wrong request for category_questions endpoint"""
        response = self.client().get('/categories/66/questions')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Not found')

    # Test quizzes endpoint
    def test_quizzes(self):
        """test quizzes endpoint"""
        response = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Art', 'id': '2'}})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['question'])

    def test_wrongcategoryid_quizzes(self):
        """test wrong category"""
        response = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Art', 'id': '90'}})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['message'], 'Not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
