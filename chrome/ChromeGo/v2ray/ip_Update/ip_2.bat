@Echo Off
Title ��COD�ƶ˸�G� v2ray ��G¿��� IP or ����
cd /d %~dp0
..\..\wget --ca-certificate=ca-bundle.crt -c https://coding.net/u/Alvin9999/p/pac/git/raw/master/guiNConfig.json
del "..\guiNConfig.json_backup"
ren "..\guiNConfig.json"  guiNConfig.json_backup
copy /y "%~dp0guiNConfig.json" ..\guiNConfig.json
del "%~dp0guiNConfig.json"
ECHO.&ECHO.�Ѹ�G������G¿���v2ray����,�밴������˳�,��������G�. &PAUSE >NUL 2>NUL