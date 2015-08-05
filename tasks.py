from invoke import run, task


@task
def test():
    run('nosetests')


@task
def install():
    run('pip install -e .')


@task
def uninstall():
    run('pip uninstall frozen')


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


@task(pre=[pep8, pylint, pyflakes, flake8])
def lint():
    pass
