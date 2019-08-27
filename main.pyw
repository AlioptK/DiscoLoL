import ruamel_yaml, socket
import os, sys, time
import subprocess

command = f'mode con: cols=52 lines=2'

batFile = """
@echo off
mode con: cols=52 lines=2

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------


"""
commands = ['netsh advfirewall firewall add rule name="lolchat" dir=out remoteip=%IP% protocol=TCP action=block', 'netsh advfirewall firewall delete rule name=lolchat']

def getCorrespondingIP(domain):
    return socket.gethostbyname(domain)

def getConfig():
    with open('./config/config.yaml', "r") as f:
        data = ruamel_yaml.safe_load(f)
    return data['isCurrentlyOffline'], getCorrespondingIP(data["Servers"][data["Region"]])

def writeBat(bat):
    with open("./config/temp.bat", "w") as f:
        f.write(bat)

def deleteBat():
    os.remove("./config/temp.bat")

def changeConfig():
    with open('./config/config.yaml') as f:
        data = ruamel_yaml.YAML().load(f)
        if data["isCurrentlyOffline"] == False:
            data['isCurrentlyOffline'] = True
        else:
            data["isCurrentlyOffline"] = False
    with open('./config/config.yaml', "w") as f:
            ruamel_yaml.YAML().dump(data, f)

def blockIP(baseDir):
    isOffline, IP = getConfig()

    if isOffline:
        batFile1 = batFile + commands[1]
        os.system(f'{command} && ECHO You will appear connected on League of Legends. & color 0A & TITLE Chat ON && ping 127.0.0.1 -n 3 > nul')
    else:
        batFile1 = batFile + f'\nset IP=' + str(IP) + '\n' + commands[0]
        os.system(f'{command} && ECHO You will appear disconnected on League of Legends. & color 04 & TITLE Chat OFF && ping 127.0.0.1 -n 3 > nul')
    
    writeBat(batFile1)
    print(baseDir+'\\config\\temp.bat')
        
    proc = subprocess.Popen(baseDir+'\\config\\temp.bat',
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            stdin=subprocess.PIPE,
                            cwd=os.getcwd(),
                            env=os.environ)
    proc.stdin.close()
    time.sleep(3)
    deleteBat()
    changeConfig()
    
    
if __name__ == "__main__":
    baseDir = os.path.dirname(sys.argv[0])
    blockIP(baseDir)
