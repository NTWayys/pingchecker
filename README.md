# pingchecker
Checks if a domain is pingable and keeps track

## To run app

run the following commands

    pip install pipenv
    pipenv shell
    pip install django-q
    pip install djangorestframework
    python manage.py runserver
    python manage.pyq cluster

## to add domain

Go to /server/view/The_domain    <-- I recommend updating the urls in pingserver/urls.py ( just remove server/)
To enable auto updates -> make a task in django q for pingserver.utils.updateServerStatus
