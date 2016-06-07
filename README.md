# FallBall

## Overview
FallBall is the best in class file sharing service that offers cloud storage and file synchronization for small and medium businesses (SMBs) worldwide.
This dummy service helps developers to learn [APS Lite](http://aps.odin.com) technology 

## How To Deploy
1. Create application database:
  
    ```
    python manage.py migrate
    ```

2. Load initial data

    ```
    python manage.py loaddata dbdump
    ```

3. Get admin token

    ```
    python manage.py shell
    ```
    ```python
    from django.contrib.auth.models import User 
    from rest_framework.authtoken.models import Token
    a = User.objects.filter(username='admin')
    Token.objects.filter(user=a)
    [<Token: 4395ef69e0701a85866485e57ad40fab167bd544>]
    ```

## Run
In order to run server you need to execute the following command from the root folder of the project:

```
python manage.py runserver <host_name>:<port>
```

## Tests
To run tests simply execute the following command:

```
python manage.py test fallballapp.tests
```