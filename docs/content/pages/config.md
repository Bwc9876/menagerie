Title: Configuration
Description: Guide to configuring your menagerie site
Sort_Priority: 95

# Configuration

Configuration is done in a single file at the root of your site called `config.json`.  

If you want reference on what each property in this file does, take a look at the [schema]({{ 'Configuration Schema'|route }}).  

## Using a Different Config File

You can use a different config file during generation using the `--config` flag
```shell
$ python -m menageri generate --config=path/to/config.json
```

# Environment Variables

The `URL_PREFIX` environment variable is used to prepend paths when calling `route` and `static`.  
This is most useful when developing on a local machine where links don't work.

For example, PyCharm's dev server serves file relative to the root of the project, but if my `docs/out/` folder isn't at the root of the site links will not work.  
To counteract this I can set my `URL_PREFIX` variable to `/docs/out/` so that way all links will point to the correct location.  

If you're using pipenv this is as simple as making a file called `.env` at the root of your docs folder and doing
```shell
$ pipenv run python -m menagerie generate
```
Pipenv should automatically load environment variables from `.env` for you

## Note About GitHub Actions

If you're running site generation in an action, you'll want to set `base_url` to "https://YourUser.gihub.io/" and `URL_PREFIX` to "YourRepo".  
Setting environment variables in GitHub Actions can be done with the `env` property at the root level.

```yaml
name: My Action
on:
  # ...
env:
  URL_PREFIX: /my-repo/
jobs:
  # ...
```

If you want an example of how to build menagerie pages with GitHub actions, the menagerie docs [has one set up already](https://github.com/Bwc9876/menagerie/blob/master/.github/workflows/build-docs.yml).  
**Important Note**: You can remove the "Install Self" step of the job as that is specific to menagerie, this also assumes you're using pipenv and have a folder called `docs` in the root of your repo.