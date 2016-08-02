# Grafana (armhf)

### Debian
* [grafana_3.0.2_armhf.deb](https://s3.eu-central-1.amazonaws.com/belodetech/grafana_3.0.2_armhf.deb)
* [grafana_3.0.4_armhf.deb](https://s3.eu-central-1.amazonaws.com/belodetech/grafana_3.0.4_armhf.deb)

### Fedora/CentOS
* [grafana-3.0.2.armv7l.rpm](https://s3.eu-central-1.amazonaws.com/belodetech/grafana-3.0.2.armv7l.rpm)
* [grafana-3.0.4.armv7l.rpm](https://s3.eu-central-1.amazonaws.com/belodetech/grafana-3.0.4.armv7l.rpm)

### Build
Tested with `Grafana v3.0.4` on `2016-06-06`.

```
# update gcc and g++ (run once per build environment)
update-alternatives --remove-all gcc
update-alternatives --remove-all g++
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.6 20
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 50
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.6 20
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.9 50
update-alternatives --config gcc
update-alternatives --config g++

# install phantomjs globally to v2.1.1 (run once per build environment, until dep. version changes)
git clone https://github.com/shabadoo75/phantomjs-2.1.1-raspberrypi-armv7
cp phantomjs-2.1.1-raspberrypi-armv7/phantomjs /usr/bin/
# make sure libicu48 is installed, https://packages.debian.org/wheezy/armhf/libicu48/download

# get sources
export VERSION=v3.0.4
gvm use go1.5
gvm pkgset create grafana
gvm pkgset use grafana
cd ~/.gvm/pkgsets/go1.5/grafana
export GOPATH=`pwd`
go get github.com/grafana/grafana || go get -u github.com/grafana/grafana
cd $GOPATH/src/github.com/grafana/grafana
git checkout $VERSION

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
