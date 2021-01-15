#!/usr/bin/python
# Filename: pyCom.py
# Module pyCom
# python classes to interact with a M1 Controller through M1Com and ctypes.

import ctypes, os.path, shutil, sys
from ctypes.test import ctypes
from ctypes.test.test_pointers import ctype_types


#Const:
MIO_INFOLEN_A        = 200
MIO_CNAMELEN_A       = 24
MIO_PRODNBLEN_A      = 12
M_FILENAMELEN_A      = 16
M_MODNAMELEN_A       = 12
M_UNAMELEN2_A        = 64
M_PWORDLEN2          = 32
M_CARDNAMELEN_A      = 24
SVI_ADDRLEN_A        = 64
MIO_PRODNBLEN_A      = 12
BOOT_LEN1            = 20
ONLINE               = 0
OFFLINE              = 1
ERROR                = 2
OK                   = 0
#Protocol types:
PROTOCOL_TCP         = 0
PROTOCOL_QSOAP       = 1
PROTOCOL_SSL         = 2
PROTOCOL_UDP         = 4

SMI_PERM_REBOOT      = 0x80000 

#SVI FORMAT:
SVI_F_IN             = 0x80     #Type is input (server view) */
SVI_F_OUT            = 0x40     #Type is output (server view) */
SVI_F_INOUT          = 0xc0     #Type is input and output */
SVI_F_BLK            = 0x20     #Block value */
SVI_F_HIDDEN         = 0x100    #Hidden service variable */
SVI_F_UNKNOWN        = 0x00     #Format unknown */
SVI_F_UINT1          = 0x01     #Bit value */
SVI_F_UINT8          = 0x02     #8-bit unsigned integer */
SVI_F_SINT8          = 0x03     #8-bit signed integer */
SVI_F_UINT16         = 0x04     #16-bit unsigned integer */
SVI_F_SINT16         = 0x05     #16-bit signed integer */
SVI_F_UINT32         = 0x06     #32-bit unsigned integer */
SVI_F_SINT32         = 0x07     #32-bit signed integer */
SVI_F_REAL32         = 0x08     #32-bit float */
SVI_F_BOOL8          = 0x09     #Boolean value */
SVI_F_CHAR8          = 0x0a     #8-bit character */
SVI_F_MIXED          = 0x0b     #mixed; for SVI_F_BLK */
SVI_F_UINT64         = 0x0c     #64-bit unsigned integer */
SVI_F_SINT64         = 0x0d     #64-bit signed integer */
SVI_F_REAL64         = 0x0e     #64-bit float */
SVI_F_CHAR16         = 0x0f     #16-bit character (Unicode) */
SVI_F_STRINGLSTBASE  = 0x10     #base of String list type */
SVI_F_USTRINGLSTBASE = 0x11     #base of Unicode String list type */

#Structures:
class MODULE_NAME(ctypes.Structure):
    _fields_ = [("name", (ctypes.c_char * M_MODNAMELEN_A))]

class MODULE_NAME_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY',      ctypes.POINTER(MODULE_NAME))]

    def __init__(self, num_of_structs):
        elems = (MODULE_NAME * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(MODULE_NAME))
        self.array_size = num_of_structs

class MODULE_LIST(ctypes.Structure):
    _fields_ = [("countModules", ctypes.c_ushort),
                ("names"       , ctypes.POINTER(MODULE_NAME))]

class VARIABLE_INFO(ctypes.Structure):
    _fields_ = [("name",    (ctypes.c_char * (M_MODNAMELEN_A + 1 + SVI_ADDRLEN_A))),
                ("format",  ctypes.c_ushort),
                ("len",     ctypes.c_ushort)]

class VARIABLE_INFO_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY',      ctypes.POINTER(VARIABLE_INFO))]

    def __init__(self, num_of_structs):
        elems = (VARIABLE_INFO * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(VARIABLE_INFO))
        self.array_size = num_of_structs

class VARIABLE_INFO_LIST(ctypes.Structure):
    _fields_ = [("countVariables", ctypes.c_uint),
                ("varInfo", ctypes.POINTER(VARIABLE_INFO))]

class VARIABLE_BUFFER(ctypes.Structure):
    _fields_ = [("varHandle", ctypes.c_void_p),
                ("bufferLen", ctypes.c_uint),
                ("buffer",    ctypes.c_char_p),
                ("lastError", ctypes.c_long)]

class VARIABLE_BUFFER_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(VARIABLE_BUFFER))]

    def __init__(self,num_of_structs):
        elems = (VARIABLE_BUFFER * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(VARIABLE_BUFFER))
        self.array_size = num_of_structs

class RES_EXTPING_R(ctypes.Structure):
    _fields_ = [("RetCode",    ctypes.c_int32),
                ("ProdNb",     (ctypes.c_char * MIO_PRODNBLEN_A)),
                ("VersCode",   (ctypes.c_uint32 * 3)),
                ("VersType",   ctypes.c_uint32),
                ("TargetName", (ctypes.c_char * BOOT_LEN1)),
                ("Mode",       ctypes.c_uint32),
                ("Dhcp",       ctypes.c_ubyte),
                ("OpSystem",   ctypes.c_ubyte),
                ("Reserved",   (ctypes.c_ubyte * 2)),
                ("Type",       ctypes.c_uint32),
                ("Variant",    ctypes.c_uint32)]

class _SysPerm(ctypes.Union):
    _fields_ = [("__64", ctypes.c_longlong),
                ("__32", (ctypes.c_uint32 * 2))]

class _AppPerm(ctypes.Union):
    _fields_ = [("__64", ctypes.c_longlong),
                ("__32", (ctypes.c_uint32 * 2))]

class RES_USER_ACCESS(ctypes.Structure):
    _anonymous_ = ("SysPerm","AppPerm")
    _fields_ = [("Group",       ctypes.c_uint8),
                ("Level",       ctypes.c_uint8),
                ("Priority",    ctypes.c_uint8),
                ("Spare0",      ctypes.c_uint8),
                ("SysPerm",     _SysPerm),
                ("AppPerm",     _AppPerm),
                ("AppData",     ctypes.c_int32),
                ("Spare1",      (ctypes.c_uint32 * 3))]

class RES_LOGIN2_C(ctypes.Structure):
    _fields_ = [("UserParm",    ctypes.c_uint32),
                ("MainVers",    ctypes.c_uint32),
                ("SubVers",     ctypes.c_uint32),
                ("ToolName",    (ctypes.c_char * M_MODNAMELEN_A)),
                ("UserName",    (ctypes.c_char * M_UNAMELEN2_A)),
                ("Password",    (ctypes.c_char * M_PWORDLEN2)),
                ("Local",       ctypes.c_bool),
                ("Spare1",      (ctypes.c_bool * 3)),
                ("Spare2",      ctypes.c_uint32),
                ("Spare3",      ctypes.c_uint32),
                ("Spare4",      ctypes.c_uint32),
                ("Spare5",      ctypes.c_uint32)]

class RES_LOGIN2_R(ctypes.Structure):
    _fields_ = [("RetCode",         ctypes.c_int32),
                ("SecurityLevel",   ctypes.c_uint32),
                ("Spare1",          ctypes.c_uint32),
                ("UserAcc",         RES_USER_ACCESS),
                ("AuthLen",         ctypes.c_uint32),
                ("Authent",         (ctypes.c_uint8 * 128)),
                ("UserData",        (ctypes.c_uint8 * 128)),
                ("Reserv",          (ctypes.c_uint8 * 128))]
    
class TARGET_INFO(ctypes.Structure):
    _fields_ = [("extPingR", RES_EXTPING_R),
                ("hostAddr", ctypes.c_char * 16)]

class TARGET_INFO_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY',      ctypes.POINTER(TARGET_INFO))]

    def __init__(self, num_of_structs):
        elems = (TARGET_INFO * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(TARGET_INFO))
        self.array_size = num_of_structs

class MIO_GETDRV_C(ctypes.Structure):
    _fields_ = [("CardNb", ctypes.c_uint32),]

class MIO_GETDRV_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32),
                ("DrvId", ctypes.c_uint32)]

class MIO_CARDINF(ctypes.Structure):
    _fields_ = [("CardNb", ctypes.c_uint32),
                ("Type", ctypes.c_int32),
                ("Variant", ctypes.c_int32),
                ("Category", ctypes.c_int32),
                ("Flags", ctypes.c_int32),
                ("MaxChan", ctypes.c_uint32)]
 
class MIO_GETCDINF_C(ctypes.Structure):
    _fields_ = [("DrvId", ctypes.c_uint32),]

class MIO_GETCDINF_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32),
                ("Inf", MIO_CARDINF)]

class tm(ctypes.Structure):
    _fields_ = [("tm_sec", ctypes.c_int32),
                ("tm_min", ctypes.c_int32),
                ("tm_hour", ctypes.c_int32),
                ("tm_mday", ctypes.c_int32),
                ("tm_mon", ctypes.c_int32),
                ("tm_year", ctypes.c_int32),
                ("tm_wday", ctypes.c_int32),
                ("tm_yday", ctypes.c_int32),
                ("tm_isdst", ctypes.c_int32)] 

class Ver(ctypes.Structure):
    _fields_ = [("Major", ctypes.c_uint8),
                ("Minor", ctypes.c_uint8),
                ("SubMin", ctypes.c_uint8),
                ("Type", ctypes.c_uint8)]
                
class MIO_VERS(ctypes.Structure):
    _fields_ = [("Ver", Ver),
                ("Ver32", ctypes.c_uint32)]

class MIO_EXTCDINF(ctypes.Structure):
    _fields_ = [("CardNb", ctypes.c_uint32),
                ("StationNb", ctypes.c_int32),
                ("SlotNb", ctypes.c_int32),
                ("PreSlotS", ctypes.c_int32),
                ("PostSlots", ctypes.c_int32),
                ("Mode", ctypes.c_int32),
                ("State", ctypes.c_int32),
                ("Type", ctypes.c_int32),
                ("Variant", ctypes.c_int32),
                ("Category", ctypes.c_int32),
                ("Flags", ctypes.c_int32),
                ("MaxChan", ctypes.c_uint32),
                ("Version", ctypes.c_int32),
                ("DrvVersion", ctypes.c_int32),
                ("Attribute", ctypes.c_uint32),
                ("ProdTime", tm),
                ("ProdNb",     (ctypes.c_char * MIO_PRODNBLEN_A)),
                ("Name",     (ctypes.c_char * MIO_CNAMELEN_A)),
                ("Info",     (ctypes.c_char * MIO_INFOLEN_A)),
                ("DrvName",     (ctypes.c_char * M_FILENAMELEN_A)),
                ("Power", ctypes.c_int32),
                ("Current_5V", ctypes.c_int32),
                ("Current_P15V", ctypes.c_int32),
                ("Current_M15V", ctypes.c_int32),
                ("ModVerType", ctypes.c_int32),
                ("Current_5V", ctypes.c_int32),
                ("RedundantRead",   ctypes.c_bool),
                ("WriteVerify",   ctypes.c_bool),
                ("BusCheck",   ctypes.c_bool),
                ("AliveCheck",   ctypes.c_bool),
                ("AssemblyCode", ctypes.c_uint16),
                ("HwVariant", ctypes.c_uint8),
                ("Reserved1", ctypes.c_uint8),
                ("Settings", ctypes.c_uint32),
                ("Fware", MIO_VERS),
                ("ExStateInfo", ctypes.c_uint32)]

class MIO_GETEXTCDINF_C(ctypes.Structure):
    _fields_ = [("CardNb", ctypes.c_uint32),]

class MIO_GETEXTCDINF_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32),
                ("Inf", MIO_EXTCDINF)]

class INF_CARDINFO(ctypes.Structure):
    _fields_ = [("Name", (ctypes.c_char * M_CARDNAMELEN_A)),
                ("CardNb", ctypes.c_uint32),
                ("StationNb", ctypes.c_uint32),
                ("SlotNb", ctypes.c_uint32),
                ("MaxChan", ctypes.c_uint32),
                ("Mode", ctypes.c_uint32),
                ("Type", ctypes.c_uint32),
                ("State", ctypes.c_uint32),
                ("BusType", ctypes.c_int16),
                ("NetNb", ctypes.c_int16)]

class INF_CARDINFOLST_C(ctypes.Structure):
    _fields_ = [("FirstIdx", ctypes.c_uint32),
                ("LastIdx", ctypes.c_uint32),
                ("Filter", ctypes.c_uint32)]

class INF_CARDINFOLST_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32),
                ("Last", ctypes.c_uint32),
                ("NbOfObj", ctypes.c_uint32),
                ("Inf", INF_CARDINFO)]

#pyCom ExceptionTypes:
class PyComException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PyComTypeException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class PyCom:
    """
    Instance loading the M1COM DLL.

    Usage:

    >>> dll = PyCom()
    >>> dll.getDllVersion()
    'V1.14.99 Release'
    >>> dll.getDllBits()
    '64bit'
    """
    def __init__(self, dllpath = ""):

        if dllpath == "":
            
            # Select correct dll (32bit or 64bit)
            if sys.maxsize > 2**32: # 64bit
                dllname = "m1com64.dll"
                self.bits = '64bit'
            else: # 32bit
                dllname = "m1com.dll"
                self.bits = '32bit'

            # The search paths
            searchPath = sys.path
            searchPath.append("C:\\bachmann\\M1sw\\PC-Communication\\Windows\\m1com\\x64")
            searchPath.append("C:\\bachmann\\M1sw\\PC-Communication\\Windows\\m1com\\win32")
            searchPath.append("D:\\bachmann\\M1sw\\PC-Communication\\Windows\\m1com\\x64")
            searchPath.append("D:\\bachmann\\M1sw\\PC-Communication\\Windows\\m1com\\win32")
        
            # Look for the correct m1com dll in system paths
            for syspath in sys.path:
                for root, _, files in os.walk(syspath):
                    for file in files:
                        if file == dllname:

                            # m1com found, set dll path
                            dllpath = os.path.join(root, file)

                            # Assume that the log.prp file can also be found here
                            logprp = os.path.join(root, "log.prp")

                            # Check if logpath is really correct
                            if not os.path.isfile(logprp):
                                raise PyComException("pyCom Error: make sure " + dllname + " and log.prp are in the same directory")

                            break

                    if dllpath != "":
                        break

                if dllpath != "":
                    break      

            # Raise exception if the dll and log.prp cannot be found
            if dllpath == "":
                raise PyComException("pyCom Error: cannot find " + dllname + " and log.prp in sys.path or Application Directory")
        
        if(not(os.path.isfile("log.prp"))):
            print("pyCom Info: Missing log.prp in Application Directory!")
            logprp = os.path.dirname(dllpath)+"\\log.prp"
            print("            Copy log.prp from dllpath: " + logprp)
            try:
                shutil.copyfile(logprp, "log.prp")
            except Exception as e:
                print("pyCom Warn: Can't Copy log.prp from path:\n" + logprp + "\n" + e)
        m1Dll = ctypes.CDLL(dllpath)
        
        #configuration:
        self.servicename = "PyCom"
        
        #UnitTested: yes
        #returns the version of the m1com.dll
        # void M1C_GetVersion(CHAR* version, UINT32 strLen)
        self.M1C_GetVersion = m1Dll.M1C_GetVersion
        self.M1C_GetVersion.argtypes = [ctypes.c_char_p, ctypes.c_uint]
        
        #only load config if version matches:
        latestVersion = 'V1.14.99 Release'
        currentVersion = self.getDllVersion()
        if(currentVersion != latestVersion):
            raise PyComException("pyCom Error: Wrong Dll Version expected Version: " + str(latestVersion) + " version is: " + str(currentVersion))
        
        #UnitTested: no
        #TODO:
        #M1COM VOID GetErrorMsg(SINT32 errorCode, CHAR * errorMsg, UINT32 errorMsgLen);
        self.GetErrorMsg = m1Dll.GetErrorMsg
        self.GetErrorMsg.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_uint]
        
        #Protocol types:
        #PROTOCOL_TCP   = 0
        #PROTOCOL_QSOAP = 1    
        #PROTOCOL_SSL   = 2    
        #PROTOCOL_UDP   = 4
        #UnitTested: no
        # creates a controller configuration
        # void* TARGET_Create(char* ip, long protocol, unsigned int timeout);
        self.TARGET_Create = m1Dll.TARGET_Create
        self.TARGET_Create.argtypes = [ctypes.c_char_p, ctypes.c_long, ctypes.c_uint]
        self.TARGET_Create.restype  = ctypes.c_void_p
        
        #UnitTested: no
        #TODO:
        #VOID TARGET_Dispose(M1C_H_TARGET targetHandle);
        self.TARGET_Dispose = m1Dll.TARGET_Dispose
        self.TARGET_Dispose.argtypes = [ctypes.c_void_p]
        
        #UnitTested: no
        #Connects a targetHandle
        #SINT32 TARGET_Connect(void* ctrl, char* username, char* password, char* clientname);
        self.TARGET_Connect = m1Dll.TARGET_Connect
        self.TARGET_Connect.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.TARGET_Connect.restype  = ctypes.c_long

        #UnitTested: no
        #Gets session live time.
        #SINT32 TARGET_GetSessionLiveTime(M1C_H_TARGET targetHandle, UINT32* sessionLiveTime);
        self.TARGET_GetSessionLiveTime = m1Dll.TARGET_GetSessionLiveTime
        self.TARGET_GetSessionLiveTime.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.TARGET_GetSessionLiveTime.restype  = ctypes.c_long

        #UnitTested: no
        #Returns information about the current login session.
        #SINT32 TARGET_GetLoginInfo(M1C_H_TARGET targetHandle, RES_LOGIN2_R * resLogin2Reply);
        self.TARGET_GetLoginInfo = m1Dll.TARGET_GetLoginInfo
        self.TARGET_GetLoginInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(RES_LOGIN2_R)]
        self.TARGET_GetLoginInfo.restype  = ctypes.c_long

        #UnitTested: no
        #Renews the connection to the target.
        #SINT32 TARGET_RenewConnection(M1C_H_TARGET targetHandle);
        self.TARGET_RenewConnection = m1Dll.TARGET_RenewConnection
        self.TARGET_RenewConnection.argtypes = [ctypes.c_void_p]
        self.TARGET_RenewConnection.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #SINT32 TARGET_Close(M1C_H_TARGET targetHandle);
        self.TARGET_Close = m1Dll.TARGET_Close
        self.TARGET_Close.argtypes = [ctypes.c_void_p]
        self.TARGET_Close.restype  = ctypes.c_long
        
        #UnitTested: no
        #Read number of the installed modules on ctrl.
        #SINT32 TARGET_GetCountModules(void* targetHandle, unsigned short* moduleCount);
        self.TARGET_GetCountModules = m1Dll.TARGET_GetCountModules
        self.TARGET_GetCountModules.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]
        self.TARGET_GetCountModules.restype  = ctypes.c_long
        
        #UnitTested: no
        #Read module list from ctrl.
        #SINT32 TARGET_GetModules(M1C_H_TARGET targetHandle, const UINT16 moduleCount, MODULE_LIST* moduleList);
        self.TARGET_GetModules = m1Dll.TARGET_GetModules
        self.TARGET_GetModules.argtypes = [ctypes.c_void_p, ctypes.c_ushort, ctypes.POINTER(MODULE_LIST)]
        self.TARGET_GetModules.restype  = ctypes.c_long
        
        #UnitTested: no
        #Create SwModuleHandler
        #M1C_H_MODULE TARGET_CreateModule(M1C_H_TARGET targetHandle, CHAR* name);
        self.TARGET_CreateModule = m1Dll.TARGET_CreateModule
        self.TARGET_CreateModule.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.TARGET_CreateModule.restype  = ctypes.c_void_p
        
        #UnitTested: no
        #Attach ModuleHandle to Controller
        #SINT32 MODULE_Connect(M1C_H_MODULE moduleHandle);
        self.MODULE_Connect = m1Dll.MODULE_Connect
        self.MODULE_Connect.argtypes = [ctypes.c_void_p]
        self.MODULE_Connect.restype = ctypes.c_long
        
        #UnitTested: no
        #Count SVI Variables of a SwModule
        #SINT32 MODULE_GetCountVariables(M1C_H_MODULE moduleHandle, UINT32* varCount);
        self.MODULE_GetCountVariables = m1Dll.MODULE_GetCountVariables
        self.MODULE_GetCountVariables.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.MODULE_GetCountVariables.restype  = ctypes.c_long
        
        #UnitTested: no
        #Reads a List of SVI Variables from a SwModule
        #SINT32 MODULE_GetVariables(M1C_H_MODULE moduleHandle, const UINT32 varCount, VARIABLE_INFO_LIST* varList);
        self.MODULE_GetVariables = m1Dll.MODULE_GetVariables
        self.MODULE_GetVariables.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(VARIABLE_INFO_LIST)]
        self.MODULE_GetVariables.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1C_H_VARIABLE TARGET_CreateVariable(M1C_H_TARGET targetHandle, CHAR* name);
        self.TARGET_CreateVariable = m1Dll.TARGET_CreateVariable
        self.TARGET_CreateVariable.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.TARGET_CreateVariable.restype  = ctypes.c_void_p
        
        #UnitTested: no
        #TODO:
        #M1COM VOID VARIABLE_Dispose(M1C_H_VARIABLE variable);
        self.VARIABLE_Dispose = m1Dll.VARIABLE_Dispose
        self.VARIABLE_Dispose.argtypes = [ctypes.c_void_p]
        
        #UnitTested: no
        #TODO:
        #SINT32 TARGET_InitVariables(M1C_H_TARGET targetHandle, M1C_H_VARIABLE* variables, UINT32 countVariables);
        self.TARGET_InitVariables = m1Dll.TARGET_InitVariables
        self.TARGET_InitVariables.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_InitVariables.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #SINT32 VARIABLE_GetInfo(M1C_H_VARIABLE variable, VARIABLE_INFO* varInfo);
        self.VARIABLE_GetInfo = m1Dll.VARIABLE_GetInfo
        self.VARIABLE_GetInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_GetInfo.restype  = ctypes.c_long

        #UnitTested: no
        #TODO:VARIABLE_GetFullName
        #M1COM CHAR8* (M1C_H_VARIABLE variable);
        self.VARIABLE_GetFullName = m1Dll.VARIABLE_GetFullName
        self.VARIABLE_GetFullName.argtypes = [ctypes.c_void_p]
        self.VARIABLE_GetFullName.restype  = ctypes.c_char_p
        
        #UnitTested: no
        #TODO:
        #M1COM UINT32 VARIABLE_GetBufferLen(VARIABLE_INFO* varInfo);
        self.VARIABLE_GetBufferLen = m1Dll.VARIABLE_GetBufferLen
        self.VARIABLE_GetBufferLen.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_GetBufferLen.restype  = ctypes.c_uint
        
        #UnitTested: no
        #TODO:
        #M1COM UINT32 VARIABLE_getArrayLen(VARIABLE_INFO* varInfo);
        self.VARIABLE_getArrayLen = m1Dll.VARIABLE_getArrayLen
        self.VARIABLE_getArrayLen.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_getArrayLen.restype  = ctypes.c_uint
        
        #UnitTested: no
        #TODO
        #SINT32 TARGET_ReadVariables(M1C_H_TARGET targetHandle, VARIABLE_BUFFER* variableBuffers, UINT32 countVariables);
        self.TARGET_ReadVariables = m1Dll.TARGET_ReadVariables
        self.TARGET_ReadVariables.argtypes = [ctypes.c_void_p, ctypes.POINTER(VARIABLE_BUFFER), ctypes.c_uint]
        self.TARGET_ReadVariables.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #SINT32 TARGET_ReadVariable(M1C_H_TARGET targetHandle, M1C_H_VARIABLE variableHandle, VOID* buffer, UINT32 bufferSize);
        self.TARGET_ReadVariable = m1Dll.TARGET_ReadVariable
        self.TARGET_ReadVariable.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_ReadVariable.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #SINT32 TARGET_WriteVariables(M1C_H_TARGET targetHandle, VARIABLE_BUFFER* variables, UINT32 countVariables);
        self.TARGET_WriteVariables = m1Dll.TARGET_WriteVariables
        self.TARGET_WriteVariables.argtypes = [ctypes.c_void_p, ctypes.POINTER(VARIABLE_BUFFER), ctypes.c_uint]
        self.TARGET_WriteVariables.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 TARGET_WriteVariable(M1C_H_TARGET targetHandle, M1C_H_VARIABLE variableHandle, VOID* buffer, UINT32 bufferSize);
        self.TARGET_WriteVariable = m1Dll.TARGET_WriteVariable
        self.TARGET_WriteVariable.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_WriteVariable.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM BOOL8  VARIABLE_IsReadable(VARIABLE_INFO* varInfo);
        self.VARIABLE_IsReadable = m1Dll.VARIABLE_IsReadable
        self.VARIABLE_IsReadable.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_IsReadable.restype  = ctypes.c_ubyte
        
        #UnitTested: no
        #TODO:
        #M1COM BOOL8  VARIABLE_IsWritable(VARIABLE_INFO* varInfo);
        self.VARIABLE_IsWritable = m1Dll.VARIABLE_IsWritable
        self.VARIABLE_IsWritable.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_IsWritable.restype  = ctypes.c_ubyte
        
        #UnitTested: no
        #TODO:
        #SINT32 VARIABLE_GetState(M1C_H_VARIABLE variable, M1C_CONNECTION_STATE* state);
        self.VARIABLE_GetState = m1Dll.VARIABLE_GetState
        self.VARIABLE_GetState.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.VARIABLE_GetState.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM  M1C_H_OBSLIST TARGET_CreateObservationList(M1C_H_TARGET targetHandle, VARIABLE_BUFFER* variableBuffers, UINT32 countVariables);
        self.TARGET_CreateObservationList = m1Dll.TARGET_CreateObservationList
        self.TARGET_CreateObservationList.argtypes = [ctypes.c_void_p, ctypes.POINTER(VARIABLE_BUFFER), ctypes.c_uint]
        self.TARGET_CreateObservationList.restype  = ctypes.c_void_p
        
        #UnitTested: no
        #TODO:
        #M1COM  SINT32 OBSLIST_Dispose(M1C_H_OBSLIST obsListHandle);
        self.OBSLIST_Dispose = m1Dll.OBSLIST_Dispose
        self.OBSLIST_Dispose.argtypes = [ctypes.c_void_p]
        self.OBSLIST_Dispose.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 OBSLIST_Update(M1C_H_OBSLIST obsListHandle, SINT32* indexList, UINT32 listSize);
        self.OBSLIST_Update = m1Dll.OBSLIST_Update
        self.OBSLIST_Update.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_long), ctypes.c_uint]
        self.OBSLIST_Update.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 OBSLIST_Reset(M1C_H_OBSLIST obsListHandle);
        self.OBSLIST_Reset = m1Dll.OBSLIST_Reset
        self.OBSLIST_Reset.argtypes = [ctypes.c_void_p]
        self.OBSLIST_Reset.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #SINT32 MODULE_Dispose(M1C_H_MODULE moduleHandle);
        self.MODULE_Dispose = m1Dll.MODULE_Dispose
        self.MODULE_Dispose.argtypes = [ctypes.c_void_p]
        self.MODULE_Dispose.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO: missing implementation of args!
        #VOID GetErrorSrc(SINT32 errorCode, CHAR * errorSrc, UINT32 errorSrcLen);
        self.GetErrorSrc = m1Dll.GetErrorSrc
        
        #UnitTested: no
        #TODO:
        #UINT32 VARIABLE_getBaseDataType(VARIABLE_INFO* varInfo);
        self.VARIABLE_getBaseDataType = m1Dll.VARIABLE_getBaseDataType
        self.VARIABLE_getBaseDataType.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_getBaseDataType.restype  = ctypes.c_uint
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 TARGET_SmiPing(CHAR* addr, UINT32 timeout, M1C_PROTOCOL protocol, RES_EXTPING_R * extping_r );
        self.TARGET_SmiPing = m1Dll.TARGET_SmiPing
        self.TARGET_SmiPing.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(RES_EXTPING_R)]
        self.TARGET_SmiPing.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 TARGET_SetUintParam(M1C_H_TARGET targetHandle, M1C_UINT_PARAM_KEY key, UINT32 value);
        self.TARGET_SetUintParam = m1Dll.TARGET_SetUintParam
        self.TARGET_SetUintParam.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]
        self.TARGET_SetUintParam.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 TARGET_SetStringParam(M1C_H_TARGET targetHandle, M1C_STRING_PARAM_KEY key, CHAR* value, UINT32 valueLen);
        self.TARGET_SetStringParam = m1Dll.TARGET_SetStringParam
        self.TARGET_SetStringParam.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint]
        self.TARGET_SetStringParam.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM UINT32 TARGET_GetUintParam(M1C_H_TARGET targetHandle, M1C_UINT_PARAM_KEY key);
        self.TARGET_GetUintParam = m1Dll.TARGET_GetUintParam
        self.TARGET_GetUintParam.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_GetUintParam.restype  = ctypes.c_uint
        
        #UnitTested: no
        #TODO:
        #M1COM CHAR*  TARGET_GetStringParam(M1C_H_TARGET targetHandle, M1C_STRING_PARAM_KEY key);
        self.TARGET_GetStringParam = m1Dll.TARGET_GetStringParam
        self.TARGET_GetStringParam.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_GetStringParam.restype  = ctypes.c_char_p

        #UnitTested: no
        #TODO:
        #M1COM SINT32 TARGET_GetMaxCallSize(M1C_H_TARGET targetHandle, UINT32* maxCallSize);
        self.TARGET_GetMaxCallSize = m1Dll.TARGET_GetMaxCallSize
        self.TARGET_GetMaxCallSize.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.TARGET_GetMaxCallSize.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 TARGET_GetConnectionState(M1C_H_TARGET targetHandle, M1C_CONNECTION_STATE* state);
        self.TARGET_GetConnectionState = m1Dll.TARGET_GetConnectionState
        self.TARGET_GetConnectionState.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.TARGET_GetConnectionState.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 TARGET_GetTargetState(M1C_H_TARGET targetHandle, UINT16* appState, UINT16* rebootCount);
        self.TARGET_GetTargetState = m1Dll.TARGET_GetTargetState
        self.TARGET_GetTargetState.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort), ctypes.POINTER(ctypes.c_ushort)]
        self.TARGET_GetTargetState.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 MODULE_SendCall(M1C_H_MODULE moduleHandle, UINT32 proc, UINT32 version, const PVOID send, UINT16 sendSize, PVOID recv, UINT16 recvSize, UINT32 timeout);
        self.MODULE_SendCall = m1Dll.MODULE_SendCall
        self.MODULE_SendCall.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_uint]
        self.MODULE_SendCall.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 TARGET_BroadcastSmiPing( UINT32 timeout, TARGET_INFO * targetInfos, UINT32 len );
        self.TARGET_BroadcastSmiPing = m1Dll.TARGET_BroadcastSmiPing
        self.TARGET_BroadcastSmiPing.argtypes = [ctypes.c_uint, ctypes.POINTER(TARGET_INFO), ctypes.c_uint]
        self.TARGET_BroadcastSmiPing.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 RFS_CopyToTarget(M1C_H_TARGET targetHandle, CHAR *remoteFileName, CHAR *localFileName); 
        self.RFS_CopyToTarget = m1Dll.RFS_CopyToTarget
        self.RFS_CopyToTarget.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        self.RFS_CopyToTarget.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 RFS_CopyFromTarget(M1C_H_TARGET targetHandle, CHAR *localFileName, CHAR *remoteFilename); 
        self.RFS_CopyFromTarget = m1Dll.RFS_CopyFromTarget
        self.RFS_CopyFromTarget.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        self.RFS_CopyFromTarget.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 RFS_CopyRemote(M1C_H_TARGET targetHandle, CHAR *destFile, CHAR *srcFile); 
        self.RFS_CopyRemote = m1Dll.RFS_CopyRemote
        self.RFS_CopyRemote.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        self.RFS_CopyRemote.restype  = ctypes.c_long
        
        #UnitTested: no
        #TODO:
        #M1COM SINT32 RFS_Remove(M1C_H_TARGET targetHandle, CHAR *filename); 
        self.RFS_Remove = m1Dll.RFS_Remove
        self.RFS_Remove.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.RFS_Remove.restype  = ctypes.c_long
        
    def getDllVersion(self):
        """Return the DLL version of the m1com.dll.

        >>> dll = PyCom()
        >>> dll.getDllVersion()
        'V1.14.99 Release'
        """

        version = ctypes.c_char_p(40*"".encode('utf-8'))    #40byte buffer
        self.M1C_GetVersion(version, 40)
        return version.value.decode("utf-8")

    def getDllBits(self):
        """Return whether the m1com.dll is 32bit or 64bit.

        >>> dll = PyCom()
        >>> dll.getDllBits()
        '64bit'
        """
        return self.bits

class M1Controller:
    """
    The M1Controller class.

    Usage:

    >>> mh = M1Controller(ip='169.254.141.136')
    >>> mh.connect(timeout=3000)
    >>> mh.getSessionLiveTime()                                                                 # doctest: +SKIP
    0
    >>> mh.getLoginInfo()                                                                       # doctest: +SKIP
    >>> mh.renewConnection()
    >>> mh.getNumberofSwModules()                                                               # doctest: +SKIP
    9
    >>> mh.getSwModuleByName('RES')                                                             # doctest: +SKIP
    >>> mh.getListofSwModules()                                                                 # doctest: +SKIP
    >>> mh.getListofHwModules()                                                                 # doctest: +SKIP
    >>> mh.getDrvId(7)                                                                          # doctest: +SKIP
    >>> mh.getCardInfo(7)                                                                       # doctest: +SKIP
    >>> mh.getCardInfoExt(7)                                                                    # doctest: +SKIP
    >>> mh.copyFromTarget('/cfc0/mconfig.ini', 'localCopyMconfig.ini')                          # doctest: +SKIP
    >>> mh.copyToTarget('localCopyMconfig.ini', '/cfc0/localCopyMconfig.ini')                   # doctest: +SKIP
    >>> mh.copyRemote('/cfc0/localCopyMconfig.ini', '/cfc0/localCopyMconfig2.ini')              # doctest: +SKIP
    >>> mh.remove('/cfc0/localCopyMconfig.ini')                                                 # doctest: +SKIP
    >>> mh.resetAll()                                                                           # doctest: +SKIP
    >>> mh.reboot()                                                                             # doctest: +SKIP
    >>> mh.sendCall("MOD", 134, ctypes.c_int32(0), ctypes.c_int32(0), timeout=3000, version=2)  # doctest: +SKIP
    c_long(0)
    >>> mh.disconnect()
    0
    """

    def __init__(self, pycom=PyCom(), ip='169.254.141.136', username='M1', password='bachmann'):
        self._pycom = pycom
        self._ip = ip
        self._username = username
        self._password = password
        self._ctrlHandle = None
    
    def getCtrlHandle(self):
        """
        Get control handle from target.
        """
        if(self._ctrlHandle == None):
            raise PyComException(("pyCom Error: Can't access Controller["+self._ip+"] when not connected!"))
        return self._ctrlHandle
    
    def connect(self, protocol=PROTOCOL_TCP, timeout=1000):
        """
        Make a connection with the target using the following protocols:
        TCP:    PROTOCOL_TCP
        QSOAP:  PROTOCOL_QSOAP
        SSL:    PROTOCOL_SSL
        UDP:    PROTOCOL_UDP
        """
        if(self._ctrlHandle == None):
            self._ctrlHandle = self._pycom.TARGET_Create(self._ip.encode('utf-8'), protocol, timeout)
            if(self._pycom.TARGET_Connect(self._ctrlHandle, self._username.encode('utf-8'), self._password.encode('utf-8'), self._pycom.servicename.encode('utf-8')) != OK):
                raise PyComException(("pyCom Error: Can't connect to "+self._ip+" through '"+repr(protocol)+"' with username:"+self._username))
        else:
            raise PyComException(("pyCom Error: Should not connect to a already connected Target! (call disconnect first!)"))
    
    def getSessionLiveTime(self):
        """
        Get session live time in seconds of the connection to the target if configured.
        renewConnection has to be called before the session expires.
        """
        vartime = ctypes.c_uint(0)
        if(self._ctrlHandle == None):
            raise PyComException(("pyCom Error: Make sure you are connected to the Target first! (call connect first!)"))
        else:
            if(self._pycom.TARGET_GetSessionLiveTime(self._ctrlHandle, ctypes.byref(vartime)) != OK):
                raise PyComException(("pyCom Error: Cannot get session live time of Controller["+self._ip+"]"))
        return vartime.value
    
    def getLoginInfo(self):
        """
        Get information about the current login session.
        MSYS Version >= 3.70 on the target is required.
        """
        if(self._ctrlHandle == None):
            raise PyComException(("pyCom Error: Make sure you are connected to the Target first! (call connect first!)"))
        else:
            mod = self._pycom.TARGET_CreateModule(self.getCtrlHandle(), b"RES")        
            self._pycom.MODULE_Connect(mod)

            send = RES_LOGIN2_C()
            send.MainVers = 0
            send.SubVers = 0
            send.ToolName = self._pycom.servicename.encode()
            send.UserName = self._username.encode()
            send.Password = self._password.encode()
            recv = RES_LOGIN2_R() 

            returnSendCall = self._pycom.MODULE_SendCall(
                mod, 
                ctypes.c_uint(304), 
                ctypes.c_uint(2), 
                ctypes.pointer(send), 
                ctypes.sizeof(send), 
                ctypes.pointer(recv), 
                ctypes.sizeof(recv), 
                3000)
            if returnSendCall != OK:
                raise PyComException(("m1com Error: Can't send procedure RES_PROC_LOGIN2 to Controller['"+self._ip+"']"))
            else:
                if(self._pycom.TARGET_GetLoginInfo(self._ctrlHandle, ctypes.pointer(recv)) != OK):
                    raise PyComException(("pyCom Error: Cannot get login info of Controller["+self._ip+"]"))
        return recv
    
    def renewConnection(self):
        """
        Renews the connection to the target.
        If Session Life Time is configured for the target the connection session is renewed with this function.
        """
        if(self._ctrlHandle == None):
            raise PyComException(("pyCom Error: Make sure you are connected to the Target first! (call connect first!)"))
        elif(self._pycom.TARGET_RenewConnection(self._ctrlHandle) != OK):
            raise PyComException(("pyCom Error: Cannot renew connection of Controller['"+self._ip+"']"))
    
    def disconnect(self):
        """
        Closes all connections to the target.
        The communication to the target is stopped and all module handles of the target are disposed!
        If a login has been performed, logout is called. 
        """
        ret = self._pycom.TARGET_Close(self.getCtrlHandle())
        self._pycom.TARGET_Dispose(self.getCtrlHandle())
        self._ctrlHandle = None
        return ret

    def getNumberofSwModules(self):
        """
        Get the count of all modules on the target.
        """
        ctrlHandle = self.getCtrlHandle()
        countSwModules = ctypes.c_ushort(0)
        if(self._pycom.TARGET_GetCountModules(ctrlHandle, ctypes.byref(countSwModules)) != OK):
            raise PyComException(("pyCom Error: Can't get Number of Modules by Controller['"+self._ip+"']"))
        return countSwModules.value
    
    def getSwModuleByName(self, name):
        """
        Get the software module information of the target by name.
        """
        try:
            return self.getListofSwModules()[name]
        except KeyError:
            raise PyComException(("pyCom Error: Module: " + name + " is not present!"))
    
    def getListofSwModules(self):
        """
        Get a list of all software module names of the target 
        """
        countSwModules = self.getNumberofSwModules()
        myModuleNames = MODULE_NAME_ARRAY(countSwModules)
        myModuleList = MODULE_LIST()
        myModuleList.names = myModuleNames.ARRAY
        py_modulelist = {}
        if (self._pycom.TARGET_GetModules(self.getCtrlHandle(), countSwModules, myModuleList) != OK):
            raise PyComException(("pyCom Error: Can't get Software ModuleList from Controller["+self._ip+"]"))
        for num in range(0, countSwModules):
            py_modulelist[myModuleNames.ARRAY[num].name.decode()] = _M1SwModule(myModuleNames.ARRAY[num].name.decode(), self)
        return py_modulelist

    def getDrvId(self, CardNb):
        """
        Get DrvId from CardNb.
        """        
        
        send = MIO_GETDRV_C()
        send.CardNb = CardNb
        recv = MIO_GETDRV_R()
        
        mio = self._pycom.TARGET_CreateModule(self._ctrlHandle, b"MIO")
        self._pycom.MODULE_Connect(mio)
        
        if(self._pycom.MODULE_SendCall(mio, ctypes.c_uint(100), ctypes.c_uint(2), ctypes.pointer(send), ctypes.sizeof(send), ctypes.pointer(recv), ctypes.sizeof(recv), 3000) != OK):
            raise PyComException(("m1com Error: Can't send procedure number 100 to Controller['"+self._ip+"']"))
        
        return recv.DrvId
    
    def getCardInfo(self, CardNb):
        """
        Get card information from CardNb.
        """        
        send = MIO_GETDRV_C()
        send.CardNb = CardNb
        recv = MIO_GETDRV_R() 

        mio = self._pycom.TARGET_CreateModule(self._ctrlHandle, b"MIO")
        self._pycom.MODULE_Connect(mio)

        if(self._pycom.MODULE_SendCall(mio, ctypes.c_uint(100), ctypes.c_uint(2), ctypes.pointer(send), ctypes.sizeof(send), ctypes.pointer(recv), ctypes.sizeof(recv), 3000) != OK):
            raise PyComException(("m1com Error: Can't send procedure number " + mio + " to Controller['"+self._ip+"']"))
        
        send = MIO_GETCDINF_C()
        send.DrvId = recv.DrvId
        recv = MIO_GETCDINF_R()
         
        if(self._pycom.MODULE_SendCall(mio, ctypes.c_uint(130), ctypes.c_uint(2), ctypes.pointer(send), ctypes.sizeof(send), ctypes.pointer(recv), ctypes.sizeof(recv), 3000) != OK):
            raise PyComException(("m1com Error: Can't send procedure number " + mio + " to Controller['"+self._ip+"']"))
      
        return recv
    
    def getCardInfoExt(self, CardNb):
        """
        Get extended card information from CardNb.
        """        
        send = MIO_GETEXTCDINF_C()
        send.CardNb = CardNb
        recv = MIO_GETEXTCDINF_R()

        mio = self._pycom.TARGET_CreateModule(self._ctrlHandle, b"MIO")
        self._pycom.MODULE_Connect(mio)
         
        if(self._pycom.MODULE_SendCall(mio, ctypes.c_uint(136), ctypes.c_uint(2), ctypes.pointer(send), ctypes.sizeof(send), ctypes.pointer(recv), ctypes.sizeof(recv), 3000) != OK):
            raise PyComException(("m1com Error: Can't send procedure number " + mio + " to Controller['"+self._ip+"']"))

        cardInfoExt = {}
        for name in recv.Inf._fields_:
            if type(getattr(recv.Inf, name[0])) == bytes:
                cardInfoExt.update({name[0]:getattr(recv.Inf, name[0]).decode()})
            else:
                cardInfoExt.update({name[0]:getattr(recv.Inf, name[0])})

        return cardInfoExt.copy()

    def getListofHwModules(self):
        """
        Get hardware list from target.
        """
        hwmodulelist = []
        
        send = INF_CARDINFOLST_C()
        send.FirstIdx = 0
        send.LastIdx = 15
        recv = INF_CARDINFOLST_R()
        
        info = self._pycom.TARGET_CreateModule(self.getCtrlHandle(), b"INFO")
        self._pycom.MODULE_Connect(info)

        for _ in range(send.LastIdx):
            if(self._pycom.MODULE_SendCall(info, ctypes.c_uint(120), ctypes.c_uint(2), ctypes.pointer(send), ctypes.sizeof(send), ctypes.pointer(recv), ctypes.sizeof(recv), 3000) != OK):
                raise PyComException(("m1com Error: Can't send procedure number 120 to Controller['"+self._ip+"']"))
            hwmodulelist.append(self.getCardInfoExt(recv.Inf.CardNb))
            send.FirstIdx += 1
            if recv.NbOfObj <= 1:
                break
                
        return hwmodulelist.copy()

    def copyFromTarget(self, remoteFileName, localFileName):
        """
        Copy a file from the target.
        """
        if(self._pycom.RFS_CopyFromTarget(self.getCtrlHandle(), localFileName.encode(), remoteFileName.encode()) != OK):
            raise PyComException(("pyCom Error: Can't get copy " + remoteFileName + " from Controller['"+self._ip+"']"))

    def copyToTarget(self, localFileName, remoteFileName):
        """
        Copy a local file to the target.
        """
        if(self._pycom.RFS_CopyToTarget(self.getCtrlHandle(), remoteFileName.encode(), localFileName.encode()) != OK):
            raise PyComException(("pyCom Error: Can't copy " + localFileName + " to Controller['"+self._ip+"']"))

    def copyRemote(self, srcFile, destFile):
        """
        Copy a file on the target and save it somewhere else on the target.
        """
        if(self._pycom.RFS_CopyRemote(self.getCtrlHandle(), destFile.encode(), srcFile.encode()) != OK):
            raise PyComException(("pyCom Error: Can't copy " + destFile + " to " + srcFile + " on Controller['"+self._ip+"']"))

    def remove(self, remoteFileName):
        """
        Remove a file on the target.
        """
        if(self._pycom.RFS_Remove(self.getCtrlHandle(), remoteFileName.encode()) != OK):
            raise PyComException(("pyCom Error: Can't remove " + remoteFileName + " on Controller['"+self._ip+"']"))
    
    def reboot(self):
        """
        Reboot the target.
        """
        mod = self._pycom.TARGET_CreateModule(self.getCtrlHandle(), b"MOD")        
        self._pycom.MODULE_Connect(mod)
        send = ctypes.c_int32(0)
        recv = ctypes.c_int32(0)        
        if(self._pycom.MODULE_SendCall(mod, ctypes.c_uint(134), ctypes.c_uint(2), ctypes.pointer(send), 4, ctypes.pointer(recv), 4, 3000) != OK):
            raise PyComException(("m1com Error: Can't send procedure number " + mod + " to Controller['"+self._ip+"']"))

    def resetAll(self):
        """
        Reset all applications on the target.
        """
        mod = self._pycom.TARGET_CreateModule(self.getCtrlHandle(), b"MOD")        
        self._pycom.MODULE_Connect(mod)
        send = ctypes.c_int32(0)
        recv = ctypes.c_int32(0)        
        if(self._pycom.MODULE_SendCall(mod, ctypes.c_uint(142), ctypes.c_uint(2), ctypes.pointer(send), 4, ctypes.pointer(recv), 4, 3000) != OK):
            raise PyComException(("m1com Error: Can't reset all models on Controller['"+self._ip+"']"))

    def sendCall(self, moduleName, proc, send, recv, timeout=1000, version=2):
        """
        Send a custom SMI call to the target.
        """
        mod = self._pycom.TARGET_CreateModule(self.getCtrlHandle(), moduleName.encode())        
        self._pycom.MODULE_Connect(mod)
        sendSize = ctypes.c_ushort(ctypes.sizeof(send))
        recvSize = ctypes.c_ushort(ctypes.sizeof(recv))
        returnSendCall = self._pycom.MODULE_SendCall(
            mod, 
            ctypes.c_uint(proc), 
            ctypes.c_uint(version), 
            ctypes.pointer(send), 
            sendSize, 
            ctypes.pointer(recv), 
            recvSize, 
            ctypes.c_uint(timeout) )
        if(returnSendCall != OK):
            raise PyComException(("pyCom Error: Can't send procedure number " + str(proc) + " to Controller['"+self._ip+"']"))
        return recv

class M1SVIObserver:
    """
    SVI Observer to monitor/read multiple SVI variables at the same time. This method is preferred above the M1SVIReader method
    since it only communicates variables that were changed during a call. If you also want the values of variables that did not
    change, you can call M1SVIObserver.getVariables(updatedOnly=False). This still returns all variables, also the variables that 
    did not change, but is also faster than using the M1SVIReader method.

    Usage:

    >>> mh = M1Controller(ip='169.254.141.136')
    >>> mh.connect(timeout=3000)
    >>> sviObserver = M1SVIObserver(['RES/Time_s', 'RES/Time_us', 'RES/Version'], mh)
    >>> sviObserver.getVariables()                                                                  # doctest: +SKIP
    >>> sviObserver.detach()
    >>> mh.disconnect()
    0
    """

    def __init__(self, sviNames, m1controller):
        if type(sviNames) != list:
            raise PyComException(("pyCom Error: Expected a list of svi names for argument 'sviNames'!"))
        self.sviNames = sviNames
        self.m1ctrl = m1controller
        self._obsHandle = None
        self._sviHandles = None
        self._sviInfos = None
        self._sviBuffers = None
        self._sviValues = None
        self._sviTypes = None
        self._indicesChanged = None
        self._countVariables = len(sviNames)
        self.attach()
    
    def detach(self):
        """
        Disposes the observation list.
        """
        self.m1ctrl._pycom.OBSLIST_Dispose(self._obsHandle)
        self._obsHandle = None
        self._sviHandles = None
        self._sviInfos = None
        self._sviBuffers = None
        self._sviValues = None
        self._sviTypes = None
        self._indicesChanged = None

    def getObsHandle(self):
        """
        Get observer handle from target.
        """
        if(self._obsHandle == None):
            raise PyComException(("pyCom Error: Can't get observer handle for Controller["+self.m1ctrl._ip+"] when not attached!"))
        return self._obsHandle

    def attach(self):
        """
        Creates an observation list. For all variables vhd lists are allocated on the controller.
        """

        # Get the SVI variable handles
        self._sviHandles = []
        for sviName in self.sviNames:
            sviHandle = self.m1ctrl._pycom.TARGET_CreateVariable(self.m1ctrl.getCtrlHandle(), sviName.encode())
            if(sviHandle == None):
                raise PyComException(("pyCom Error: Can't allocate SviVariable["+sviName+"] on Controller["+self.m1ctrl._ip+"]"))
            self._sviHandles.append(sviHandle)

        # Initialize the SVI variables
        if self.m1ctrl._pycom.getDllBits() == '64bit':
            sviHandlesArray = (ctypes.c_uint64 * len(self._sviHandles))(*self._sviHandles)
        else:
            sviHandlesArray = (ctypes.c_uint32 * len(self._sviHandles))(*self._sviHandles)
        countInited = self.m1ctrl._pycom.TARGET_InitVariables(self.m1ctrl.getCtrlHandle(), sviHandlesArray, len(self._sviHandles))
        if(countInited <= 0):
            raise PyComException("pyCom Error: Invalid handle, offline or Network error!")
        if(countInited != self._countVariables):
            raise PyComException("pyCom Error: At least one variable not found on target!")

        # Get information about the SVI variables
        self._sviInfos = []
        for i in range(len(self._sviHandles)):
            self._sviInfos.append(VARIABLE_INFO())
            if(self.m1ctrl._pycom.VARIABLE_GetInfo(self._sviHandles[i], ctypes.pointer(self._sviInfos[i])) != OK):
                raise PyComException("pyCom Error: Can't update Informations of SviVariable["+self.sviNames[i]+"] on Controller["+self.m1ctrl._ip+"]")

        # Allocate the SVI buffers
        self._sviBuffers = VARIABLE_BUFFER_ARRAY(self._countVariables)
        self._sviValues = []
        self._sviTypes = []
        for i in range(self._countVariables):
            self._sviBuffers.ARRAY[i].varHandle = self._sviHandles[i]
            self._sviBuffers.ARRAY[i].bufferLen = self.m1ctrl._pycom.VARIABLE_GetBufferLen(ctypes.pointer(self._sviInfos[i]))

            identifiyer = self._sviInfos[i].format & 0x0f
            if not(self._sviInfos[i].format & SVI_F_OUT):
                raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] is not read able!")
            if(self._sviInfos[i].format & SVI_F_BLK):
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append((ctypes.c_char * self._sviBuffers.ARRAY[i].bufferLen)()) #allocate buffer
                    self._sviTypes.append(str)
                elif (identifiyer == SVI_F_CHAR16):
                    self._sviValues.append((ctypes.c_wchar * self._sviBuffers.ARRAY[i].bufferLen)()) #allocate buffer
                    self._sviTypes.append(str)
                elif(identifiyer == SVI_F_UINT64):
                    self._sviValues.append(ctypes.c_ulonglong())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT64):
                    self._sviValues.append(ctypes.c_longlong())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_REAL64):
                    self._sviValues.append(ctypes.c_double())
                    self._sviTypes.append(float)
                elif(self._sviInfos[i].format & SVI_F_STRINGLSTBASE):
                    raise PyComTypeException("ByteAccess of String array not implemented!")
                elif(self._sviInfos[i].format & SVI_F_USTRINGLSTBASE):
                    raise PyComTypeException("ByteAccess of UNICODED String array not implemented!")
                elif(identifiyer == SVI_F_MIXED):
                    raise PyComTypeException("ByteAccess of SVI_F_MIXED not implemented!")
                elif(identifiyer == SVI_F_UINT1):
                    raise PyComTypeException("ByteAccess of UINT1 not implemented!")
                elif(identifiyer == SVI_F_UINT8):
                    raise PyComTypeException("ByteAccess of UINT8 not implemented!")
                elif(identifiyer == SVI_F_BOOL8):
                    raise PyComTypeException("ByteAccess of BOOL8 not implemented!")
                elif(identifiyer == SVI_F_UINT16):
                    raise PyComTypeException("ByteAccess of UINT16 not implemented!")
                elif(identifiyer == SVI_F_UINT32):
                    raise PyComTypeException("ByteAccess of UINT32 not implemented!")
                elif(identifiyer == SVI_F_SINT8):
                    raise PyComTypeException("ByteAccess of SINT8 not implemented!")
                elif(identifiyer == SVI_F_SINT16):
                    raise PyComTypeException("ByteAccess of SINT16 not implemented!")
                elif(identifiyer == SVI_F_SINT32):
                    raise PyComTypeException("ByteAccess of SINT32 not implemented!")
                elif(identifiyer == SVI_F_REAL32):
                    raise PyComTypeException("ByteAccess of REAL32 not implemented!")
                else:
                    raise PyComException("pyCom Error: unknown SVIBLK Type!"+str(self._sviInfos[i].format)+" of Variable:"+self.sviNames[i])
            else:
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append('char8')
                elif(identifiyer == SVI_F_CHAR16):
                    self._sviValues.append(ctypes.c_ushort())
                    self._sviTypes.append('char16')
                elif(identifiyer == SVI_F_UINT1):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append(bool)
                elif(identifiyer == SVI_F_UINT8):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_BOOL8):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append(bool)
                elif(identifiyer == SVI_F_UINT16):
                    self._sviValues.append(ctypes.c_ushort())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_UINT32):
                    self._sviValues.append(ctypes.c_uint())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT8):
                    self._sviValues.append(ctypes.c_byte())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT8):
                    self._sviValues.append(ctypes.c_byte())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT16):
                    self._sviValues.append(ctypes.c_short())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT32):
                    self._sviValues.append(ctypes.c_long())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_REAL32):
                    self._sviValues.append(ctypes.c_float())
                    self._sviTypes.append(float)
                else:
                    raise PyComException("pyCom Error: unknown SVI Type!"+str(self._sviInfos[i].format)+" of Variable:"+self.sviNames[i])
            self._sviBuffers.ARRAY[i].buffer = ctypes.cast(ctypes.pointer(self._sviValues[i]), ctypes.c_char_p)

        # Create the observation list
        self._obsHandle = self.m1ctrl._pycom.TARGET_CreateObservationList(self.m1ctrl.getCtrlHandle(), self._sviBuffers.ARRAY, self._countVariables)
        if(self._obsHandle == None):
            raise PyComException(("pyCom Error: Can't create observation list on Controller["+self.m1ctrl._ip+"]"))

        self._indicesChanged = (ctypes.c_long * self._countVariables)()

    def update(self):
        """
        The first call of this function will update all values of the contained variables. Subsequent calls will only update 
        changed variables.
        """
        countChangedVariables = self.m1ctrl._pycom.OBSLIST_Update(self._obsHandle, self._indicesChanged, self._countVariables)
        if(countChangedVariables < 0):
            raise PyComException(("pyCom Error: Can't update the observation list on Controller["+self.m1ctrl._ip+"]"))

        return countChangedVariables

    def getVariables(self, updatedOnly=True):
        """
        Gets the updated variables from the controller. This function already calls M1SVIObserver.update() to make sure the
        newest values are inside the observer buffer. By default, only the changed variables are returned. If all variables
        should be returned, the 'updatedOnly' argument of this method can be set to False.
        """

        countChangedVariables = self.update()

        variables = {}

        value = None
        if updatedOnly:
            for i in range(countChangedVariables):
                if self._sviValues[self._indicesChanged[i]].value == None:
                    value = self._sviValues[self._indicesChanged[i]]
                else:
                    value = self._sviValues[self._indicesChanged[i]].value

                if type(value) == bytes:
                    value = self._sviTypes[self._indicesChanged[i]](value.decode())
                elif self._sviTypes[self._indicesChanged[i]] == 'char8':
                    value = ((value).to_bytes(1, byteorder='big')).decode('utf-8')
                elif self._sviTypes[self._indicesChanged[i]] == 'char16':
                    value = ((value).to_bytes(1, byteorder='big')).decode('utf-8')
                else:
                    value = self._sviTypes[self._indicesChanged[i]](value)
                variables.update({self.sviNames[self._indicesChanged[i]]:value})
        else:
            for i in range(self._countVariables):
                if self._sviValues[i].value == None:
                    value = self._sviValues[i]
                else:
                    value = self._sviValues[i].value

                if type(value) == bytes:
                    value = self._sviTypes[i](value.decode())
                elif self._sviTypes[i] == 'char8':
                    value = ((value).to_bytes(1, byteorder='big')).decode('utf-8')
                elif self._sviTypes[i] == 'char16':
                    value = ((value).to_bytes(1, byteorder='big')).decode('utf-8')
                else:
                    value = self._sviTypes[i](value)
                variables.update({self.sviNames[i]:value})

        return variables

    def reset(self):
        """
        Resets the observation list. All allocated vhd lists associated with this observation list on the controller will 
        be resetted. The next call to M1SVIObserver.update() will update all values of the contained variables. 
        """
        if(self.m1ctrl._pycom.OBSLIST_Reset(self._obsHandle) != OK):
            raise PyComException(("pyCom Error: Can't reset the observation list on Controller["+self.m1ctrl._ip+"]"))

class M1SVIReader:
    """
    SVI Reader to read multiple SVI variables at the same time (not recommended since the M1SVIObserver is faster and
    has the same functionality).

    Usage:

    >>> mh = M1Controller(ip='169.254.141.136')
    >>> mh.connect(timeout=3000)
    >>> sviReader = M1SVIReader(['SVIWRITE/boolVar', 'SVIWRITE/real64Var', 'SVIWRITE/stringVar'], mh)       # doctest: +SKIP
    >>> sviReader.getVariables()                                                                            # doctest: +SKIP
    [True, 1.0, "Hello"]
    >>> sviReader.detach()                                                                                  # doctest: +SKIP
    >>> mh.disconnect()
    0
    """

    def __init__(self, sviNames, m1controller):
        if type(sviNames) != list:
            raise PyComException(("pyCom Error: Expected a list of svi names for argument 'sviNames'!"))
        self.sviNames = sviNames
        self.m1ctrl = m1controller
        self._sviHandles = None
        self._sviInfos = None
        self._sviBuffers = None
        self._sviValues = None
        self._countVariables = len(sviNames)
        self.attach()

    def detach(self):
        """
        Disposes all SVI variables and resets the internal buffers.
        """
        for sviHandle in self._sviHandles:
            self.m1ctrl._pycom.VARIABLE_Dispose(sviHandle)
        self._sviHandles = None
        self._sviInfos = None
        self._sviBuffers = None
        self._sviValues = None
        self._sviTypes = None

    def getSVIHandles(self):
        """
        Get the SVI variable handles from the target.
        """
        if(self._sviHandles == None):
            raise PyComException(("pyCom Error: Can't get SVI variable handles for Controller["+self.m1ctrl._ip+"] when not attached!"))
        return self._sviHandles

    def attach(self):
        """
        Allocates buffers for the to be read SVI variables. This function is already automatically called during the initialization 
        and should therefore only be called if 'M1SVIReader.detach()' was called.
        """

        # Get the SVI variable handles
        self._sviHandles = []
        for sviName in self.sviNames:
            sviHandle = self.m1ctrl._pycom.TARGET_CreateVariable(self.m1ctrl.getCtrlHandle(), sviName.encode())
            if(sviHandle == None):
                raise PyComException(("pyCom Error: Can't allocate SviVariable["+sviName+"] on Controller["+self.m1ctrl._ip+"]"))
            self._sviHandles.append(sviHandle)

        # Initialize the SVI variables
        if self.m1ctrl._pycom.getDllBits() == '64bit':
            sviHandlesArray = (ctypes.c_uint64 * len(self._sviHandles))(*self._sviHandles)
        else:
            sviHandlesArray = (ctypes.c_uint32 * len(self._sviHandles))(*self._sviHandles)
        countInited = self.m1ctrl._pycom.TARGET_InitVariables(self.m1ctrl.getCtrlHandle(), sviHandlesArray, len(self._sviHandles))
        if(countInited <= 0):
            raise PyComException("pyCom Error: Invalid handle, offline or Network error!")
        if(countInited != self._countVariables):
            raise PyComException("pyCom Error: At least one variable not found on target!")

        # Get information about the SVI variables
        self._sviInfos = []
        for i in range(len(self._sviHandles)):
            self._sviInfos.append(VARIABLE_INFO())
            if(self.m1ctrl._pycom.VARIABLE_GetInfo(self._sviHandles[i], ctypes.pointer(self._sviInfos[i])) != OK):
                raise PyComException("pyCom Error: Can't update Informations of SVI Variable["+self.sviNames[i]+"] on Controller["+self.m1ctrl._ip+"]")

        # Allocate the SVI buffers
        self._sviBuffers = VARIABLE_BUFFER_ARRAY(self._countVariables)
        self._sviValues = []
        self._sviTypes = []
        for i in range(self._countVariables):
            self._sviBuffers.ARRAY[i].varHandle = self._sviHandles[i]
            self._sviBuffers.ARRAY[i].bufferLen = self.m1ctrl._pycom.VARIABLE_GetBufferLen(ctypes.pointer(self._sviInfos[i]))

            identifiyer = self._sviInfos[i].format & 0x0f
            if not(self._sviInfos[i].format & SVI_F_OUT):
                raise PyComException("pyCom Error: SVI Variable["+self.sviNames[i]+"] is not read able!")
            if(self._sviInfos[i].format & SVI_F_BLK):
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append((ctypes.c_char * self._sviBuffers.ARRAY[i].bufferLen)()) #allocate buffer
                    self._sviTypes.append(str)
                elif (identifiyer == SVI_F_CHAR16):
                    self._sviValues.append((ctypes.c_wchar * self._sviBuffers.ARRAY[i].bufferLen)()) #allocate buffer
                    self._sviTypes.append(str)
                elif(identifiyer == SVI_F_UINT64):
                    self._sviValues.append(ctypes.c_ulonglong())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT64):
                    self._sviValues.append(ctypes.c_longlong())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_REAL64):
                    self._sviValues.append(ctypes.c_double())
                    self._sviTypes.append(float)
                elif(self._sviInfos[i].format & SVI_F_STRINGLSTBASE):
                    raise PyComTypeException("ByteAccess of String array not implemented!")
                elif(self._sviInfos[i].format & SVI_F_USTRINGLSTBASE):
                    raise PyComTypeException("ByteAccess of UNICODED String array not implemented!")
                elif(identifiyer == SVI_F_MIXED):
                    raise PyComTypeException("ByteAccess of SVI_F_MIXED not implemented!")
                elif(identifiyer == SVI_F_UINT1):
                    raise PyComTypeException("ByteAccess of UINT1 not implemented!")
                elif(identifiyer == SVI_F_UINT8):
                    raise PyComTypeException("ByteAccess of UINT8 not implemented!")
                elif(identifiyer == SVI_F_BOOL8):
                    raise PyComTypeException("ByteAccess of BOOL8 not implemented!")
                elif(identifiyer == SVI_F_UINT16):
                    raise PyComTypeException("ByteAccess of UINT16 not implemented!")
                elif(identifiyer == SVI_F_UINT32):
                    raise PyComTypeException("ByteAccess of UINT32 not implemented!")
                elif(identifiyer == SVI_F_SINT8):
                    raise PyComTypeException("ByteAccess of SINT8 not implemented!")
                elif(identifiyer == SVI_F_SINT16):
                    raise PyComTypeException("ByteAccess of SINT16 not implemented!")
                elif(identifiyer == SVI_F_SINT32):
                    raise PyComTypeException("ByteAccess of SINT32 not implemented!")
                elif(identifiyer == SVI_F_REAL32):
                    raise PyComTypeException("ByteAccess of REAL32 not implemented!")
                else:
                    raise PyComException("pyCom Error: unknown SVIBLK Type!"+str(self._sviInfos[i].format)+" of Variable:"+self.sviNames[i])
            else:
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append('char8')
                elif(identifiyer == SVI_F_CHAR16):
                    self._sviValues.append(ctypes.c_ushort())
                    self._sviTypes.append('char16')
                elif(identifiyer == SVI_F_UINT1):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append(bool)
                elif(identifiyer == SVI_F_UINT8):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_BOOL8):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append(bool)
                elif(identifiyer == SVI_F_UINT16):
                    self._sviValues.append(ctypes.c_ushort())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_UINT32):
                    self._sviValues.append(ctypes.c_uint())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT8):
                    self._sviValues.append(ctypes.c_byte())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT8):
                    self._sviValues.append(ctypes.c_byte())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT16):
                    self._sviValues.append(ctypes.c_short())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT32):
                    self._sviValues.append(ctypes.c_long())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_REAL32):
                    self._sviValues.append(ctypes.c_float())
                    self._sviTypes.append(float)
                else:
                    raise PyComException("pyCom Error: unknown SVI Type!"+str(self._sviInfos[i].format)+" of Variable:"+self.sviNames[i])
            self._sviBuffers.ARRAY[i].buffer = ctypes.cast(ctypes.byref(self._sviValues[i]), ctypes.c_char_p)

    def getVariables(self):
        """
        Gets the SVI values of the controller.
        """
        if self.m1ctrl._pycom.TARGET_ReadVariables(self.m1ctrl.getCtrlHandle(), self._sviBuffers.ARRAY, self._countVariables) < 0:
            raise PyComException("pyCom Error: could not read SVI Variables:")

        sviValues = []
        for i in range(self._countVariables):
            if self._sviValues[i].value == None:
                if type(self._sviValues[i]) == bytes:
                    sviValues.append(self._sviTypes[i](self._sviValues[i].decode()))
                elif self._sviTypes[i] == 'char8':
                    sviValues.append(((self._sviValues[i]).to_bytes(1, byteorder='big')).decode('utf-8'))
                elif self._sviTypes[i] == 'char16':
                    sviValues.append(((self._sviValues[i]).to_bytes(1, byteorder='big')).decode('utf-8'))
                else:
                    sviValues.append(self._sviTypes[i](self._sviValues[i]))
            else:
                if type(self._sviValues[i].value) == bytes:
                    sviValues.append(self._sviTypes[i](self._sviValues[i].value.decode()))
                elif self._sviTypes[i] == 'char8':
                    sviValues.append(((self._sviValues[i].value).to_bytes(1, byteorder='big')).decode('utf-8'))
                elif self._sviTypes[i] == 'char16':
                    sviValues.append(((self._sviValues[i].value).to_bytes(1, byteorder='big')).decode('utf-8'))
                else:
                    sviValues.append(self._sviTypes[i](self._sviValues[i].value))

        return sviValues

class M1SVIWriter:
    """
    SVI Writer to write to multiple SVI variables at the same time.

    Usage:

    >>> mh = M1Controller(ip='169.254.141.136')
    >>> mh.connect(timeout=3000)
    >>> sviWriter = M1SVIWriter(['SVIWRITE/boolVar', 'SVIWRITE/real64Var', 'SVIWRITE/stringVar'], mh)       # doctest: +SKIP
    >>> sviWriter.setVariables([True, 1.0, "Hello"])                                                        # doctest: +SKIP
    >>> sviWriter.detach()                                                                                  # doctest: +SKIP
    >>> mh.disconnect()
    0
    """

    def __init__(self, sviNames, m1controller):
        if type(sviNames) != list:
            raise PyComException(("pyCom Error: Expected a list of svi names for argument 'sviNames'!"))
        self.sviNames = sviNames
        self.m1ctrl = m1controller
        self._sviHandles = None
        self._sviInfos = None
        self._sviBuffers = None
        self._sviValues = None
        self._countVariables = len(sviNames)
        self.attach()

    def detach(self):
        """
        Disposes all SVI variables and resets the internal buffers.
        """
        for sviHandle in self._sviHandles:
            self.m1ctrl._pycom.VARIABLE_Dispose(sviHandle)
        self._sviHandles = None
        self._sviInfos = None
        self._sviBuffers = None
        self._sviValues = None
        self._sviTypes = None

    def getSVIHandles(self):
        """
        Get the SVI variable handles from the target.
        """
        if(self._sviHandles == None):
            raise PyComException(("pyCom Error: Can't get SVI variable handles for Controller["+self.m1ctrl._ip+"] when not attached!"))
        return self._sviHandles

    def attach(self):
        """
        Allocates buffers for the to be written SVI variables. This function is already automatically called during the initialization 
        and should therefore only be called if 'M1SVIWriter.detach()' was called.
        """

        # Get the SVI variable handles
        self._sviHandles = []
        for sviName in self.sviNames:
            sviHandle = self.m1ctrl._pycom.TARGET_CreateVariable(self.m1ctrl.getCtrlHandle(), sviName.encode())
            if(sviHandle == None):
                raise PyComException(("pyCom Error: Can't allocate SviVariable["+sviName+"] on Controller["+self.m1ctrl._ip+"]"))
            self._sviHandles.append(sviHandle)

        # Initialize the SVI variables
        if self.m1ctrl._pycom.getDllBits() == '64bit':
            sviHandlesArray = (ctypes.c_uint64 * len(self._sviHandles))(*self._sviHandles)
        else:
            sviHandlesArray = (ctypes.c_uint32 * len(self._sviHandles))(*self._sviHandles)
        countInited = self.m1ctrl._pycom.TARGET_InitVariables(self.m1ctrl.getCtrlHandle(), sviHandlesArray, len(self._sviHandles))
        if(countInited <= 0):
            raise PyComException("pyCom Error: Invalid handle, offline or Network error!")
        if(countInited != self._countVariables):
            raise PyComException("pyCom Error: At least one variable not found on target!")

        # Get information about the SVI variables
        self._sviInfos = []
        for i in range(len(self._sviHandles)):
            self._sviInfos.append(VARIABLE_INFO())
            if(self.m1ctrl._pycom.VARIABLE_GetInfo(self._sviHandles[i], ctypes.pointer(self._sviInfos[i])) != OK):
                raise PyComException("pyCom Error: Can't update Informations of SVI Variable["+self.sviNames[i]+"] on Controller["+self.m1ctrl._ip+"]")

        # Allocate the SVI buffers
        self._sviBuffers = VARIABLE_BUFFER_ARRAY(self._countVariables)
        self._sviValues = []
        self._sviTypes = []
        for i in range(self._countVariables):
            self._sviBuffers.ARRAY[i].varHandle = self._sviHandles[i]
            self._sviBuffers.ARRAY[i].bufferLen = self.m1ctrl._pycom.VARIABLE_GetBufferLen(ctypes.pointer(self._sviInfos[i]))

            identifiyer = self._sviInfos[i].format & 0x0f
            if not(self._sviInfos[i].format & SVI_F_IN):
                raise PyComException("pyCom Error: SVI Variable["+self.sviNames[i]+"] is not write able!")
            if(self._sviInfos[i].format & SVI_F_BLK):
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append((ctypes.c_char * self._sviBuffers.ARRAY[i].bufferLen)()) #allocate buffer
                    self._sviTypes.append(str)
                elif (identifiyer == SVI_F_CHAR16):
                    self._sviValues.append((ctypes.c_wchar * self._sviBuffers.ARRAY[i].bufferLen)()) #allocate buffer
                    self._sviTypes.append(str)
                elif(identifiyer == SVI_F_UINT64):
                    self._sviValues.append(ctypes.c_ulonglong())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT64):
                    self._sviValues.append(ctypes.c_longlong())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_REAL64):
                    self._sviValues.append(ctypes.c_double())
                    self._sviTypes.append(float)
                elif(self._sviInfos[i].format & SVI_F_STRINGLSTBASE):
                    raise PyComTypeException("ByteAccess of String array not implemented!")
                elif(self._sviInfos[i].format & SVI_F_USTRINGLSTBASE):
                    raise PyComTypeException("ByteAccess of UNICODED String array not implemented!")
                elif(identifiyer == SVI_F_MIXED):
                    raise PyComTypeException("ByteAccess of SVI_F_MIXED not implemented!")
                elif(identifiyer == SVI_F_UINT1):
                    raise PyComTypeException("ByteAccess of UINT1 not implemented!")
                elif(identifiyer == SVI_F_UINT8):
                    raise PyComTypeException("ByteAccess of UINT8 not implemented!")
                elif(identifiyer == SVI_F_BOOL8):
                    raise PyComTypeException("ByteAccess of BOOL8 not implemented!")
                elif(identifiyer == SVI_F_UINT16):
                    raise PyComTypeException("ByteAccess of UINT16 not implemented!")
                elif(identifiyer == SVI_F_UINT32):
                    raise PyComTypeException("ByteAccess of UINT32 not implemented!")
                elif(identifiyer == SVI_F_SINT8):
                    raise PyComTypeException("ByteAccess of SINT8 not implemented!")
                elif(identifiyer == SVI_F_SINT16):
                    raise PyComTypeException("ByteAccess of SINT16 not implemented!")
                elif(identifiyer == SVI_F_SINT32):
                    raise PyComTypeException("ByteAccess of SINT32 not implemented!")
                elif(identifiyer == SVI_F_REAL32):
                    raise PyComTypeException("ByteAccess of REAL32 not implemented!")
                else:
                    raise PyComException("pyCom Error: unknown SVIBLK Type!"+str(self._sviInfos[i].format)+" of Variable:"+self.sviNames[i])
            else:
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append('char8')
                elif(identifiyer == SVI_F_CHAR16):
                    self._sviValues.append(ctypes.c_ushort())
                    self._sviTypes.append('char16')
                elif(identifiyer == SVI_F_UINT1):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append(bool)
                elif(identifiyer == SVI_F_UINT8):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_BOOL8):
                    self._sviValues.append(ctypes.c_ubyte())
                    self._sviTypes.append(bool)
                elif(identifiyer == SVI_F_UINT16):
                    self._sviValues.append(ctypes.c_ushort())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_UINT32):
                    self._sviValues.append(ctypes.c_uint())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT8):
                    self._sviValues.append(ctypes.c_byte())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT8):
                    self._sviValues.append(ctypes.c_byte())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT16):
                    self._sviValues.append(ctypes.c_short())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT32):
                    self._sviValues.append(ctypes.c_long())
                    self._sviTypes.append(int)
                elif(identifiyer == SVI_F_REAL32):
                    self._sviValues.append(ctypes.c_float())
                    self._sviTypes.append(float)
                else:
                    raise PyComException("pyCom Error: unknown SVI Type!"+str(self._sviInfos[i].format)+" of Variable:"+self.sviNames[i])
            self._sviBuffers.ARRAY[i].buffer = ctypes.cast(ctypes.byref(self._sviValues[i]), ctypes.c_char_p)

    def setVariables(self, sviValues):
        """
        Sets the SVI variables on the controller.
        """
        if type(sviValues) != list:
            raise PyComException("pyCom Error: 'sviValues' should be of type 'list'!")
        if len(sviValues) != self._countVariables:
            raise PyComException("pyCom Error: length of 'sviValues' should be equal to "+str(self._countVariables)+"!")

        for i in range(self._countVariables):
            if (self._sviTypes[i] == 'char8' and len(sviValues[i]) > 1) or (self._sviTypes[i] == 'char8' and type(sviValues[i]) != str):
                raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'str' with a maximum length of 1")
            elif (self._sviTypes[i] == 'char16' and len(sviValues[i]) > 1) or (self._sviTypes[i] == 'char16' and type(sviValues[i]) != str):
                raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'str' with a maximum length of 1")
            elif type(sviValues[i]) != self._sviTypes[i] and self._sviTypes[i] != 'char8' and self._sviTypes[i] != 'char16':
                raise PyComException("pyCom Error: expects sviValues["+str(i)+"] ("+self.sviNames[i]+") to be of type "+str(self._sviTypes[i])+"!")

            if self._sviValues[i].value == None:
                if self._sviTypes[i] == 'char8':
                    self._sviValues[i] = int.from_bytes(sviValues[i].encode('utf-8'), byteorder='big', signed=False)
                elif self._sviTypes[i] == 'char16':
                    self._sviValues[i] = int.from_bytes(sviValues[i].encode('utf-8'), byteorder='big', signed=False)
                elif self._sviTypes[i] == str:
                    self._sviValues[i] = sviValues[i].encode('utf-8')
                else:
                    self._sviValues[i] = sviValues[i]
            else:
                if self._sviTypes[i] == 'char8':
                    self._sviValues[i].value = int.from_bytes(sviValues[i].encode('utf-8'), byteorder='big', signed=False)
                elif self._sviTypes[i] == 'char16':
                    self._sviValues[i].value = int.from_bytes(sviValues[i].encode('utf-8'), byteorder='big', signed=False)
                elif self._sviTypes[i] == str:
                    self._sviValues[i].value = sviValues[i].encode('utf-8')
                else:
                    self._sviValues[i].value = sviValues[i]

        if self.m1ctrl._pycom.TARGET_WriteVariables(self.m1ctrl.getCtrlHandle(), self._sviBuffers.ARRAY, self._countVariables) < 0:
            raise PyComException("pyCom Error: could not write SVI Variables:")

class M1TargetFinder:
    """
    Look for targets on the network and return their information.
    Usage:

    >>> mt = M1TargetFinder()                                                                   # doctest: +SKIP
    >>> mt.TargetBroadcastSmiPing(timeout=3000)                                                 # doctest: +SKIP
    >>> mt.TargetSmiPing(ip='169.254.141.136', timeout=3000)                                    # doctest: +SKIP
    """

    def __init__(self, pycom=PyCom(), maxdevices=50):
        self._pycom = pycom
        self._maxdevices = maxdevices
        self._targets = {}
    
    def TargetBroadcastSmiPing(self, timeout=1000):
        """
        Look for targets on the network and return their information.
        """
        targetsInfo = (TARGET_INFO * self._maxdevices)()
        founddevices = self._pycom.TARGET_BroadcastSmiPing(timeout, targetsInfo, self._maxdevices)

        for dev in range(founddevices):
            targetInfo = {}
            targetinfoitems = [keyword for keyword in dir(targetsInfo[dev]) if not keyword.startswith('_')]        
            for targetinfoitem in targetinfoitems:
                if targetinfoitem == 'extPingR':
                    pingInfo = {}
                    keywords = [keyword for keyword in dir(targetsInfo[dev].extPingR) if not keyword.startswith('_')]
                    for keyword in keywords:
                        if type(getattr(targetsInfo[dev].extPingR, keyword)) == bytes:
                            pingInfo[keyword] = getattr(targetsInfo[dev].extPingR, keyword).decode()                        
                        else:    
                            pingInfo[keyword] = getattr(targetsInfo[dev].extPingR, keyword)
                    targetInfo['extPingR'] = pingInfo
                else:
                    if type(getattr(targetsInfo[dev], targetinfoitem)) == bytes:
                        targetInfo[targetinfoitem] = getattr(targetsInfo[dev], targetinfoitem).decode()
                    else:
                        targetInfo[targetinfoitem] = getattr(targetsInfo[dev], targetinfoitem)
            self._targets[targetsInfo[dev].extPingR.ProdNb.decode()] = targetInfo
                    
        return self._targets.copy()

    def TargetSmiPing(self, ip='169.254.141.136', timeout=3000, protocol=PROTOCOL_TCP):
        """
        Ping target and return infomation about the target.
        """
        buffer = RES_EXTPING_R()
        pingInfo = {}
        keywords = [keyword for keyword in dir(buffer) if not keyword.startswith('_')]

        self._pycom.TARGET_SmiPing(ip.encode('utf-8'), timeout, protocol, buffer)

        for keyword in keywords:
            if type(getattr(buffer, keyword)) == bytes:
                pingInfo[keyword] = getattr(buffer, keyword).decode()                        
            else:    
                pingInfo[keyword] = getattr(buffer, keyword)
        self._smitargetsInfo = pingInfo

        return self._smitargetsInfo.copy()

class _M1SwModule:
    """
    The _M1SwModule class.

    Usage:

    >>> mh = M1Controller(ip='169.254.141.136')
    >>> mh.connect(timeout=3000)
    >>> swModule = _M1SwModule('RES', mh)
    >>> swModule.getModHandle()                                                                 # doctest: +SKIP
    >>> swModule.getNumberofSviVariables()                                                      # doctest: +SKIP
    371
    >>> swModule.getListofSviVariables()                                                        # doctest: +SKIP
    >>> mh.disconnect()
    0
    """

    def __init__(self, name, m1controller):
        self.name = name
        self.m1ctrl = m1controller
        self._modHandle = None
        self.attach()

    def detach(self):
        """
        Performs cleanup of the software module.
        Note: RES module can not be disposed with this function.
        The handle is no longer valid after calling this function.
        If other threads use the module the caller has to stop them before disposing the module!
        """
        self.m1ctrl._pycom.MODULE_Dispose(self._modHandle)
        self._modHandle = None

    def getModHandle(self):
        """
        Get module handle from target.
        """
        if(self._modHandle == None):
            raise PyComException(("pyCom Error: Can't access Module["+self.name+"] on Controller["+self.m1ctrl._ip+"] when not attached!"))
        return self._modHandle

    def attach(self):
        """
        Creates a handle to a software module. This function is already automatically called after initializing a software module.
        """
        self._modHandle = self.m1ctrl._pycom.TARGET_CreateModule(self.m1ctrl.getCtrlHandle(), self.name.encode())
        if(self.m1ctrl._pycom.MODULE_Connect(self._modHandle) != OK):
            raise PyComException(("pyCom Error: Can't attach to SwModule:"+self.name+" on Controller["+self.m1ctrl._ip+"]"))

    def getNumberofSviVariables(self):
        """
        Get the count of variables of the software module.
        """
        varcount = ctypes.c_uint(0)
        if (self.m1ctrl._pycom.MODULE_GetCountVariables(self.getModHandle(), ctypes.byref(varcount)) != OK):
            raise PyComException(("pyCom Error: Can't get number of svi Variables of SwModule:"+self.name+" on Controller["+self.m1ctrl._ip+"]"))
        return varcount.value

    def getListofSviVariables(self):
        """
        Get a list (in dictonary format) of all variables of the software module.
        """
        nbsvivars = self.getNumberofSviVariables()
        myVarEntrys = VARIABLE_INFO_ARRAY(nbsvivars)
        myVarList = VARIABLE_INFO_LIST()
        myVarList.varInfo = myVarEntrys.ARRAY
        py_svivarlist = {}
        if(self.m1ctrl._pycom.MODULE_GetVariables(self.getModHandle(), nbsvivars, myVarList) != OK):
            raise PyComException(("pyCom Error: Can't get SviVariable List from Module["+self.name+"] on Controller["+self.m1ctrl._ip+"]"))
        for num in range(0, nbsvivars):
            py_svivarlist[myVarEntrys.ARRAY[num].name.decode()] = _SVIVariable(myVarEntrys.ARRAY[num].name.decode(), self)
        return py_svivarlist

class _SVIVariable:
    """
    The _SVIVariable class.

    Usage:

    >>> mh = M1Controller(ip='169.254.141.136')
    >>> mh.connect(timeout=3000)
    >>> swModule = _M1SwModule('RES', mh)
    >>> sviVariable = _SVIVariable('RES/CPU/TempCelsius', swModule)
    >>> sviVariable.getVarHandle()                                                              # doctest: +SKIP
    >>> sviVariable.getVarInfo()                                                                # doctest: +SKIP
    >>> sviVariable.updateVarInfo()                                                             # doctest: +SKIP
    >>> sviVariable.read()                                                                      # doctest: +SKIP
    40
    >>> sviVariable.write(22)                                                                   # doctest: +SKIP
    >>> sviVariable.getConnectionState()
    0
    >>> sviVariable.detach()
    >>> mh.disconnect()
    0
    """
    def __init__(self, name, module):
        self.name = name
        self._m1ctrl = module.m1ctrl
        self._module = module
        self._varHandle = None
        self._varInfo = None
        self._bufferLen = None
        self.attach()

    def detach(self):
        """
        Disposes the variable handle.
        """
        self._m1ctrl._pycom.VARIABLE_Dispose(self._varHandle)
        self._varHandle = None
        self._varInfo = None
        self._bufferLen = None

    def getVarHandle(self):
        """
        Get the variable handle from target.
        """
        if(self._varHandle == None):
            raise PyComException(("pyCom Error: Can't access SviVariable["+self.name+"] of Module["+self._module.name+"] on Controller["+self._m1ctrl._ip+"] when not attached!"))
        return self._varHandle

    def getVarInfo(self):
        """
        Get information about the variable from the target.
        """
        if(self._varInfo == None):
            raise PyComException(("pyCom Error: Can't get Info from SviVariable["+self.name+"] of Module["+self._module.name+"] on Controller["+self._m1ctrl._ip+"]!"))
        return self._varInfo

    def attach(self):
        """
        Creates a handle to a variable and initializes it. This function is already automatically called after initializing a software module.
        """
        self._varHandle = self._m1ctrl._pycom.TARGET_CreateVariable(self._m1ctrl.getCtrlHandle(), self.name.encode())
        if(self._varHandle == None):
            raise PyComException(("pyCom Error: Can't allocate SviVariable["+self.name+"] from Module["+self._module.name+"] on Controller["+self._m1ctrl._ip+"]"))
        if(self._m1ctrl._pycom.TARGET_InitVariables(self._m1ctrl.getCtrlHandle(), self._varHandle, 1) <= 0):
            raise PyComException(("pyCom Error: Can't attach SviVariable["+self.name+"] from Module["+self._module.name+"] on Controller["+self._m1ctrl._ip+"]"))
        self.updateVarInfo()

    def updateVarInfo(self):
        """
        Update the variable information.
        """
        self._varInfo = VARIABLE_INFO()
        if(self._m1ctrl._pycom.VARIABLE_GetInfo(self.getVarHandle(), ctypes.pointer(self._varInfo)) != OK):
            raise PyComException("pyCom Error: Can't update Informations of SviVariable["+self.name+"] from Module["+self._module.name+"] on Controller["+self._m1ctrl._ip+"]")
        self._bufferLen = self._m1ctrl._pycom.VARIABLE_GetBufferLen(ctypes.pointer(self._varInfo))
    
    def read(self):
        """
        Read a single SVI variable from the target.
        """
        if(self.getConnectionState() != ONLINE):
            raise PyComException("pyCom Error: read SviVariable["+self.name+"] from Module["+self._module.name+"] on Controller["+self._m1ctrl._ip+"] it is not available!")
        
        value = None
        valueType = None
        identifiyer = self._varInfo.format & 0x0f
        if not(self._varInfo.format & SVI_F_OUT):
            raise PyComException("pyCom Error: Svi Variable["+self.name+"] is not read able!")
        if(self._varInfo.format & SVI_F_BLK):
            if(identifiyer == SVI_F_CHAR8):
                value = (ctypes.c_char * self._bufferLen)() #allocate buffer
                valueType = str
            elif (identifiyer == SVI_F_CHAR16):
                value = (ctypes.c_wchar * self._bufferLen)() #allocate buffer
                valueType = str
            elif(identifiyer == SVI_F_UINT64):
                value = ctypes.c_ulonglong()
                valueType = int
            elif(identifiyer == SVI_F_SINT64):
                value = ctypes.c_longlong()
                valueType = int
            elif(identifiyer == SVI_F_REAL64):
                value = ctypes.c_double()
                valueType = float
            elif(self._varInfo.format & SVI_F_STRINGLSTBASE):                        
                raise PyComTypeException("ByteAccess of String array not implemented!")
            elif(self._varInfo.format & SVI_F_USTRINGLSTBASE):                        
                raise PyComTypeException("ByteAccess of UNICODED String array not implemented!")
            elif(identifiyer == SVI_F_MIXED):
                raise PyComTypeException("ByteAccess of SVI_F_MIXED not implemented!")
            elif(identifiyer == SVI_F_UINT1):
                raise PyComTypeException("ByteAccess of UINT1 not implemented!")
            elif(identifiyer == SVI_F_UINT8):
                raise PyComTypeException("ByteAccess of UINT8 not implemented!")
            elif(identifiyer == SVI_F_BOOL8):
                raise PyComTypeException("ByteAccess of BOOL8 not implemented!")
            elif(identifiyer == SVI_F_UINT16):
                raise PyComTypeException("ByteAccess of UINT16 not implemented!")
            elif(identifiyer == SVI_F_UINT32):
                raise PyComTypeException("ByteAccess of UINT32 not implemented!")
            elif(identifiyer == SVI_F_SINT8):
                raise PyComTypeException("ByteAccess of SINT8 not implemented!")
            elif(identifiyer == SVI_F_SINT16):
                raise PyComTypeException("ByteAccess of SINT16 not implemented!")
            elif(identifiyer == SVI_F_SINT32):
                raise PyComTypeException("ByteAccess of SINT32 not implemented!")
            elif(identifiyer == SVI_F_REAL32):
                raise PyComTypeException("ByteAccess of REAL32 not implemented!")
            else:
                raise PyComException("pyCom Error: unknown SVIBLK Type!"+str(self._varInfo.format)+" of Variable:"+self.name)
        else:
            if(identifiyer == SVI_F_CHAR8):
                value = ctypes.c_ubyte()
                valueType = 'char8'
            elif(identifiyer == SVI_F_CHAR16):
                value = ctypes.c_ushort()
                valueType = 'char16'
            elif(identifiyer == SVI_F_UINT1):
                value = ctypes.c_ubyte()
                valueType = bool
            elif(identifiyer == SVI_F_UINT8):
                value = ctypes.c_ubyte()
                valueType = int
            elif(identifiyer == SVI_F_BOOL8):
                value = ctypes.c_ubyte()
                valueType = bool
            elif(identifiyer == SVI_F_UINT16):
                value = ctypes.c_ushort()
                valueType = int
            elif(identifiyer == SVI_F_UINT32):
                value = ctypes.c_uint()
                valueType = int
            elif(identifiyer == SVI_F_SINT8):
                value = ctypes.c_byte()
                valueType = int
            elif(identifiyer == SVI_F_SINT8):
                value = ctypes.c_byte()
                valueType = int
            elif(identifiyer == SVI_F_SINT16):
                value = ctypes.c_short()
                valueType = int
            elif(identifiyer == SVI_F_SINT32):
                value = ctypes.c_long()
                valueType = int
            elif(identifiyer == SVI_F_REAL32):
                value = ctypes.c_float()
                valueType = float
            else:
                raise PyComException("pyCom Error: unknown SVI Type!"+str(self._varInfo.format)+" of Variable:"+self.name)

        ret = self._m1ctrl._pycom.TARGET_ReadVariable(self._m1ctrl.getCtrlHandle(), self._varHandle, ctypes.pointer(value), self._bufferLen)
        if ret != 0:
            raise PyComException("pyCom Error: could not read SVI Variable:"+self.name)
        if value.value == None:
            if type(value) == bytes:
                return valueType(value.decode())
            elif valueType == 'char8':
                return ((value).to_bytes(1, byteorder='big')).decode('utf-8')
            elif valueType == 'char16':
                return ((value).to_bytes(1, byteorder='big')).decode('utf-8')
            else:
                return valueType(value)
        else:
            if type(value.value) == bytes:
                return valueType(value.value.decode())
            elif valueType == 'char8':
                return ((value.value).to_bytes(1, byteorder='big')).decode('utf-8')
            elif valueType == 'char16':
                return ((value.value).to_bytes(1, byteorder='big')).decode('utf-8')
            else:
                return valueType(value.value)

    def write(self, data):
        """
        Write a single SVI variable to the target.
        """
        if(self.getConnectionState() != ONLINE):
            raise PyComException("pyCom Error: read SviVariable["+self.name+"] from Module["+self._module.name+"] on Controller["+self._m1ctrl._ip+"] it is not available!")

        value = None
        identifiyer = self._varInfo.format & 0x0f
        if not(self._varInfo.format & SVI_F_IN):
            raise PyComException("pyCom Error: Svi Variable["+self.name+"] is not write able!")
        if(self._varInfo.format & SVI_F_BLK):
            if(identifiyer == SVI_F_CHAR8):
                if type(data) != str:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str'")
                value = ctypes.create_string_buffer(data.encode('utf-8')) #allocate buffer
            elif (identifiyer == SVI_F_CHAR16):
                if type(data) != str:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str'")
                value = ctypes.create_unicode_buffer(data) #allocate buffer
            elif(identifiyer == SVI_F_UINT64):
                if type(data) != int:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                value = ctypes.c_ulonglong(data)
            elif(identifiyer == SVI_F_SINT64):
                if type(data) != int:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                value = ctypes.c_longlong(data)
            elif(identifiyer == SVI_F_REAL64):
                if type(data) != float:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'float'")
                value = ctypes.c_double(data)
            elif(self._varInfo.format & SVI_F_STRINGLSTBASE):                        
                raise PyComTypeException("ByteAccess of String array not implemented!")
            elif(self._varInfo.format & SVI_F_USTRINGLSTBASE):                        
                raise PyComTypeException("ByteAccess of UNICODED String array not implemented!")
            elif(identifiyer == SVI_F_MIXED):
                raise PyComTypeException("ByteAccess of SVI_F_MIXED not implemented!")
            elif(identifiyer == SVI_F_UINT1):
                raise PyComTypeException("ByteAccess of UINT1 not implemented!")
            elif(identifiyer == SVI_F_UINT8):
                raise PyComTypeException("ByteAccess of UINT8 not implemented!")
            elif(identifiyer == SVI_F_BOOL8):
                raise PyComTypeException("ByteAccess of BOOL8 not implemented!")
            elif(identifiyer == SVI_F_UINT16):
                raise PyComTypeException("ByteAccess of UINT16 not implemented!")
            elif(identifiyer == SVI_F_UINT32):
                raise PyComTypeException("ByteAccess of UINT32 not implemented!")
            elif(identifiyer == SVI_F_SINT8):
                raise PyComTypeException("ByteAccess of SINT8 not implemented!")
            elif(identifiyer == SVI_F_SINT16):
                raise PyComTypeException("ByteAccess of SINT16 not implemented!")
            elif(identifiyer == SVI_F_SINT32):
                raise PyComTypeException("ByteAccess of SINT32 not implemented!")
            elif(identifiyer == SVI_F_REAL32):
                raise PyComTypeException("ByteAccess of REAL32 not implemented!")
            else:
                raise PyComException("pyCom Error: unknown SVIBLK Type!"+str(self._varInfo.format)+" of Variable:"+self.name)
        else:
            if(identifiyer == SVI_F_CHAR8):
                if type(data) != str or len(data) > 1:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str' with a maximum length of 1")
                value = ctypes.c_ubyte(int.from_bytes(data.encode('utf-8'), byteorder='big', signed=False))
            elif(identifiyer == SVI_F_CHAR16):
                if type(data) != str or len(data) > 1:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str' with a maximum length of 1")
                value = ctypes.c_ushort(int.from_bytes(data.encode('utf-8'), byteorder='big', signed=False))
            elif(identifiyer == SVI_F_UINT1):
                if type(data) != bool:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'bool'")
                value = ctypes.c_ubyte(data)
            elif(identifiyer == SVI_F_UINT8):
                if type(data) != int:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                value = ctypes.c_ubyte(data)
            elif(identifiyer == SVI_F_BOOL8):
                if type(data) != bool:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'bool'")
                value = ctypes.c_ubyte(data)
            elif(identifiyer == SVI_F_UINT16):
                if type(data) != int:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                value = ctypes.c_ushort(data)
            elif(identifiyer == SVI_F_UINT32):
                if type(data) != int:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                value = ctypes.c_uint(data)
            elif(identifiyer == SVI_F_SINT8):
                if type(data) != int:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                value = ctypes.c_byte(data)
            elif(identifiyer == SVI_F_SINT8):
                if type(data) != int:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                value = ctypes.c_byte(data)
            elif(identifiyer == SVI_F_SINT16):
                if type(data) != int:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                value = ctypes.c_short(data)
            elif(identifiyer == SVI_F_SINT32):
                if type(data) != int:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                value = ctypes.c_long(data)
            elif(identifiyer == SVI_F_REAL32):
                if type(data) != float:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'float'")
                value = ctypes.c_float(data)
            else:
                raise PyComException("pyCom Error: unknown SVI Type!"+str(self._varInfo.format)+" of Variable:"+self.name)
        
        if self._m1ctrl._pycom.TARGET_WriteVariable(self._m1ctrl.getCtrlHandle(), self._varHandle, ctypes.byref(value), self._bufferLen) != 0:
            raise PyComException("pyCom Error: could not write Svi Variable:" + str(self.name))
        
    def getConnectionState(self):
        """
        Get the connection state of the variable.
        """
        state = ctypes.c_uint(0)
        self._m1ctrl._pycom.VARIABLE_GetState(self._varHandle, ctypes.pointer(state))
        return state.value
    
if __name__ == "__main__":

    #help(PyCom)
    #help(M1Controller)
    #help(M1SVIObserver)
    #help(M1SVIReader)
    #help(M1SVIWriter)
    #help(M1TargetFinder)
    #help(_M1SwModule)
    #help(_SVIVariable)

    import doctest
    doctest.testmod(verbose=False)