# api_yamdb

**REST API** for **YaMDb** service - *movie, book* and *music* reviews database. Team project of [Practicum students by Yandex](https://practicum.yandex.com/)

## API for YaMDb service allows to run the following functions:

### Reviews
* Get a list of all reviews;
* Create a new review. User may post only one review per object;
* Get a review by id;
* Partially update the review by id;
* Delete review by id.

### Comments
* Get a list of all comments to the review by id;
* Create a new comment for the review;
* Get a comment for a review by id;
* Partially update the comment on the review by id;
* Delete a comment to the review by id.

### Auth
* Getting a JWT token in exchange for email and confirmation_code;
* Sending confirmation_code to the email.

### Users
* Get a list of all users;
* Create an user;
* Get user by username;
* Change user data by username;
* Delete user by username;
* Get personal account details;
* Change the personal account details.

### Categories
* Get a list of all categories;
* Create a category;
* Delete a category.

### Genres
* Get a list of all genres;
* Create a genre;
* Delete a genre.

### Titles
* Get a list of all titles;
* Create an title for reviews;
* Get title information;
* Update title information;
* Delete title.


For details, please read the *Documentation*: [English version](https://github.com/olifirovai/api_yamdb/blob/master/static/redoc_en.yaml) and [Russian version](https://github.com/olifirovai/api_yamdb/blob/master/static/redoc_ru.yaml)

## Launch using Docker
*All of the following commands should be made directly from the project folder*

### Starting docker-compose:
```
docker-compose up
```
### First Start
**For the first launch**, for project functionality, while running the container please do migrations and collect provided static files: 
```
docker-compose exec web python manage.py migrate
```
**Create a super user:**
```
docker-compose exec web python manage.py createsuperuser
```
**Loading the prepared data to the DataBase:**
```
docker-compose exec web python manage.py loaddata fixtures.json
```
**If you obtain the ```the input device is not a TTY``` error**, please add to previous commands in the beginning ```winpty```

*Example:*
```
winpty docker-compose exec web python manage.py migrate
```

## Authors
* **[Denis](https://github.com/JackDaniels07)** - **Content Part** (reviews, comments, categories, genres, titles): models, views, endpoints, permissions related to part, rating score.
* **[Irina Olifirova](https://github.com/olifirovai)** - **User and Auth parts**: registration and authentication, permissions, roles, token authentication, e-mail confirmation system.
