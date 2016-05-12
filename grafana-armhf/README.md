# Grafana (armhf)

### Debian

* [grafana_3.0.2-1463058303_armhf.deb](https://s3.eu-central-1.amazonaws.com/belodetech/grafana_3.0.2-1463058303_armhf.deb)

### Fedora/CentOS

* [grafana-3.0.2-1463058303.armv7l.rpm](https://s3.eu-central-1.amazonaws.com/belodetech/grafana-3.0.2-1463058303.armv7l.rpm)

### Build
Tested with `Grafana v3.0.2` on `2016-05-12`.

```
# update gcc ang g++
update-alternatives --remove-all gcc
update-alternatives --remove-all g++
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.6 20
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 50
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.6 20
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.9 50
update-alternatives --config gcc
update-alternatives --config g++

# install phantomjs globally
git clone https://github.com/shabadoo75/phantomjs-2.1.1-raspberrypi-armv7
cp phantomjs-2.1.1-raspberrypi-armv7/phantomjs /usr/bin/

# get sources
gvm use go1.5
gvm pkgset create grafana
gvm pkgset use grafana
cd ~/.gvm/pkgsets/go1.5/grafana
export GOPATH=`pwd`
go get github.com/grafana/grafana || go get -u github.com/grafana/grafana
cd $GOPATH/src/github.com/grafana/grafana

# build
go run build.go setup
$GOPATH/bin/godep restore
npm install npm -g
npm install
npm install -g grunt-cli
npm rebuild node-sass
go run build.go build package
```

### Install (Debian)

```
dpkg -i dist/*.deb
```

#### References

* http://www.aymerick.com/2013/09/24/go_language_on_raspberrypi.html
* http://www.aymerick.com/2015/10/07/influxdb-telegraf-grafana-raspberry-pi.html
* https://hwwong168.wordpress.com/2015/11/19/building-grafana-for-raspberry-pi-2/
* http://giatro.me/2015/09/30/install-influxdb-and-grafana-on-raspberry-pi.html
* https://github.com/shabadoo75/phantomjs-2.1.1-raspberrypi-armv7
