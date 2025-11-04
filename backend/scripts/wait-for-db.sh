#!/bin/sh
# wait-for-db.sh

set -e

# Pega o host e a porta das variáveis de ambiente
host="$1"
port="$2"
shift 2
cmd="$@"

# Loop até que a porta do banco esteja aberta
# Usamos 'nc' (netcat) que precisa ser instalado
until nc -z -v "$host" "$port"; do
  >&2 echo "MySQL está indisponível - esperando..."
  sleep 1
done

>&2 echo "MySQL está pronto - executando comando"
exec $cmd