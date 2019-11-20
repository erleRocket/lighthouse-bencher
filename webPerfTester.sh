#!/bin/bash
E_BAD_ARGS=85
E_NO_URLCONFIGFILE=85
E_NO_ENV_NAME=85

if [[ -z "${URL_TYPE}" ]]; then
  URLCONFIGFILE=./urlConfig.json
  echo "____not URL_TYPE____\n"
fi

case $URL_TYPE in
    "all")
        URLCONFIGFILE=./urlConfig.json
        ;;
esac

DATE=`date '+%Y%m%d-%H%M%S'`
RESULTDIR=/lighthouse_bench/reports/lighthouse-auto


# $SLEEP
if [[ -z $SLEEP ]]; then
    SLEEP=10
fi

echo '######################################################'
echo '##               '$DATE'              ########'
echo '## REEZOCAR: WAR TEAM - LightHouse Auto Bench ########'
echo '##               '$URL_TYPE'      ########'
echo '##         Sleep      '$SLEEP'      ########'
echo '######################################################'

# testName parameter test
if [[ -z "${ENV_NAME}" ]]; then
  exit $E_NO_ENV_NAME
else
  echo "👨🏻‍💻 lightHouse - $DATE - $ENV_NAME init:"
  echo "________\n"
fi

# create results directory
if [[ ! -e $RESULTDIR ]]; then
    mkdir -p $RESULTDIR
    echo 'info: result directories created'
fi

# urlConfig.json test
if [ ! -f $URLCONFIGFILE ]; then
   echo "warning: File $URLCONFIGFILE does not exist."
   exit $E_NO_URLCONFIGFILE
fi

# run
cat $URLCONFIGFILE | while read key value; do
  sleep $SLEEP

  FILE="$ENV_NAME-$DATE-$key-report"
  echo "🤖 $key: generate $ENV_NAME $key report"

  lighthouse $ENV_URL$value --quiet --chrome-flags="--headless --no-sandbox --user-agent=lighthouse-bench" --only-categories=performance --output=json --output-path=$RESULTDIR/$FILE.json

  # aggregation
  echo "👓 $key: parse "
  python parseResult.py $FILE.json

  # transfert
  echo "🚀 $key: transfert data "
  cat "$RESULTDIR/$FILE-results.json" | curl -X POST "https://listener.logz.io:8071?token=$LOGZIOTOKEN&type=elasticsearch" --data-binary @-  > /dev/null

  # clean
  find $RESULTDIR/ -iname "*.json" -type f -exec /bin/rm -fr {} \;
  echo "________"
done

DATE=`date '+%Y%m%d-%H%M%S'`
echo '## Finish at '$DATE'                    ########'
