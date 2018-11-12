from invoke import run, task


@task
def test():
        run('nosetests')


@task
def install():
        run('pip install -e .')


@task
def uninstall():
        run('pip uninstall liquidnitrogen')


@task
def publish():
        run('python setup.py register')
        run('python setup.py sdist upload')


@task
def pep8():
        run('pep8 .')


@task
def pylint():
        run('pylint *.py')


@task
def pyflakes():
        run('pyflakes .')


@task
def flake8():
        run('flake8 .')


@task
def bandit():
        run('find . -name \'*.py\' | xargs bandit')


@task(pre=[pep8, pylint, pyflakes, flake8, bandit])
def lint():
        pass


@task
def clean():
        run('rm -rf dist/; true')
        run('find . -type d -name __pycache__ -exec rm -rf {} \\;; true')
        run('rm -rf *.egg-info; true')
