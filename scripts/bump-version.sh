#! /bin/bash
BUMP=${1-minor}
MESSAGE=${2-"No description provided. Deal with it."}
export EDITOR=${EDITOR-"code --wait"}

echo
echo " ******* gpx2artdata versioning ********* "
echo " ***                                  *** "
echo " ***       ok, this is final          *** "
echo " ***                                  *** "
echo " ******* e l e k t r o s l ö j d ******** "
echo

if [ -z "$(git status --untracked-files=no --porcelain)" ]; then
    hatch version $BUMP
    VERSION="v$(hatch version)"
    git-changelog -B $VERSION
    
    echo "# $VERSION" > requirements.txt
    pip freeze >> requirements.txt
    
    echo -e "# Version $VERSION - $(date)\n\n$(cat RELEASE.md)" > RELEASE.md
    echo "Provide a witty release description ..."
    $EDITOR RELEASE.md
    
    git add .
    git status
    
    read -p "Happy (y/n)? " CONT
    if [ "$CONT" = "y" ]; then
        git 
        git commit -m "Version $VERSION"
        git tag -fa $VERSION -m "$MESSAGE"
        echo
        echo " ***************  done!  **************** "
        echo " ***                                  *** "
        echo " ***         congratulations!         *** "
        echo " ***      please git push --tags      *** "
        echo " ***        if you're serious         *** "
        echo " ***                                  *** "
        echo " ******* e l e k t r o s l ö j d ******** "
        echo

    else
        echo "Aborted on operator request. Your tree is dirty."
    fi
else 
    echo Aborting: we do not bump version when there are uncommitted changes in this house
fi
