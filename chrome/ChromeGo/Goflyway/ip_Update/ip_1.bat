@Echo Off
Title ��GitHub�ƶ˸��� Goflyway ��������
cd /d %~dp0
..\..\wget --ca-certificate=ca-bundle.crt -c https://raw.githubusercontent.com/Alvin9999/pac2/master/config.ini
del "..\config.ini_backup"
ren "..\config.ini"  config.ini_backup
copy /y "%~dp0config.ini" ..\config.ini
del "%~dp0config.ini"
ECHO.&ECHO.�Ѹ���������¿���Goflyway����,�밴������˳�,����������. &PAUSE >NUL 2>NUL