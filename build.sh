#!/bin/bash
###
# @Author: gandli
# @Date: 2022-03-14 11:59:28
# @LastEditTime: 2022-03-14 12:43:57
# @LastEditors: gandli
# @Description:
# @FilePath: \gandli\build.sh
###

export VERSION=$1
npm run build
zip -q -r bin.zip bin/
