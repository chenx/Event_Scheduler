# Python_Django_demo3

A Django project to demo the creation of models and APIs in a meeting scheduler.

Use Django REST Framework (DRF) to provide API end points.

User needs to log in to access personal homepage and API end points.

The schema design includes a new field “phone” in the User table, so we need a customized User model. To create a customized User model, one can use either `AbstractUser` or `AbstractBaseUser`. As a comparison, `AbstractUser` includes all the default Django user fields and is best for minor customizations, while `AbstractBaseUser` is a minimal base class for when you need to redefine the entire user model from scratch. In this case, `AbstractUser` is used.


Environment:
- Python 3.13.1
- DJango 6.0

## High level flowchart

<img width="652" height="491" alt="image" src="https://github.com/user-attachments/assets/b5c2cdb3-dd1c-4948-913e-2c4ced5577ef" />

## Database schema

<img width="634" height="536" alt="image" src="https://github.com/user-attachments/assets/452938e5-c8af-4d1a-acf8-5642f7b6f483" />

Created using https://dbdiagram.io

## Web UI

### 1) homepage
<kbd>
<img width="883" height="675" alt="image" src="https://github.com/user-attachments/assets/1ffddb67-a2a5-4bd3-8034-7ee0bf36d210" />
</kbd>

### 2) agent/agent2: Ask me anything (v2)
This is an AI agent powered by OpenAI API.
<kbd>
<img width="889" height="339" alt="image" src="https://github.com/user-attachments/assets/0c6d0f22-a171-43f1-8f78-b2b4fb56c372" />
</kbd>

### 3) datastore
<kbd>
<img width="906" height="533" alt="image" src="https://github.com/user-attachments/assets/fd8c5ede-9770-45fb-b135-e22b52e0b3a5" />
</kbd>

### 4) events
<kbd>
<img width="903" height="363" alt="image" src="https://github.com/user-attachments/assets/13ded703-f423-4478-a6e3-2a6a62b03bb3" />
</kbd>

### 5) api/events
<kbd>
<img width="902" height="652" alt="image" src="https://github.com/user-attachments/assets/0e7dfd3b-2d76-4bc8-99bd-895069b27d1c" />
</kbd>
