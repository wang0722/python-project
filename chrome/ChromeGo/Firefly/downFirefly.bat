@Echo Off
echo .
echo .
echo ================================================== 
echo ��������firefly�����Ժ򣬲���ɱ�������������...
echo ================================================== 
echo .
echo .
cd /d %~dp0
..\wget --ca-certificate=ca-bundle.crt -c https://github.com/yinghuocho/download/blob/master/firefly_windows_386.exe?raw=true -O firefly.exe
ECHO.&ECHO.������Firefly. 
exit
