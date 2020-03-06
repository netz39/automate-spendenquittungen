#! bin/bash
indir=$1
mkdir -p $(pwd)/tmp
cp indir/*.json.xml $(pwd)/tmp/
docker run \
    -v $(pwd)/tmp:/work \
    xml2pdf \
    -rm
cp tmp/*.pdf indir/
rm -r tmp/