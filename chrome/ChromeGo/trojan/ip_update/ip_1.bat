@Echo Off
Title ��GitHub�ƶ˸��� Trojan ��������
cd /d %~dp0
..\..\wget --ca-certificate=ca-bundle.crt -c https://raw.githubusercontent.com/Alvin9999/pac2/master/config.json
del "..\config.json_backup"
ren "..\config.json"  config.json_backup
copy /y "%~dp0config.json" ..\config.json
del "%~dp0config.json"
ECHO.&ECHO.�Ѹ���IP������Ϣ������������֤���ļ���

..\..\wget --ca-certificate=ca-bundle.crt -c https://raw.githubusercontent.com/Alvin9999/pac2/master/crt/private.crt
del "..\private.crt_backup"
ren "..\private.crt"  private.crt_backup
copy /y "%~dp0private.crt" ..\private.crt
del "%~dp0private.crt"
ECHO.&ECHO.�Ѹ���֤���ļ���

ECHO.&ECHO.�Ѹ���������¿���trojan����,�밴������˳�,����������. &PAUSE >NUL 2>NUL