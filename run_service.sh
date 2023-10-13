export COMPOSE_HTTP_TIMEOUT=1200
export DOCKER_CLIENT_TIMEOUT=1200

RESTART_FLAG=0
TRAIN_DATA=''

SERVER_IP='127.0.0.1'
TRAIN_CONTAINER='gpt-insight-model-openai'
INFERENCE_CONTAINER='gpt-insight-inference-openai'
INTERFACE_CONTAINER='gpt-insight-web-openai'
OPENAI_API_TYPE=''
OPENAI_API_BASE=''
OPENAI_API_VERSION=''
OPENAI_API_KEY=''
OPENAI_ENGINE=''
OPENAI_ENCODER=''
SKIP=''

while getopts i:d:t:b:v:k:e:c:s: flag
do
    case "$flag" in
        i) SERVER_IP=${OPTARG};;
        d) TRAIN_DATA=${OPTARG};;
        t) OPENAI_API_TYPE=${OPTARG};;
        b) OPENAI_API_BASE=${OPTARG};;
        v) OPENAI_API_VERSION=${OPTARG};;
        k) OPENAI_API_KEY=${OPTARG};;
        e) OPENAI_ENGINE=${OPTARG};;
        c) OPENAI_ENCODER=${OPTARG};;
        s) SKIP=${OPTARG};;
    esac
done


if [[ ! $(docker --version) ]];
then
    sudo apt-get update -y
    sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
    sudo apt-get update -y
    sudo apt-get install -y docker-ce
    sudo usermod -a -G docker $USER
    RESTART_FLAG=1
else
    echo "docker has been installed."
    docker network inspect nginx_network --format {{.Id}} >/dev/null 2>&1 || docker network create --driver bridge nginx_network
fi

if [[ ! $(docker compose version) ]];
then
    sudo apt-get install -y docker-compose-plugin
else
    echo "docker compose has been installed."
fi

if [[ $RESTART_FLAG == 1 ]];
then
    sudo reboot
fi

base_path=$(pwd)
docker-compose -f $base_path/docker-compose.yml down

if [ -n "$TRAIN_DATA" ]
then
    cp $TRAIN_DATA $base_path/data/raw_data.xlsx
fi

if [[ $SKIP == "skip-train" ]]
then
    if [ -n "$OPENAI_API_TYPE" ]
    then
        OPENAI_API_TYPE=$OPENAI_API_TYPE OPENAI_API_BASE=$OPENAI_API_BASE OPENAI_API_VERSION=$OPENAI_API_VERSION OPENAI_API_KEY=$OPENAI_API_KEY docker-compose -f $base_path/docker-compose.yml up -d $TRAIN_CONTAINER
        docker exec -it $TRAIN_CONTAINER bash -c "python3 /app/fine-tuning.py --data /data/raw_data.xlsx"
        docker-compose -f $base_path/docker-compose.yml down
    else
        echo "Since Azure temporarily disable the fine-tuning feature, the training stage is skipped."
    fi
fi

if [[ $SKIP == "skip-inference" ]]
then
    echo "set server ip: $SERVER_IP"
    cp $base_path/build/interface/web/gpt_qa/template/main.js.temp $base_path/build/interface/web/gpt_qa/main.js
    sed -i "s/SERVER_IP/$SERVER_IP/g" $base_path/build/interface/web/gpt_qa/main.js
    docker-compose -f $base_path/docker-compose.yml up -d $INTERFACE_CONTAINER
    OPENAI_API_TYPE=$OPENAI_API_TYPE OPENAI_API_BASE=$OPENAI_API_BASE OPENAI_API_VERSION=$OPENAI_API_VERSION OPENAI_API_KEY=$OPENAI_API_KEY OPENAI_ENGINE=$OPENAI_ENGINE OPENAI_ENCODER=$OPENAI_ENCODER docker-compose -f $base_path/docker-compose.yml up -d $INFERENCE_CONTAINER
    echo "Please enter the URL link below into your browser to activate the dialog interface
        URL link: http://$SERVER_IP/gpt/qa/"
fi
