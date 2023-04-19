# Usage

## Introduction

This document is for users who are editing this project for their own purposes and would like to add their own pipelines. If you are looking to contribute to the open source templates themselves, please refer to [`CONTRIBUTING`](CONTRIBUTING.md).

## How to add a Django App

### Folder structure

Add your new Django app as a folder under the `ecommerce` directory. Within your new Django app folder you should have the following files:

* `admin.py` - This file is used to register your models with the Django admin site. You can read more about this [here](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/).
* `apps.py` - This file is used to configure your app. You can read more about this [here](https://docs.djangoproject.com/en/3.2/ref/applications/).
* `models.py` - This file is used to define your models. You can read more about this [here](https://docs.djangoproject.com/en/3.2/topics/db/models/).
* `api/serializers.py` - This file is used to define your serializers. You can read more about this [here](https://www.django-rest-framework.org/api-guide/serializers/).
* `api/views.py` - This file is used to define your views. You can read more about this [here](https://www.django-rest-framework.org/api-guide/views/).
* `urls.py` - This file is used to define your urls. You can read more about this [here](https://docs.djangoproject.com/en/3.2/topics/http/urls/).
* `tests/` - This folder is used to define your tests. You can read more about this [here](https://docs.djangoproject.com/en/3.2/topics/testing/overview/).

## Testing

Please refer to [`CONTRIBUTING.md`](CONTRIBUTING.md#Testing) for information on how to write both unit and end-to-end (E2E) pipeline tests for your pipeline. It is advisable to check that your pipelines pass all tests before being shared with others.

### Migrating

To migrate your database, run the following command:

```bash
py manage.py migrate
```

This will create the database tables for your Django app. You can also use this command to update your database tables if you make any changes to your models.

### Populating

To populate your database with some fake data, run the following command:

```bash
py manage.py populate_db
```

This command will create a many entries in the database. It also will create a superuser with the following credentials. To edit this command, please refer to [`ecommerce/core/management/commands/populate_db.py`](ecommerce/core/management/commands/populate_db.py).

### Running

To run your Django API project, run the following command:

```bash
py manage.py runserver
```

This will start the Django development server. You can access the admin panel at `http://localhost:8000/admin/` and the API at `http://localhost:8000/api/`. You also can access the API documentation at `http://localhost:8000/api/docs/`.
