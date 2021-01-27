import unittest
import sys
import os
import shutil 
import m1com
import ctypes
import time

def assertNotBytes(test, methodReturn):

    test.assertNotEqual(type(methodReturn), bytes)

    if hasattr(methodReturn, '_fields_'):
        for attribute in methodReturn._fields_:
            assertType = type(getattr(methodReturn, attribute[0]))
            test.assertNotEqual(assertType, bytes)
    elif type(methodReturn) != int:
        if type(methodReturn) == list:
            for listItem in methodReturn:
                assertNotBytes(test, listItem)
        elif type(methodReturn) == dict:
            for key in methodReturn.keys():
                assertNotBytes(test, methodReturn[key])
        elif type(methodReturn) == str:
            pass
        elif type(methodReturn) == bool:
            pass
        else:
            for attribute in list(dir(methodReturn)):
                if not attribute.startswith('__'):
                    assertType = type(getattr(methodReturn, attribute))
                    test.assertNotEqual(assertType, bytes)

def sviAppInstall(mh):

    # Determine current directory
    curDir = os.path.dirname(os.path.abspath(__file__))

    # Copy test application to bachmann
    mh.copyToTarget(curDir + '/unittestFiles/sviwrite.m', '/cfc0/app/sviwrite.m')

    # Make a copy of the mconfig.ini
    mh.copyFromTarget('/cfc0/mconfig.ini', curDir + '/unittestFiles/mconfigBackup.ini')
    shutil.copyfile(curDir + '/unittestFiles/mconfigBackup.ini', curDir + '/unittestFiles/mconfigSVIWrite.ini')

    # Add application to mconfig.ini
    f = open(curDir + '/unittestFiles/mconfigSVIWrite.ini', 'a')
    f.write("[SVIWRITE]\n")
    f.write("(BaseParms)\n")
    f.write("  Partition = 2\n")
    f.write("  DebugMode = 0x0\n")
    f.write("  Priority = 130\n")
    f.write("  ModuleIndex = 0\n")
    f.write("  ModulePath = /cfc0/app/\n")
    f.write("  ModuleName = sviwrite.m\n")
    f.write("(ControlTask)\n")
    f.write("  CycleTime = 1000000\n")
    f.write("  Priority = 90\n")
    f.close()

    # Remove old mconfig.ini from target, copy the new mconfig.ini and reboot
    mh.remove('/cfc0/mconfig.ini')
    mh.copyToTarget(curDir + '/unittestFiles/mconfigSVIWrite.ini', '/cfc0/mconfig.ini')
    mh.reboot()
    mh.disconnect()
    time.sleep(20)

    # Reconnect to the target
    mh.connect(timeout=3000)

def sviAppRemove(mh):

    # Determine current directory
    curDir = os.path.dirname(os.path.abspath(__file__))

    # Remove application and mconfig.ini from target, copy back the original mconfig.ini and reboot
    mh.remove('/cfc0/app/sviwrite.m')
    mh.remove('/cfc0/mconfig.ini')
    mh.copyToTarget(curDir + '/unittestFiles/mconfigBackup.ini', '/cfc0/mconfig.ini')
    mh.reboot()
    mh.disconnect()
    os.remove(curDir + '/unittestFiles/mconfigBackup.ini')
    os.remove(curDir + '/unittestFiles/mconfigSVIWrite.ini')
    time.sleep(20)

class Test_PyComException(unittest.TestCase):
    def test_with_traceback(self):
        exception = m1com.PyComException('PyComException Test')
        
        self.assertEqual(exception.value, 'PyComException Test')
        assertNotBytes(self, exception)

        tb = sys.exc_info()[2]
        exception = m1com.PyComException('PyComException Test').with_traceback(tb)

        self.assertEqual(exception.value, 'PyComException Test')
        assertNotBytes(self, exception)

        try:
            raise m1com.PyComException('PyComException Test')
        except:
            tb = sys.exc_info()[2]
            exception = m1com.PyComException('PyComException Test').with_traceback(tb)

        self.assertEqual(exception.value, 'PyComException Test')
        assertNotBytes(self, exception)

        testedMethods.append('PyComException.with_traceback')

class Test_PyComTypeException(unittest.TestCase):
    def test_with_traceback(self):
        exception = m1com.PyComTypeException('PyComTypeException Test')
        
        self.assertEqual(exception.value, 'PyComTypeException Test')
        assertNotBytes(self, exception)

        tb = sys.exc_info()[2]
        exception = m1com.PyComTypeException('PyComTypeException Test').with_traceback(tb)

        self.assertEqual(exception.value, 'PyComTypeException Test')
        assertNotBytes(self, exception)

        try:
            raise m1com.PyComTypeException('PyComTypeException Test')
        except:
            tb = sys.exc_info()[2]
            exception = m1com.PyComTypeException('PyComTypeException Test').with_traceback(tb)

        self.assertEqual(exception.value, 'PyComTypeException Test')
        assertNotBytes(self, exception)

        testedMethods.append('PyComTypeException.with_traceback')

class Test_PyCom(unittest.TestCase):
    def test_getDllVersion(self):
        dll = m1com.PyCom()
        dllVersion = dll.getDllVersion()

        version = ctypes.c_char_p(40*''.encode())
        dll.M1C_GetVersion(version, 40)

        self.assertEqual(dllVersion, version.value.decode())
        assertNotBytes(self, dllVersion)

        testedMethods.append('PyCom.getDllVersion')

    def test_getDllBits(self):
        dll = m1com.PyCom()
        dllBits = dll.getDllBits()

        if sys.maxsize > 2**32: # 64bit
            self.assertEqual(dllBits, '64bit')
        else:
            self.assertEqual(dllBits, '32bit')
        assertNotBytes(self, dllBits)

        testedMethods.append('PyCom.getDllBits')

class Test_M1Controller(unittest.TestCase):
    def test_getCtrlHandle(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.getCtrlHandle(), mh._ctrlHandle)
        assertNotBytes(self, mh.getCtrlHandle())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getCtrlHandle')

    def test_connect(self):
        mh = m1com.M1Controller(ip=ipAddress)

        mh.connect(timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        mh.connect(protocol='TCP', timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol TCP failed!")
        self.assertEqual(mh.disconnect(), 0)

        mh.connect(protocol='QSOAP', timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol QSOAP failed!")
        self.assertEqual(mh.disconnect(), 0)

        mh.connect(protocol='UDP', timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol UDP failed!")
        self.assertEqual(mh.disconnect(), 0)

        #mh.connect(protocol='SSL', timeout=3000)
        #self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol SSL failed!")
        #self.assertEqual(mh.disconnect(), 0)

        crtFile = 'C:/Users/COEK/Documents/XCA Database/coek.p12'
        mh.connect(protocol='SSL', clientCert=crtFile, clientCertPassword='bachmann', timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None, msg="Connect with protocol SSL and client certificate failed!")
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.connect')

    def test_getSessionLiveTime(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertGreaterEqual(mh.getSessionLiveTime(), 0)
        assertNotBytes(self, mh.getSessionLiveTime())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getSessionLiveTime')


    def test_getLoginInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        loginInfo = mh.getLoginInfo()

        self.assertEqual(str(type(loginInfo)), "<class 'm1com.RES_LOGIN2_R'>")
        assertNotBytes(self, loginInfo)
        self.assertGreaterEqual(loginInfo.SecurityLevel, 0)
        self.assertLessEqual(loginInfo.SecurityLevel, 4)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getLoginInfo')

    def test_renewConnection(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.renewConnection(), None)
        assertNotBytes(self, mh.renewConnection())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.renewConnection')

    def test_getNumberofSwModules(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertGreaterEqual(mh.getNumberofSwModules(), 8)
        assertNotBytes(self, mh.getNumberofSwModules())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getNumberofSwModules')

    def test_getSwModuleByName(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(str(type(mh.getSwModuleByName('RES'))), "<class 'm1com._M1SwModule'>")
        self.assertEqual(mh.getSwModuleByName('RES').name, 'RES')
        assertNotBytes(self, mh.getSwModuleByName('RES'))
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getSwModuleByName')
    
    def test_getListofSwModules(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(str(type(mh.getListofSwModules())), "<class 'dict'>")
        self.assertEqual(len(mh.getListofSwModules()), mh.getNumberofSwModules())
        assertNotBytes(self, mh.getListofSwModules())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getListofSwModules')
    
    def test_getListofHwModules(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertGreater(lastHwModuleNb, 0)
        assertNotBytes(self, mh.getListofHwModules())
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getListofHwModules')
    
    def test_getDrvId(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertGreater(mh.getDrvId(lastHwModuleNb), 0)
        assertNotBytes(self, mh.getDrvId(lastHwModuleNb))
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getDrvId')

    def test_getCardInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertEqual(str(type(mh.getCardInfo(lastHwModuleNb))), "<class 'm1com.MIO_GETCDINF_R'>")
        self.assertEqual(mh.getCardInfo(lastHwModuleNb).Inf.CardNb, lastHwModuleNb)
        assertNotBytes(self, mh.getCardInfo(lastHwModuleNb))
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getCardInfo')

    def test_getCardInfoExt(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertEqual(mh.getCardInfoExt(lastHwModuleNb)['CardNb'], lastHwModuleNb)
        assertNotBytes(self, mh.getCardInfoExt(lastHwModuleNb))
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.getCardInfoExt')

    def test_copyFromTarget(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.copyFromTarget('/cfc0/mconfig.ini', 'localCopyMconfig.ini'), None)
        self.assertEqual(mh.disconnect(), 0)
        self.assertTrue(os.path.isfile('localCopyMconfig.ini'))
        os.remove('localCopyMconfig.ini')

        testedMethods.append('M1Controller.copyFromTarget')

    def test_copyToTarget(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        f = open('test_copyToTarget.txt', 'w')
        f.write("Test for mh.copyToTarget('test_copyToTarget.txt', '/cfc0/test_copyToTarget.txt')")
        f.close()

        self.assertEqual(mh.copyToTarget('test_copyToTarget.txt', '/cfc0/test_copyToTarget.txt'), None)
        self.assertEqual(mh.disconnect(), 0)

        os.remove('test_copyToTarget.txt')

        testedMethods.append('M1Controller.copyToTarget')

    def test_copyRemote(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.copyRemote('/cfc0/mconfig.ini', '/cfc0/test_copyRemoteOfMconfig.txt'), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.copyRemote')

    def test_remove(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.remove('/cfc0/test_copyRemoteOfMconfig.txt'), None)
        self.assertEqual(mh.remove('/cfc0/test_copyToTarget.txt'), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1Controller.remove')

    def test_resetAll(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            self.assertEqual(mh.resetAll(), None)
            self.assertEqual(mh.reboot(), None)
            self.assertEqual(mh.disconnect(), 0)
            time.sleep(20)

            testedMethods.append('M1Controller.resetAll')

    def test_reboot(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            self.assertEqual(mh.reboot(), None)
            self.assertEqual(mh.disconnect(), 0)
            time.sleep(20)

            testedMethods.append('M1Controller.reboot')

    def test_disconnect(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        self.assertEqual(mh.disconnect(), 0)
        self.assertEqual(mh._ctrlHandle, None)

        testedMethods.append('M1Controller.disconnect')

    def test_sendCall(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            self.assertEqual(str(mh.sendCall('MOD', 134, ctypes.c_int32(0), ctypes.c_int32(0), timeout=3000, version=2)), 'c_long(0)')
            self.assertEqual(mh.disconnect(), 0)
            time.sleep(20)

            testedMethods.append('M1Controller.sendCall')


class Test_M1SVIObserver(unittest.TestCase):
    def test_detach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertNotEqual(sviObserver._obsHandle, None)
        self.assertEqual(sviObserver.detach(), None)

        self.assertEqual(sviObserver._obsHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.detach')

    def test_getObsHandle(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)

        self.assertEqual(sviObserver.getObsHandle(), sviObserver._obsHandle)
        self.assertNotEqual(sviObserver._obsHandle, None)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.getObsHandle')

    def test_attach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertEqual(sviObserver.getObsHandle(), sviObserver._obsHandle)
        self.assertNotEqual(sviObserver._obsHandle, None)
        self.assertEqual(len(sviObserver._sviHandles), 4)
        for i in range(4):
            self.assertEqual(type(sviObserver._sviHandles[i]), int)
        self.assertEqual(len(sviObserver._sviInfos), 4)
        for i in range(4):
            self.assertEqual(str(type(sviObserver._sviInfos[i])), "<class 'm1com.VARIABLE_INFO'>")
        self.assertEqual(len(sviObserver._sviValues), 4)
        self.assertEqual(str(type(sviObserver._sviValues[0])), "<class 'ctypes.c_ulong'>")
        self.assertEqual(str(type(sviObserver._sviValues[1])), "<class 'ctypes.c_ulong'>")
        self.assertEqual(str(type(sviObserver._sviValues[2])), "<class 'ctypes.c_ulong'>")
        self.assertEqual(str(type(sviObserver._sviValues[3])), "<class 'm1com.c_char_Array_20'>")
        self.assertNotEqual(sviObserver._indicesChanged, None)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.attach')

    def test_update(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertEqual(sviObserver.update(), 4)
        time.sleep(1)
        self.assertEqual(sviObserver.update(), 2)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.update')

    def test_getVariables(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertEqual(len(sviObserver.getVariables(updatedOnly=True)), 4)
        assertNotBytes(self, sviObserver.getVariables(updatedOnly=True))
        time.sleep(1)
        for i in range(5):
            self.assertEqual(len(sviObserver.getVariables(updatedOnly=True)), 2)
            assertNotBytes(self, sviObserver.getVariables(updatedOnly=True))
            time.sleep(1)
        self.assertEqual(sviObserver.detach(), None)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        self.assertEqual(len(sviObserver.getVariables(updatedOnly=False)), 4)
        assertNotBytes(self, sviObserver.getVariables(updatedOnly=False))
        time.sleep(1)
        for i in range(5):
            self.assertEqual(len(sviObserver.getVariables(updatedOnly=False)), 4)
            assertNotBytes(self, sviObserver.getVariables(updatedOnly=False))
            time.sleep(1)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:

            # Connect to the target
            mh.connect(timeout=3000)

            # Install the svi test application
            sviAppInstall(mh)

            # Perform the read tests
            readVariables = { 'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int, 'SVIWRITE/sInt8Var': int,
                              'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int, 'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int,
                              'SVIWRITE/uInt64Var': int, 'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                              'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                              'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int], 'SVIWRITE/sInt8Array': [int],
                              'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int], 'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int],
                              'SVIWRITE/uInt64Array': [int], 'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                              'SVIWRITE/char8Array': str, 'SVIWRITE/char16Array': str}

            readValues = [False, False, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, "O", "O", "O",
                          [False, False, False], [False, False, False], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                          [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                          "OOO", "OOO"]

            Error = False
            ErrorMsg = ''
            try:
                # Setup the observer
                sviObserver = m1com.M1SVIObserver(list(readVariables.keys()), mh)
                obtainedVariables = sviObserver.getVariables(updatedOnly=False)

                j = 0
                for key in readVariables:
                    sviValue = obtainedVariables[key]
                    if type(readValues[j]) == list:
                        for i in range(len(readValues[j])):
                            self.assertEqual(type(sviValue[i]), readVariables[key][0], msg='for ' + key + '=' + str(readValues[j][i]))
                            if type(sviValue[i]) == float:
                                self.assertAlmostEqual(sviValue[i], readValues[j][i], msg='for ' + key + '=' + str(readValues[j][i]))
                            else:
                                self.assertEqual(sviValue[i], readValues[j][i], msg='for ' + key + '=' + str(readValues[j][i]))
                    else:
                        self.assertEqual(type(sviValue), readVariables[key], msg='for ' + key + '=' + str(readValues[j]))
                        if type(sviValue) == float:
                            self.assertAlmostEqual(sviValue, readValues[j], msg='for ' + key + '=' + str(readValues[j]))
                        else:
                            self.assertEqual(sviValue, readValues[j], msg='for ' + key + '=' + str(readValues[j]))
                    j = j + 1

                # Setup the observer
                sviObserver = m1com.M1SVIObserver(list(readVariables.keys()), mh)
                obtainedVariables = sviObserver.getVariables(updatedOnly=True)

                j = 0
                for key in readVariables:
                    sviValue = obtainedVariables[key]
                    if type(readValues[j]) == list:
                        for i in range(len(readValues[j])):
                            self.assertEqual(type(sviValue[i]), readVariables[key][0], msg='for ' + key + '=' + str(readValues[j][i]))
                            if type(sviValue[i]) == float:
                                self.assertAlmostEqual(sviValue[i], readValues[j][i], msg='for ' + key + '=' + str(readValues[j][i]))
                            else:
                                self.assertEqual(sviValue[i], readValues[j][i], msg='for ' + key + '=' + str(readValues[j][i]))
                    else:
                        self.assertEqual(type(sviValue), readVariables[key], msg='for ' + key + '=' + str(readValues[j]))
                        if type(sviValue) == float:
                            self.assertAlmostEqual(sviValue, readValues[j], msg='for ' + key + '=' + str(readValues[j]))
                        else:
                            self.assertEqual(sviValue, readValues[j], msg='for ' + key + '=' + str(readValues[j]))
                    j = j + 1

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('M1SVIObserver.getVariables')

    def test_reset(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        sviObserver = m1com.M1SVIObserver(['RES/TypeVers', 'RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
        for i in range(5):
            self.assertEqual(len(sviObserver.getVariables(updatedOnly=True)), 4)
            assertNotBytes(self, sviObserver.getVariables(updatedOnly=True))
            self.assertEqual(sviObserver.reset(), None)
            time.sleep(1)
        self.assertEqual(sviObserver.detach(), None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('M1SVIObserver.reset')

class Test_M1SVIReader(unittest.TestCase):
    def test_detach(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            # Install the svi test application
            sviAppInstall(mh)

            Error = False
            ErrorMsg = ''
            try:
                readVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int, 'SVIWRITE/sInt8Var': int,
                                    'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int, 'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int,
                                    'SVIWRITE/uInt64Var': int, 'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                                    'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                                    'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int], 'SVIWRITE/sInt8Array': [int],
                                    'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int], 'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int],
                                    'SVIWRITE/uInt64Array': [int], 'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                                    'SVIWRITE/char8Array': str, 'SVIWRITE/char16Array': str}

                # Setup the observer
                sviReader = m1com.M1SVIReader(list(readVariables.keys()), mh)

                self.assertNotEqual(sviReader._sviHandles, None)
                self.assertEqual(sviReader.detach(), None)

                self.assertEqual(sviReader._sviHandles, None)

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('M1SVIReader.detach')

    def test_getSVIHandles(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            # Install the svi test application
            sviAppInstall(mh)

            Error = False
            ErrorMsg = ''
            try:
                readVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int, 'SVIWRITE/sInt8Var': int,
                                    'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int, 'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int,
                                    'SVIWRITE/uInt64Var': int, 'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                                    'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                                    'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int], 'SVIWRITE/sInt8Array': [int],
                                    'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int], 'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int],
                                    'SVIWRITE/uInt64Array': [int], 'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                                    'SVIWRITE/char8Array': str, 'SVIWRITE/char16Array': str}

                # Setup the observer
                sviReader = m1com.M1SVIReader(list(readVariables.keys()), mh)

                self.assertNotEqual(sviReader.getSVIHandles(), None)
                self.assertEqual(type(sviReader.getSVIHandles()), list)
                self.assertEqual(sviReader.getSVIHandles(), sviReader._sviHandles)
                for sviHandle in sviReader.getSVIHandles():
                    self.assertGreater(sviHandle, 0)
                self.assertEqual(sviReader.detach(), None)
                self.assertEqual(sviReader._sviHandles, None)

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('M1SVIReader.getSVIHandles')

    def test_attach(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            # Install the svi test application
            sviAppInstall(mh)

            Error = False
            ErrorMsg = ''
            try:
                readVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int, 'SVIWRITE/sInt8Var': int,
                                    'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int, 'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int,
                                    'SVIWRITE/uInt64Var': int, 'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                                    'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                                    'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int], 'SVIWRITE/sInt8Array': [int],
                                    'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int], 'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int],
                                    'SVIWRITE/uInt64Array': [int], 'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                                    'SVIWRITE/char8Array': str, 'SVIWRITE/char16Array': str}

                # Setup the observer
                sviReader = m1com.M1SVIReader(list(readVariables.keys()), mh)

                self.assertEqual(sviReader.getSVIHandles(), sviReader._sviHandles)
                self.assertNotEqual(sviReader.getSVIHandles(), None)
                self.assertEqual(len(sviReader._sviHandles), len(list(readVariables.keys())))
                for i in range(len(list(readVariables.keys()))):
                    self.assertEqual(type(sviReader._sviHandles[i]), int)
                self.assertEqual(len(sviReader._sviInfos), len(list(readVariables.keys())))
                for i in range(len(list(readVariables.keys()))):
                    self.assertEqual(str(type(sviReader._sviInfos[i])), "<class 'm1com.VARIABLE_INFO'>")
                self.assertEqual(len(sviReader._sviValues), len(list(readVariables.keys())))
                self.assertEqual(sviReader.detach(), None)

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('M1SVIReader.attach')

    def test_getVariables(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            # Connect to the target
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            # Install the svi test application
            sviAppInstall(mh)

            # Perform the read tests
            readVariables = {   'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                                'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                                'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                                'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                                'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                                'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                                'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                                'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                                'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                                'SVIWRITE/char8Array': str, 'SVIWRITE/char16Array': str}

            readValues = [  [True,  True,  1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1.1, "L", "L", "Hello World",
                             [True, True, True], [True, True, True], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3],
                             [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1.1, 2.2, 3.3], [1.1, 2.2, 3.3],
                             "KLM", "KLM"],

                            [False, False, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, "O", "O", "O",
                             [False, False, False], [False, False, False], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                             [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                             "OOO", "OOO"] ]

            # Setup the SVI writer and reader
            sviWriter = m1com.M1SVIWriter(list(readVariables.keys()), mh)
            sviReader = m1com.M1SVIReader(list(readVariables.keys()), mh)

            Error = False
            ErrorMsg = ''
            try:
                for i in range(len(readValues)):

                    sviWriter.setVariables(readValues[i])
                    obtainedVariables = sviReader.getVariables()

                    j = 0
                    for key in readVariables:
                        sviValue = obtainedVariables[j]
                        realValue = readValues[i][j]
                        if type(realValue) == list:
                            for k in range(len(realValue)):
                                self.assertEqual(type(sviValue[k]), readVariables[key][0], msg='for ' + key + '=' + str(realValue[k]))
                                if type(sviValue[k]) == float:
                                    self.assertAlmostEqual(sviValue[k], realValue[k], msg='for ' + key + '=' + str(realValue[k]))
                                else:
                                    self.assertEqual(sviValue[k], realValue[k], msg='for ' + key + '=' + str(realValue[k]))
                        else:
                            self.assertEqual(type(sviValue), readVariables[key], msg='for ' + key + '=' + str(realValue))
                            if type(sviValue) == float:
                                self.assertAlmostEqual(sviValue, realValue, msg='for ' + key + '=' + str(realValue))
                            else:
                                self.assertEqual(sviValue, realValue, msg='for ' + key + '=' + str(realValue))

                        j = j + 1

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('M1SVIReader.getVariables')

class Test_M1SVIWriter(unittest.TestCase):
    def test_detach(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            # Install the svi test application
            sviAppInstall(mh)

            Error = False
            ErrorMsg = ''
            try:
                writeVariables = {  'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int, 'SVIWRITE/sInt8Var': int,
                                    'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int, 'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int,
                                    'SVIWRITE/uInt64Var': int, 'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                                    'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                                    'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                                    'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                                    'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                                    'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                                    'SVIWRITE/char8Array': str, 'SVIWRITE/char16Array': str}

                # Setup the observer
                sviWriter = m1com.M1SVIWriter(list(writeVariables.keys()), mh)

                self.assertNotEqual(sviWriter._sviHandles, None)
                self.assertEqual(sviWriter.detach(), None)

                self.assertEqual(sviWriter._sviHandles, None)

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('M1SVIWriter.detach')

    def test_getSVIHandles(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            # Install the svi test application
            sviAppInstall(mh)

            Error = False
            ErrorMsg = ''
            try:
                writeVariables = {  'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int, 'SVIWRITE/sInt8Var': int,
                                    'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int, 'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int,
                                    'SVIWRITE/uInt64Var': int, 'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                                    'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                                    'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                                    'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                                    'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                                    'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                                    'SVIWRITE/char8Array': str, 'SVIWRITE/char16Array': str}

                # Setup the observer
                sviWriter = m1com.M1SVIWriter(list(writeVariables.keys()), mh)

                self.assertNotEqual(sviWriter.getSVIHandles(), None)
                self.assertEqual(type(sviWriter.getSVIHandles()), list)
                self.assertEqual(sviWriter.getSVIHandles(), sviWriter._sviHandles)
                for sviHandle in sviWriter.getSVIHandles():
                    self.assertGreater(sviHandle, 0)
                self.assertEqual(sviWriter.detach(), None)
                self.assertEqual(sviWriter._sviHandles, None)

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('M1SVIWriter.getSVIHandles')

    def test_attach(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            # Install the svi test application
            sviAppInstall(mh)

            Error = False
            ErrorMsg = ''
            try:
                writeVariables = {  'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int, 'SVIWRITE/sInt8Var': int,
                                    'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int, 'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int,
                                    'SVIWRITE/uInt64Var': int, 'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                                    'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                                    'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                                    'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                                    'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                                    'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                                    'SVIWRITE/char8Array': str, 'SVIWRITE/char16Array': str}

                # Setup the observer
                sviWriter = m1com.M1SVIWriter(list(writeVariables.keys()), mh)

                self.assertEqual(sviWriter.getSVIHandles(), sviWriter._sviHandles)
                self.assertNotEqual(sviWriter.getSVIHandles(), None)
                self.assertEqual(len(sviWriter._sviHandles), len(list(writeVariables.keys())))
                for i in range(len(list(writeVariables.keys()))):
                    self.assertEqual(type(sviWriter._sviHandles[i]), int)
                self.assertEqual(len(sviWriter._sviInfos), len(list(writeVariables.keys())))
                for i in range(len(list(writeVariables.keys()))):
                    self.assertEqual(str(type(sviWriter._sviInfos[i])), "<class 'm1com.VARIABLE_INFO'>")
                self.assertEqual(len(sviWriter._sviValues), len(list(writeVariables.keys())))
                self.assertEqual(sviWriter.detach(), None)

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('M1SVIWriter.attach')

    def test_setVariables(self):
        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:
            # Connect to the target
            mh = m1com.M1Controller(ip=ipAddress)
            mh.connect(timeout=3000)

            # Install the svi test application
            sviAppInstall(mh)

            # Perform the read tests
            writeVariables = {  'SVIWRITE/boolVar': bool, 'SVIWRITE/bool8Var': bool, 'SVIWRITE/uInt8Var': int,
                                'SVIWRITE/sInt8Var': int, 'SVIWRITE/uInt16Var': int, 'SVIWRITE/sInt16Var': int,
                                'SVIWRITE/uInt32Var': int, 'SVIWRITE/sInt32Var': int, 'SVIWRITE/uInt64Var': int,
                                'SVIWRITE/sInt64Var': int, 'SVIWRITE/real32Var': float, 'SVIWRITE/real64Var': float,
                                'SVIWRITE/char8Var': str, 'SVIWRITE/char16Var': str, 'SVIWRITE/stringVar': str,
                                'SVIWRITE/boolArray': [bool], 'SVIWRITE/bool8Array': [bool], 'SVIWRITE/uInt8Array': [int],
                                'SVIWRITE/sInt8Array': [int], 'SVIWRITE/uInt16Array': [int], 'SVIWRITE/sInt16Array': [int],
                                'SVIWRITE/uInt32Array': [int], 'SVIWRITE/sInt32Array': [int], 'SVIWRITE/uInt64Array': [int],
                                'SVIWRITE/sInt64Array': [int], 'SVIWRITE/real32Array': [float], 'SVIWRITE/real64Array': [float],
                                'SVIWRITE/char8Array': str, 'SVIWRITE/char16Array': str}

            writeValues = [  [True,  True,  1, 1, 1, 1, 1, 1, 1, 1, 1.1, 1.1, "L", "L", "Hello World",
                             [True, True, True], [True, True, True], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3],
                             [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1.1, 2.2, 3.3], [1.1, 2.2, 3.3],
                             "KLM", "KLM"],

                            [False, False, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, "O", "O", "O",
                             [False, False, False], [False, False, False], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                             [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                             "OOO", "OOO"] ]

            # Setup the writer and observer
            sviWriter = m1com.M1SVIWriter(list(writeVariables.keys()), mh)
            sviObserver = m1com.M1SVIObserver(list(writeVariables.keys()), mh)

            Error = False
            ErrorMsg = ''
            try:
                for i in range(len(writeValues)):

                    sviWriter.setVariables(writeValues[i])
                    obtainedVariables = sviObserver.getVariables()

                    j = 0
                    for key in writeVariables:
                        sviValue = obtainedVariables[key]
                        realValue = writeValues[i][j]
                        if type(realValue) == list:
                            for k in range(len(realValue)):
                                self.assertEqual(type(sviValue[k]), writeVariables[key][0], msg='for ' + key + '=' + str(realValue[k]))
                                if type(sviValue[k]) == float:
                                    self.assertAlmostEqual(sviValue[k], realValue[k], msg='for ' + key + '=' + str(realValue[k]))
                                else:
                                    self.assertEqual(sviValue[k], realValue[k], msg='for ' + key + '=' + str(realValue[k]))
                        else:
                            self.assertEqual(type(sviValue), writeVariables[key], msg='for ' + key + '=' + str(realValue))
                            if type(sviValue) == float:
                                self.assertAlmostEqual(sviValue, realValue, msg='for ' + key + '=' + str(realValue))
                            else:
                                self.assertEqual(sviValue, realValue, msg='for ' + key + '=' + str(realValue))

                        j = j + 1

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('M1SVIWriter.setVariables')

class Test_M1TargetFinder(unittest.TestCase):
    def test_TargetBroadcastSmiPing(self):
        mt = m1com.M1TargetFinder()
        broadcastSmiPing = mt.TargetBroadcastSmiPing(timeout=3000)
        
        # Check if broadcastSmiPing returns something
        self.assertNotEqual(broadcastSmiPing, None)

        # Check if broadcastSmiPing also finds the ip we are using
        ipFound = ''
        for target in broadcastSmiPing:
            if broadcastSmiPing[target]['hostAddr'] == ipAddress:
                ipFound = broadcastSmiPing[target]['hostAddr']

        self.assertEqual(ipFound, ipAddress)
        assertNotBytes(self, broadcastSmiPing)

        testedMethods.append('M1TargetFinder.TargetBroadcastSmiPing')

    def test_TargetSmiPing(self):
        mt = m1com.M1TargetFinder()
        smiPing = mt.TargetSmiPing(ip=ipAddress, timeout=3000)
        
        # Check if smiPing returns something
        self.assertNotEqual(smiPing, None)
        assertNotBytes(self, smiPing)

        testedMethods.append('M1TargetFinder.TargetSmiPing')

class Test_M1SwModule(unittest.TestCase):
    def test_attach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        self.assertEqual(swModule.attach(), None)
        self.assertNotEqual(swModule._modHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.attach')

    def test_detach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        self.assertEqual(swModule.detach(), None)
        self.assertEqual(swModule._modHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.detach')

    def test_getModHandle(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        self.assertEqual(swModule.getModHandle(), swModule._modHandle)
        self.assertNotEqual(swModule._modHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.getModHandle')

    def test_getNumberofSviVariables(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        self.assertGreater(swModule.getNumberofSviVariables(), 200)
        self.assertEqual(type(swModule.getNumberofSviVariables()), int)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.getNumberofSviVariables')

    def test_getListofSviVariables(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)

        listOfSviVariables = swModule.getListofSviVariables()

        self.assertEqual(type(listOfSviVariables), dict)
        assertNotBytes(self, listOfSviVariables)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.getListofSviVariables')

class Test_SVIVariable(unittest.TestCase):
    def test_attach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)

        self.assertEqual(sviVariable.attach(), None)
        self.assertNotEqual(sviVariable._varHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.attach')

    def test_detach(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)

        self.assertEqual(sviVariable.detach(), None)
        self.assertEqual(sviVariable._varHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.detach')

    def test_getVarHandle(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)

        self.assertEqual(sviVariable.getVarHandle(), sviVariable._varHandle)
        self.assertNotEqual(sviVariable._varHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getVarHandle')

    def test_getVarInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        sviInfo = sviVariable.getVarInfo()

        self.assertEqual(sviInfo, sviVariable._varInfo)
        self.assertNotEqual(sviInfo, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getVarInfo')

    def test_updateVarInfo(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        updateSviInfo = sviVariable.updateVarInfo()

        self.assertEqual(updateSviInfo, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.updateVarInfo')

    def test_read(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        sviValue = sviVariable.read()

        self.assertEqual(type(sviValue), int)
        self.assertGreaterEqual(sviValue, 20)
        self.assertLessEqual(sviValue, 100)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.read')

    def test_write(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)

        try:
            sviVariable.write(60)
        except m1com.PyComException as error:
            error = str(error.value)
            self.assertEqual(error, 'pyCom Error: Svi Variable[RES/CPU/TempCelsius] is not write able!')

        if fastTest:
            print('Requires reboot, skipped for faster testing')
        else:

            # Install the svi test application
            sviAppInstall(mh)

            # Perform the write tests
            swModule = m1com._M1SwModule('SVIWRITE', mh)
            writeVariables = { 'boolVar': bool, 'bool8Var': bool, 'uInt8Var': int, 'sInt8Var': int,
                               'uInt16Var': int, 'sInt16Var': int, 'uInt32Var': int, 'sInt32Var': int,
                               'uInt64Var': int, 'sInt64Var': int, 'real32Var': float, 'real64Var': float,
                               'char8Var': str, 'char16Var': str, 'stringVar': str,
                               'boolArray': [bool], 'bool8Array': [bool], 'uInt8Array': [int], 'sInt8Array': [int],
                               'uInt16Array': [int], 'sInt16Array': [int], 'uInt32Array': [int], 'sInt32Array': [int],
                               'uInt64Array': [int], 'sInt64Array': [int], 'real32Array': [float], 'real64Array': [float],
                               'char8Array': str, 'char16Array': str
                               }

            Error = False
            ErrorMsg = ''
            try:
                for key in writeVariables:
                    sviVariable = m1com._SVIVariable('SVIWRITE/' + key, swModule)
                    sviVariable2 = m1com._SVIVariable('SVIWRITE/' + key, swModule)
                    if writeVariables[key] == bool:
                        value = [True, False]
                    elif writeVariables[key] == int:
                        value = [1, 0]
                    elif writeVariables[key] == float:
                        value = [1.1, 0.0]
                    elif writeVariables[key] == str:
                        value = ['L', 'O']
                    elif writeVariables[key] == [bool]:
                        value = [[True, True, True], [False, False, False]]
                    elif writeVariables[key] == [int]:
                        value = [[1, 2, 3], [0, 0, 0]]
                    elif writeVariables[key] == [float]:
                        value = [[1.1, 2.2, 3.3], [0.0, 0.0, 0.0]]
                    else:
                        value = None
                        print('Unsupported type: ' + str(writeVariables[key]) + ' for ' + str(key))
                    sviVariable.write(value[0])
                    sviValue = sviVariable.read()
                    sviValue2 = sviVariable2.read()
                    if type(sviValue) == list:
                        for i in range(len(sviValue)):
                            self.assertEqual(type(sviValue[i]), writeVariables[key][0], msg='for ' + key + '=' + str(value[0][i]))
                            self.assertEqual(type(sviValue2[i]), writeVariables[key][0], msg='for ' + key + '=' + str(value[0][i]))
                            if type(sviValue[i]) == float:
                                self.assertAlmostEqual(sviValue[i], value[0][i], msg='for ' + key + '=' + str(value[0][i]))
                                self.assertAlmostEqual(sviValue2[i], value[0][i], msg='for ' + key + '=' + str(value[0][i]))
                            else:
                                self.assertEqual(sviValue[i], value[0][i], msg='for ' + key + '=' + str(value[0][i]))
                                self.assertEqual(sviValue2[i], value[0][i], msg='for ' + key + '=' + str(value[0][i]))
                    else:
                        self.assertEqual(type(sviValue), writeVariables[key], msg='for ' + key + '=' + str(value[0]))
                        self.assertEqual(type(sviValue2), writeVariables[key], msg='for ' + key + '=' + str(value[0]))
                        if type(sviValue) == float:
                            self.assertAlmostEqual(sviValue, value[0], msg='for ' + key + '=' + str(value[0]))
                            self.assertAlmostEqual(sviValue2, value[0], msg='for ' + key + '=' + str(value[0]))
                        else:
                            self.assertEqual(sviValue, value[0], msg='for ' + key + '=' + str(value[0]))
                            self.assertEqual(sviValue2, value[0], msg='for ' + key + '=' + str(value[0]))

                    sviVariable.write(value[1])
                    sviValue = sviVariable.read()
                    sviValue2 = sviVariable2.read()
                    if type(sviValue) == list:
                        for i in range(len(sviValue)):
                            self.assertEqual(type(sviValue[i]), writeVariables[key][0], msg='for ' + key + '=' + str(value[1][i]))
                            self.assertEqual(type(sviValue2[i]), writeVariables[key][0], msg='for ' + key + '=' + str(value[1][i]))
                            self.assertEqual(sviValue[i], value[1][i], msg='for ' + key + '=' + str(value[1][i]))
                            self.assertEqual(sviValue2[i], value[1][i], msg='for ' + key + '=' + str(value[1][i]))
                    else:
                        self.assertEqual(type(sviValue), writeVariables[key], msg='for ' + key + '=' + str(value[1]))
                        self.assertEqual(type(sviValue2), writeVariables[key], msg='for ' + key + '=' + str(value[1]))
                        self.assertEqual(sviValue, value[1], msg='for ' + key + '=' + str(value[1]))
                        self.assertEqual(sviValue2, value[1], msg='for ' + key + '=' + str(value[1]))

            except Exception as e:
                ErrorMsg = e
                Error = True
                print(str(e))

            # Remove the svi test application
            sviAppRemove(mh)

            if Error:
                raise ErrorMsg
            else:
                testedMethods.append('_SVIVariable.write')

    def test_getConnectionState(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        connectionState = sviVariable.getConnectionState()

        self.assertEqual(connectionState, 0)
        self.assertEqual(type(connectionState), int)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getConnectionState')

    def test_getFullName(self):
        mh = m1com.M1Controller(ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule('RES', mh)
        sviVariable = m1com._SVIVariable('RES/CPU/TempCelsius', swModule)
        name = sviVariable.getFullName()

        self.assertEqual(type(name), str)
        self.assertEqual(name, 'RES/CPU/TempCelsius')
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getFullName')

if __name__ == "__main__":
    
    # Settings
    ipAddress  = '169.254.141.136' #'10.14.41.163'      # Set ip address of the Bachmann PLC used for testing
    fastTest   = False                # Skip tests that require a reboot
    
    # List where name of tested methods will be saved
    testedMethods = []

    # Find all classes and there callable methods in m1com
    M1comClasses = {}
    for Class in dir(m1com):

        # Check if the class is callable
        if callable(getattr(m1com, Class)):

            # Find all methods in the callable class
            M1comClassMethods = [Method for Method in dir(getattr(m1com, Class)) if callable(getattr(getattr(m1com, Class), Method)) and not Method.startswith('__')]

            # Add class and its methods to dictionary if it does have methods
            if len(M1comClassMethods) != 0:
                M1comClasses.update({Class:M1comClassMethods})

    # Perform the unit test
    unittest.main(verbosity=2, exit=False)

    # Check if all methods in m1com where tested
    count = 0
    for Class in M1comClasses:
        for Method in M1comClasses[Class]:
            if (Class + '.' + Method) not in testedMethods:
                if count == 0:
                    print('\nThe following methods were not tested or failed the unittest:')
                print(Class + '.' + Method + '()')
                count = count + 1

    # Print number of not tested methods
    if count > 0:
        print('\n' + str(count) + ' methods were not tested or failed the unittest!')

