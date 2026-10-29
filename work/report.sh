#!/usr/bin/env bash
# report.sh <sql-file> <pop>  ->  CSV on stdout, logs on stderr
set -Eeuo pipefail

usage() { echo "usage: $0 <sql-file> <pop>" >&2; exit 2; }
[[ $# -eq 2 ]] || usage
sql_file=$1
pop=$2
[[ -r $sql_file ]]     || { echo "cannot read $sql_file" >&2; exit 2; }
[[ $pop =~ ^[a-z]{3}$ ]] || { echo "invalid pop: $pop" >&2; exit 2; }

export PGOPTIONS='-c statement_timeout=30s -c lock_timeout=2s'

exec psql service="${PGSERVICE:-edge_rw}" \
     -X -q -w -v ON_ERROR_STOP=1 --csv \
     -v pop="$pop" -f "$sql_file"
