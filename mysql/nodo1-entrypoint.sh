#!/bin/sh
set -eu

if [ -f /var/lib/mysql/grastate.dat ]; then
  sed -i 's/^safe_to_bootstrap: .*/safe_to_bootstrap: 1/' /var/lib/mysql/grastate.dat
fi

exec /usr/local/bin/docker-entrypoint.sh mariadbd --wsrep-new-cluster
