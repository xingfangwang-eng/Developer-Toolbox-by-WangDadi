@echo off
e:
:: 确保进入了母舰仓库的根目录
cd E:\Developer-Toolbox-by-WangDadi

echo [1/2] Running Bridge...
:: 尝试直接运行 python bridge.py，而不是带绝对路径，这样更稳
python bridge.py

echo [2/2] Pushing to GitHub...
python brute_push.py

echo.
echo Done! All SaaS tools are now live and monitored.
pause