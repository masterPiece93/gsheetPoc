# Gsheets POC
This deals with poc on google sheets access and manipulation in a web application ( client-server architechture ) .

It also demonstrates the Google Oauth2 authentication in such a setup .

| `Djnago` | `python` | `sqlite` | 

### Running server :

```sh
# using Makefile
make runserver
```

```sh
# manually
python3 manage.py runserver localhost:5000
```

### On Browser :
- `/` points to base path points to gsheets app .
    - `/sheet/api` points to api specific enpoints .
- `/auth` points to gauth app .
- `/admin` points to django admin .
    - admin panel credentials :
        - **username** : _admin_
        - **password** : _admin_
        
        If credential not set , generate them by running command ( on terminal/shell/cmd ): 
        ```sh
        python3 manage.py createsuperuser
        ```

##### Globally 
> git config --global credential.helper 'cache --timeout=3600'

##### Locally 
> git config credential.helper 'cache --timeout=3600'