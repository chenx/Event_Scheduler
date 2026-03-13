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
