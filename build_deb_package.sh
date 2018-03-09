#!/bin/bash -x

set -eu


DIST_DIR_NAME="dist"
INSTALL_DIR_PATH="/usr/bin"
DIST_DIR_PATH="./${DIST_DIR_NAME}/${INSTALL_DIR_PATH}"
PKG_NAME="tcconfig"

have_pyinstaller=0
if type pyinstaller > /dev/null 2>&1; then
    have_pyinstaller=1
fi

if [ ${have_pyinstaller} -eq 0 ];then
    exit 2
fi

# initialize
rm -rf $DIST_DIR_NAME
mkdir -p "${DIST_DIR_NAME}/DEBIAN"

pip install --upgrade .
PKG_VERSION=$(python -c "import pkg_resources; print(pkg_resources.get_distribution('${PKG_NAME}').version)")

echo $PKG_NAME $PKG_VERSION


# build an executable binary file
pyinstaller cli_tcset.py --clean --onefile --distpath $DIST_DIR_PATH --name tcset
pyinstaller cli_tcdel.py --clean --onefile --distpath $DIST_DIR_PATH --name tcdel
pyinstaller cli_tcshow.py --clean --onefile --distpath $DIST_DIR_PATH --name tcshow


# build a deb package
cat << _CONTROL_ > "${DIST_DIR_NAME}/DEBIAN/control"
Package: $PKG_NAME
Version: $PKG_VERSION
Maintainer: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
Architecture: amd64
Description: $(cat docs/pages/introduction/summary.txt)
Homepage: https://github.com/thombashi/tcconfig
Priority: extra
_CONTROL_

fakeroot dpkg-deb --build $DIST_DIR_NAME $DIST_DIR_NAME
