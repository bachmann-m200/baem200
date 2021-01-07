import unittest
import sys
import os
import m1com
import ctypes
import time

class Test_M1Controller(unittest.TestCase):
    def test_getCtrlHandle(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)
        self.assertEqual(mh.getCtrlHandle(), mh._ctrlHandle)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getCtrlHandle')

    def test_connect(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)
        self.assertNotEqual(mh._ctrlHandle, None)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('connect')

    def test_getSessionLiveTime(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)
        self.assertGreaterEqual(mh.getSessionLiveTime(), 0)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getSessionLiveTime')


    def test_getLoginInfo(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)
        self.assertEqual(str(type(mh.getLoginInfo())), "<class 'm1com.RES_LOGIN2_R'>")

        securityLevel = mh.getLoginInfo().SecurityLevel
        self.assertGreaterEqual(securityLevel, 0)
        self.assertLessEqual(securityLevel, 4)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getLoginInfo')

    def test_renewConnection(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)
        self.assertEqual(mh.renewConnection(), None)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('renewConnection')

    def test_getNumberofSwModules(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)
        self.assertGreaterEqual(mh.getNumberofSwModules(), 8)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getNumberofSwModules')

    def test_getSwModuleByName(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        self.assertEqual(str(type(mh.getSwModuleByName('RES'))), "<class 'm1com._M1SwModule'>")
        self.assertEqual(mh.getSwModuleByName('RES').name.decode(), 'RES')
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getSwModuleByName')
    
    def test_getListofSwModules(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        self.assertEqual(str(type(mh.getListofSwModules())), "<class 'dict'>")
        self.assertEqual(len(mh.getListofSwModules()), mh.getNumberofSwModules())
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getListofSwModules')
    
    def test_getListofHwModules(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertGreater(lastHwModuleNb, 0)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getListofHwModules')
    
    def test_getDrvId(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertGreater(mh.getDrvId(lastHwModuleNb), 0)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getDrvId')

    def test_getCardInfo(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertEqual(str(type(mh.getCardInfo(lastHwModuleNb))), "<class 'm1com.MIO_GETCDINF_R'>")
        self.assertEqual(mh.getCardInfo(lastHwModuleNb).Inf.CardNb, lastHwModuleNb)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getCardInfo')

    def test_getCardInfoExt(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        lastHwModuleNb = mh.getListofHwModules()[-1]['CardNb']

        self.assertEqual(mh.getCardInfoExt(lastHwModuleNb)['CardNb'], lastHwModuleNb)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('getCardInfoExt')

    def test_copyFromTarget(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        self.assertEqual(mh.copyFromTarget('/cfc0/mconfig.ini', 'localCopyMconfig.ini'), None)
        self.assertEqual(mh.disconnect(), 0)
        self.assertTrue(os.path.isfile('localCopyMconfig.ini'))
        os.remove('localCopyMconfig.ini')

        testedFunctions.append('copyFromTarget')

    def test_copyToTarget(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        f = open('test_copyToTarget.txt', 'w')
        f.write("Test for mh.copyToTarget('test_copyToTarget.txt', '/cfc0/test_copyToTarget.txt')")
        f.close()

        self.assertEqual(mh.copyToTarget('test_copyToTarget.txt', '/cfc0/test_copyToTarget.txt'), None)
        self.assertEqual(mh.disconnect(), 0)

        os.remove('test_copyToTarget.txt')

        testedFunctions.append('copyToTarget')

    def test_copyRemote(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        self.assertEqual(mh.copyRemote('/cfc0/mconfig.ini', '/cfc0/test_copyRemoteOfMconfig.txt'), None)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('copyRemote')

    def test_remove(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        self.assertEqual(mh.remove('/cfc0/test_copyRemoteOfMconfig.txt'), None)
        self.assertEqual(mh.remove('/cfc0/test_copyToTarget.txt'), None)
        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('remove')

    @unittest.skip("Requires reboot, skip for faster testing")
    def test_resetAll(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        self.assertEqual(mh.resetAll(), None)
        self.assertEqual(mh.reboot(), None)
        self.assertEqual(mh.disconnect(), 0)
        time.sleep(20)

        testedFunctions.append('resetAll')

    @unittest.skip("Requires reboot, skip for faster testing")
    def test_reboot(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        self.assertEqual(mh.reboot(), None)
        self.assertEqual(mh.disconnect(), 0)
        time.sleep(20)

        testedFunctions.append('reboot')

    def test_disconnect(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        self.assertEqual(mh.disconnect(), 0)

        testedFunctions.append('disconnect')

    @unittest.skip("Requires reboot, skip for faster testing")
    def test_sendCall(self):
        mh = m1com.M1Controller(ip='169.254.141.136')
        mh.connect(timeout=3000)

        self.assertEqual(str(mh.sendCall("MOD", 134, ctypes.c_int32(0), ctypes.c_int32(0), timeout=3000, version=2)), 'c_long(0)')
        self.assertEqual(mh.disconnect(), 0)
        time.sleep(20)

        testedFunctions.append('sendCall')

if __name__ == "__main__":
    testedFunctions = []
    M1ControllerFunctions = [func for func in dir(m1com.M1Controller) if callable(getattr(m1com.M1Controller, func)) and not func.startswith("__")]
    unittest.main(verbosity=2, exit=False)

    for functionName in M1ControllerFunctions:
        if functionName not in testedFunctions:
            print("\nFunction M1Controller." + functionName + "() not tested!")
