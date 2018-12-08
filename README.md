# brite

Backend server containing models for Insurance forms. Allows creating Dynamic fields based on requirements.

#### Technical details
Server runs on Python 2.7 + Django
Low performance SQLite Database with S3 backups
Deployed on AWS Lambda using Zappa

API documentation: https://2lmqgnfs2l.execute-api.us-east-1.amazonaws.com/dev/

API tests in `userData/tests.py`

Dependencies:
- Django
- Whitenoise (To serve static files)
- Django Rest Framework (For APIs)
- django-cors-headers (To enable CORS)
- drf-yasg (API documentation)
- Zappa (Deployments)
- zappa-django-utils (Supporting SQLite3 backed up on S3)

#### Usage details 
Credentials: kunal / test1234
- Create Enum Choices here: https://2lmqgnfs2l.execute-api.us-east-1.amazonaws.com/dev/admin/core/enumchoice/
- Create Fields here: https://2lmqgnfs2l.execute-api.us-east-1.amazonaws.com/dev/admin/core/datafield/
- Finally, select fields for an Insurance form here: https://2lmqgnfs2l.execute-api.us-east-1.amazonaws.com/dev/admin/core/insuranceform/
- Fill the form details using Frontend: https://kunalgrover05.github.io/brite-vue/#/

