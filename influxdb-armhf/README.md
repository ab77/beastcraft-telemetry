# influxdb build notes

export VERSION=0.12.1
gvm use go1.4.3
gvm pkgset create influxdb
gvm pkgset use influxdb
cd ~/.gvm/pkgsets/go1.4.3/influxdb
export GOPATH=`pwd`
go get github.com/influxdata/influxdb
cd $GOPATH/src/github.com/influxdata/influxdb
./build.py --package --version=$VERSION --arch=armhf

# install using 'dpkg -i build/*.deb'
