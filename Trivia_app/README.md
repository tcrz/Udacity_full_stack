# Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game. Since it needed an API to fully function, I worked on building it and have now brought this trivia app to life! The application does the following:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


## Starting the project

Firstly, you will need to [clone](https://help.github.com/en/articles/cloning-a-repository) this repository to your machine.

## Backend
### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Running Flask
The flask app is responsible for setting up the API endpoints. In order to run flask, you must be in the `backend` folder. Next export the flask env variables:
```bash
> export FLAST_APP=flaskr
> export FLASK_ENV=development
```
Now you can run the flask app using:
```bash
> flask run
```
Open [http://localhost:5000](http://localhost:5000) to view it in the browser.


## Frontend
### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```
3. **Start the app**
   The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.
   
```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.



## API Documentation
This app can only be run locally. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 405,
    "message": "Method not allowed"
}
```
The API will return three error types when requests fail:
- 405: Method not allowed
- 404: Not found
- 422: Unprocessable 

### Endpoints 
#### `GET '/categories'`
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Sample: `curl http://127.0.0.1:5000/categories`
```json
{
  "categories": { 
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
  }
}
```

#### `GET '/questions?page=${integer}'`
- General:
    - Fetches a paginated set of questions, a total number of questions and all categories.
    - Request Arguments: page - integer
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`
```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 2
        },
    ],
    "total_questions": 20,
    "categories": { 
     "1": "Science",
     "2": "Art",
     "3": "Geography",
     "4": "History",
     "5": "Entertainment",
     "6": "Sports"
     }
}
```

#### `DELETE '/questions/${id}'`
- General:
    - Deletes a specified question using the id of the question
    - Request Arguments: id - integer 
    - Return: a dictionary containing the id of the deleted object, success of the request and total number of questions
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/10`
```json
{
  "question_deleted_id": 10, 
  "success": true, 
  "total_questions": 19
}
```

#### `POST '/questions'`
- General:
    - Creates and stores a question object
    - Return: a dictionary containing the id of the created question object, success of the request and total nmber of questions
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the nickname of the Ghana men's football team?", "answer":"Black Stars","category": "6", "difficulty":"3"}' http://127.0.0.1:5000/questions`
```json
{
  "question_created_id": 32, 
  "success": true, 
  "total_questions": 20
}
```

#### `POST '/search_questions'`
- General:
    - Sends a post request in order to search for a specific question by search term
    - Request Body example:
    ```json
    {
    "searchTerm": "title"
    }

    ```
    - Return: a dictionary containing the list of questions and total number of questions that match search query
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}' http://127.0.0.1:5000/search_questions`
```json
{
     "questions": [
       {
         "answer": "Maya Angelou", 
         "category": 4, 
         "difficulty": 2, 
         "id": 5, 
         "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
       }, 
       {
         "answer": "Edward Scissorhands", 
         "category": 5, 
         "difficulty": 3, 
         "id": 6, 
         "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
       }
     ], 
     "total_questions": 2
}
```

#### `GET '/categories/${id}/questions'`
- General:
    - Fetches questions for a cateogry specified by id request argument
    - Request Arguments: id - integer 
    - Returns: A dictionary with questions for the specified category, total questions, and current category string
- Sample: `curl localhost:5000/categories/6/questions`
```json
{
  "current_category": "Sports", 
  "questions": [
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "Black Stars", 
      "category": 6, 
      "difficulty": 3, 
      "id": 32, 
      "question": "What is the nickname of the Ghana mens football team?"
    }
  ], 
  "total_questions": 2
}
```

#### `POST '/quizzes'`
- General:
   - Sends a post request in order to get the next question
   - Request body example:
   ```json
   {
    "previous_questions": [1, 4, 20, 15]
    "quiz_category": 'current category'
   }
   ```
   - Returns: a single new question object
- Sample response:
```json
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
```




