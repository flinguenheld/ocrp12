![badge](https://img.shields.io/static/v1?label=Project&nbsp;OC&message=12&color=blueviolet&style=for-the-badge)
![badge](https://img.shields.io/static/v1?label=Status&message=InProgress&color=blue&style=for-the-badge)

# ocrp12

Develop a Secure Back-End Architecture Using Django ORM

![Logo epicevents](https://raw.githubusercontent.com/FLinguenheld/ocrp12/main/logos/epicevents.png "Logo")


****
### Documentation

All endpoints are explained in the Postman documentation :  

[![Logo PostMan](https://raw.githubusercontent.com/FLinguenheld/ocrp12/main/logos/postman.png "Postman")](https://documenter.getpostman.com/view/19051270/2s8YzXwLV1)


****
### Database

This application uses [postgresql](https://www.postgresql.org). You have to install it according to your distribution then 
create a dabase and an user with this information :

    database name : epic_events
    user : epic_user
    user password : 01234

Django will search the database on localhost with the port 5432.  
You can change this behaviour in the settings files.

Here an example to create a new database :

    sudo -u postgres psql
    create database epic_events
    (drop database epic_events)

Django administration is activated, you can create a superuser and open it with the link :  
http://localhost:8000/admin/

    admin@epiccrm.com
    admin01234

****
### Testing

This code used the framework [pytest](https://docs.pytest.org/en/latest/contents.html) to test endpoints.  
To launch a new test, open a terminal, navigate into the ocrp12/ folder and activate the virtual environment.  
Then launch the command :

    pytest -v

These tests need an user, you can create him with the django administration interface with these information :

    test@test.com
    01234

