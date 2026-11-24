@echo off
title TEDDYSHOP - DEPLOY RA INTERNET CONG KHAI (HTTPS)
cd /d D:\GauBongDjango
color 0B
echo ====================================================================
echo      TEDDYSHOP - HE THONG DEPLOY TOAN CAU QUA INTERNET (HTTPS)
echo ====================================================================
echo.
echo  [*] Dang kiem tra May chu Production (Waitress WSGI)...
tasklist /fi "imagename eq python.exe" | findstr /i "python.exe" > nul
if errorlevel 1 (
    echo  [*] Dang bat May chu Production Waitress tren cong 8000...
    start "[SERVER] TEDDYSHOP WAITRESS PRODUCTION" cmd /c "python deploy_production.py"
    timeout /t 3 /nobreak > nul
) else (
    echo  [OK] May chu Production Waitress da dang chay san sang!
)

echo.
echo ====================================================================
echo  BAN CO 2 KENH TAO LINK HTTPS VA MA QR DE THAY CO TEST:
echo ====================================================================
echo.
echo  [1] Kenh SSH Tunnel (CO MA QR QUET TREN DIEN THOAI - KHONG SO LOI 429)
echo  [2] Kenh Cloudflare Tunnel (trycloudflare.com)
echo.
set /p opt="Nhap lua chon [1 hoac 2, mac dinh bam Enter la 1]: "

if "%opt%"=="2" goto cloudflare_mode

:ssh_mode
echo.
echo  [*] Dang khoi tao duong truyen HTTPS va ma QR (Vui long doi 3 giay)...
echo.
ssh -o StrictHostKeyChecking=no -R 80:localhost:8000 nokey@localhost.run
pause
exit

:cloudflare_mode
echo.
echo  [*] Dang ket noi Cloudflare Tunnel...
cloudflared.exe tunnel --url http://127.0.0.1:8000
pause
exit
