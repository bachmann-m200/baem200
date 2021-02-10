#!/usr/bin/python
# Filename: pyCom.py
# Module pyCom
# python classes to interact with a M1 Controller through M1Com and ctypes.

import ctypes, os.path, shutil, sys
from ctypes.test import ctypes
from ctypes.test.test_pointers import ctype_types
from ctypes import wintypes

# Const:
MIO_INFOLEN_A        = 200
MIO_CNAMELEN_A       = 24
MIO_PRODNBLEN_A      = 12
M_PATHLEN            = 80
M_PATHLEN_A          = ((M_PATHLEN + 1 + 3) & 0xfffffffc)
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

# Return values for application
M_E_INSTALL          = ctypes.c_int32(0x80000122).value
M_E_SMODE            = ctypes.c_int32(0x80000121).value
M_E_NOMEM            = ctypes.c_int32(0x80000123).value
M_E_NOGLOBMEM        = ctypes.c_int32(0x80000153).value
M_E_NOAPPMEM         = ctypes.c_int32(0x80000154).value
M_E_NOFILE           = ctypes.c_int32(0x80000111).value
M_E_BADREAD          = ctypes.c_int32(0x80000142).value
M_E_WRONGVERS        = ctypes.c_int32(0x8000013E).value
M_E_BADELEM          = ctypes.c_int32(0x80000136).value
M_E_BADSEEK          = ctypes.c_int32(0x80000144).value
M_E_NOLIBREG         = ctypes.c_int32(0x80000148).value
M_E_BADCHECK         = ctypes.c_int32(0x80000145).value
M_E_BADVXWLD         = ctypes.c_int32(0x80000146).value
M_E_BADMEMLD         = ctypes.c_int32(0x80000147).value
M_E_NOWRITE          = ctypes.c_int32(0x80000141).value
M_E_NOMODNBR         = ctypes.c_int32(0x80000125).value
M_E_NOMOD2           = ctypes.c_int32(0x8000012A).value
M_E_NOENTRY          = ctypes.c_int32(0x8000014E).value
M_E_NOREG            = ctypes.c_int32(0x8000014F).value
M_E_BADINIT          = ctypes.c_int32(0x80000150).value
M_E_BADNAME          = ctypes.c_int32(0x80000137).value
M_E_FAILED           = ctypes.c_int32(0x80000100).value
M_E_NOTSUPP          = ctypes.c_int32(0x80000124).value
M_E_NOMOD1           = ctypes.c_int32(0x80000129).value
M_E_NODELSYS         = ctypes.c_int32(0x80000171).value
M_E_NODELTSK         = ctypes.c_int32(0x8000012C).value
M_ES_SMI             = 0x00020000
SMI_E_OK             = 0
SMI_E_NAME           = (M_ES_SMI | M_E_BADNAME)
SMI_E_FAILED         = (M_ES_SMI | M_E_FAILED)
SMI_E_SUPPORT        = (M_ES_SMI | M_E_NOTSUPP)
SMI_E_NOMEM          = (M_ES_SMI | M_E_NOMEM)
M_ES_MOD             = 0x00080000
MOD_E_OK             = 0
MOD_E_INSTALL        = (M_ES_MOD | M_E_INSTALL)
MOD_E_SMODE          = (M_ES_MOD | M_E_SMODE)
MOD_E_NOMEM          = (M_ES_MOD | M_E_NOMEM)
MOD_E_NOGLOBMEM      = (M_ES_MOD | M_E_NOGLOBMEM)
MOD_E_NOAPPMEM       = (M_ES_MOD | M_E_NOAPPMEM)
MOD_E_NOFILE         = (M_ES_MOD | M_E_NOFILE)
MOD_E_BADREAD        = (M_ES_MOD | M_E_BADREAD)
MOD_E_WRONGVERS      = (M_ES_MOD | M_E_WRONGVERS)
MOD_E_BADELEM        = (M_ES_MOD | M_E_BADELEM)
MOD_E_BADSEEK        = (M_ES_MOD | M_E_BADSEEK)
MOD_E_NOLIBREG       = (M_ES_MOD | M_E_NOLIBREG)
MOD_E_BADCHECK       = (M_ES_MOD | M_E_BADCHECK)
MOD_E_BADVXWLD       = (M_ES_MOD | M_E_BADVXWLD)
MOD_E_BADMEMLD       = (M_ES_MOD | M_E_BADMEMLD)
MOD_E_NOWRITE        = (M_ES_MOD | M_E_NOWRITE)
MOD_E_NOMODNBR       = (M_ES_MOD | M_E_NOMODNBR)
MOD_E_NOMOD2         = (M_ES_MOD | M_E_NOMOD2)
MOD_E_NOENTRY        = (M_ES_MOD | M_E_NOENTRY)
MOD_E_NOREG          = (M_ES_MOD | M_E_NOREG)
MOD_E_BADINIT        = (M_ES_MOD | M_E_BADINIT)
MOD_E_NOMOD1         = (M_ES_MOD | M_E_NOMOD1)
MOD_E_NODELSYS       = (M_ES_MOD | M_E_NODELSYS)
MOD_E_NODELTASK      = (M_ES_MOD | M_E_NODELTSK)

# Possible appstates for TARGET_GetTargetState:
RES_S_RUN            = 1
RES_S_ERROR          = 2
RES_S_STOP           = 3
RES_S_INIT           = 4
RES_S_DEINIT         = 5
RES_S_EOI            = 6
RES_S_RESET          = 7
RES_S_WARNING        = 8
RES_S_ERROR_SMART    = 9

# Possible errorcodes:
M1C_BASE				= 0x81100000      # indicates that m1com is error source for other error sources refer to msys.h
M1C_OK                  = 0               # everything is fine
M1C_E_MEM_ALLOC         = (M1C_BASE|0x01) # not enough memory
M1C_E_INVALID_PARTNER   = (M1C_BASE|0x02) # network connection closed by partner
M1C_E_WSA_INIT          = (M1C_BASE|0x03) # WINSOCK could not be initialized
M1C_E_ENET_DOWN         = (M1C_BASE|0x04) # Network is down
M1C_E_ADDRESS_SUPPORT   = (M1C_BASE|0x05) # address family not supported by protocol family
M1C_E_SOCKET_PROGRESS   = (M1C_BASE|0x06) # operation now in progress
M1C_E_NOMORE_SOCKETS    = (M1C_BASE|0x07) # no more sockets
M1C_E_PROTOCOL          = (M1C_BASE|0x08) # wrong protocol type for socket
M1C_E_SOCKET            = (M1C_BASE|0x09) # socket error
M1C_E_SOCKET_ACCESS     = (M1C_BASE|0x0A) # invalid socket access
M1C_E_INVALID_IPA       = (M1C_BASE|0x0B) # bad address
M1C_E_SOCKET_CONN       = (M1C_BASE|0x0C) # socket connect error
M1C_E_INVALID_SOCKET    = (M1C_BASE|0x0D) # invalid socket
M1C_E_RECEIVE_SIZE      = (M1C_BASE|0x0E) # message too long
M1C_E_SOCKET_INUSE      = (M1C_BASE|0x0F) # socket already in use
M1C_E_TIME_OUT          = (M1C_BASE|0x10) # connection timed out
M1C_E_WINSOCKET         = (M1C_BASE|0x11) # WINSOCK error
M1C_E_RPCCALL_STATE     = (M1C_BASE|0x13) # invalid XiD
M1C_E_PROG_MISMATCH     = (M1C_BASE|0x14) # module with that number not found on controller
M1C_E_PROC_UNAVAIL      = (M1C_BASE|0x15) # SMI function not supported by module
M1C_E_INV_RESPONSE      = (M1C_BASE|0x16) # invalid response
M1C_E_AUTH_ERROR        = (M1C_BASE|0x17) # authentication failed
M1C_E_NO_CONN	        = (M1C_BASE|0x18) # no connection established
M1C_E_QSOAP_FRAME       = (M1C_BASE|0x19) # invalid QSOAP frame
M1C_E_NEG_RESP	        = (M1C_BASE|0x1A) # SMI: negative response
M1C_E_SSL               = (M1C_BASE|0x1B) # SSL error
M1C_E_INVALID_PARAMETER	= (M1C_BASE|0x1C) # invalid parameter
M1C_E_INVALID_HANDLE	= (M1C_BASE|0x1E) # invalid handle
M1C_E_NOT_INITIALIZED   = (M1C_BASE|0x1F) # not initialized
M1C_E_NO_VAR            = (M1C_BASE|0x20) # variable not found
M1C_E_LOCAL_FILE_ERROR  = (M1C_BASE|0x22) # error accessing the local file
M1C_E_HTTP_ERROR        = (M1C_BASE|0x23) # HTTP error
M1C_E_NO_PERMISSON      = (M1C_BASE|0x24) # access denied
M1C_E_UNKNOWN_HOST      = (M1C_BASE|0x25) # host not found
M1C_E_REMOTE_FILE_ERROR = (M1C_BASE|0x26) # error accessing the remote file
M1C_E_UNSPECIFIED_ERROR = (M1C_BASE|0x27) # unspecified
M1C_E_NO_LIST           = (M1C_BASE|0x28) # no observation list
M1C_E_INVALID_STATE     = (M1C_BASE|0x29) # operation not allowed in the current state
M1C_E_WRONG_MSYS        = (M1C_BASE|0x30) # function not supported by used MSYS

# Protocol types:
PROTOCOL_TCP         = 0
PROTOCOL_QSOAP       = 1
PROTOCOL_SSL         = 2
PROTOCOL_UDP         = 4

# Possible keys for TARGET_Set/GetUintParam()
M1C_PROXY_USED              = 0x0
M1C_PROXY_PORT              = 0x1
M1C_QSOAP_PORT              = 0x2
M1C_IGNORE_SERVER_CERT      = 0x3
M1C_COUNT_SOCKETS           = 0x4
M1C_IGNORE_SERVER_CERT_CN   = 0x5
M1C_LOGIN2_USER_PARAM       = 0x6

# Possible keys for TARGET_Set/GetStringParam()
M1C_PROXY_HOST              = 0x00010000
M1C_PROXY_USERNAME          = 0x00010001
M1C_PROXY_PASSWD            = 0x00010002
M1C_QSOAP_PATH              = 0x00010003
M1C_VHD_SESSIONNAME         = 0x00010004

# SSL/Windows store specific defines
CERT_CLOSE_STORE_FORCE_FLAG = 1
PKCS12_ALLOW_OVERWRITE_KEY  = 0x00004000
PKCS12_NO_PERSIST_KEY       = 0x00008000

#SVI FORMAT:
SVI_F_IN             = 0x80                                 # Type is input (server view)
SVI_F_OUT            = 0x40                                 # Type is output (server view)
SVI_F_INOUT          = 0xc0                                 # Type is input and output
SVI_F_BLK            = 0x20                                 # Block value
SVI_F_HIDDEN         = 0x100                                # Hidden service variable
SVI_F_UNKNOWN        = 0x00                                 # Format unknown
SVI_F_UINT1          = 0x01                                 # Bit value
SVI_F_UINT8          = 0x02                                 # 8-bit unsigned integer
SVI_F_SINT8          = 0x03                                 # 8-bit signed integer
SVI_F_UINT16         = 0x04                                 # 16-bit unsigned integer
SVI_F_SINT16         = 0x05                                 # 16-bit signed integer
SVI_F_UINT32         = 0x06                                 # 32-bit unsigned integer
SVI_F_SINT32         = 0x07                                 # 32-bit signed integer
SVI_F_REAL32         = 0x08                                 # 32-bit float
SVI_F_BOOL8          = 0x09                                 # Boolean value
SVI_F_CHAR8          = 0x0a                                 # 8-bit character
SVI_F_MIXED          = 0x0b                                 # mixed; for SVI_F_BLK
SVI_F_UINT64         = 0x0c                                 # 64-bit unsigned integer
SVI_F_SINT64         = 0x0d                                 # 64-bit signed integer
SVI_F_REAL64         = 0x0e                                 # 64-bit float
SVI_F_CHAR16         = 0x0f                                 # 16-bit character (Unicode)
SVI_F_STRINGLSTBASE  = 0x10                                 # base of String list type
SVI_F_USTRINGLSTBASE = 0x11                                 # base of Unicode String list type
SVI_F_STRINGLST      = (SVI_F_BLK | SVI_F_STRINGLSTBASE)    # String list type
SVI_F_USTRINGLST     = (SVI_F_BLK | SVI_F_USTRINGLSTBASE)   # Unicode string list type
SVI_F_STRING         = (SVI_F_BLK | SVI_F_CHAR8)            # String type
SVI_F_USTRING        = (SVI_F_BLK | SVI_F_CHAR16)           # Unicode string type

def ctypesArray2list(ctypesArray):
    listInfo = []
    for item in ctypesArray:
        listInfo.append(item)
    return listInfo

def ctypesInfo2dict(ctypesInfo):
    dictInfo = {}
    for field in ctypesInfo._fields_:
        dictKey = field[0]
        dictValue = getattr(ctypesInfo, field[0])
        if type(dictValue) == bytes:
            dictValue = dictValue.decode('utf-8')
        elif hasattr(dictValue, '_fields_'):
            dictValue = ctypesInfo2dict(dictValue)
        elif hasattr(dictValue, '_type_'):
            dictValue = ctypesArray2list(dictValue)
        dictInfo.update({dictKey:dictValue})

    return dictInfo.copy()

class CERT_CONTEXT(ctypes.Structure):
    _fields_ = [("dwCertEncodingType", ctypes.wintypes.DWORD),
                ("pbCertEncoded", ctypes.POINTER(ctypes.wintypes.BYTE)),
                ("cbCertEncoded", ctypes.wintypes.DWORD),
                ("pCertInfo", ctypes.c_void_p),
                ("hCertStore", ctypes.c_void_p)]

class CRYPT_DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD),
                ("pbData", ctypes.POINTER(ctypes.wintypes.BYTE))]

class WINBYTE_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.wintypes.BYTE))]

    def __init__(self,num_of_structs):
        elems = (ctypes.wintypes.BYTE * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.wintypes.BYTE))
        self.array_size = num_of_structs

class BYTE_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_byte))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_byte * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_byte))
        self.array_size = num_of_structs

class UBYTE_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_ubyte))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_ubyte * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_ubyte))
        self.array_size = num_of_structs

class SHORT_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_short))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_short * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_short))
        self.array_size = num_of_structs

class USHORT_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_ushort))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_ushort * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_ushort))
        self.array_size = num_of_structs

class LONG_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_long))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_long * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_long))
        self.array_size = num_of_structs

class UINT_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_uint))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_uint * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_uint))
        self.array_size = num_of_structs

class FLOAT_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_float))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_float * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_float))
        self.array_size = num_of_structs

class DOUBLE_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_double))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_double * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_double))
        self.array_size = num_of_structs

class LONGLONG_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_longlong))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_longlong * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_longlong))
        self.array_size = num_of_structs

class ULONGLONG_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_ulonglong))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_ulonglong * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_ulonglong))
        self.array_size = num_of_structs

class UNICODE_ARRAY(ctypes.Structure):
    _fields_ = [('array_size', ctypes.c_short),
                ('ARRAY', ctypes.POINTER(ctypes.c_wchar))]

    def __init__(self,num_of_structs):
        elems = (ctypes.c_wchar * num_of_structs)()
        self.ARRAY = ctypes.cast(elems, ctypes.POINTER(ctypes.c_wchar))
        self.array_size = num_of_structs

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

class SMI_RESET_C(ctypes.Structure):
    _fields_ = [("Name", (ctypes.c_char*M_MODNAMELEN_A))]

class SMI_RESET_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32)]

class SMI_ENDOFINIT_C(ctypes.Structure):
    _fields_ = [("Name", (ctypes.c_char*M_MODNAMELEN_A))]

class SMI_ENDOFINIT_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32)]

class SMI_DEINIT_C(ctypes.Structure):
    _fields_ = [("Name", (ctypes.c_char*M_MODNAMELEN_A))]

class SMI_DEINIT_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32)]

class SMI_STOP_C(ctypes.Structure):
    _fields_ = [("Name", (ctypes.c_char*M_MODNAMELEN_A))]

class SMI_STOP_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32)]

class SMI_INIT_C(ctypes.Structure):
    _fields_ = [("Name", (ctypes.c_char*M_MODNAMELEN_A))]

class SMI_INIT_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32)]

class SMI_RUN_C(ctypes.Structure):
    _fields_ = [("Name", (ctypes.c_char*M_MODNAMELEN_A))]

class SMI_RUN_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32)]

class SYS_VERSION(ctypes.Structure):
    _fields_ = [("Code", (ctypes.c_uint32*3)),
                ("Type", ctypes.c_uint32)]

class RES_MODXINFO(ctypes.Structure):
    _fields_ = [("TypeName",    (ctypes.c_char*M_MODNAMELEN_A)),
                ("AppName",     (ctypes.c_char*M_MODNAMELEN_A)),
                ("AppIdx",      ctypes.c_uint32),
                ("AppPart",     ctypes.c_uint32),
                ("MinVers",     ctypes.c_uint32),
                ("MaxVers",     ctypes.c_uint32),
                ("MaxUser",     ctypes.c_uint32),
                ("Attr",        ctypes.c_uint32),
                ("ModuleId",    ctypes.c_uint32),
                ("ActUser",     ctypes.c_uint32),
                ("State",       ctypes.c_uint32),
                ("ModuleNb",    ctypes.c_uint32),
                ("TaskId",      ctypes.c_uint32),
                ("PortNb",      ctypes.c_uint32),
                ("TcpPortNb",   ctypes.c_uint32),
                ("Checksum",    ctypes.c_uint32),
                ("Version",     SYS_VERSION),
                ("Incarnation", ctypes.c_uint32),
                ("OwnTaskId",   ctypes.c_uint32),
                ("Affinity",    ctypes.c_uint32),
                ("Spare3",      ctypes.c_uint32)]

class RES_MODXINFO_C(ctypes.Structure):
    _fields_ = [("AppName", (ctypes.c_char*M_MODNAMELEN_A))]

class RES_MODXINFO_R(ctypes.Structure):
    _fields_ = [("RetCode", ctypes.c_int32),
                ("Inf",     RES_MODXINFO)]

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

        #VOID GetErrorSrc(SINT32 errorCode, CHAR * errorSrc, UINT32 errorSrcLen);
        self.GetErrorSrc = m1Dll.GetErrorSrc
        self.GetErrorSrc.argtypes = [ctypes.c_long, ctypes.c_char_p, ctypes.c_uint]

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

        #VOID TARGET_Dispose(M1C_H_TARGET targetHandle);
        self.TARGET_Dispose = m1Dll.TARGET_Dispose
        self.TARGET_Dispose.argtypes = [ctypes.c_void_p]

        #SINT32 TARGET_Connect(void* ctrl, char* username, char* password, char* clientname);
        self.TARGET_Connect = m1Dll.TARGET_Connect
        self.TARGET_Connect.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.TARGET_Connect.restype  = ctypes.c_long

        #SINT32 TARGET_GetSessionLiveTime(M1C_H_TARGET targetHandle, UINT32* sessionLiveTime);
        self.TARGET_GetSessionLiveTime = m1Dll.TARGET_GetSessionLiveTime
        self.TARGET_GetSessionLiveTime.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.TARGET_GetSessionLiveTime.restype  = ctypes.c_long

        #SINT32 TARGET_GetLoginInfo(M1C_H_TARGET targetHandle, RES_LOGIN2_R * resLogin2Reply);
        self.TARGET_GetLoginInfo = m1Dll.TARGET_GetLoginInfo
        self.TARGET_GetLoginInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(RES_LOGIN2_R)]
        self.TARGET_GetLoginInfo.restype  = ctypes.c_long

        #SINT32 TARGET_RenewConnection(M1C_H_TARGET targetHandle);
        self.TARGET_RenewConnection = m1Dll.TARGET_RenewConnection
        self.TARGET_RenewConnection.argtypes = [ctypes.c_void_p]
        self.TARGET_RenewConnection.restype  = ctypes.c_long

        #SINT32 TARGET_Close(M1C_H_TARGET targetHandle);
        self.TARGET_Close = m1Dll.TARGET_Close
        self.TARGET_Close.argtypes = [ctypes.c_void_p]
        self.TARGET_Close.restype  = ctypes.c_long

        #SINT32 TARGET_GetCountModules(void* targetHandle, unsigned short* moduleCount);
        self.TARGET_GetCountModules = m1Dll.TARGET_GetCountModules
        self.TARGET_GetCountModules.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort)]
        self.TARGET_GetCountModules.restype  = ctypes.c_long

        #SINT32 TARGET_GetModules(M1C_H_TARGET targetHandle, const UINT16 moduleCount, MODULE_LIST* moduleList);
        self.TARGET_GetModules = m1Dll.TARGET_GetModules
        self.TARGET_GetModules.argtypes = [ctypes.c_void_p, ctypes.c_ushort, ctypes.POINTER(MODULE_LIST)]
        self.TARGET_GetModules.restype  = ctypes.c_long

        #M1C_H_MODULE TARGET_CreateModule(M1C_H_TARGET targetHandle, CHAR* name);
        self.TARGET_CreateModule = m1Dll.TARGET_CreateModule
        self.TARGET_CreateModule.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.TARGET_CreateModule.restype  = ctypes.c_void_p

        #SINT32 MODULE_Connect(M1C_H_MODULE moduleHandle);
        self.MODULE_Connect = m1Dll.MODULE_Connect
        self.MODULE_Connect.argtypes = [ctypes.c_void_p]
        self.MODULE_Connect.restype = ctypes.c_long

        #SINT32 MODULE_GetCountVariables(M1C_H_MODULE moduleHandle, UINT32* varCount);
        self.MODULE_GetCountVariables = m1Dll.MODULE_GetCountVariables
        self.MODULE_GetCountVariables.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.MODULE_GetCountVariables.restype  = ctypes.c_long

        #SINT32 MODULE_GetVariables(M1C_H_MODULE moduleHandle, const UINT32 varCount, VARIABLE_INFO_LIST* varList);
        self.MODULE_GetVariables = m1Dll.MODULE_GetVariables
        self.MODULE_GetVariables.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(VARIABLE_INFO_LIST)]
        self.MODULE_GetVariables.restype  = ctypes.c_long

        #M1C_H_VARIABLE TARGET_CreateVariable(M1C_H_TARGET targetHandle, CHAR* name);
        self.TARGET_CreateVariable = m1Dll.TARGET_CreateVariable
        self.TARGET_CreateVariable.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.TARGET_CreateVariable.restype  = ctypes.c_void_p

        #M1COM VOID VARIABLE_Dispose(M1C_H_VARIABLE variable);
        self.VARIABLE_Dispose = m1Dll.VARIABLE_Dispose
        self.VARIABLE_Dispose.argtypes = [ctypes.c_void_p]

        #SINT32 TARGET_InitVariables(M1C_H_TARGET targetHandle, M1C_H_VARIABLE* variables, UINT32 countVariables);
        self.TARGET_InitVariables = m1Dll.TARGET_InitVariables
        self.TARGET_InitVariables.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_InitVariables.restype  = ctypes.c_long

        #SINT32 VARIABLE_GetInfo(M1C_H_VARIABLE variable, VARIABLE_INFO* varInfo);
        self.VARIABLE_GetInfo = m1Dll.VARIABLE_GetInfo
        self.VARIABLE_GetInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_GetInfo.restype  = ctypes.c_long

        #M1COM CHAR8* (M1C_H_VARIABLE variable);
        self.VARIABLE_GetFullName = m1Dll.VARIABLE_GetFullName
        self.VARIABLE_GetFullName.argtypes = [ctypes.c_void_p]
        self.VARIABLE_GetFullName.restype  = ctypes.c_char_p

        #M1COM UINT32 VARIABLE_GetBufferLen(VARIABLE_INFO* varInfo);
        self.VARIABLE_GetBufferLen = m1Dll.VARIABLE_GetBufferLen
        self.VARIABLE_GetBufferLen.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_GetBufferLen.restype  = ctypes.c_uint

        #M1COM UINT32 VARIABLE_getArrayLen(VARIABLE_INFO* varInfo);
        self.VARIABLE_getArrayLen = m1Dll.VARIABLE_getArrayLen
        self.VARIABLE_getArrayLen.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_getArrayLen.restype  = ctypes.c_uint

        #SINT32 TARGET_ReadVariables(M1C_H_TARGET targetHandle, VARIABLE_BUFFER* variableBuffers, UINT32 countVariables);
        self.TARGET_ReadVariables = m1Dll.TARGET_ReadVariables
        self.TARGET_ReadVariables.argtypes = [ctypes.c_void_p, ctypes.POINTER(VARIABLE_BUFFER), ctypes.c_uint]
        self.TARGET_ReadVariables.restype  = ctypes.c_long

        #SINT32 TARGET_ReadVariable(M1C_H_TARGET targetHandle, M1C_H_VARIABLE variableHandle, VOID* buffer, UINT32 bufferSize);
        self.TARGET_ReadVariable = m1Dll.TARGET_ReadVariable
        self.TARGET_ReadVariable.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_ReadVariable.restype  = ctypes.c_long

        #SINT32 TARGET_WriteVariables(M1C_H_TARGET targetHandle, VARIABLE_BUFFER* variables, UINT32 countVariables);
        self.TARGET_WriteVariables = m1Dll.TARGET_WriteVariables
        self.TARGET_WriteVariables.argtypes = [ctypes.c_void_p, ctypes.POINTER(VARIABLE_BUFFER), ctypes.c_uint]
        self.TARGET_WriteVariables.restype  = ctypes.c_long

        #M1COM SINT32 TARGET_WriteVariable(M1C_H_TARGET targetHandle, M1C_H_VARIABLE variableHandle, VOID* buffer, UINT32 bufferSize);
        self.TARGET_WriteVariable = m1Dll.TARGET_WriteVariable
        self.TARGET_WriteVariable.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_WriteVariable.restype  = ctypes.c_long

        #M1COM BOOL8  VARIABLE_IsReadable(VARIABLE_INFO* varInfo);
        self.VARIABLE_IsReadable = m1Dll.VARIABLE_IsReadable
        self.VARIABLE_IsReadable.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_IsReadable.restype  = ctypes.c_ubyte

        #M1COM BOOL8  VARIABLE_IsWritable(VARIABLE_INFO* varInfo);
        self.VARIABLE_IsWritable = m1Dll.VARIABLE_IsWritable
        self.VARIABLE_IsWritable.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_IsWritable.restype  = ctypes.c_ubyte

        #SINT32 VARIABLE_GetState(M1C_H_VARIABLE variable, M1C_CONNECTION_STATE* state);
        self.VARIABLE_GetState = m1Dll.VARIABLE_GetState
        self.VARIABLE_GetState.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.VARIABLE_GetState.restype  = ctypes.c_long

        #M1COM  M1C_H_OBSLIST TARGET_CreateObservationList(M1C_H_TARGET targetHandle, VARIABLE_BUFFER* variableBuffers, UINT32 countVariables);
        self.TARGET_CreateObservationList = m1Dll.TARGET_CreateObservationList
        self.TARGET_CreateObservationList.argtypes = [ctypes.c_void_p, ctypes.POINTER(VARIABLE_BUFFER), ctypes.c_uint]
        self.TARGET_CreateObservationList.restype  = ctypes.c_void_p

        #M1COM  SINT32 OBSLIST_Dispose(M1C_H_OBSLIST obsListHandle);
        self.OBSLIST_Dispose = m1Dll.OBSLIST_Dispose
        self.OBSLIST_Dispose.argtypes = [ctypes.c_void_p]
        self.OBSLIST_Dispose.restype  = ctypes.c_long

        #M1COM SINT32 OBSLIST_Update(M1C_H_OBSLIST obsListHandle, SINT32* indexList, UINT32 listSize);
        self.OBSLIST_Update = m1Dll.OBSLIST_Update
        self.OBSLIST_Update.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_long), ctypes.c_uint]
        self.OBSLIST_Update.restype  = ctypes.c_long

        #M1COM SINT32 OBSLIST_Reset(M1C_H_OBSLIST obsListHandle);
        self.OBSLIST_Reset = m1Dll.OBSLIST_Reset
        self.OBSLIST_Reset.argtypes = [ctypes.c_void_p]
        self.OBSLIST_Reset.restype  = ctypes.c_long

        #SINT32 MODULE_Dispose(M1C_H_MODULE moduleHandle);
        self.MODULE_Dispose = m1Dll.MODULE_Dispose
        self.MODULE_Dispose.argtypes = [ctypes.c_void_p]
        self.MODULE_Dispose.restype  = ctypes.c_long

        #UINT32 VARIABLE_getBaseDataType(VARIABLE_INFO* varInfo);
        self.VARIABLE_getBaseDataType = m1Dll.VARIABLE_getBaseDataType
        self.VARIABLE_getBaseDataType.argtypes = [ctypes.POINTER(VARIABLE_INFO)]
        self.VARIABLE_getBaseDataType.restype  = ctypes.c_uint

        #M1COM SINT32 TARGET_SmiPing(CHAR* addr, UINT32 timeout, M1C_PROTOCOL protocol, RES_EXTPING_R * extping_r );
        self.TARGET_SmiPing = m1Dll.TARGET_SmiPing
        self.TARGET_SmiPing.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(RES_EXTPING_R)]
        self.TARGET_SmiPing.restype  = ctypes.c_long

        #M1COM SINT32 TARGET_SetUintParam(M1C_H_TARGET targetHandle, M1C_UINT_PARAM_KEY key, UINT32 value);
        self.TARGET_SetUintParam = m1Dll.TARGET_SetUintParam
        self.TARGET_SetUintParam.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]
        self.TARGET_SetUintParam.restype  = ctypes.c_long

        #M1COM SINT32 TARGET_SetStringParam(M1C_H_TARGET targetHandle, M1C_STRING_PARAM_KEY key, CHAR* value, UINT32 valueLen);
        self.TARGET_SetStringParam = m1Dll.TARGET_SetStringParam
        self.TARGET_SetStringParam.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint]
        self.TARGET_SetStringParam.restype  = ctypes.c_long

        #M1COM UINT32 TARGET_GetUintParam(M1C_H_TARGET targetHandle, M1C_UINT_PARAM_KEY key);
        self.TARGET_GetUintParam = m1Dll.TARGET_GetUintParam
        self.TARGET_GetUintParam.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_GetUintParam.restype  = ctypes.c_uint

        #M1COM CHAR*  TARGET_GetStringParam(M1C_H_TARGET targetHandle, M1C_STRING_PARAM_KEY key);
        self.TARGET_GetStringParam = m1Dll.TARGET_GetStringParam
        self.TARGET_GetStringParam.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        self.TARGET_GetStringParam.restype  = ctypes.c_char_p

        #M1COM SINT32 TARGET_GetMaxCallSize(M1C_H_TARGET targetHandle, UINT32* maxCallSize);
        self.TARGET_GetMaxCallSize = m1Dll.TARGET_GetMaxCallSize
        self.TARGET_GetMaxCallSize.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.TARGET_GetMaxCallSize.restype  = ctypes.c_long

        #M1COM SINT32 TARGET_SetSSLClientCertificateContext(M1C_H_TARGET targetHandle, PCERT_CONTEXT clientCertContext);
        self.TARGET_SetSSLClientCertificateContext = m1Dll.TARGET_SetSSLClientCertificateContext
        self.TARGET_SetSSLClientCertificateContext.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self.TARGET_SetSSLClientCertificateContext.restype  = ctypes.c_long

        #M1COM SINT32 TARGET_GetConnectionState(M1C_H_TARGET targetHandle, M1C_CONNECTION_STATE* state);
        self.TARGET_GetConnectionState = m1Dll.TARGET_GetConnectionState
        self.TARGET_GetConnectionState.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)]
        self.TARGET_GetConnectionState.restype  = ctypes.c_long

        #M1COM SINT32 TARGET_GetTargetState(M1C_H_TARGET targetHandle, UINT16* appState, UINT16* rebootCount);
        self.TARGET_GetTargetState = m1Dll.TARGET_GetTargetState
        self.TARGET_GetTargetState.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort), ctypes.POINTER(ctypes.c_ushort)]
        self.TARGET_GetTargetState.restype  = ctypes.c_long

        #M1COM SINT32 MODULE_SendCall(M1C_H_MODULE moduleHandle, UINT32 proc, UINT32 version, const PVOID send, UINT16 sendSize, PVOID recv, UINT16 recvSize, UINT32 timeout);
        self.MODULE_SendCall = m1Dll.MODULE_SendCall
        self.MODULE_SendCall.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_void_p, ctypes.c_ushort, ctypes.c_uint]
        self.MODULE_SendCall.restype  = ctypes.c_long

        #M1COM SINT32 TARGET_BroadcastSmiPing( UINT32 timeout, TARGET_INFO * targetInfos, UINT32 len );
        self.TARGET_BroadcastSmiPing = m1Dll.TARGET_BroadcastSmiPing
        self.TARGET_BroadcastSmiPing.argtypes = [ctypes.c_uint, ctypes.POINTER(TARGET_INFO), ctypes.c_uint]
        self.TARGET_BroadcastSmiPing.restype  = ctypes.c_long

        #M1COM SINT32 RFS_CopyToTarget(M1C_H_TARGET targetHandle, CHAR *remoteFileName, CHAR *localFileName); 
        self.RFS_CopyToTarget = m1Dll.RFS_CopyToTarget
        self.RFS_CopyToTarget.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        self.RFS_CopyToTarget.restype  = ctypes.c_long

        #M1COM SINT32 RFS_CopyFromTarget(M1C_H_TARGET targetHandle, CHAR *localFileName, CHAR *remoteFilename); 
        self.RFS_CopyFromTarget = m1Dll.RFS_CopyFromTarget
        self.RFS_CopyFromTarget.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        self.RFS_CopyFromTarget.restype  = ctypes.c_long

        #M1COM SINT32 RFS_CopyRemote(M1C_H_TARGET targetHandle, CHAR *destFile, CHAR *srcFile); 
        self.RFS_CopyRemote = m1Dll.RFS_CopyRemote
        self.RFS_CopyRemote.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
        self.RFS_CopyRemote.restype  = ctypes.c_long

        #M1COM SINT32 RFS_Remove(M1C_H_TARGET targetHandle, CHAR *filename); 
        self.RFS_Remove = m1Dll.RFS_Remove
        self.RFS_Remove.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.RFS_Remove.restype  = ctypes.c_long

        # SSL certificate import functions
        crypt32 = ctypes.WinDLL("crypt32.dll", use_last_error=True)

        self.PFXImportCertStore = crypt32.PFXImportCertStore
        self.PFXImportCertStore.argtypes = [ctypes.POINTER(CRYPT_DATA_BLOB), ctypes.wintypes.LPCWSTR, ctypes.wintypes.DWORD]
        self.PFXImportCertStore.restype = ctypes.c_void_p

        self.CertEnumCertificatesInStore = crypt32.CertEnumCertificatesInStore
        self.CertEnumCertificatesInStore.argtypes = [ctypes.c_void_p, ctypes.POINTER(CERT_CONTEXT)]
        self.CertEnumCertificatesInStore.restype = ctypes.POINTER(CERT_CONTEXT)

        self.CertCloseStore = crypt32.CertCloseStore
        self.CertCloseStore.argtypes = [ctypes.c_void_p, ctypes.wintypes.DWORD]
        self.CertCloseStore.restype = ctypes.wintypes.BOOL

    def getDllVersion(self):
        """Return the DLL version of the m1com.dll.

        >>> dll = PyCom()
        >>> dll.getDllVersion()
        'V1.14.99 Release'
        """

        version = ctypes.c_char_p(40*"".encode('utf-8'))    #40byte buffer
        self.M1C_GetVersion(version, 40)
        return version.value.decode('utf-8')

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
    >>> mh.getConnectionState()                                                                 # doctest: +SKIP
    'ONLINE'
    >>> mh.getTargetState()                                                                     # doctest: +SKIP
    {'appState': 'RES_S_RUN', 'rebootCount': 100}
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
    >>> mh.setUintParam('M1C_IGNORE_SERVER_CERT', 1)
    >>> mh.getUintParam('M1C_IGNORE_SERVER_CERT')
    1
    >>> mh.setStringParam('M1C_PROXY_USERNAME', 'Example')
    >>> mh.getStringParam('M1C_PROXY_USERNAME')
    'Example'
    >>> mh.getMaxCallSize()
    8148
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
    
    def connect(self, protocol='TCP', clientCert=None, clientCertPassword=None, timeout=1000):
        """
        Make a connection with the target using the protocols: 'TCP', 'QSOAP', 'SSL' or 'UDP'. When using SSL with client certificate, the path of the client certificate (*.p12 file)
        and its password should be specified using the clientCert and clientCertPassword arguments respectively.
        """
        if protocol == 'TCP':
            protocol = PROTOCOL_TCP
        elif protocol == 'QSOAP':
            protocol = PROTOCOL_QSOAP
        elif protocol == 'SSL':
            protocol = PROTOCOL_SSL
            if clientCert == None and clientCertPassword != None:
                raise PyComException(("pyCom Error: Also provide the client certificate when providing a client certificate password!"))
            if clientCert != None and not os.path.isfile(clientCert):
                raise PyComException(("pyCom Error: Provided path to the client certificate cannot be found!"))
            if clientCert != None and clientCertPassword == None:
                raise PyComException(("pyCom Error: Provide a password for the client certificate!"))
        elif protocol == 'UDP':
            protocol = PROTOCOL_UDP
        else:
            raise PyComException(("pyCom Error: Unknown protocol '"+str(protocol)+"' given as argument. Use 'TCP', 'QSOAP', 'SLL' or 'UDP'!"))

        if(self._ctrlHandle == None):
            self._ctrlHandle = self._pycom.TARGET_Create(self._ip.encode('utf-8'), protocol, timeout)
            if(self._ctrlHandle == None):
                raise PyComException(("pyCom Error: Can't create handle to "+self._ip+" through '"+repr(protocol)+"' with username:"+self._username))

            if protocol == PROTOCOL_SSL:
                if(self._pycom.TARGET_SetUintParam(self._ctrlHandle, M1C_IGNORE_SERVER_CERT, True) != OK):
                    raise PyComException(("pyCom Error: Can't set uint parameter M1C_IGNORE_SERVER_CERT to True for "+self._ip))

            if protocol == PROTOCOL_SSL and clientCert != None and clientCertPassword != None:

                PFX = CRYPT_DATA_BLOB()
                fp = open(clientCert, 'rb')
                buffer = fp.read()
                fp.close()
                byteArray = WINBYTE_ARRAY(len(buffer))
                for i in range(len(buffer)):
                    byteArray.ARRAY[i] = buffer[i]
                PFX.pbData = byteArray.ARRAY
                PFX.cbData = len(buffer)
                storeHandle = self._pycom.PFXImportCertStore(ctypes.pointer(PFX), clientCertPassword, PKCS12_ALLOW_OVERWRITE_KEY | PKCS12_NO_PERSIST_KEY)
                if storeHandle == None:
                    raise PyComException(("pyCom Error: Could not import client certificate in store, incorrect password?"))

                pCertCtx = self._pycom.CertEnumCertificatesInStore(storeHandle, None)
                if pCertCtx:
                    CERT_CONTEXT = pCertCtx[0]
                else:
                    raise PyComException(("pyCom Error: Could not get context of certificate"))

                if(self._pycom.TARGET_SetSSLClientCertificateContext(self._ctrlHandle, ctypes.pointer(CERT_CONTEXT)) != OK):
                    raise PyComException(("pyCom Error: Can't set SSL client certificate context to "+self._ip))

            if(self._pycom.TARGET_Connect(self._ctrlHandle, self._username.encode('utf-8'), self._password.encode('utf-8'), self._pycom.servicename.encode('utf-8')) != OK):
                raise PyComException(("pyCom Error: Can't connect to "+self._ip+" through '"+repr(protocol)+"' with username:"+self._username))

            if protocol == PROTOCOL_SSL and clientCert != None and clientCertPassword != None:
                if(self._pycom.CertCloseStore(storeHandle, CERT_CLOSE_STORE_FORCE_FLAG) == False):
                    raise PyComException(("pyCom Error: Can't close certificate store to "+self._ip))

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
            recv = RES_LOGIN2_R() 
            if(self._pycom.TARGET_GetLoginInfo(self._ctrlHandle, ctypes.pointer(recv)) != OK):
                raise PyComException(("pyCom Error: Cannot get login info of Controller["+self._ip+"]"))

        return ctypesInfo2dict(recv)
    
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

    def getConnectionState(self):
        """
        Get the state of the communication. Returns 'ONLINE', 'OFFLINE' or 'ERROR'.
        """
        state = ctypes.c_uint()
        if(self._pycom.TARGET_GetConnectionState(self.getCtrlHandle(), ctypes.pointer(state)) != OK):
            raise PyComException(("pyCom Error: Can't get connection state of Controller["+self._ip+"]"))

        if state.value == ONLINE:
            return 'ONLINE'
        elif state.value == OFFLINE:
            return 'OFFLINE'
        elif state.value == ERROR:
            return 'ERROR'
        else:
            raise PyComException(("pyCom Error: Get connection state returned unknown value "+str(state.value)+" for Controller["+self._ip+"]"))

    def getTargetState(self):
        """
        Get the state of the target. Returns the appstate and the reboot count. Appstate can have the following returns:
        'RES_S_RUN'         --> Resource is OK and runs
        'RES_S_ERROR'       --> Resource is in error
        'RES_S_STOP'        --> Resource has been stopped
        'RES_S_INIT'        --> Resource is being initialized
        'RES_S_DEINIT'      --> Resource has been un-installed
        'RES_S_EOI'         --> Resource waits for #SMI_PROC_ENDOFINIT
        'RES_S_RESET'       --> Resource is in reset state
        'RES_S_WARNING'     --> Resource is in warning state
        'RES_S_ERROR_SMART' --> Resource is in S.M.A.R.T. error state
        """
        appState = ctypes.c_uint16()
        rebootCount = ctypes.c_uint16()
        if(self._pycom.TARGET_GetTargetState(self.getCtrlHandle(), ctypes.pointer(appState), ctypes.pointer(rebootCount)) != OK):
            raise PyComException(("pyCom Error: Can't get target state of Controller["+self._ip+"]"))

        if appState.value == RES_S_RUN:
            appState = 'RES_S_RUN'
        elif appState.value == RES_S_ERROR:
            appState = 'RES_S_ERROR'
        elif appState.value == RES_S_STOP:
            appState = 'RES_S_STOP'
        elif appState.value == RES_S_INIT:
            appState = 'RES_S_INIT'
        elif appState.value == RES_S_DEINIT:
            appState = 'RES_S_DEINIT'
        elif appState.value == RES_S_EOI:
            appState = 'RES_S_EOI'
        elif appState.value == RES_S_RESET:
            appState = 'RES_S_RESET'
        elif appState.value == RES_S_WARNING:
            appState = 'RES_S_WARNING'
        else:
            raise PyComException(("pyCom Error: Get target state returned unknown value for appState["+str(appState.value)+"] for Controller["+self._ip+"]"))

        return {'appState': appState, 'rebootCount': rebootCount.value}

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
            py_modulelist[myModuleNames.ARRAY[num].name.decode('utf-8')] = _M1SwModule(myModuleNames.ARRAY[num].name.decode('utf-8'), self)

        return py_modulelist

    def getDrvId(self, CardNb):
        """
        Get DrvId from CardNb.
        """        
        
        send = MIO_GETDRV_C()
        send.CardNb = CardNb
        recv = MIO_GETDRV_R()
        
        mio = self._pycom.TARGET_CreateModule(self._ctrlHandle, b"MIO")
        if(self._pycom.MODULE_Connect(mio) != OK):
            raise PyComException(("pyCom Error: Could not connect to module[MIO] on Controller['"+self._ip+"']"))
        
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
        if(self._pycom.MODULE_Connect(mio) != OK):
            raise PyComException(("pyCom Error: Could not connect to module[MIO] on Controller['"+self._ip+"']"))

        if(self._pycom.MODULE_SendCall(mio, ctypes.c_uint(100), ctypes.c_uint(2), ctypes.pointer(send), ctypes.sizeof(send), ctypes.pointer(recv), ctypes.sizeof(recv), 3000) != OK):
            raise PyComException(("m1com Error: Can't send procedure number " + mio + " to Controller['"+self._ip+"']"))
        
        send = MIO_GETCDINF_C()
        send.DrvId = recv.DrvId
        recv = MIO_GETCDINF_R()
         
        if(self._pycom.MODULE_SendCall(mio, ctypes.c_uint(130), ctypes.c_uint(2), ctypes.pointer(send), ctypes.sizeof(send), ctypes.pointer(recv), ctypes.sizeof(recv), 3000) != OK):
            raise PyComException(("m1com Error: Can't send procedure number " + mio + " to Controller['"+self._ip+"']"))

        return ctypesInfo2dict(recv.Inf)
    
    def getCardInfoExt(self, CardNb):
        """
        Get extended card information from CardNb.
        """        
        send = MIO_GETEXTCDINF_C()
        send.CardNb = CardNb
        recv = MIO_GETEXTCDINF_R()

        mio = self._pycom.TARGET_CreateModule(self._ctrlHandle, b"MIO")
        if(self._pycom.MODULE_Connect(mio) != OK):
            raise PyComException(("pyCom Error: Could not connect to module[MIO] on Controller['"+self._ip+"']"))
         
        if(self._pycom.MODULE_SendCall(mio, ctypes.c_uint(136), ctypes.c_uint(2), ctypes.pointer(send), ctypes.sizeof(send), ctypes.pointer(recv), ctypes.sizeof(recv), 3000) != OK):
            raise PyComException(("m1com Error: Can't send procedure number " + mio + " to Controller['"+self._ip+"']"))

        return ctypesInfo2dict(recv.Inf)

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
        if(self._pycom.MODULE_Connect(info) != OK):
            raise PyComException(("pyCom Error: Could not connect to module[INFO] on Controller['"+self._ip+"']"))

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
        if(self._pycom.RFS_CopyFromTarget(self.getCtrlHandle(), localFileName.encode('utf-8'), remoteFileName.encode('utf-8')) != OK):
            raise PyComException(("pyCom Error: Can't get copy " + remoteFileName + " from Controller['"+self._ip+"']"))

    def copyToTarget(self, localFileName, remoteFileName):
        """
        Copy a local file to the target.
        """
        if(self._pycom.RFS_CopyToTarget(self.getCtrlHandle(), remoteFileName.encode('utf-8'), localFileName.encode('utf-8')) != OK):
            raise PyComException(("pyCom Error: Can't copy " + localFileName + " to Controller['"+self._ip+"']"))

    def copyRemote(self, srcFile, destFile):
        """
        Copy a file on the target and save it somewhere else on the target.
        """
        if(self._pycom.RFS_CopyRemote(self.getCtrlHandle(), destFile.encode('utf-8'), srcFile.encode('utf-8')) != OK):
            raise PyComException(("pyCom Error: Can't copy " + destFile + " to " + srcFile + " on Controller['"+self._ip+"']"))

    def remove(self, remoteFileName):
        """
        Remove a file on the target.
        """
        if(self._pycom.RFS_Remove(self.getCtrlHandle(), remoteFileName.encode('utf-8')) != OK):
            raise PyComException(("pyCom Error: Can't remove " + remoteFileName + " on Controller['"+self._ip+"']"))
    
    def reboot(self):
        """
        Reboot the target.
        """
        mod = self._pycom.TARGET_CreateModule(self.getCtrlHandle(), b"MOD")        
        if(self._pycom.MODULE_Connect(mod) != OK):
            raise PyComException(("pyCom Error: Could not connect to module[MOD] on Controller['"+self._ip+"']"))

        send = ctypes.c_int32(0)
        recv = ctypes.c_int32(0)        
        if(self._pycom.MODULE_SendCall(mod, ctypes.c_uint(134), ctypes.c_uint(2), ctypes.pointer(send), 4, ctypes.pointer(recv), 4, 3000) != OK):
            raise PyComException(("m1com Error: Can't send procedure number " + mod + " to Controller['"+self._ip+"']"))

    def resetAll(self):
        """
        Reset all applications on the target.
        """
        mod = self._pycom.TARGET_CreateModule(self.getCtrlHandle(), b"MOD")        
        if(self._pycom.MODULE_Connect(mod) != OK):
            raise PyComException(("pyCom Error: Could not connect to module[MOD] on Controller['"+self._ip+"']"))
        send = ctypes.c_int32(0)
        recv = ctypes.c_int32(0)        
        if(self._pycom.MODULE_SendCall(mod, ctypes.c_uint(142), ctypes.c_uint(2), ctypes.pointer(send), 4, ctypes.pointer(recv), 4, 3000) != OK):
            raise PyComException(("m1com Error: Can't reset all models on Controller['"+self._ip+"']"))

    def sendCall(self, moduleName, proc, send, recv, timeout=1000, version=2):
        """
        Send a custom SMI call to the target.
        """
        mod = self._pycom.TARGET_CreateModule(self.getCtrlHandle(), moduleName.encode('utf-8'))
        if (self._pycom.MODULE_Connect(mod) != OK):
            raise PyComException(("pyCom Error: Could not connect to module["+str(moduleName)+"] on Controller['"+self._ip+"']"))
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
            ctypes.c_uint(timeout))
        if(returnSendCall != OK):
            errorMsg = self.getErrorInfo(returnSendCall)
            raise PyComException(("pyCom Error: Can't send procedure number " + str(proc) + " to Controller['"+self._ip+"']: " + str(errorMsg)))
        return recv

    def setUintParam(self, key, value):
        """
        Sets a special parameter for the target. Possible keys are: 'M1C_PROXY_USED', 'M1C_PROXY_PORT', 'M1C_QSOAP_PORT',
        'M1C_IGNORE_SERVER_CERT', 'M1C_COUNT_SOCKETS', 'M1C_IGNORE_SERVER_CERT_CN' and 'M1C_LOGIN2_USER_PARAM'.
        """
        if key == 'M1C_PROXY_USED':
            key = M1C_PROXY_USED
        elif key == 'M1C_PROXY_PORT':
            key = M1C_PROXY_PORT
        elif key == 'M1C_QSOAP_PORT':
            key = M1C_QSOAP_PORT
        elif key == 'M1C_IGNORE_SERVER_CERT':
            key = M1C_IGNORE_SERVER_CERT
        elif key == 'M1C_COUNT_SOCKETS':
            key = M1C_COUNT_SOCKETS
        elif key == 'M1C_IGNORE_SERVER_CERT_CN':
            key = M1C_IGNORE_SERVER_CERT_CN
        elif key == 'M1C_LOGIN2_USER_PARAM':
            key = M1C_LOGIN2_USER_PARAM
        else:
            raise PyComException(("pyCom Error: Unknown uint parameter "+str(key)+" for "+self._ip))

        if type(value) != int and type(value) != bool:
            raise PyComException(("pyCom Error: Argument 'value' should be of type 'int' or 'bool' and not type "+str(type(value))))
        if type(value) == bool:
            value = int(value)

        if(self._pycom.TARGET_SetUintParam(self._ctrlHandle, key, value) != OK):
            raise PyComException(("pyCom Error: Can't set uint parameter "+str(key)+" to "+str(value)+" for "+self._ip))

    def setStringParam(self, key, value):
        """
        Sets a special parameter for the target. Possible keys are: 'M1C_PROXY_HOST', 'M1C_PROXY_USERNAME', 'M1C_PROXY_PASSWD',
        'M1C_QSOAP_PATH' and 'M1C_VHD_SESSIONNAME'.
        """
        if key == 'M1C_PROXY_HOST':
            key = M1C_PROXY_HOST
        elif key == 'M1C_PROXY_USERNAME':
            key = M1C_PROXY_USERNAME
        elif key == 'M1C_PROXY_PASSWD':
            key = M1C_PROXY_PASSWD
        elif key == 'M1C_QSOAP_PATH':
            key = M1C_QSOAP_PATH
        elif key == 'M1C_VHD_SESSIONNAME':
            key = M1C_VHD_SESSIONNAME
        else:
            raise PyComException(("pyCom Error: Unknown string parameter "+str(key)))

        if type(value) != str:
            raise PyComException(("pyCom Error: Argument 'value' should be of type 'str'"))

        if(self._pycom.TARGET_SetStringParam(self._ctrlHandle, key, value.encode('utf-8'), len(value)) != OK):
            raise PyComException(("pyCom Error: Can't set string parameter "+str(key)+" to "+str(value)+" for "+self._ip))

    def getUintParam(self, key):
        """
        Gets the value of a special parameter for the target. Possible keys are: 'M1C_PROXY_USED', 'M1C_PROXY_PORT', 'M1C_QSOAP_PORT',
        'M1C_IGNORE_SERVER_CERT', 'M1C_COUNT_SOCKETS', 'M1C_IGNORE_SERVER_CERT_CN' and 'M1C_LOGIN2_USER_PARAM'.
        """
        if key == 'M1C_PROXY_USED':
            key = M1C_PROXY_USED
        elif key == 'M1C_PROXY_PORT':
            key = M1C_PROXY_PORT
        elif key == 'M1C_QSOAP_PORT':
            key = M1C_QSOAP_PORT
        elif key == 'M1C_IGNORE_SERVER_CERT':
            key = M1C_IGNORE_SERVER_CERT
        elif key == 'M1C_COUNT_SOCKETS':
            key = M1C_COUNT_SOCKETS
        elif key == 'M1C_IGNORE_SERVER_CERT_CN':
            key = M1C_IGNORE_SERVER_CERT_CN
        elif key == 'M1C_LOGIN2_USER_PARAM':
            key = M1C_LOGIN2_USER_PARAM
        else:
            raise PyComException(("pyCom Error: Unknown uint parameter "+str(key)+" for "+self._ip))

        return self._pycom.TARGET_GetUintParam(self._ctrlHandle, key)

    def getStringParam(self, key):
        """
        Gets the value of a special parameter from the target. Possible keys are: 'M1C_PROXY_HOST', 'M1C_PROXY_USERNAME', 'M1C_PROXY_PASSWD',
        'M1C_QSOAP_PATH' and 'M1C_VHD_SESSIONNAME'.
        """
        if key == 'M1C_PROXY_HOST':
            key = M1C_PROXY_HOST
        elif key == 'M1C_PROXY_USERNAME':
            key = M1C_PROXY_USERNAME
        elif key == 'M1C_PROXY_PASSWD':
            key = M1C_PROXY_PASSWD
        elif key == 'M1C_QSOAP_PATH':
            key = M1C_QSOAP_PATH
        elif key == 'M1C_VHD_SESSIONNAME':
            key = M1C_VHD_SESSIONNAME
        else:
            raise PyComException(("pyCom Error: Unknown string parameter "+str(key)))

        value = self._pycom.TARGET_GetStringParam(self._ctrlHandle, key)

        if type(value) == bytes:
            return str(value.decode('utf-8'))
        else:
            return str(value)

    def getMaxCallSize(self):
        """
        Gets the maximum length of an rpc call.
        """
        size = ctypes.c_uint()
        if(self._pycom.TARGET_GetMaxCallSize(self._ctrlHandle, ctypes.pointer(size)) != OK):
            raise PyComException(("pyCom Error: Can't get max call size for controller["+self._ip+"]"))

        return size.value

    def getErrorInfo(self, errorCode):
        """
        Gets the source and message information of an error. The argument 'errorCode' can be any m1com error code 
        such as: m1com.M1C_E_MEM_ALLOC, m1com.M1C_E_INVALID_PARTNER, m1com.M1C_E_WSA_INIT, etc. or a not yet
        defined error code number as integer value.
        """
        errorSrc = ctypes.create_string_buffer(200)
        errorMsg = ctypes.create_string_buffer(200)

        self._pycom.GetErrorSrc(ctypes.c_long(errorCode), errorSrc, ctypes.c_uint(errorSrc._length_))
        self._pycom.GetErrorMsg(ctypes.c_long(errorCode), errorMsg, ctypes.c_uint(errorMsg._length_))

        return {"errorSrc":errorSrc.value.decode('utf-8'), "errorMsg":errorMsg.value.decode('utf-8')}

class M1Application:
    """
    The M1Application class. Can be used to stop, start, reset, deinit an application on a target.

    Usage:

    >>> mh = M1Controller(ip='169.254.141.136')
    >>> mh.connect(timeout=3000)
    >>> app = M1Application('SVIWRITE', mh)                                                     # doctest: +SKIP
    >>> app.stop()                                                                              # doctest: +SKIP
    >>> app.start()                                                                             # doctest: +SKIP
    >>> app.reset()                                                                             # doctest: +SKIP
    >>> app.deinit()                                                                            # doctest: +SKIP
    >>> app.getInfo()                                                                           # doctest: +SKIP
    >>> app.getState()                                                                          # doctest: +SKIP
    >>> mh.disconnect()
    0
    """

    def __init__(self, applicationName, m1controller):

        if type(applicationName) != str:
            raise PyComException(("pyCom Error: Expected 'applicationName' argument to be of type 'str'!"))
        if len(applicationName) > 8:
            print("pyCom Warning: Argument 'applicationName' longer than 8 characters and will be sliced to "+applicationName[0:8].upper()+"!")
            applicationName = applicationName[0:8]

        self.applicationName = applicationName.upper()
        self._m1ctrl = m1controller

    def deinit(self):
        """
        Deinitializes the application on the target.
        """
        send = SMI_DEINIT_C()
        send.AppName = self.applicationName.encode('utf-8')
        recv = SMI_DEINIT_R()
        self._m1ctrl.sendCall(self.applicationName, 4, send, recv)
        if recv.RetCode == SMI_E_OK:
            pass
        elif recv.RetCode == SMI_E_NAME:
            raise PyComException(("pyCom Error: Could not deinitialize software module on target Controller["+self._m1ctrl._ip+"], Function not possible, because the instance does not exist!"))
        elif recv.RetCode == SMI_E_FAILED:
            raise PyComException(("pyCom Error: Could not deinitialize software module on target Controller["+self._m1ctrl._ip+"], The function could not be executed properly!"))
        else:
            raise PyComException(("pyCom Error: Unknown return code '"+str(recv.RetCode)+"' for deinit on target Controller["+self._m1ctrl._ip+"]!"))

    def reset(self):
        """
        Resets the application on the target.
        """
        send = SMI_RESET_C()
        send.AppName = self.applicationName.encode('utf-8')
        recv = SMI_RESET_R()
        self._m1ctrl.sendCall(self.applicationName, 6, send, recv)
        if recv.RetCode == SMI_E_OK:
            send = SMI_ENDOFINIT_C()
            send.AppName = self.applicationName.encode('utf-8')
            recv = SMI_ENDOFINIT_R()
            self._m1ctrl.sendCall(self.applicationName, 14, send, recv)
            if recv.RetCode == SMI_E_OK:
                pass
            elif recv.RetCode == SMI_E_NAME:
                raise PyComException(("pyCom Error: Could not reset software module on target Controller["+self._m1ctrl._ip+"], Function not possible, because the instance does not exist!"))
            elif recv.RetCode == SMI_E_FAILED:
                raise PyComException(("pyCom Error: Could not reset software module on target Controller["+self._m1ctrl._ip+"], The function could not be executed properly!"))
            else:
                raise PyComException(("pyCom Error: Unknown return code '"+str(recv.RetCode)+"' for reset on target Controller["+self._m1ctrl._ip+"]!"))
        elif recv.RetCode == SMI_E_NAME:
            raise PyComException(("pyCom Error: Could not reset software module on target Controller["+self._m1ctrl._ip+"], Function not possible, because the instance does not exist!"))
        elif recv.RetCode == SMI_E_FAILED:
            raise PyComException(("pyCom Error: Could not reset software module on target Controller["+self._m1ctrl._ip+"], The function could not be executed properly!"))
        else:
            raise PyComException(("pyCom Error: Unknown return code '"+str(recv.RetCode)+"' for reset on target Controller["+self._m1ctrl._ip+"]!"))

    def stop(self):
        """
        Stops the application on the target.
        """
        send = SMI_STOP_C()
        send.AppName = self.applicationName.encode('utf-8')
        recv = SMI_STOP_R()
        self._m1ctrl.sendCall(self.applicationName, 18, send, recv)
        if recv.RetCode == SMI_E_OK:
            pass
        elif recv.RetCode == SMI_E_NAME:
            raise PyComException(("pyCom Error: Could not stop software module on target Controller["+self._m1ctrl._ip+"], Function not possible, because the instance does not exist!"))
        elif recv.RetCode == SMI_E_FAILED:
            raise PyComException(("pyCom Error: Could not stop software module on target Controller["+self._m1ctrl._ip+"], The function could not be executed properly!"))
        else:
            raise PyComException(("pyCom Error: Unknown return code '"+str(recv.RetCode)+"' for stop on target Controller["+self._m1ctrl._ip+"]!"))

    def init(self):
        """
        Initializes the application on the target.
        """
        send = SMI_INIT_C()
        send.AppName = self.applicationName.encode('utf-8')
        recv = SMI_INIT_R()
        self._m1ctrl.sendCall(self.applicationName, 2, send, recv)
        if recv.RetCode == SMI_E_OK:
            pass
        elif recv.RetCode == SMI_E_NAME:
            raise PyComException(("pyCom Error: Could not restart software module on target Controller["+self._m1ctrl._ip+"], Function not possible, because the instance does not exist!"))
        elif recv.RetCode == SMI_E_FAILED:
            raise PyComException(("pyCom Error: Could not restart software module on target Controller["+self._m1ctrl._ip+"], The function could not be executed properly!"))
        elif recv.RetCode == SMI_E_SUPPORT:
            raise PyComException(("pyCom Error: Could not restart software module on target Controller["+self._m1ctrl._ip+"], Function not supported!"))
        elif recv.RetCode == SMI_E_NOMEM:
            raise PyComException(("pyCom Error: Could not restart software module on target Controller["+self._m1ctrl._ip+"], Not enough system memory!"))
        else:
            raise PyComException(("pyCom Error: Unknown return code '"+str(recv.RetCode)+"' for run on target Controller["+self._m1ctrl._ip+"]!"))

    def start(self):
        """
        Starts the stopped application on the target.
        """
        send = SMI_RUN_C()
        send.AppName = self.applicationName.encode('utf-8')
        recv = SMI_RUN_R()
        self._m1ctrl.sendCall(self.applicationName, 20, send, recv)
        if recv.RetCode == SMI_E_OK:
            pass
        elif recv.RetCode == SMI_E_NAME:
            raise PyComException(("pyCom Error: Could not restart software module on target Controller["+self._m1ctrl._ip+"], Function not possible, because the instance does not exist!"))
        elif recv.RetCode == SMI_E_FAILED:
            raise PyComException(("pyCom Error: Could not restart software module on target Controller["+self._m1ctrl._ip+"], The function could not be executed properly!"))
        else:
            raise PyComException(("pyCom Error: Unknown return code '"+str(recv.RetCode)+"' for run on target Controller["+self._m1ctrl._ip+"]!"))

    def getInfo(self):
        """
        Gets info about the application from the target.
        """
        send = RES_MODXINFO_C()
        send.AppName = self.applicationName.encode('utf-8')
        recv = RES_MODXINFO_R()
        self._m1ctrl.sendCall('RES', 116, send, recv)
        if recv.RetCode != OK:
            raise PyComException(("pyCom Error: Could not get information about application from target Controller["+self._m1ctrl._ip+"]!"))

        return ctypesInfo2dict(recv.Inf)

    def getState(self):
        """
        Gets the current state of the application from the target.
        """
        appState = self.getInfo()['State']
        if appState == RES_S_RUN:
            appState = 'RES_S_RUN'
        elif appState == RES_S_ERROR:
            appState = 'RES_S_ERROR'
        elif appState == RES_S_STOP:
            appState = 'RES_S_STOP'
        elif appState == RES_S_INIT:
            appState = 'RES_S_INIT'
        elif appState == RES_S_DEINIT:
            appState = 'RES_S_DEINIT'
        elif appState == RES_S_EOI:
            appState = 'RES_S_EOI'
        elif appState == RES_S_RESET:
            appState = 'RES_S_RESET'
        elif appState == RES_S_WARNING:
            appState = 'RES_S_WARNING'
        else:
            raise PyComException(("pyCom Error: Get target state returned unknown value for appState["+str(appState.value)+"] for Controller["+self._ip+"]"))

        return appState

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
            sviHandle = self.m1ctrl._pycom.TARGET_CreateVariable(self.m1ctrl.getCtrlHandle(), sviName.encode('utf-8'))
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

            identifiyer = self.m1ctrl._pycom.VARIABLE_getBaseDataType(self._sviInfos[i])
            if not(self._sviInfos[i].format & SVI_F_OUT):
                raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] is not readable!")
            if(self._sviInfos[i].format & SVI_F_BLK):
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append(ctypes.create_string_buffer(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append(['char8'])
                elif (identifiyer == SVI_F_CHAR16):
                    self._sviValues.append(ctypes.create_unicode_buffer(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append(['char16'])
                elif(identifiyer == SVI_F_UINT64):
                    if self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) > 1:
                        self._sviValues.append(ULONGLONG_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                        self._sviTypes.append([int])
                    else:
                        self._sviValues.append(ctypes.c_ulonglong())
                        self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT64):
                    if self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) > 1:
                        self._sviValues.append(LONGLONG_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                        self._sviTypes.append([int])
                    else:
                        self._sviValues.append(ctypes.c_longlong())
                        self._sviTypes.append(int)
                elif(identifiyer == SVI_F_REAL64):
                    if self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) > 1:
                        self._sviValues.append(DOUBLE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                        self._sviTypes.append([float])
                    else:
                        self._sviValues.append(ctypes.c_double())
                        self._sviTypes.append(float)
                elif(identifiyer == SVI_F_MIXED):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_UINT1):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([bool])
                elif(identifiyer == SVI_F_UINT8):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_BOOL8):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([bool])
                elif(identifiyer == SVI_F_UINT16):
                    self._sviValues.append(USHORT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_UINT32):
                    self._sviValues.append(UINT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_SINT8):
                    self._sviValues.append(BYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_SINT16):
                    self._sviValues.append(SHORT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_SINT32):
                    self._sviValues.append(LONG_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_REAL32):
                    self._sviValues.append(FLOAT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([float])
                elif(identifiyer == SVI_F_STRINGLSTBASE):
                    self._sviValues.append(ctypes.create_string_buffer(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([str])
                elif(identifiyer == SVI_F_USTRINGLSTBASE):
                    self._sviValues.append(UNICODE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append(['ustr'])
                else:
                    raise PyComException("pyCom Error: unknown SVIBLK Type!"+str(self._sviInfos[i].format)+" of Variable:"+self.sviNames[i])
            else:
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append(ctypes.c_char())
                    self._sviTypes.append('char8')
                elif(identifiyer == SVI_F_CHAR16):
                    self._sviValues.append(ctypes.c_wchar())
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
            if hasattr(self._sviValues[i], 'ARRAY'):
                self._sviBuffers.ARRAY[i].buffer = ctypes.cast(self._sviValues[i].ARRAY, ctypes.c_char_p)
            else:
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
                if hasattr(self._sviValues[self._indicesChanged[i]], 'value') and self._sviTypes[self._indicesChanged[i]] != [str]:
                    value = self._sviValues[self._indicesChanged[i]].value
                else:
                    value = self._sviValues[self._indicesChanged[i]]

                if type(value) == bytes:
                    value = str(value.decode('utf-8'))
                elif self._sviTypes[self._indicesChanged[i]] == 'char8' or self._sviTypes[self._indicesChanged[i]] == ['char8']:
                    value = str(value.decode('utf-8'))
                elif self._sviTypes[self._indicesChanged[i]] == 'char16' or self._sviTypes[self._indicesChanged[i]] == ['char16']:
                    value = str(value)
                elif self._sviTypes[self._indicesChanged[i]] == [bool]:
                    value = [bool(value.ARRAY[i]) for i in range(value.array_size)]
                elif self._sviTypes[self._indicesChanged[i]] == [int]:
                    value = [int(value.ARRAY[i]) for i in range(value.array_size)]
                elif self._sviTypes[self._indicesChanged[i]] == [float]:
                    value = [float(value.ARRAY[i]) for i in range(value.array_size)]
                elif self._sviTypes[self._indicesChanged[i]] == [str]:
                    value = value.raw.decode('utf-8').split('\x00')
                    value = value[0:len(value)-1]
                elif self._sviTypes[self._indicesChanged[i]] == ['ustr']:
                    value = [str(value.ARRAY[i]) for i in range(value.array_size)]
                    value = ''.join(value).split('\x00')
                    value = value[0:len(value)-1]
                else:
                    value = self._sviTypes[self._indicesChanged[i]](value)
                variables.update({self.sviNames[self._indicesChanged[i]]:value})
        else:
            for i in range(self._countVariables):
                if hasattr(self._sviValues[i], 'value') and self._sviTypes[i] != [str] and self._sviTypes[i] != ['ustr']:
                    value = self._sviValues[i].value
                else:
                    value = self._sviValues[i]

                if type(value) == bytes:
                    value = str(value.decode('utf-8'))
                elif self._sviTypes[i] == 'char8' or self._sviTypes[i] == ['char8']:
                    value = str(value.decode('utf-8'))
                elif self._sviTypes[i] == 'char16' or self._sviTypes[i] == ['char16']:
                    value = str(value)
                elif self._sviTypes[i] == [bool]:
                    value = [bool(value.ARRAY[i]) for i in range(value.array_size)]
                elif self._sviTypes[i] == [int]:
                    value = [int(value.ARRAY[i]) for i in range(value.array_size)]
                elif self._sviTypes[i] == [float]:
                    value = [float(value.ARRAY[i]) for i in range(value.array_size)]
                elif self._sviTypes[i] == [str]:
                    value = value.raw.decode('utf-8').split('\x00')
                    value = value[0:len(value)-1]
                elif self._sviTypes[i] == ['ustr']:
                    value = [str(value.ARRAY[i]) for i in range(value.array_size)]
                    value = ''.join(value).split('\x00')
                    value = value[0:len(value)-1]
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
        self._sviTypes = None
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
            sviHandle = self.m1ctrl._pycom.TARGET_CreateVariable(self.m1ctrl.getCtrlHandle(), sviName.encode('utf-8'))
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

            identifiyer = self.m1ctrl._pycom.VARIABLE_getBaseDataType(self._sviInfos[i])
            if not(self._sviInfos[i].format & SVI_F_OUT):
                raise PyComException("pyCom Error: SVI Variable["+self.sviNames[i]+"] is not readable!")
            if(self._sviInfos[i].format & SVI_F_BLK):
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append(ctypes.create_string_buffer(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append(['char8'])
                elif (identifiyer == SVI_F_CHAR16):
                    self._sviValues.append(ctypes.create_unicode_buffer(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append(['char16'])
                elif(identifiyer == SVI_F_UINT64):
                    if self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) > 1:
                        self._sviValues.append(ULONGLONG_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                        self._sviTypes.append([int])
                    else:
                        self._sviValues.append(ctypes.c_ulonglong())
                        self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT64):
                    if self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) > 1:
                        self._sviValues.append(LONGLONG_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                        self._sviTypes.append([int])
                    else:
                        self._sviValues.append(ctypes.c_longlong())
                        self._sviTypes.append(int)
                elif(identifiyer == SVI_F_REAL64):
                    if self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) > 1:
                        self._sviValues.append(DOUBLE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                        self._sviTypes.append([float])
                    else:
                        self._sviValues.append(ctypes.c_double())
                        self._sviTypes.append(float)
                elif(identifiyer == SVI_F_MIXED):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_UINT1):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([bool])
                elif(identifiyer == SVI_F_UINT8):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_BOOL8):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([bool])
                elif(identifiyer == SVI_F_UINT16):
                    self._sviValues.append(USHORT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_UINT32):
                    self._sviValues.append(UINT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_SINT8):
                    self._sviValues.append(BYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_SINT16):
                    self._sviValues.append(SHORT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_SINT32):
                    self._sviValues.append(LONG_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_REAL32):
                    self._sviValues.append(FLOAT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([float])
                elif(identifiyer == SVI_F_STRINGLSTBASE):
                    self._sviValues.append(ctypes.create_string_buffer(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([str])
                elif(identifiyer == SVI_F_USTRINGLSTBASE):
                    self._sviValues.append(UNICODE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append(['ustr'])
                else:
                    raise PyComException("pyCom Error: unknown SVIBLK Type!"+str(self._sviInfos[i].format)+" of Variable:"+self.sviNames[i])
            else:
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append(ctypes.c_char())
                    self._sviTypes.append('char8')
                elif(identifiyer == SVI_F_CHAR16):
                    self._sviValues.append(ctypes.c_wchar())
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
            if hasattr(self._sviValues[i], 'ARRAY'):
                self._sviBuffers.ARRAY[i].buffer = ctypes.cast(self._sviValues[i].ARRAY, ctypes.c_char_p)
            else:
                self._sviBuffers.ARRAY[i].buffer = ctypes.cast(ctypes.pointer(self._sviValues[i]), ctypes.c_char_p)

    def getVariables(self):
        """
        Gets the SVI values of the controller.
        """
        if self.m1ctrl._pycom.TARGET_ReadVariables(self.m1ctrl.getCtrlHandle(), self._sviBuffers.ARRAY, self._countVariables) < 0:
            raise PyComException("pyCom Error: could not read SVI Variables:")

        sviValues = []
        for i in range(self._countVariables):
            if hasattr(self._sviValues[i], 'value') and self._sviTypes[i] != [str] and self._sviTypes[i] != ['ustr']:
                value = self._sviValues[i].value
            else:
                value = self._sviValues[i]

            if type(value) == bytes:
                sviValues.append(str(value.decode('utf-8')))
            elif self._sviTypes[i] == 'char8' or self._sviTypes[i] == ['char8']:
                sviValues.append(str(value.decode('utf-8')))
            elif self._sviTypes[i] == 'char16' or self._sviTypes[i] == ['char16']:
                sviValues.append(str(value))
            elif self._sviTypes[i] == [bool]:
                sviValues.append([bool(value.ARRAY[i]) for i in range(value.array_size)])
            elif self._sviTypes[i] == [int]:
                sviValues.append([int(value.ARRAY[i]) for i in range(value.array_size)])
            elif self._sviTypes[i] == [float]:
                sviValues.append([float(value.ARRAY[i]) for i in range(value.array_size)])
            elif self._sviTypes[i] == [str]:
                value = value.raw.decode('utf-8').split('\x00')
                sviValues.append(value[0:len(value)-1])
            elif self._sviTypes[i] == ['ustr']:
                value = [str(value.ARRAY[i]) for i in range(value.array_size)]
                value = ''.join(value).split('\x00')
                sviValues.append(value[0:len(value)-1])
            else:
                sviValues.append(self._sviTypes[i](value))

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
        self._sviTypes = None
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
            sviHandle = self.m1ctrl._pycom.TARGET_CreateVariable(self.m1ctrl.getCtrlHandle(), sviName.encode('utf-8'))
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

            identifiyer = self.m1ctrl._pycom.VARIABLE_getBaseDataType(self._sviInfos[i])
            if not(self._sviInfos[i].format & SVI_F_IN):
                raise PyComException("pyCom Error: SVI Variable["+self.sviNames[i]+"] is not writable!")
            if(self._sviInfos[i].format & SVI_F_BLK):
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append(ctypes.create_string_buffer(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append(['char8'])
                elif (identifiyer == SVI_F_CHAR16):
                    self._sviValues.append(ctypes.create_unicode_buffer(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append(['char16'])
                elif(identifiyer == SVI_F_UINT64):
                    if self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) > 1:
                        self._sviValues.append(ULONGLONG_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                        self._sviTypes.append([int])
                    else:
                        self._sviValues.append(ctypes.c_ulonglong())
                        self._sviTypes.append(int)
                elif(identifiyer == SVI_F_SINT64):
                    if self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) > 1:
                        self._sviValues.append(LONGLONG_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                        self._sviTypes.append([int])
                    else:
                        self._sviValues.append(ctypes.c_longlong())
                        self._sviTypes.append(int)
                elif(identifiyer == SVI_F_REAL64):
                    if self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) > 1:
                        self._sviValues.append(DOUBLE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                        self._sviTypes.append([float])
                    else:
                        self._sviValues.append(ctypes.c_double())
                        self._sviTypes.append(float)
                elif(identifiyer == SVI_F_MIXED):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_UINT1):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([bool])
                elif(identifiyer == SVI_F_UINT8):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_BOOL8):
                    self._sviValues.append(UBYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([bool])
                elif(identifiyer == SVI_F_UINT16):
                    self._sviValues.append(USHORT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_UINT32):
                    self._sviValues.append(UINT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_SINT8):
                    self._sviValues.append(BYTE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_SINT16):
                    self._sviValues.append(SHORT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_SINT32):
                    self._sviValues.append(LONG_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([int])
                elif(identifiyer == SVI_F_REAL32):
                    self._sviValues.append(FLOAT_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append([float])
                elif(identifiyer == SVI_F_STRINGLSTBASE):
                    self._sviValues.append(ctypes.create_string_buffer(self.m1ctrl._pycom.VARIABLE_GetBufferLen(self._sviInfos[i])))
                    self._sviTypes.append([str])
                elif(identifiyer == SVI_F_USTRINGLSTBASE):
                    self._sviValues.append(UNICODE_ARRAY(self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
                    self._sviTypes.append(['ustr'])
                else:
                    raise PyComException("pyCom Error: unknown SVIBLK Type!"+str(self._sviInfos[i].format)+" of Variable:"+self.sviNames[i])
            else:
                if(identifiyer == SVI_F_CHAR8):
                    self._sviValues.append(ctypes.c_char())
                    self._sviTypes.append('char8')
                elif(identifiyer == SVI_F_CHAR16):
                    self._sviValues.append(ctypes.c_wchar())
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
            if hasattr(self._sviValues[i], 'ARRAY'):
                self._sviBuffers.ARRAY[i].buffer = ctypes.cast(self._sviValues[i].ARRAY, ctypes.c_char_p)
            else:
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
            elif (self._sviTypes[i] == [bool]):
                if type(sviValues[i]) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]))+" elements of type 'bool'")
                if (self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) != len(sviValues[i])):
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]))+" elements of type 'bool'")
                for j in range(len(sviValues[i])):
                    if type(sviValues[i][j]) != bool:
                        raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with type 'bool' elements")
            elif (self._sviTypes[i] == [int]):
                if type(sviValues[i]) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]))+" elements of type 'int'")
                if (self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) != len(sviValues[i])):
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]))+" elements of type 'int'")
                for j in range(len(sviValues[i])):
                    if type(sviValues[i][j]) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with type 'int' elements")
            elif (self._sviTypes[i] == [float]):
                if type(sviValues[i]) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]))+" elements of type 'float'")
                if (self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) != len(sviValues[i])):
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]))+" elements of type 'float'")
                for j in range(len(sviValues[i])):
                    if type(sviValues[i][j]) != float:
                        raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with type 'float' elements")
            elif (self._sviTypes[i] == ['char8']):
                if (self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) < len(sviValues[i]) or type(sviValues[i]) != str):
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'str' with a maximum length of "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
            elif (self._sviTypes[i] == ['char16']):
                if (self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i]) < len(sviValues[i]) or type(sviValues[i]) != str):
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'str' with a maximum length of "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])))
            elif (self._sviTypes[i] == [str] or self._sviTypes[i] == ['ustr']):
                bufferLen = self.m1ctrl._pycom.VARIABLE_GetBufferLen(self._sviInfos[i])
                arrayLen = self.m1ctrl._pycom.VARIABLE_getArrayLen(self._sviInfos[i])
                if type(sviValues[i]) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with type 'str' elements")
                if ((arrayLen % len(sviValues[i])) != 0):
                    raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with correct number of elements of type 'str'")
                for j in range(len(sviValues[i])):
                    if type(sviValues[i][j]) != str:
                        raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'list' with type 'str' elements")
                    if int(bufferLen/len(sviValues[i])) < len(sviValues[i][j]):
                        raise PyComException("pyCom Error: Svi Variable["+self.sviNames[i]+"] expects type 'str' or maximum length "+str(int(bufferLen/len(sviValues[i]))))
            elif type(sviValues[i]) != self._sviTypes[i] and self._sviTypes[i] != 'char8' and self._sviTypes[i] != 'char16' and self._sviTypes[i] != ['char8'] and self._sviTypes[i] != ['char16']:
                raise PyComException("pyCom Error: expects sviValues["+str(i)+"] ("+self.sviNames[i]+") to be of type "+str(self._sviTypes[i])+"!")

            if self._sviTypes[i] == 'char8' or self._sviTypes[i] == ['char8']:
                self._sviValues[i].value = sviValues[i].encode('utf-8')
            elif self._sviTypes[i] == 'char16' or self._sviTypes[i] == ['char16']:
                self._sviValues[i].value = sviValues[i]
            elif self._sviTypes[i] == [bool]:
                for j in range(len(sviValues[i])):
                    self._sviValues[i].ARRAY[j] = sviValues[i][j]
            elif self._sviTypes[i] == [int]:
                for j in range(len(sviValues[i])):
                    self._sviValues[i].ARRAY[j] = sviValues[i][j]
            elif self._sviTypes[i] == [float]:
                for j in range(len(sviValues[i])):
                    self._sviValues[i].ARRAY[j] = sviValues[i][j]
            elif self._sviTypes[i] == [str]:
                bufferLen = self.m1ctrl._pycom.VARIABLE_GetBufferLen(self._sviInfos[i])
                byteArray = ''
                for j in range(len(sviValues[i])):
                    byteArray = byteArray + sviValues[i][j] + '\x00'
                self._sviValues[i].raw = byteArray.encode('utf-8')
            elif self._sviTypes[i] == ['ustr']:
                bufferLen = self.m1ctrl._pycom.VARIABLE_GetBufferLen(self._sviInfos[i])
                byteArray = ''
                for j in range(len(sviValues[i])):
                    byteArray = byteArray + sviValues[i][j] + '\x00'
                for j in range(len(byteArray)):
                    self._sviValues[i].ARRAY[j] = byteArray[j]
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
                            pingInfo[keyword] = getattr(targetsInfo[dev].extPingR, keyword).decode('utf-8')
                        elif hasattr(getattr(targetsInfo[dev].extPingR, keyword), '_type_'):
                            pingInfo[keyword] = ctypesArray2list(getattr(targetsInfo[dev].extPingR, keyword))
                        else:
                            pingInfo[keyword] = getattr(targetsInfo[dev].extPingR, keyword)
                    targetInfo['extPingR'] = pingInfo
                else:
                    if type(getattr(targetsInfo[dev], targetinfoitem)) == bytes:
                        targetInfo[targetinfoitem] = getattr(targetsInfo[dev], targetinfoitem).decode('utf-8')
                    else:
                        targetInfo[targetinfoitem] = getattr(targetsInfo[dev], targetinfoitem)
            self._targets[targetsInfo[dev].extPingR.ProdNb.decode('utf-8')] = targetInfo
                    
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
                pingInfo[keyword] = getattr(buffer, keyword).decode('utf-8')
            elif hasattr(getattr(buffer, keyword), '_type_'):
                pingInfo[keyword] = ctypesArray2list(getattr(buffer, keyword))
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
        self._modHandle = self.m1ctrl._pycom.TARGET_CreateModule(self.m1ctrl.getCtrlHandle(), self.name.encode('utf-8'))
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
            py_svivarlist[myVarEntrys.ARRAY[num].name.decode('utf-8')] = _SVIVariable(myVarEntrys.ARRAY[num].name.decode('utf-8'), self)
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
    'ONLINE'
    >>> sviVariable.getBaseDataType()
    'SVI_F_SINT32'
    >>> sviVariable.checkWritable()
    False
    >>> sviVariable.checkReadable()
    True
    >>> sviVariable.getArrayLen()
    1
    >>> sviVariable.getFullName()
    'RES/CPU/TempCelsius'
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
        return ctypesInfo2dict(self._varInfo)

    def attach(self):
        """
        Creates a handle to a variable and initializes it. This function is already automatically called after initializing a software module.
        """
        self._varHandle = self._m1ctrl._pycom.TARGET_CreateVariable(self._m1ctrl.getCtrlHandle(), self.name.encode('utf-8'))
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
        if(self.getConnectionState() != 'ONLINE'):
            raise PyComException("pyCom Error: read SviVariable["+self.name+"] from Module["+self._module.name+"] on Controller["+self._m1ctrl._ip+"] it is not available!")
        
        value = None
        valueType = None
        identifiyer = self._m1ctrl._pycom.VARIABLE_getBaseDataType(self._varInfo)
        if not(self._varInfo.format & SVI_F_OUT):
            raise PyComException("pyCom Error: Svi Variable["+self.name+"] is not readable!")
        if(self._varInfo.format & SVI_F_BLK):
            if(identifiyer == SVI_F_CHAR8):
                value = ctypes.create_string_buffer(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = ['char8']
            elif (identifiyer == SVI_F_CHAR16):
                value = ctypes.create_unicode_buffer(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = ['char16']
            elif(identifiyer == SVI_F_UINT64):
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) > 1:
                    value = ULONGLONG_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                    valueType = [int]
                else:
                    value = ctypes.c_ulonglong()
                    valueType = int
            elif(identifiyer == SVI_F_SINT64):
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) > 1:
                    value = LONGLONG_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                    valueType = [int]
                else:
                    value = ctypes.c_longlong()
                    valueType = int
            elif(identifiyer == SVI_F_REAL64):
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) > 1:
                    value = DOUBLE_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                    valueType = [float]
                else:
                    value = ctypes.c_double()
                    valueType = float
            elif(identifiyer == SVI_F_MIXED):
                value = UBYTE_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [int]
            elif(identifiyer == SVI_F_UINT1):
                value = UBYTE_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [bool]
            elif(identifiyer == SVI_F_UINT8):
                value = UBYTE_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [int]
            elif(identifiyer == SVI_F_BOOL8):
                value = UBYTE_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [bool]
            elif(identifiyer == SVI_F_UINT16):
                value = USHORT_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [int]
            elif(identifiyer == SVI_F_UINT32):
                value = UINT_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [int]
            elif(identifiyer == SVI_F_SINT8):
                value = BYTE_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [int]
            elif(identifiyer == SVI_F_SINT16):
                value = SHORT_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [int]
            elif(identifiyer == SVI_F_SINT32):
                value = LONG_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [int]
            elif(identifiyer == SVI_F_REAL32):
                value = FLOAT_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [float]
            elif(identifiyer == SVI_F_STRINGLSTBASE):
                value = ctypes.create_string_buffer(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = [str]
            elif(identifiyer == SVI_F_USTRINGLSTBASE):
                value = UNICODE_ARRAY(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))
                valueType = ['ustr']
            else:
                raise PyComException("pyCom Error: unknown SVIBLK Type!"+str(self._varInfo.format)+" of Variable:"+self.name)
        else:
            if(identifiyer == SVI_F_CHAR8):
                value = ctypes.c_char()
                valueType = 'char8'
            elif(identifiyer == SVI_F_CHAR16):
                value = ctypes.c_wchar()
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

        if hasattr(value, 'ARRAY'):
            ret = self._m1ctrl._pycom.TARGET_ReadVariable(self._m1ctrl.getCtrlHandle(), self._varHandle, value.ARRAY, self._bufferLen)
            if ret != 0:
                raise PyComException("pyCom Error: could not read SVI Variable Array:"+self.name)
        else:
            ret = self._m1ctrl._pycom.TARGET_ReadVariable(self._m1ctrl.getCtrlHandle(), self._varHandle, ctypes.pointer(value), self._bufferLen)
            if ret != 0:
                raise PyComException("pyCom Error: could not read SVI Variable:"+self.name)
        if hasattr(value, 'value') and valueType != [str] and valueType != ['ustr']:
            value = value.value

        if type(value) == bytes:
            return str(value.decode('utf-8'))
        elif valueType == 'char8' or valueType == ['char8']:
            return str(value.decode('utf-8'))
        elif valueType == 'char16' or valueType == ['char16']:
            return str(value)
        elif valueType == [bool]:
            return [bool(value.ARRAY[i]) for i in range(value.array_size)]
        elif valueType == [int]:
            return [int(value.ARRAY[i]) for i in range(value.array_size)]
        elif valueType == [float]:
            return [float(value.ARRAY[i]) for i in range(value.array_size)]
        elif valueType == [str]:
            value = value.raw.decode('utf-8').split('\x00')
            return value[0:len(value)-1]
        elif valueType == ['ustr']:
            value = [str(value.ARRAY[i]) for i in range(value.array_size)]
            value = ''.join(value).split('\x00')
            return value[0:len(value)-1]
        else:
            return valueType(value)

    def write(self, data):
        """
        Write a single SVI variable to the target.
        """
        if(self.getConnectionState() != 'ONLINE'):
            raise PyComException("pyCom Error: read SviVariable["+self.name+"] from Module["+self._module.name+"] on Controller["+self._m1ctrl._ip+"] it is not available!")

        value = None
        identifiyer = self._m1ctrl._pycom.VARIABLE_getBaseDataType(self._varInfo)
        if not(self._varInfo.format & SVI_F_IN):
            raise PyComException("pyCom Error: Svi Variable["+self.name+"] is not writable!")
        if(self._varInfo.format & SVI_F_BLK):
            if(identifiyer == SVI_F_CHAR8):
                if type(data) != str or self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) < len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str' or maximum length "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo)))
                value = ctypes.create_string_buffer(data.encode('utf-8'))
            elif (identifiyer == SVI_F_CHAR16):
                if type(data) != str or self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) < len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str' or maximum length "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo)))
                value = ctypes.create_unicode_buffer(data)
            elif(identifiyer == SVI_F_UINT64):
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) > 1:
                    if type(data) != list:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                    if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'int'")
                    value = ULONGLONG_ARRAY(len(data))
                    for i in range(len(data)):
                        if type(data[i]) != int:
                            raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                        value.ARRAY[i] = data[i]
                else:
                    if type(data) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                    value = ctypes.c_ulonglong(data)
            elif(identifiyer == SVI_F_SINT64):
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) > 1:
                    if type(data) != list:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                    if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'int'")
                    value = LONGLONG_ARRAY(len(data))
                    for i in range(len(data)):
                        if type(data[i]) != int:
                            raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                        value.ARRAY[i] = data[i]
                else:
                    if type(data) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'int'")
                    value = ctypes.c_longlong(data)
            elif(identifiyer == SVI_F_REAL64):
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) > 1:
                    if type(data) != list:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'float' elements")
                    if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'float'")
                    value = DOUBLE_ARRAY(len(data))
                    for i in range(len(data)):
                        if type(data[i]) != float:
                            raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'float' elements")
                        value.ARRAY[i] = data[i]
                else:
                    if type(data) != float:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'float'")
                    value = ctypes.c_double(data)
            elif(identifiyer == SVI_F_MIXED):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'int'")
                value = UBYTE_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_UINT1):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'bool' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'bool'")
                value = UBYTE_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != bool:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'bool' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_UINT8):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'int'")
                value = UBYTE_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_BOOL8):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'bool' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'bool'")
                value = UBYTE_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != bool:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'bool' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_UINT16):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'int'")
                value = USHORT_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_UINT32):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'int'")
                value = UINT_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_SINT8):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'int'")
                value = BYTE_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_SINT16):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'int'")
                value = SHORT_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_SINT32):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'int'")
                value = LONG_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != int:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'int' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_REAL32):
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'float' elements")
                if self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo) != len(data):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with "+str(self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo))+" elements of type 'float'")
                value = FLOAT_ARRAY(len(data))
                for i in range(len(data)):
                    if type(data[i]) != float:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'float' elements")
                    value.ARRAY[i] = data[i]
            elif(identifiyer == SVI_F_STRINGLSTBASE):
                bufferLen = self._m1ctrl._pycom.VARIABLE_GetBufferLen(self._varInfo)
                arrayLen = self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo)
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'str' elements")
                if ((arrayLen % len(data)) != 0):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with correct number of elements of type 'str'")
                value = ctypes.create_string_buffer(bufferLen)
                byteArray = ''
                for i in range(len(data)):
                    if type(data[i]) != str:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'str' elements")
                    if int(bufferLen/len(data)) < len(data[i]):
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str' or maximum length "+str(int(bufferLen/len(data))))
                    byteArray = byteArray + data[i] + '\x00'
                value.raw = byteArray.encode('utf-8')
            elif(identifiyer == SVI_F_USTRINGLSTBASE):
                bufferLen = self._m1ctrl._pycom.VARIABLE_GetBufferLen(self._varInfo)
                arrayLen = self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo)
                if type(data) != list:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'str' elements")
                if ((arrayLen % len(data)) != 0):
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with correct number of elements of type 'str'")
                value = UNICODE_ARRAY(bufferLen)
                byteArray = ''
                for i in range(len(data)):
                    if type(data[i]) != str:
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'list' with type 'str' elements")
                    if int(bufferLen/len(data)) < len(data[i]):
                        raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str' or maximum length "+str(int(bufferLen/len(data))))
                    byteArray = byteArray + data[i] + '\x00'
                for i in range(len(byteArray)):
                    value.ARRAY[i] = byteArray[i]
            else:
                raise PyComException("pyCom Error: unknown SVIBLK Type! "+str(self._varInfo.format)+" of Variable:"+self.name)
        else:
            if(identifiyer == SVI_F_CHAR8):
                if type(data) != str or len(data) > 1:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str' with a maximum length of 1")
                value = ctypes.c_char(data.encode('utf-8'))
            elif(identifiyer == SVI_F_CHAR16):
                if type(data) != str or len(data) > 1:
                    raise PyComException("pyCom Error: Svi Variable["+self.name+"] expects type 'str' with a maximum length of 1")
                value = ctypes.c_wchar(data)
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
                raise PyComException("pyCom Error: unknown SVI Type! "+str(self._varInfo.format)+" of Variable:"+self.name)
        
        if hasattr(value, 'ARRAY'):
            if self._m1ctrl._pycom.TARGET_WriteVariable(self._m1ctrl.getCtrlHandle(), self._varHandle, value.ARRAY, self._bufferLen) != 0:
                raise PyComException("pyCom Error: Could not write SVI Variable:" + str(self.name))
        else:
            if self._m1ctrl._pycom.TARGET_WriteVariable(self._m1ctrl.getCtrlHandle(), self._varHandle, ctypes.byref(value), self._bufferLen) != 0:
                raise PyComException("pyCom Error: Could not write SVI Variable:" + str(self.name))

    def getConnectionState(self):
        """
        Get the connection state of the SVI variable.
        """
        state = ctypes.c_uint(0)
        self._m1ctrl._pycom.VARIABLE_GetState(self._varHandle, ctypes.pointer(state))

        if state.value == ONLINE:
            return 'ONLINE'
        elif state.value == OFFLINE:
            return 'OFFLINE'
        elif state.value == ERROR:
            return 'ERROR'
        else:
            raise PyComException(("pyCom Error: Get connection state returned unknown value "+str(state.value)+" for Controller["+self._ip+"]"))

    def getFullName(self):
        """
        Get the full name of the SVI variable.
        """
        fullName = str(self._m1ctrl._pycom.VARIABLE_GetFullName(self._varHandle).decode('utf-8'))
        if fullName == "":
            raise PyComException("pyCom Error: Could not get full SVI Variable name of " + str(self.name))

        return fullName

    def getArrayLen(self):
        """
        Get the array length of the SVI variable.
        """
        return self._m1ctrl._pycom.VARIABLE_getArrayLen(self._varInfo)

    def getBaseDataType(self):
        """
        Get the base datatype of the SVI variable.
        """
        sviDataType = self._m1ctrl._pycom.VARIABLE_getBaseDataType(self._varInfo)

        if sviDataType == SVI_F_UNKNOWN:
            return "SVI_F_UNKNOWN"
        elif sviDataType == SVI_F_UINT1:
            return "SVI_F_UINT1"
        elif sviDataType == SVI_F_UINT8:
            return "SVI_F_UINT8"
        elif sviDataType == SVI_F_SINT8:
            return "SVI_F_SINT8"
        elif sviDataType == SVI_F_UINT16:
            return "SVI_F_UINT16"
        elif sviDataType == SVI_F_SINT16:
            return "SVI_F_SINT16"
        elif sviDataType == SVI_F_UINT32:
            return "SVI_F_UINT32"
        elif sviDataType == SVI_F_SINT32:
            return "SVI_F_SINT32"
        elif sviDataType == SVI_F_REAL32:
            return "SVI_F_REAL32"
        elif sviDataType == SVI_F_BOOL8:
            return "SVI_F_BOOL8"
        elif sviDataType == SVI_F_CHAR8:
            return "SVI_F_CHAR8"
        elif sviDataType == SVI_F_MIXED:
            return "SVI_F_MIXED"
        elif sviDataType == SVI_F_UINT64:
            return "SVI_F_UINT64"
        elif sviDataType == SVI_F_SINT64:
            return "SVI_F_SINT64"
        elif sviDataType == SVI_F_REAL64:
            return "SVI_F_REAL64"
        elif sviDataType == SVI_F_CHAR16:
            return "SVI_F_CHAR16"
        elif sviDataType == SVI_F_STRINGLSTBASE:
            return "SVI_F_STRINGLSTBASE"
        elif sviDataType == SVI_F_USTRINGLSTBASE:
            return "SVI_F_USTRINGLSTBASE"
        else:
            raise PyComException("pyCom Error: Unknown datatype for SVI variable " + str(self.name))

    def checkReadable(self):
        """
        Check if the SVI variable is readable (returns True or False).
        """
        return bool(self._m1ctrl._pycom.VARIABLE_IsReadable(self._varInfo))

    def checkWritable(self):
        """
        Check if the SVI variable is writable (returns True or False).
        """
        return bool(self._m1ctrl._pycom.VARIABLE_IsWritable(self._varInfo))
    
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