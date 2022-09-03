# pingchecker
Checks if a domain is pingable and keeps track


## Preview

![image](https://user-images.githubusercontent.com/92786821/188270751-c5d9a30f-d72e-49c6-bf37-70abafa1a550.png)


Currently still need to add whois data, Don't have an web provider I can test this with so Will complete once able to.

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

