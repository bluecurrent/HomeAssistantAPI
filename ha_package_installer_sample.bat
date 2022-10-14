:: This script is an sample for installing an unreleased api package into the Ha devcontainer.
:: To use, please copy this file and name it ha_package_installer.* so it will be ignored by git and change the variables.
:: If you are on Linux and cannot run batch scripts, copy the commands and create a bash script. (named ha_package_installer)

@echo off

:: CHANGE ME
set container="CONTAINER"
set version="VERSION"

:: build the package
make build


:: copy the .whl file to the HA container
docker cp dist\bluecurrent_api-%version%-py3-none-any.whl %container%:/workspaces/core/

:: install the package in the container
docker exec %container% pip install core/bluecurrent_api-%version%-py3-none-any.whl --no-deps --force-reinstall

:: delete the .whl file
docker exec %container% rm core/bluecurrent_api-%version%-py3-none-any.whl