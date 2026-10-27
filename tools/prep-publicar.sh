#!/bin/bash
# Prepara la publicación de un curso sobre la versión del servidor:
#   prep-publicar.sh <slug> <servidor.json> [campos de enriquecer] [--estructura]
# Deja en /mnt/user-data/outputs: site-<T>.tgz (código + ilustraciones del curso), <slug>-imp-<T>.json,
# glosario-<T>.json y pub-<slug>-<T>.sh, e imprime los sha256 para verificar en la PC.
set -e
SLUG=$1; SRV=$2; CAMPOS=${3:-fig,auto,teoria,teoria_figs,concepts,steps}; EST=$4
R=/home/claude/ies-training; W=/tmp/claude-0/prep; mkdir -p $W
cd $R
python3 tools/enriquecer.py $SRV $SLUG $W/$SLUG-e.json --campos $CAMPOS
if [ "$EST" = "--estructura" ]; then python3 tools/estructura.py $W/$SLUG-e.json $SLUG $W/$SLUG.json; else cp $W/$SLUG-e.json $W/$SLUG.json; fi
T=$(date +%H%M%S); O=/mnt/user-data/outputs
(cd site2 && tar czf $O/site-$T.tgz --exclude='*.png' ./index.html ./assets ./api ./ilustraciones/$SLUG)
cp site2/data/glosario.json $O/glosario-$T.json
cp $W/$SLUG.json $O/$SLUG-imp-$T.json
M=$(md5sum $SRV | cut -c1-32)
PROBE=$(cd site2/ilustraciones/$SLUG && ls *-t1.svg 2>/dev/null | head -1); PROBE=${PROBE:-1.webp}
sed -e "s/__SLUG__/$SLUG/" -e "s/__MD5__/$M/" -e "s#__PROBE__#/ilustraciones/$SLUG/$PROBE#" tools/publicar-plantilla.sh > $O/pub-$SLUG-$T.sh
echo "T=$T  tamaño=$(stat -c %s $O/site-$T.tgz)"
cd $O && sha256sum site-$T.tgz $SLUG-imp-$T.json glosario-$T.json
