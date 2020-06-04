# Guidelines for Contributing

As a scientific community-driven software project, WildfirePy welcomes contributions from interested individuals or groups. These guidelines are provided to give potential contributors information to make their contribution compliant with the conventions of the WildfirePy project, and maximize the probability of such contributions to be merged as quickly and efficiently as possible.

There are 4 main ways of contributing to the WildfirePy project (in descending order of difficulty or scope):

* Adding new or improved functionality to the existing codebase.
* Fixing outstanding issues (bugs) with the existing codebase. They range from low-level software bugs to higher-level design problems.
* Contributing or improving the documentation (`docs`)
* Submitting issues related to bugs or desired enhancements.

# Opening issues

We appreciate being notified of problems with the existing WildfirePy code. We prefer that issues be filed on [Github Issue Tracker](https://github.com/wildfirepy/wildfirepy/issues), rather than on social media or by direct email to the developers.

Please verify that your issue is not being currently addressed by other issues or pull requests by using the GitHub search tool to look for key words in the project issue tracker.

# Contributing code via pull requests

While issue reporting is valuable, we strongly encourage users who are
inclined to do so to submit patches for new or existing issues via pull
requests. This is particularly the case for simple fixes, such as typos
or tweaks to documentation, which do not require a heavy investment
of time and attention.

Contributors are also encouraged to contribute new code to enhance WildfirePy's
functionality, also via pull requests.

## Steps before starting work
Before starting a work on a pull request double check that no one else is working on the ticket in both issue tickets and pull requests.

### If an issue ticket exists
If an issue exists check the ticket to ensure no one else has started work. If first to start work, comment on the ticket to make it evident to others. If the comment looks old or abandoned leave a comment asking if you may start work.

### If an issue ticket doesn't exist
Open an issue ticket for the issue and state that you'll be solving the issue with a pull request. Optionally create a pull request and add `[WIP]` in the title to indicate Work in Progress.

### In the event of a conflict
In the event of two or more people working on the same issue, the general precedence will go to the person who first commented in the issue. If no comments it will go to the first person to submit a PR for review. Each situation will differ though, and the core contributors will make the best judgement call if needed.

## Making the pull request
The preferred workflow for contributing to WildfirePy is to fork
the [GitHub repository](https://github.com/wildfirepy/wildfirepy), clone it to your local machine, and develop on a feature branch.

## Steps

1. Fork the [project repository](https://github.com/wildfirepy/wildfirepy) by clicking on the 'Fork' button near the top right of the main repository page. This creates a copy of the code under your GitHub user account.

2. Clone your fork of the WildFirePy repo from your GitHub account to your local disk, and add the base repository as a remote:

   ```bash
   $ git clone git@github.com:<your GitHub handle>/wildfirepy.git
   $ cd wildfirepy
   $ git remote add upstream git@github.com:wildfirepy/wildfirepy.git
   ```

3. Create a ``feature`` branch to hold your development changes:

   ```bash
   $ git checkout -b my-feature
   ```

   Always use a ``feature`` branch. It's good practice to never routinely work on the ``master`` branch of any repository.

4. Project requirements are in ``requirements.txt``, and libraries used for development are in ``requirements-dev.txt``.  To set up a development environment, you may (probably in a [virtual environment](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)) run:

   ```bash
   $ pip install -r requirements.txt
   $ pip install -r requirements-dev.txt
   ```

5. Develop the feature on your feature branch. Add changed files using ``git add`` and then ``git commit`` files:

   ```bash
   $ git add modified_files
   $ git commit -m "commit message here"
   ```

   to record your changes locally.
   After committing, it is a good idea to sync with the base repository in case there have been any changes:

   ```bash
   $ git fetch upstream
   $ git rebase upstream/master
   ```

   Then push the changes to your GitHub account with:

   ```bash
   $ git push -u origin my-feature
   ```

6. Go to the GitHub web page of your fork of the WildfirePy repo. Click the 'Pull request' button to send your changes to the project's maintainers for review. This will send an email to the committers.

## Pull request checklist

We recommend that your contribution complies with the following guidelines before you submit a pull request:

* If your pull request addresses an issue, please use the pull request title to describe the issue and mention the issue number in the pull request description. This will make sure a link back to the original issue is created.

* All public methods must have informative docstrings with sample usage when appropriate.

* Please prefix the title of incomplete contributions with `[WIP]` (to indicate a work in progress). WIPs may be useful to (1) indicate you are working on something to avoid duplicated work, (2) request broad review of functionality or API, or (3) seek collaborators.

* When adding additional functionality, provide at least one example script or Jupyter Notebook.

* Added tests follow the [pytest fixture pattern](https://docs.pytest.org/en/latest/fixture.html#fixture)

* Documentation and high-coverage tests are necessary for enhancements to be accepted.

* Documentation follows Numpy style guide.

* Create a file named `<#-PR-number>.<feature/trivial/bugfix/docfix>.rst` to `changelog` directory. And add a summary of the changes to it.

#### This guide was derived from the [arviz guide to contributing](https://github.com/arviz-devs/arviz/blob/master/CONTRIBUTING.md)