#!/bin/bash
sh summary.sh

# git config user.name "Jamison Chen"
# git config user.email "106208004@g.nccu.edu.tw"

git add .

if [[ -z $1 ]]; then
    git commit -m "Update"
else
    git commit -m "$1"
fi

# ssh-add -D
# ssh-add ~/.ssh/id_rsa

git push -u origin master
