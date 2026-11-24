@echo off
title [1] TEDDYSHOP - MAY CHU PRODUCTION (WAITRESS WSGI)
cd /d D:\GauBongDjango
color 0B
echo ====================================================================
echo      CU'A HA`NG GA'U BO^NG TEDDYSHOP - PRODUCTION SERVER
echo ====================================================================
echo.
echo  [*] Cong nghe WSGI : Waitress Multi-Threaded Server (8 luong)
echo  [*] Co so du lieu  : Microsoft SQL Server (SQLEXPRESS)
echo  [*] Thu muc goc    : D:\GauBongDjango
echo.
echo  Dia chi truy cap tren may tinh:
echo  --^> http://127.0.0.1:8000
echo  --^> http://localhost:8000
echo.
echo  Tai khoan Admin:
echo  --^> Username: THAWNGS
echo  --^> Password: 01688583194a
echo.
echo ====================================================================
echo Nhan Ctrl + C de dung may chu.
echo.
python deploy_production.py
pause
