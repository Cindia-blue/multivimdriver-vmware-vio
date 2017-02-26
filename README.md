1 prepare CentOS7 and Docker
Please refer to Reference for docker install and setup
https://wiki.open-o.org/display/IN/Using+Open-O+Docker+Images
2 prepare image
docker pull openoint/common-services-msb
docker pull openoint/common-services-extsys
docker pull openoint/common-services-drivermanager
docker pull openoint/gso-service-gateway
docker pull openoint/gso-service-manager
docker pull openoint/gso-gui-portal
docker pull openoint/multivim-driver-vio
3 start service
docker run  -t --name i-msb -p 80:80 openoint/common-services-msb
docker inspect --format '{{ .NetworkSettings.IPAddress }}' i-msb
4 registry service
docker run -t -e MSB_ADDR=172.17.0.2:80 openoint/gso-service-gateway
docker run -t -e MSB_ADDR=172.17.0.2:80 openoint/common-services-extsys
docker run -t -e MSB_ADDR=172.17.0.2:80 openoint/common-services-drivermanager
docker run -t -e MSB_ADDR=172.17.0.2:80 openoint/gso-gui-portal
docker run -t -e MSB_ADDR=172.17.0.2:80 openoint/gso-service-manager
docker run -t --name multivim-driver-vio -e MSB_ADDR=172.17.0.2:80 openoint/multivim-driver-vio
5 Check result
Check http://192.168.130.132/openoapi/multivim-vio/v1/swagger.json
6 Tune the code of VIO driver API
docker exec -it multivim-driver-vio /bin/bash
replace the /service/vio by code from github
https://github.com/Cindia-blue/multivimdriver-vmware-vio/
Please commit into your change to GitHub firstly before push to the OPENO gerrit repo:
6 More check
Registry VIO on http://localhost/openoui/microservices/index.html
get vim id  from http://localhost/openoui/default/common/default.html
