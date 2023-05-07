#!/bin/bash
set -e
# git config user.name "Jamison Chen"
# git config user.email "106208004@g.nccu.edu.tw"

git checkout dev
git add .

if [[ -z $1 ]]; then
    git commit -m "Update"
else
    git commit -m "$1"
fi

# ssh-add -D
# ssh-add ~/.ssh/id_rsa

git push origin dev

git checkout master
git merge -Xtheirs dev -m "Merge branch 'dev'"

python summary.py
python normalize_img_links.py

set +e

git add .
git commit -m "Update"
git push origin master

git checkout dev
