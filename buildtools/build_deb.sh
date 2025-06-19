#!/bin/bash

set -e

# App metadata
APP_NAME="m3"
VERSION="3.139.1"
ARCH="amd64"

# Directories
BUILD_DIR="build"
DIST_DIR="dist"
BIN_NAME="${APP_NAME}_bin"
PKG_DIR="$BUILD_DIR/pkg"

# Clean old builds
rm -rf "$BUILD_DIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR"

# Build the standalone binary using build.py with PyInstaller setup
python3.10 build.py

# Copy the binary to the packaging directory
cp "$DIST_DIR/$APP_NAME" "$BUILD_DIR/$BIN_NAME"

# Prepare .deb package layout
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/usr/local/bin"

# Move binary to proper location
cp "$BUILD_DIR/$BIN_NAME" "$PKG_DIR/usr/local/bin/$APP_NAME"
chmod 755 "$PKG_DIR/usr/local/bin/$APP_NAME"

# Create control file
cat <<EOF > "$PKG_DIR/DEBIAN/control"
Package: $APP_NAME
Version: $VERSION
Section: base
Priority: optional
Architecture: $ARCH
Maintainer: Your Name <you@example.com>
Description: m3 CLI application built with PyInstaller.
EOF

# Build the .deb package
dpkg-deb --build "$PKG_DIR" $DIST_DIR/"${APP_NAME}_${VERSION}_${ARCH}.deb"

echo "✅ Package built: ${APP_NAME}_${VERSION}_${ARCH}.deb"
