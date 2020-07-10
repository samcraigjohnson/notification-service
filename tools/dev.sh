#!/bin/bash
# Helper file for running things

pexec() {
  docker exec -it postgres "$@"
}

clean() {
    find . -name "*.pyc" -delete
    rm -rf **/*__pycache__
}

killdb() {
  docker rm -f postgres
}

start-postgres() {
  echo "Starting postgres..."

  if docker ps | grep -q postgres; then
    echo "Postgres already started!"
    return 0
  fi

  docker start postgres && return 0

  docker run --name postgres \
       -e POSTGRES_DB=notifs \
       -e POSTGRES_PASSWORD=postgres \
       -p 5432:5432 -d postgres

  sleep 10
  pexec psql -U postgres -c "create database notifications_test"
}

case "$1" in
  postgres)
    start-postgres
    ;;

  deploy)
    clean

    echo "Deploying web prod!"
    eb deploy japanese-prod

    echo "Deploying worker!"
    eb deploy worker1-prod
    ;;

  docker-build)
    docker build -t notifications .
    ;;

  dev)
    start-postgres
    echo "Starting yarn..."
    (cd web; yarn start) &

    echo "Starting unicorn..."
    gunicorn --reload --bind=0.0.0.0:3000 --access-logfile - --error-logfile - --log-level debug app:application
    ;;

  test)
    TEST=true pytest test_notifications.py
    ;;

  clean)
    clean
    ;;

  psql)
    shift
    pexec psql -U postgres "$@"
    ;;

  pexec)
    shift
    pexec "$@"
    ;;

  *) echo "Not an option"
     ;;
esac
