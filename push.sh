#!/usr/bin/env bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" != "dev" ]; then
    printf "${RED}Error: You are not on the correct branch. Aborting.${RESET}\n"
    exit 1
fi

git add -A

if [[ -z $1 ]]; then
    git commit -m Update
else
    git commit -m "$1"
fi

git push origin dev
printf "${BLUE}------------ Remote branch 'dev' updated ------------${RESET}\n"

git switch master
git merge -Xtheirs dev -m "Merge branch 'dev'"
printf "${BLUE}------ Local branch 'dev' merged into 'master' ------${RESET}\n"

python -B summary.py
python -B normalize_img_links.py
python -B normalize_internal_links.py

set +e

git add -A
git commit -m Update
git push origin master
printf "${BLUE}----------- Remote branch 'master' updated -----------${RESET}\n"

git switch dev
printf "${GREEN}Done!${RESET}\n"
