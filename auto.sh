#!/usr/bin/env bash
# Filename: auto.sh

clNoColor='\033[0m'
clBlack='\033[0;30m'     
clRed='\033[0;31m'     
clGreen='\033[0;32m'     
clOrange='\033[0;33m'     
clBlue='\033[0;34m'     
clPurple='\033[0;35m'     
clCyan='\033[0;36m'     
clLight_Gray='\033[0;37m'
clDark_Gray='\033[1;30m'
clLight_Red='\033[1;31m'
clLight_Green='\033[1;32m'
clYellow='\033[1;33m'
clLight_Blue='\033[1;34m'
clLight_Purple='\033[1;35m'
clLight_Cyan='\033[1;36m'
clWhite='\033[1;37m'

if [[ $1 = 'pull' ]]
then
	git pull
fi

if [[ $1 = 'push' ]]
then
	msg="Auto $(date)"  
	git add --all
	git commit -m "$msg"
	echo -e "${clYellow}"
	git push
	echo -e "${clNoColor}"
	echo ""
	echo -e "${clLight_Red}Pushou ${clYellow}''$msg''${clLight_Red}"
	echo -e "${clNoColor}"
	echo ""	
fi

if [[ $1 = 'req' ]]
then
	pip freeze > requirements.txt
fi

if [[ $1 = 'docker-build-run' ]]
then
	docker build -t image-dhremoto:latest .
	docker run --env-file .envfordocker --name dhremoto -p 8000:8000 image-dhremoto:latest
fi


if [[ $1 = 'docker-stop-rm-build-run' ]]
then
	docker container stop dhremoto
	docker container rm dhremoto
	docker build -t image-dhremoto:latest .
	docker run --env-file .envfordocker --name dhremoto -p 8000:8000 image-dhremoto:latest
	docker tag image-dhremoto harbor.cl.df.gov.br/direitoshumanos/direitoshumanos-remoto:1.0.1
	docker push harbor.cl.df.gov.br/direitoshumanos/direitoshumanos-remoto:1.0.1
fi

if [[ $1 = 'bash' ]]
then
	docker exec -it dhremoto bash
fi

if [[ $1 = 'run' ]]
then
	python manage.py runserver
fi

if [[ $1 = 'pg-restart' ]]
then
	sudo service postgresql restart
fi

if [[ $1 = 'apache-restart' ]]
then
	sudo service apache2 restart
fi

if [[ $1 = 'up' ]]
then
  if [[ $2 != '' ]]
  then
    echo -e "${clLight_Red}Construindo imagem com tag ${clYellow}''$2''${clLight_Red}"
    sleep 1
    docker build -t image-dhremoto:latest . &&
    sleep 2

    echo -e "${clLight_Red}Construindo tag ${clYellow}''$2''${clLight_Red}"
    sleep 1
    docker tag image-dhremoto harbor.cl.df.gov.br/direitoshumanos/direitoshumanos-remoto:$2 &&
    sleep 2

    echo -e "${clLight_Red}Subindo para o harbor ${clNoColor}"
    sleep 1
    docker push harbor.cl.df.gov.br/direitoshumanos/direitoshumanos-remoto:$2
  fi
fi


if [[ $1 = 'apache-restart' ]]
then
	docker run container-postgres --restart always
fi

if [[ $1 = 'plus' ]]
then
	versao=$(cat version.txt)
	echo -e "${clOrange}Versão lida: ${clYellow} $versao ${clNoColor}"
	IFS='.' read -ra partes <<< "$versao"
	parte_menor=$((partes[2] + 1))
	nova_versao="${partes[0]}.${partes[1]}.$parte_menor"
	echo -e "${clOrange}Incrementar para ${clYellow}$nova_versao ${clOrange}e fazer o deploy? [Ss] para Sim${clNoColor}"
	read -n 1 -r
	echo # (optional) move to a new line
	if [[ $REPLY =~ ^[Ss]$ ]]
	then
		echo "$nova_versao" > version.txt &&
		sleep 2

		echo -e "${clLight_Red}Construindo imagem com tag ${clYellow}''$nova_versao''${clLight_Red}"
		sleep 1
		docker build -t image-dhremoto:latest . &&
		sleep 2

		echo -e "${clLight_Red}Construindo tag ${clYellow}''$nova_versao''${clLight_Red}"
		sleep 1
		docker tag image-dhremoto harbor.cl.df.gov.br/direitoshumanos/direitoshumanos-remoto:$nova_versao &&
		sleep 2

		echo -e "${clLight_Red}Subindo para o harbor ${clNoColor}"
		sleep 1
		docker push harbor.cl.df.gov.br/direitoshumanos/direitoshumanos-remoto:$nova_versao
	fi	
fi