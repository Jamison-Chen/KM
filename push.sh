#!/bin/bash
set -e

git checkout dev
git add .

if [[ -z $1 ]]; then
    git commit -m "Update"
else
    git commit -m "$1"
fi

git push origin dev

git checkout master
git merge -Xtheirs dev -m "Merge branch 'dev'"

python -B summary.py
python -B normalize_img_links.py

set +e

git add .
git commit -m "Update"
git push origin master

git checkout dev
