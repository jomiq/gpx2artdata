#! /bin/bash
BUMP=${1-minor}
MESSAGE=${2-"No description provided. Deal with it."}
export EDITOR=${EDITOR-"code"}

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
    git add .
    
    
    git commit -m "Version $VERSION"
    git tag $VERSION -m "$MESSAGE"
    git-changelog
    
    echo "# Version $VERSION - $(date)\n" > RELEASE.md
    echo "Provide a short release description ...."
    $EDITOR RELEASE.md
    echo "Thank you"
    git add CHANGELOG.md RELEASE.md
    git commit --amend --no-edit
    git tag -fa $VERSION -m "$MESSAGE"

else 
    echo Aborting: we do not bump version when there are uncommitted changes in this house
fi

echo
echo " ***************  done!  **************** "
echo " ***                                  *** "
echo " ***         congratulations!         *** "
echo " ***      please git push --tags      *** "
echo " ***        if you're serious         *** "
echo " ***                                  *** "
echo " ******* e l e k t r o s l ö j d ******** "
echo