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

        self.assertEqual(str(type(mh.getLoginInfo())), "<class 'm1com.RES_LOGIN2_R'>")

        assertNotBytes(self, mh.getLoginInfo())

        securityLevel = mh.getLoginInfo().SecurityLevel
        self.assertGreaterEqual(securityLevel, 0)
        self.assertLessEqual(securityLevel, 4)
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
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)

        self.assertEqual(swModule.attach(), None)
        self.assertNotEqual(swModule._modHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.attach')

    def test_detach(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)

        self.assertEqual(swModule.detach(), None)
        self.assertEqual(swModule._modHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.detach')

    def test_getModHandle(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)

        self.assertEqual(swModule.getModHandle(), swModule._modHandle)
        self.assertNotEqual(swModule._modHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.getModHandle')

    def test_getNumberofSviVariables(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)

        self.assertGreater(swModule.getNumberofSviVariables(), 200)
        self.assertEqual(type(swModule.getNumberofSviVariables()), int)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.getNumberofSviVariables')

    def test_getListofSviVariables(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)

        listOfSviVariables = swModule.getListofSviVariables()

        self.assertEqual(type(listOfSviVariables), dict)
        assertNotBytes(self, listOfSviVariables)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_M1SwModule.getListofSviVariables')

class Test_SVIVariable(unittest.TestCase):
    def test_attach(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)
        sviVariable = m1com._SVIVariable(dll, 'RES/CPU/TempCelsius', swModule)

        self.assertEqual(sviVariable.attach(), None)
        self.assertNotEqual(sviVariable._varHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.attach')

    def test_detach(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)
        sviVariable = m1com._SVIVariable(dll, 'RES/CPU/TempCelsius', swModule)

        self.assertEqual(sviVariable.detach(), None)
        self.assertEqual(sviVariable._varHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.detach')

    def test_getVarHandle(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)
        sviVariable = m1com._SVIVariable(dll, 'RES/CPU/TempCelsius', swModule)

        self.assertEqual(sviVariable.getVarHandle(), sviVariable._varHandle)
        self.assertNotEqual(sviVariable._varHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getVarHandle')

    def test_getVarInfo(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)
        sviVariable = m1com._SVIVariable(dll, 'RES/CPU/TempCelsius', swModule)
        sviInfo = sviVariable.getVarInfo()

        self.assertEqual(sviInfo, sviVariable._varInfo)
        self.assertNotEqual(sviInfo, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getVarInfo')

    def test_updateVarInfo(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)
        sviVariable = m1com._SVIVariable(dll, 'RES/CPU/TempCelsius', swModule)
        updateSviInfo = sviVariable.updateVarInfo()

        self.assertEqual(updateSviInfo, None)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.updateVarInfo')

    def test_read(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)
        sviVariable = m1com._SVIVariable(dll, 'RES/CPU/TempCelsius', swModule)
        sviValue = sviVariable.read()

        self.assertEqual(type(sviValue), int)
        self.assertGreaterEqual(sviValue, 20)
        self.assertLessEqual(sviValue, 100)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.read')

    def test_write(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)
        sviVariable = m1com._SVIVariable(dll, 'RES/CPU/TempCelsius', swModule)

        try:
            sviVariable.write(60)
        except m1com.PyComException as error:
            error = str(error.value)
            self.assertEqual(error, 'pyCom Error: Svi Variable[RES/CPU/TempCelsius] is not write able!')

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

        # Reconnect to the rebooted target and write svi variable
        mh.connect(timeout=3000)

        # Perform the write tests
        swModule = m1com._M1SwModule(dll, 'SVIWRITE', mh)
        sviVariable = m1com._SVIVariable(dll, 'SVIWRITE/writeTestVariable', swModule)
        sviVariable.write(1)
        sviValue = sviVariable.read()
        self.assertEqual(type(sviValue), int)
        self.assertEqual(sviValue, 1)

        sviVariable.write(0)
        sviValue = sviVariable.read()
        self.assertEqual(type(sviValue), int)
        self.assertEqual(sviValue, 0)

        # Remove application and mconfig.ini from target, copy back the original mconfig.ini and reboot
        mh.remove('/cfc0/app/sviwrite.m')
        mh.remove('/cfc0/mconfig.ini')
        mh.copyToTarget(curDir + '/unittestFiles/mconfigBackup.ini', '/cfc0/mconfig.ini')
        mh.reboot()
        self.assertEqual(mh.disconnect(), 0)
        os.remove(curDir + '/unittestFiles/mconfigBackup.ini')
        os.remove(curDir + '/unittestFiles/mconfigSVIWrite.ini')
        time.sleep(20)

        testedMethods.append('_SVIVariable.write')

    def test_getConnectionState(self):
        dll = m1com.PyCom()
        mh = m1com.M1Controller(pycom=dll, ip=ipAddress)
        mh.connect(timeout=3000)

        swModule = m1com._M1SwModule(dll, 'RES', mh)
        sviVariable = m1com._SVIVariable(dll, 'RES/CPU/TempCelsius', swModule)
        connectionState = sviVariable.getConnectionState()

        self.assertEqual(connectionState, 0)
        self.assertEqual(type(connectionState), int)
        self.assertEqual(mh.disconnect(), 0)

        testedMethods.append('_SVIVariable.getConnectionState')

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
                print('\nMethod ' + Class + '.' + Method + '() not tested!')
                count = count + 1

    # Print number of not tested methods
    if count > 0:
        print('\n' + str(count) + ' methods are not tested!')

