# grafana build notes
# http://www.aymerick.com/2015/10/07/influxdb-telegraf-grafana-raspberry-pi.html
# https://hwwong168.wordpress.com/2015/11/19/building-grafana-for-raspberry-pi-2/
# http://giatro.me/2015/09/30/install-influxdb-and-grafana-on-raspberry-pi.html

update-alternatives --remove-all gcc
update-alternatives --remove-all g++
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.6 20
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 50
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.6 20
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.9 50
update-alternatives --config gcc
update-alternatives --config g++

gvm use go1.5
gvm pkgset use grafana
cd ~/.gvm/pkgsets/go1.5/grafana
export GOPATH=`pwd`
go get github.com/grafana/grafana
cd $GOPATH/src/github.com/grafana/grafana

# add "--force" flag to build.go, line 76
# comment phantomjs and karma:test lines in:
#  tasks/build_task.js
#  tasks/default_task.js
# remove in package.json:
#  "karma-phantomjs-launcher": "0.1.4"
go run build.go setup

$GOPATH/bin/godep restore
npm install npm -g
npm install
npm install -g grunt-cli
npm rebuild node-sass
grunt --force
go run build.go build package

# install using 'dpkg -i dist/*.deb'
