# Setup

You will need the pipenv venv manager installed:

```shell
$ pip install pipenv --user
```

Once pipenv is installed, run the following to set up a dev environment:

```shell
$ pipenv install --dev
```

# Building Documentation

Since the documentation is built with the package itself we use it for general testing.

To set up:

```shell
$ pip install . --editable
```

Will install the package to your venv and watch for changes.

## Schemas

You will also need to manually copy over the schemas folder from `menagerie/schemas/` to `docs/content/pages/schemas`, this is part of the run config on PyCharm already.

## Generating

Now, navigate to `docs/` and run the generate command to build.

```shell
$ python -m menagerie generate
```

## Note for PyCharm users

You're going to want to set `URL_PREFIX` to `/menagerie/docs/out/` if you plan on using the built-in web server.
(A run config is included with the repo)

## Note for CLI users

You're going to want to set `URL_PREFIX` to the absolute path to `docs/out/` if you want to do everything from command line.