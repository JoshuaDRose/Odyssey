#!/bin/bash

function help {
    echo "usage: ./update arguments"
    echo "  compile                 Upgrades the pinned version of all packages."
    echo "  sync-all                Update your virtual environment of all packages."
    echo "  sync-dev                Update your virtual environment for base, dev and test."
    echo "  sync-tests              Update your virtual environment for base and test."
    echo "  sync-ci                 Update your virtual environment for base and test."
    echo "  sync-production         Update your virtual environment for base and production."
    echo "  upgrade                 Upgrades pip, setuptools and pip-tools."
}

if [ $# -eq  0 ]; then
    help
    exit 1
fi

if [ "$1" == "sync-production" ]; then
    pip install --no-cache-dir -r requirements/production.txt
    exit 0
elif [ "$1" == "sync-ci" ]; then
    pip install --no-cache-dir -r requirements/tests.txt
    exit 0
elif [ "$1" == "upgrade" ]; then
    pip install --upgrade pip setuptools pip-tools
    exit 0
fi

if ! pip list | grep "pip-tools" > /dev/null ; then
    echo "This action requires pip-tools. Run 'pip install pip-tools' or './update.sh upgrade'."
    help
    exit 1
fi

if [ "$1" == "sync-all" ]; then
    pip-sync requirements/base.txt requirements/dev.txt requirements/tests.txt requirements/production.txt
    exit 0

elif [ "$1" == "sync-dev" ]; then
    pip-sync requirements/base.txt requirements/dev.txt requirements/tests.txt
    exit 0

elif [ "$1" == "sync-tests" ]; then
    pip-sync requirements/base.txt requirements/tests.txt
    exit 0

elif [ "$1" == "compile" ]; then
    pip-compile --upgrade requirements/base.in -o requirements/base.txt
    pip-compile --upgrade requirements/base.in requirements/tests.in requirements/dev.in -o requirements/dev.txt
    pip-compile --upgrade requirements/base.in requirements/tests.in -o requirements/tests.txt
    pip-compile --upgrade requirements/base.in requirements/production.in -o requirements/production.txt

else
    help
    exit 1
fi

