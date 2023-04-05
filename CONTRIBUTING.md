# Contributing

Welcome to the Django Ecommerce API demo, and thank you for your interest in contributing! This guide will help you get started.

This guide is chiefly for users wishing to contribute to the opensource version of this tutorial. Those who want just to use the project to suit their own purposes should look at [USAGE](USAGE.md), but may find some sections useful.

## Links to Important Resources

- [pytest](https://docs.pytest.org)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [pdm](https://pdm.fming.dev)
- [black](https://black.readthedocs.io/en/stable/)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [pre-commit](https://pre-commit.com)
- [commitizen](https://commitizen-tools.github.io/commitizen/)

## Python code guidelines

### Code linting and formatting

We use linting to highlight problems in our Python code which could later produce errors or affect efficiency. For example, linting detects things such as uninitialised or undefined variables, unused imported modules, and missing parentheses. To detect and enact fixes to these problems, we make use of the Python linter: [Flake8](https://flake8.pycqa.org/en/latest/) and the formatter [Black](https://black.readthedocs.io/en/stable/). These are run as part of our [pre-commit checks](#Pre-commit-checks). We have some configurations for Flake8 that you can find [here](pyproject.toml).

### Docstring format

Please include docstrings that are compliant with the [Google Style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

In brief, the docstring is a triple quoted string placed immediately after the function definition and should contain:

- A brief description of the function
- A section `Args:` where you list the function arguments
  - For each argument, include the argument type in brackets
- A section `Returns:` where you list what the function returns
  - For each returned item, include the type

## Testing

Testing is an important way for us to check that our code works as expected and forms a key part of our CI/CD strategy. For example, pull requests will not pass our checks if any unit tests fail. You should therefore ensure that your pull request passes all tests before merging.

### Unit Tests

We use unit tests to test small sections of logically isolated code in our pipeline components.

#### Mocking & patching

When we test a function that makes an external API call (for example to a service on GCP), we mock the associated module or class and its functions and attributes. The rationale behind this is that we want to test our own logic and not the API call(s) themselves. Indeed, API calls can be broken, computationally expensive, slow, or limited, and we do not want our unit tests to fail because of any of these. Instead, we want to test that our code behaves as expected when the API call is successful or fails.

#### How to write unit tests

Some things to consider testing for in your code:

- **Do you have any logical conditions?** Consider writing tests that assert the desired outcome occurs for each possible outcome. In particular, you can assert that a certain error is raised in your function under certain conditions. For example, considering a function named `get_configuration` raises a `RuntimeError` if no configuration are found:

```python
if fail_on_configuration_not_found:
  raise RuntimeError("Failed as configuration not found.")
```

Now in `test_configuration.py`, in the unit test `test_get_configuration_when_no_config_fail` you can use `pytest.raises` to check that `get_configuration` actually raises a `RuntimeError`:

``` python
with pytest.raises(RuntimeError):
  get_configuration(params)
```

#### How to run unit tests

Unit tests for pipeline components are run automatically on each pull request. You can also run them on your local machine:

```bash
pdm run tests
```

Or just use `pytest` directly:

```bash
pytest
```

## Adding or changing python dependencies

We use [pdm](https://pdm.fming.dev/) to handle our packages and their dependencies.

### Adding python dependencies

You may need to add new packages for your own use cases. To do this, run pdm add. If you are adding a package that should be used just in development, add the `--dev` flag.

```bash
pdm add <package name>
```

## Committing Changes

### Add changed files to staging area

```bash
git add <path(s) of changed file(s)>
```

### Commit messages

To allow others (and yourself!) to understand your changes easily, we encourage writing detailed commit messages. We use [Commitizen](https://commitizen-tools.github.io/commitizen/) as a guide. In brief, all commit messages should start with one of the following prefixes:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons etc)
- **refactor**: A change that neither fixes a bug or adds a feature
- **perf**: A change that improves performance
- **test**: Add new tests or correct existing tests
- **build**: Changes that affect the build system or external dependencies (e.g. pip, docker, npm)
- **ci**: Changes to CI configuration files and scripts

After the prefix, you can specify the scope (e.g. the class or file name) of the change in brackets. Finally, you include the details of the change. For example

```bash
git commit -s -m"prefix(scope): message here"
```

### Things to avoid in your commit messages:

- Too brief or non-specific messages (e.g. `bug fix`, `small changes`)
- Commit message does not explain why changes were made

### Pre-commit checks

We use pre-commit hooks to automatically identify and correct issues in code. You can find the details of the hooks we use [here](.pre-commit-config.yaml). If any of these fail, the commit will be unsuccessful and you will be able to see which hook failed and some additional details in your terminal.

To run the pre-commit hooks over the entire repo, run:

```bash
make pre-commit
```

#### What to do if pre-commit checks fail:

- **Checks fail and the pre-commit hook edits a file to fix the error**. Sometimes the pre-commit hook will identify an error (e.g. the absence of a blank line at the end of a file), and will correct this automatically by changing your file. You will then need to re-add these files to the staging area before trying to commit again.

- **Checks fail and displays an error message**. Some errors cannot be automatically fixed by pre-commit hooks, and instead they will display the error number and the file and line which failed. For more details beyond the error message, you can look up the error number online. The most common errors are caused by lines which exceed the character limit. Once you identify the cause of the error, you will need to fix this in your code, add the edited file to the staging area, and then commit again.

### Commit changes to Python packages and dependencies

If you have changes to `Pipfile` and `Pipfile.lock`, please make sure you commit these files!
