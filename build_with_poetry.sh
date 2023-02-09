#!/bin/bash

VERSION=$1

if [[ -z "$VERSION" ]]; then
  echo "Version number required as first argument"
  exit 1
fi

if ! which sed; then
  alias sed=gsed
fi

if ! which poetry; then
  pip install poetry
fi

ZIP_FILE="slack-okta-bot-${VERSION}.zip"
poetry export -f requirements.txt --without-hashes -o requirements.txt # Until Poetry releases 1.2 with plugins
sed -i '1d' requirements.txt
poetry run pip install . -r requirements.txt -t package
(cd package && zip -r ../${ZIP_FILE} . -x '*.pyc')
