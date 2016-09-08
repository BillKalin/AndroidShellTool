#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__='BillKalin'
__datetime__='2016.8.17'

import os,shutil,zipfile

class Command(object):

    def __init__(self, cmd_type):
        if not isinstance(cmd_type, int) or 0 >= cmd_type:
            raise ValueError('cmd_type is error')
        self.__cmd_type = cmd_type
        if cmd_type == 1:
            name = 'adb shell'
        elif cmd_type == 2:
            name = 'adb reboot'
        elif cmd_type == 3:
            name = 'adb devices'
        elif cmd_type == 4:
            name = 'show installed apps'
        elif cmd_type == 5:
            name = 'adb install app'
        elif cmd_type == 6:
            name = 'adb uninstall app'
        elif cmd_type == 7:
            name = 'clear app data'
        elif cmd_type == 8:
            name = 'force stop app'
        elif cmd_type == 9:
            name = 'dump activity'
        elif cmd_type == 10:
            name = 'dump windows'
        elif cmd_type == 11:
            name = 'decode apk'
        elif cmd_type == 12:
            name = 'decode dex'
        else:
            raise ValueError('cmd type error !!!')
        self.__name = name

    def getCmdName(self):
        return self.__name;

    def runCommand(self, error_msg='run command error!!!'):
        if self.__cmd_type == 1:
            self.__execAdbShell()
        elif self.__cmd_type == 2:
            self.__execAdbReboot()
        elif self.__cmd_type == 3:
            self.__execAdbDevices()
        elif self.__cmd_type == 4:
            self.__execAdbShowAppPkgs()
        elif self.__cmd_type == 5:
            self.__execInstallApp()
        elif self.__cmd_type == 6:
            self.__execUninstallApp()
        elif self.__cmd_type == 7:
            self.__execClearAppData()
        elif self.__cmd_type == 8:
            self.__execForceStopApp()
        elif self.__cmd_type == 9:
            self.__execDumpSysActivity()
        elif self.__cmd_type == 10:
            self.__execDumpSysWindow()
        elif self.__cmd_type == 11:
            self.__execDecodeApk()
        elif self.__cmd_type == 12:
            self.__execDecodeDex()
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

    def __execAdbReboot(self):
        os.system('adb reboot')

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
            if str(pkg).endswith('.apk') and os.path.exists(pkg):
                os.system('adb install -r %s'%pkg)
            else:
                print('apk does not exists')
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

    def __execDecodeDex(self):
        print("start decode .dex file ...")
        jar_dir = os.path.abspath('.')
        source_apk = jar_dir + '\\source_apk\\'
        output_dex_dir = jar_dir + '\\decoded_dex\\'
        d2jPath = jar_dir + '\\dextool\\d2j-dex2jar'
        if not os.path.exists(source_apk):
            os.mkdir(source_apk)
        if not os.path.exists(output_dex_dir):
            os.mkdir(output_dex_dir)
        files = os.listdir(source_apk)
        if len(files) == 0:
            print('no apk to decode !!')
            return None
        tempDex = output_dex_dir + '\\temp\\'
        print('create temp dir to put classes.dex file in')
        if not os.path.exists(tempDex):
            os.mkdir(tempDex)

        for f in os.listdir(source_apk):
            if not os.path.isfile(source_apk + "\\" + f):
                continue
            f_name = f.split('.')
            if not f.endswith('.apk'):
                continue
            tempFileName =  f_name[0]+'.zip'
            #copy apk and rename it to zip file
            shutil.copy(os.path.join(source_apk,f), os.path.join(tempDex, tempFileName))

            tempzip = zipfile.ZipFile(os.path.join(tempDex, tempFileName), 'r')
            for zf in tempzip.namelist():
                if zf.endswith('.dex'):
                    dexFilePath = output_dex_dir + f_name[0]
                    if not os.path.exists(dexFilePath):
                        os.mkdir(dexFilePath)
                    else:
                        shutil.rmtree(dexFilePath)
                        os.mkdir(dexFilePath)
                    f = open(os.path.join(dexFilePath, zf), 'wb')
                    f.write(tempzip.read(zf))
                    f.close()
                    ''' start decode dex file'''
                    os.system(d2jPath + ' -o ' + os.path.join(dexFilePath, zf.replace('.dex','.jar')) + ' ' + os.path.join(dexFilePath, zf) )
            tempzip.close()
        print('delete temp files')
        if os.path.exists(tempDex):
            shutil.rmtree(tempDex)

if __name__ == '__main__':
    tips = list()
    tips.append('Please input number listed below:')
    cmdList = {}
    for i in range(1, 13):
        cm = Command(i)
        cmdList[i] = cm
        tips.append(cm.getCmdName())

    index = 0
    for tip in tips:
        if index >= 1:
            print(index,'.',tip)
        else:
            print(tip)
        index = index+1

    error_msg = 'please input number 1-%d'%(len(cmdList))
    input_number = input('input command number: ')
    if input_number:
            try :
                input_number = int(input_number)
                if input_number <= 0 or input_number > len(cmdList):
                    print(error_msg)
                else:
                    c = cmdList[input_number]
                    c.runCommand()
            except ValueError as i:
                print(error_msg)
    else:
        print(error_msg)
    os.system('pause')