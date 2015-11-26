#!/bin/bash
START_MODE=0
DEBUG_MODE=1
RUN_MODE=2
SERVICE_MODE=3

function createFolder()
{
	if [ ! -e "$1" ] || [ ! -d "$1" ];then
		mkdir "$1"
	fi
	
	chown root:$APACHE_GROUP "$1" && chmod 775 "$1"
}

function usage()
{
	echo "-d | --debug: run in debug mode"
	echo "-r | --run: run in background"
	echo "-s | --service: run as service"
}

mode=$START_MODE

while [ "$1" != "" ]; do
    case $1 in
        -d | --debug )          mode=$DEBUG_MODE
                                ;;
        -r | --run )            mode=$RUN_MODE
                                ;;
        -s | --service)			mode=$SERVICE_MODE
        						;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

if [ "`whoami`" != "root" ];then
    echo "Error: you are not root"
    exit
fi

LOG_DIR="/var/log/roadmap"

APACHE_GROUP="apache"
OS=$(cat /etc/issue | head -n 1 | awk '{print $1}')
if [[ "$OS" == "Ubuntu" ]];then
	APACHE_GROUP="www-data"
fi

createFolder $LOG_DIR

dir=$(dirname $0)
case $mode in
	$START_MODE )		java -Dfile.encoding=UTF-8 -XX:MaxPermSize=256m -jar ${dir}/superstar-0.0.1-SNAPSHOT.jar 8043
						;;
	$DEBUG_MODE )		java -Dfile.encoding=UTF-8 -XX:MaxPermSize=256m -jar -agentlib:jdwp=transport=dt_socket,server=y,address=8000 ${dir}/superstar-0.0.1-SNAPSHOT.jar 8043
						;;
	$RUN_MODE )			nohup java -server -Dfile.encoding=UTF-8 -XX:MaxPermSize=256m -jar ${dir}/superstar-0.0.1-SNAPSHOT.jar 8043 2>&1 > /dev/null &
						;;
	$SERVICE_MODE )		java -server -Dfile.encoding=UTF-8 -XX:MaxPermSize=256m -jar ${dir}/superstar-0.0.1-SNAPSHOT.jar 8043 2>&1 > /dev/null &
						;;
esac
