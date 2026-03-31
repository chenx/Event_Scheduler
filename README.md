# Event Scheduler

A Python/Django web application project started as an event scheduler and extended to demo other functions.

Demos the creation of database models, creation and consumption of RESTful APIs, and creation of AI agents/workflows.

Use Django REST Framework (DRF) to provide API end points.

User needs to log in to access personal homepage, RESTful API end points and AI agents.

Environment:
- Python 3.13.1
- DJango 6.0

## High level flowchart

<img width="652" height="491" alt="image" src="https://github.com/user-attachments/assets/b5c2cdb3-dd1c-4948-913e-2c4ced5577ef" />

## Database schema

<img width="634" height="536" alt="image" src="https://github.com/user-attachments/assets/452938e5-c8af-4d1a-acf8-5642f7b6f483" />

Created using https://dbdiagram.io

The schema design includes a new field “phone” in the User table, so we need a customized User model. To create a customized User model, one can use either `AbstractUser` or `AbstractBaseUser`. As a comparison, `AbstractUser` includes all the default Django user fields and is best for minor customizations, while `AbstractBaseUser` is a minimal base class for when you need to redefine the entire user model from scratch. In this case, `AbstractUser` is used.


## Web UI

### 1) homepage
<kbd>
  <img width="900" height="686" alt="image" src="https://github.com/user-attachments/assets/51e4a3e8-2800-4aa2-9a6d-1adf401b14de" />
</kbd>

### 2) agent/agent2: Ask me anything (v2)
This is a conversational AI agent powered by OpenAI API. It logs the result to the datastore table below.
<kbd>
  <img width="903" height="349" alt="image" src="https://github.com/user-attachments/assets/127ba0ff-ea8d-46a2-a3d2-e4937fa24bb4" />
</kbd>

### 3) datastore
<kbd>
  <img width="906" height="460" alt="image" src="https://github.com/user-attachments/assets/34282193-699b-445a-8689-edb8a9cc6899" />
</kbd>

### 4) service/events
This retrieves data from remote API and displays the data in a table.
<kbd>
  <img width="903" height="358" alt="image" src="https://github.com/user-attachments/assets/02a6eeeb-6859-4f5c-8ecd-9d1c75e0a7a4" />
</kbd>

### 5) api/events
This is a RESTful API end point for GET and POST.
<kbd>
<img width="902" height="652" alt="image" src="https://github.com/user-attachments/assets/0e7dfd3b-2d76-4bc8-99bd-895069b27d1c" />
</kbd>
