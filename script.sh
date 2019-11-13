#!/bin/bash
echo '## Reezocar PERF WAR TEAM test init'

E_BAD_ARGS=85
E_NO_JSONFILE=85

DATE=`date '+%Y%m%d-%H%M%S'`
RESULTDIR=./results
JSONFILE=./urlConfig.json

# testName parameter test
if [ -n "$1" ]
then
  echo "$DATE - $1 init:"
  testName=$1
else
  echo '!E: $1 parameter needed'
  exit $E_BAD_ARGS
fi

# create results directory
if [[ ! -e $RESULTDIR ]]; then
    mkdir $RESULTDIR
    echo 'result Directory created'
fi

# urlConfig.json test
if [ ! -f $JSONFILE ]; then
   echo "File $JSONFILE does not exist."
   exit $E_NO_JSONFILE
fi

cat $JSONFILE | while read key value; do
  echo "# lighthouse test $key"
  FILE="$RESULTDIR/$1-$DATE-$key-report.json"
  lighthouse $value --chrome-flags="--headless --no-sandbox" --only-categories=performance --output=json --output-path=$FILE
  echo "#generate $FILE"
done
