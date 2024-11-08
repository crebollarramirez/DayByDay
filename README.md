# Day by Day Documenation

## About this Project

I have always struggled with keeping a good schedule. To manage, I used a written planner but later found it inconvenent because I would lose it.
I later resorted to using Apple's calander app for a while but I later stopped because of how much I manually needed to add events. I later realized
that I wanted to find a way to make it easier to organize big plans that I wanted to complete. I was thinking of an app where it organized almost every aspect of my life which includes, meals, exercise, homework assignments, and long term goals. Of couse, I wanted it to be A.I powered to make it easier to make plans and have a little assistent help you accomplish your goals.

## 📅 Project Timeline

| **Phase**                                    | **Description**                                                                      | **Start Date** | **End Date** | **Status**  |
| -------------------------------------------- | ------------------------------------------------------------------------------------ | -------------- | ------------ | ----------- |
| **Phase 1: Planning**                        | Choosing Tech stack, researching tools, and try new tech.                            | 07/25/2024     | 09/17/2024   | Completed   |
| **Phase 2: Frontend and Backend Setup**      | Get basic app working with frontend (react.js) and backend (django)                  | 09/17/2024     | 09/20/2024   | Completed   |
| **Phase 3: Connect Backend to Database**     | Learn to use DynamoDB and connect API to DynamoDB                                    | 09/20/2024     | 09/23/2024   | Completed   |
| **Phase 4: Organize data**                   | Figure out the best way to organize data                                             | 09/23/2024     | 09/25/2024   | Completed   |
| **Phase 5: Authentication**                  | Setup authentication using Django tool and JWT tokens for the front end              | 09/25/2024     | 10/06/2024   | Completed   |
| **Phase 6: Backend Models**                  | Finish backend data models for tasks and other entities                              | 10/10/2024     | 10/16/2024   | Completed   |
| **Phase 7: AI Task Planner**                 | Design the workflow for the AI-powered assistant to read/write tasks to the database | 10/17/2024     | 10/20/2024   | In Progress |
| **Phase 8: Complete All Unit Tests**         | Make sure to have all tests setup for each feature working well                      | 10/20/2024     | 10/27/2024   | In Progress |
| **Phase 9: Finsh All Project Documenation** | Make sure frontend is setup correctly and have decent styles                         | 10/27/2024     | 10/28/2024   | In Progress |
| **Phase 10: Finsh All Project Documenation**  | Have well documented code for each relevent backend file and frontend file           | 10/28/2024     | 10/28/2024   | In Progress |

## Bult With

React.js
DynamoDB
Django

## Developer Notes

The app features an AI-powered scheduling assistant, which uses OpenAI's API for natural language processing. You can talk to the agent to create tasks, which will be written to the database. The agent can also read from the database to suggest a better schedule for the week, adapting to your goals and tasks.

## How to start up the app

### Start Frontend React.js
```
npm run dev
```

### Start Backend Server
```
python3 manage.py runserver
```
