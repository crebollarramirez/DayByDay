# Day by Day

I have always struggled with keeping a good schedule. To manage, I used a written planner but later found it inconvenent because I would lose it.
I later resorted to using Apple's calander app for a while but I later stopped because of how much I manually needed to add events. I later realized
that I wanted to find a way to make it easier to organize big plans that I wanted to complete. I was thinking of an app where it organized almost every aspect of my life which includes, meals, exercise, homework assignments, and long term goals. Of couse, I wanted it to be A.I powered to make it easier to make plans and have a little assistent help you accomplish your goals.

---

## Table of Contents

1. [About This Project](#about-this-project)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [How to start the app](#how-to-start-up-the-app)

## About this Project

## Technologies Used

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![AmazonDynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)

## How to start up the app

### Start Frontend React.js

```
npm run dev
```

### Start Backend Server

```
python3 manage.py runserver
```

## Developer Notes

## Developer Notes

### Table of Contents for Project Documentation

1. [Frontend Endpoints](#frontend-endpoints)
2. [Backend Endpoints](#backend-endpoints)

### Frontend Endpoints

- `/home` - Home page of the application.
- `/login` - User login page.
- `/register` - User registration page.
- `/dashboard` - User dashboard with personalized schedule.

### Backend Endpoints

- `GET /api/tasks` - Retrieve all tasks.
- `POST /api/tasks` - Create a new task.
- `PUT /api/tasks/:id` - Update an existing task.
- `DELETE /api/tasks/:id` - Delete a task.
- `GET /api/schedule` - Get the suggested schedule for the week.

### API Request Template

To ensure smooth communication between the frontend and backend, here is a template for making API requests:

#### Backend Endpoints

```
URL: {BASE_URL}/{ENDPOINT}
Method: {HTTP_METHOD}
Headers:
    Content-Type: application/json
    Authorization: Bearer {TOKEN}
Body:
{
    "key1": "value1",
    "key2": "value2",
    ...
}
```

#### Example

**Create a new todo**

```
URL: {BASE_URL}/api/todos
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

**Create a new task**

```
URL: {BASE_URL}/api/tasks
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

**Get all todos for the month**
```
URL: {BASE_URL}/api/todos/<str:Date>
Method: GET
Headers:
    Content-Type: application/json
    Authorization: Bearer your_token_here
Body: {}

```

