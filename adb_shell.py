# -*- coding:utf-8 -*-

__author__='BillKalin'
__datetime__='2016.8.17'

import os,shutil

class Command(object):
    def runCommand(self, cmd, error_msg='run command error!!!'):
        if 1 <= cmd <= 9:
            if not self.__checkAdbExe():
                print('adb.exe or AdbWinApi.dll lost !!')
                return
        if cmd == 1:
            self.__execAdbShell()
        elif cmd == 2:
            self.__execAdbDevices()
        elif cmd == 3:
            self.__execAdbShowAppPkgs()
        elif cmd == 4:
            self.__execInstallApp()
        elif cmd == 5:
            self.__execUninstallApp()
        elif cmd == 6:
            self.__execClearAppData()
        elif cmd == 7:
            self.__execForceStopApp()
        elif cmd == 8:
            self.__execDumpSysActivity()
        elif cmd == 9:
            self.__execDumpSysWindow()
        elif cmd == 10:
            self.__execDecodeApk()
        else:
            print(error_msg)

    def __checkAdbExe(self):
        adb_path = os.path.abspath('.')+"\\adb.exe"
        adb_dll_path = os.path.abspath('.')+"\\\AdbWinApi.dll"
        if os.path.exists(adb_path) and  os.path.exists(adb_dll_path):
            return True
        else:
            return False

    def __execAdbShell(self):
        os.system('adb shell')

    def __execAdbDevices(self):
        os.system('adb devices')

    def __execAdbShowAppPkgs(self):
        path = os.path.abspath('.')+"\\apps.txt"
        comStr = 'adb shell pm list packages > ' + path
        os.system(comStr)
        print('dump installed apps in ' + path)

    def __execClearAppData(self):
        pkg = input('package name : ')
        if pkg:
            os.system('adb shell pm clear %s'%(pkg))
        else:
            print('package name is wrong!!')

    def __execInstallApp(self):
        pkg = input('input apk absolute path : ')
        if pkg:
           os.system('adb install -r %s'%pkg)
        else:
           print('apk does not exists')

    def __execUninstallApp(self):
        pkg = input('input uninstall app package name : ')
        if pkg:
            os.system('adb uninstall %s'%pkg)
        else:
            print('package name is wrong!!')

    def __execForceStopApp(self):
        pkg = input('input stop package name : ')
        if pkg:
            os.system('adb shell am force-stop %s'%pkg)
        else:
            print('package name is wrong!!')

    def __execDumpSysActivity(self):
        path = os.path.abspath('.')+"\\activity.txt"
        print(path)
        comStr = 'adb shell dumpsys activity activities > ' + path
        os.system(comStr)
        print('dump activity in %s'%(path))

    def __execDumpSysWindow(self):
        path = os.path.abspath('.')+"\\windows.txt"
        print(path)
        comStr = 'adb shell dumpsys window windows > ' + path
        os.system(comStr)
        print('dump windows in %s'%(path))

    def __execDecodeApk(self):
        jar_dir = os.path.abspath('.')
        source_apk = jar_dir + '\\source_apk\\'
        decoded_apk = jar_dir + "\\decoded_apk\\"
        jar_path = jar_dir + "\\apktool\\apktool_2.1.1.jar"
        if not os.path.exists(jar_path):
            print('apktool.jar is not exists')
            return None
        if not os.path.exists(source_apk):
            os.mkdir(source_apk)
        if not os.path.exists(decoded_apk):
            os.mkdir(decoded_apk)
        files = os.listdir(source_apk)
        if len(files) == 0:
            print('no apk to decode !!')
            return None
        for f in os.listdir(source_apk):
            if not os.path.isfile(source_apk + "\\" + f):
                continue
            f_name = f.split('.')
            if not 'apk' == f_name[1]:
                continue
            apk_path = source_apk + "\\" + f
            decoded_path = decoded_apk + "\\" + f_name[0] + "\\"
            if os.path.exists(decoded_path):
                shutil.rmtree(decoded_path)

            if os.path.exists(jar_path):
                os.system('java -jar ' + jar_path + ' apktool d '+ apk_path + ' -o ' + decoded_path)
            else:
                print('apktool.jar is not exists')

if __name__ == '__main__':
    tips = ['Please input number listed below:']
    tips.append('adb shell')
    tips.append('adb devices')
    tips.append('show installed apps')
    tips.append('adb install app')
    tips.append('adb uninstall app')
    tips.append('clear app data')
    tips.append('force stop app')
    tips.append('dump activity')
    tips.append('dump windows')
    tips.append('apk decode')

    index = 0
    for tip in tips:
        if index >= 1:
            print(index,'.',tip)
        else:
            print(tip)
        index = index+1

    cmd = Command()
    error_msg = 'please input number 1-%d'%(len(tips)-1)
    input_number = input('input command number: ')
    if input_number:
            try :
                input_number = int(input_number)
                cmd.runCommand(input_number, error_msg)
            except ValueError as i:
                print(error_msg)
    else:
        print(error_msg)
    os.system('pause')