docker create -ti --name dummy huangdeng/apex bash
docker cp dummy:/root/apex/dist/ ./
docker rm -fv dummy