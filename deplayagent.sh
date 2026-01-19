#!/bin/bash

WorkPath=$(cd "$(dirname "$0")"; pwd)

source ${WorkPath}/envs/bin/activate

start(){
  python main.py >> ${WorkPath}/app.log 2>&1 &
  echo $! > ${WorkPath}/run.pid
}

status() {
  mpid=$(`cat "${WorkPath}/run.pid"`)
  ps -ef |grep "$mpid" | grep -v grep
}

stop() {
  mpid=$(cat "${WorkPath}/run.pid")
  if [ -n "${mpid}" ]; then
    kill -9 $mpid
  fi
}

case "$1" in
  start)
        start
	      status
        ;;
  stop)
        stop
        ;;
  restart|reload)
        stop
        start
        ;;
  status)
        status
        ;;
  *)
	usage
        exit 1
esac

exit 0