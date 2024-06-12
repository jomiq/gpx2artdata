#! /bin/bash
BUMP=${1-minor}
MESSAGE=${2-"No description provided. Deal with it."}

if [ -z "$(git status --untracked-files=no --porcelain)" ]; then
    hatch version $BUMP
    VERSION="v$(hatch version)"
    git add .
    git commit -m "Version $VERSION"
    git tag $VERSION -m "$MESSAGE"
    git-changelog
    
    git add CHANGELOG.md
    git commit --amend --no-edit
    git tag -fa $VERSION -m "$MESSAGE"

else 
    echo Aborting: we do not bump version when there are uncommitted changes in this house
fi