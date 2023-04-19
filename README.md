[![CI/CD][github-actions-shield]][github-actions-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![pdm][pdm-managed]][pdm-url]

<div align="center">
  <a href="https://github.com/vrcadore/django-ecommerce-api">
    <img src="images/logo.png" alt="Logo" width="180" height="80">
  </a>
  <h3 align="center">Django - DRF - E-Commerce API</h3>
  <p align="center">
    A demo project using Django Rest Framework!
    <br />
    <a href="https://github.com/vrcadore/django-ecommerce-api/issues">Report Bug</a>
    ·
    <a href="https://github.com/vrcadore/django-ecommerce-api/issues">Request Feature</a>
  </p>
</div>

## About The Project

There are many great Django demo projects available on GitHub; however, I didn't find one that really suited had a structure that I liked. So, I created this project to learn more about Django and DRF. I hope you find it useful as well!

In this project, you will find a Django Rest Framework API with a simple e-commerce structure. It has a simple user authentication system, a product catalog. It also has a simple admin panel to manage the products and users. My goal was to create a simple project that could be used to demo a couple of different things that usually we need to do in a project.

The project uses a couple of libraries and tools that I like to use in my projects and are considered best practices. I'll try to explain them in the following sections. Of course, no one template will be able to fit all your needs. So, feel free to fork this project and customize it to your needs.

### Built With

These are some of the libraries and tools used in this project.

| Library | Description |
| --- | --- |
| [![python][python-shield]][python-url] | Programming language used to build the API |
| [![django][django-shield]][django-url] | Framework used to build the API |
| [![drf][drf-shield]][drf-url] | Django Library used to build the API |
| [![pdm][pdm-shield]][pdm-url] | Used to manage the project dependencies |
| [![toml][toml-shield]][toml-url] | Used to configure the project |
| [![dotenv][dotenv-shield]][dotenv-url] | Used to load environment variables from .env file |

The project also uses a couple of libraries that are not listed here. You can find them in the `pyproject.toml` file. I have used `VSCode` as my IDE to build this project, however, it is not required to use it. You can use any IDE you want.

## Getting Started

This project is a Django project, so most of the steps to get started are the same as any other Django project. However, I will try to explain the steps to get started with this project.

### Prerequisites

As mentioned before, this project is a Django project, so you will need to have Python and Django installed in your machine. You can find the instructions to install Python and Django in the following links:

* [Python](https://www.python.org/downloads/)
* [Django](https://docs.djangoproject.com/en/3.2/topics/install/)

I also recommend you to use pyenv to manage your Python versions. Pyenv is a tool that allows you to manage multiple Python versions in your machine, helping you to avoid conflicts between different projects. It also allows you to download and install Python versions from the command line very easily. You can find the instructions to install pyenv in the following link:

* [pyenv](https://github.com/pyenv/pyenv)

Also, we need to install PDM. PDM is a Python package manager that is very similar to Pipenv. It is a tool that allows you to manage your project dependencies. You can find the instructions to install PDM in the following link:

* [PDM](https://pdm.fming.dev/)

Laslty but not least, we need to install a postgres database. How to create a postgres database is out of the scope of this project, but you can find some instructions in the following link:

* [Postgres](https://www.postgresql.org/download/)

With all the prerequisites installed, we are ready to get started.

### Installation

1. Clone the repo

```bash
git clone https://github.com/vrcadore/django-ecommerce-api
```

2. Get into the project folder and install the dependencies.

```bash
cd django-ecommerce-api
pdm install
```

3. Create a `.env` file in the root folder of the project and add the following environment variables.

```bash
DJANGO_READ_DOT_ENV_FILE=True
DATABASE_URL=postgres://user:password@localhost:5432/postgres # Use your postgres connection string here
```

4. Run the migrations.

```bash
py manage.py migrate
```

5. Populate the database with some data.

```bash
py manage.py populate_db
```

This command will create a many entries in the database. It also will create a superuser with the following credentials

```bash
username: admin
password: admin1234
```

6. Run the server.

```bash
py manage.py runserver
```

After running the server, you can access the admin panel at `http://localhost:8000/admin/` and the API at `http://localhost:8000/api/`. You also can access the API documentation at `http://localhost:8000/api/docs/`.

## Usage

Information about using this project can be found in the [USAGE.md](USAGE.md) file.

## Roadmap

* [x] Create basic project structure.
* [X] Add support for commitizen and pre-commit hooks.
* [X] Add support for PDM and use TOML to configure the project.
* [ ] Add User Authentication and extend the User model.
* [X] Add Product and other models for the e-commerce demo.
* [X] Add API Documentation with Swagger
* [ ] Add markdown files to explain how to use the project.
* [ ] Add management command to populate the database.
* [ ] Add Admin Panel with Grappelli.
* [ ] Add Unit Tests.
* [ ] Add Sphinx Documentation.
* [ ] Add Github Actions to run tests and build docs.
* [ ] Add background tasks with Celery and Redis.
* [ ] Multi-language Support.
  * [ ] Portuguese

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

More information about contributing to this project can be found in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

Vinicius Cadore - [LinkedIn](https://linkedin.com/in/vrcadore)

Website: [https://www.viniciuscadore.com](https://www.viniciuscadore.com)

## Acknowledgments

I would like to thank the following people and projects for their inspiration and support by building these amazing projects/libraries/frameworks:

* [Cookiecutter Django](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html/)
* [Awesome Django GitHub](https://github.com/wsvincent/awesome-django/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Django Grappelli](https://github.com/sehmaschine/django-grappelli/)
* [Best README Template](https://github.com/othneildrew/Best-README-Template/)
* [Very Academy Youtube Channel](https://www.youtube.com/c/veryacademy/)

[contributors-shield]: https://img.shields.io/github/contributors/vrcadore/django-ecommerce-api.svg?style=flat
[contributors-url]: https://github.com/vrcadore/django-ecommerce-api/graphs/contributors
[django-shield]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[django-url]: https://www.djangoproject.com/
[dotenv-shield]: https://img.shields.io/badge/.env-ECD53F?style=for-the-badge&logo=.env&logoColor=black
[dotenv-url]: https://www.dotenv.org/
[drf-shield]: https://img.shields.io/badge/DRF-FFA500?style=for-the-badge&logo=python&logoColor=white
[drf-url]: https://www.django-rest-framework.org/
[forks-shield]: https://img.shields.io/github/forks/vrcadore/django-ecommerce-api.svg?style=flat
[forks-url]: https://github.com/vrcadore/django-ecommerce-api/network/members
[github-actions-shield]: https://github.com/vrcadore/django-ecommerce-api/actions/workflows/ci.yml/badge.svg
[github-actions-url]: https://github.com/vrcadore/django-ecommerce-api/actions/workflows/ci.yml
[issues-shield]: https://img.shields.io/github/issues/vrcadore/django-ecommerce-api.svg?style=flat
[issues-url]: https://github.com/vrcadore/django-ecommerce-api/issues
[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg?style=flat
[license-url]: https://github.com/vrcadore/django-ecommerce-api/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/vrcadore
[pdm-managed]: https://img.shields.io/badge/pdm-managed-blueviolet
[pdm-shield]: https://img.shields.io/badge/PDM-blueviolet?style=for-the-badge&logo=python&logoColor=white
[pdm-url]: https://pdm.fming.dev/
[python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[stars-shield]: https://img.shields.io/github/stars/vrcadore/django-ecommerce-api.svg?style=flat
[stars-url]: https://github.com/vrcadore/django-ecommerce-api/stargazers
[toml-shield]: https://img.shields.io/badge/TOML-9C4121?style=for-the-badge&logo=toml&logoColor=white
[toml-url]: https://toml.io/en/
