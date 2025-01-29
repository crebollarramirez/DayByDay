# Day by Day Documenation

## About this Project
---
I have always struggled with keeping a good schedule. To manage, I used a written planner but later found it inconvenent because I would lose it.
I later resorted to using Apple's calander app for a while but I later stopped because of how much I manually needed to add events. I later realized
that I wanted to find a way to make it easier to organize big plans that I wanted to complete. I was thinking of an app where it organized almost every aspect of my life which includes, meals, exercise, homework assignments, and long term goals. Of couse, I wanted it to be A.I powered to make it easier to make plans and have a little assistent help you accomplish your goals.

## Table of Contents
---
1. [About This Project](#about-this-project)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [How to start the app](#how-to-start-up-the-app)
5. [Developer Notes](#developer-notes)



## Technologies Used
---
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)

## How to start up the app
---

### Start Frontend React.js

```
npm run dev
```

### Start Backend Server

```
python3 manage.py runserver
```

## Developer Notes
---

### Table of Contents for Project Documentation

1. [Frontend Endpoints](#frontend-endpoints)
2. [Backend Endpoints](#backend-endpoints)

### Frontend Endpoints

- `/` - Home page of the application.
- `/login` - User login page.
- `/register` - User registration page.

### Backend Endpoints

- `POST /api/create` - Create a new task or todo.
- `GET /api/todos/<str:Date>` - Get all todos for the date given. 
- `GET /api/tasks/<int:Month>` - Get all tasks for that month. 
- `PUT /api/edit/<str:item_id>` - Update an existing task or todo.
- `DELETE /api/delete/<str:item_id>` - Delete a task or todo.


### API Request Template

To ensure smooth communication between the frontend and backend, here is a template for making API requests:

#### Backend Endpoints

**Create a new todo**

```
URL: {BASE_URL}/api/create
Method: POST
Headers:
    Content-Type: application/json
    Authorization: Bearer your_token_here
Body:
{
    "content": "Complete project report", 
    "date": "MM-DD-YYYY",
    "item_type: "TODO",
}
```

**Get all todos for the day**
```
URL: {BASE_URL}/api/todos/<str:Date>
Method: GET
Headers:
    Content-Type: application/json
    Authorization: Bearer your_token_here
Body: {}
```

**Edit Todo or Task**
```
URL: {BASE_URL}/api/edit/<str:item_id>
Method: PUT
Headers:
    Content-Type: application/json
    Authorization: Bearer your_token_here
Body: {
    [ANY ATTRIBUTES YOU WANT TO UPDATE]
}
```

**Delete Todo or Task**
```
URL: {BASE_URL}/api/<str:item_id>
Method: DELETE
Headers:
    Content-Type: application/json
    Authorization: Bearer your_token_here
Body: {}
```

**Create a new task**
```
URL: {BASE_URL}/api/create
Method: POST
Headers:
    Content-Type: application/json
    Authorization: Bearer your_token_here
Body:
{
    "title": "title of task"
    "content": "content of task",
    "date": "MM-DD-YYYY",
    "item_type": "TASK",
    "timeFrame": ['HH:MM', 'HH:MM']
}
```

**Get all tasks for the month**
```
URL: {BASE_URL}/api/tasks/<int:Month>
Method: GET
Headers:
    Content-Type: application/json
    Authorization: Bearer your_token_here
Body: {}
```