@echo off

setlocal enabledelayedexpansion

rem 运行翻译脚本
python global_exploit.py

rem 检查是否有未提交的更改
for /f "delims=" %%i in ('git status --porcelain') do set "has_changes=1"

if defined has_changes (
    rem 提交更改
    git add .
    git commit -m "Globalize: Translate files"
    git push
    echo 翻译完成并已推送到远程仓库
) else (
    echo 没有需要提交的更改
)

pause