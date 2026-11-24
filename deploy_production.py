"""
deploy_production.py - Chay Production Server cho TeddyShop bang Waitress WSGI
Khong can may ao, khong dung runserver thu nghiem.
"""
import os
import sys
from pathlib import Path

# Thiet lap duong dan project
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaubong.settings')

# Import Django WSGI Application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from waitress import serve

if __name__ == '__main__':
    port = 8000
    host = '0.0.0.0'
    threads = 8

    print("=" * 65)
    print("      TEDDYSHOP - PRODUCTION SERVER (WAITRESS WSGI)")
    print("=" * 65)
    print(f" [*] Cong nghe chu quan: Waitress WSGI Server ({threads} threads)")
    print(" [*] Co so du lieu     : Microsoft SQL Server (SQLEXPRESS)")
    print(" [*] Che do deploy     : Windows Native Host (No Virtual Machine)")
    print(f" [*] Localhost URL     : http://127.0.0.1:{port}")
    print(f" [*] LAN Network URL   : http://localhost:{port}")
    print("=" * 65)
    print(" May chu san sang nhan yeu cau! Nhan Ctrl + C de dung.\n")

    serve(application, host=host, port=port, threads=threads)
