#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Need to specify a project name as an arg: exiting."
    echo "Usage: $0 \$moinwiki \$confluencespace \$history"
exit 1;
fi

BASEDIR="/usr/local/etc/moin-to-cwiki/universal-wiki-converter"
CONFDIR="$BASEDIR/conf"
PROJECT=$1
SPACE=$2
HISTORY=$3

# check project dir exists

if [ ! -d "$BASEDIR/projects/$PROJECT" ]; then
    echo "This project doesnt seem to exist: exiting."
exit 1;
fi

# copy confluence.properties.template and append space variables
/bin/cp $CONFDIR/confluenceSettings.properties.template $CONFDIR/confluenceSettings.properties
echo "space=$SPACE" >> $CONFDIR/confluenceSettings.properties

# copy exporter template and append space variables
/bin/cp $CONFDIR/exporter.moinmoin.properties.template $CONFDIR/exporter.moinmoin.properties
echo "src=$BASEDIR/projects/$PROJECT/data/pages" >> $CONFDIR/exporter.moinmoin.properties
echo "out=$BASEDIR/projects/$PROJECT/data/$PROJECT-pages-out" >> $CONFDIR/exporter.moinmoin.properties
echo "history=$HISTORY" >> $CONFDIR/exporter.moinmoin.properties

# If history is true then we need to uncomment a couple of converter lines.
# but lets reset it back to template before deciding.
/bin/cp $CONFDIR/converter.moinmoin.properties.template $CONFDIR/converter.moinmoin.properties

if [ $HISTORY == true ]; then
  /bin/sed -i s'|#MoinMoin.0002|MoinMoin.0002|' $CONFDIR/converter.moinmoin.properties
  /bin/sed -i s'|#MoinMoin.0003|MoinMoin.0003|' $CONFDIR/converter.moinmoin.properties  
fi

