import ctypes as cty
import ctypes.wintypes as ctyw
from comtypes import CoClass, COMMETHOD, GUID, IUnknown, wireHWND
from packages.Startup.GlobalFiles import TaskBarLibFilePath

_lcid = 0  # change this if required
typelib_path = TaskBarLibFilePath
WSTRING = cty.c_wchar_p


class ITaskbarList(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID("{56FDF342-FD6D-11D0-958A-006097C9A090}")
    _idlflags_ = []


class ITaskbarList2(ITaskbarList):
    _case_insensitive_ = True
    _iid_ = GUID("{602D4995-B13A-429B-A66E-1935E44F4317}")
    _idlflags_ = []


class ITaskbarList3(ITaskbarList2):
    _case_insensitive_ = True
    _iid_ = GUID("{EA1AFB91-9E28-4B86-90E9-9E9F8A5EEFAF}")
    _idlflags_ = []


ITaskbarList._methods_ = [
    COMMETHOD([], cty.HRESULT, "HrInit"),
    COMMETHOD([], cty.HRESULT, "AddTab", (["in"], cty.c_int, "hwnd")),
    COMMETHOD([], cty.HRESULT, "DeleteTab", (["in"], cty.c_int, "hwnd")),
    COMMETHOD([], cty.HRESULT, "ActivateTab", (["in"], cty.c_int, "hwnd")),
    COMMETHOD([], cty.HRESULT, "SetActivateAlt", (["in"], cty.c_int, "hwnd")),
]

################################################################
# code template for ITaskbarList implementation
# class ITaskbarList_Impl(object):
#     def HrInit(self):
#         '-no docstring-'
#         #return
#
#     def AddTab(self, hwnd):
#         '-no docstring-'
#         #return
#
#     def DeleteTab(self, hwnd):
#         '-no docstring-'
#         #return
#
#     def ActivateTab(self, hwnd):
#         '-no docstring-'
#         #return
#
#     def SetActivateAlt(self, hwnd):
#         '-no docstring-'
#         #return
#

ITaskbarList2._methods_ = [
    COMMETHOD(
        [],
        cty.HRESULT,
        "MarkFullscreenWindow",
        (["in"], cty.c_int, "hwnd"),
        (["in"], cty.c_int, "fFullscreen"),
    ),
]

################################################################
# code template for ITaskbarList2 implementation
# class ITaskbarList2_Impl(object):
#     def MarkFullscreenWindow(self, hwnd, fFullscreen):
#         '-no docstring-'
#         #return
#
# values for enumeration 'TBPFLAG'
TBPF_NOPROGRESS = 0
TBPF_INDETERMINATE = 1
TBPF_NORMAL = 2
TBPF_ERROR = 4
TBPF_PAUSED = 8
TBPFLAG = cty.c_int  # enum
# values for enumeration 'TBATFLAG'
TBATF_USEMDITHUMBNAIL = 1
TBATF_USEMDILIVEPREVIEW = 2
TBATFLAG = cty.c_int  # enum


class tagTHUMBBUTTON(cty.Structure):
    pass


ITaskbarList3._methods_ = [
    COMMETHOD(
        [],
        cty.HRESULT,
        "SetProgressValue",
        (["in"], cty.c_int, "hwnd"),
        (["in"], cty.c_ulonglong, "ullCompleted"),
        (["in"], cty.c_ulonglong, "ullTotal"),
    ),
    COMMETHOD(
        [],
        cty.HRESULT,
        "SetProgressState",
        (["in"], cty.c_int, "hwnd"),
        (["in"], TBPFLAG, "tbpFlags"),
    ),
    COMMETHOD(
        [],
        cty.HRESULT,
        "RegisterTab",
        (["in"], cty.c_int, "hwndTab"),
        (["in"], wireHWND, "hwndMDI"),
    ),
    COMMETHOD([], cty.HRESULT, "UnregisterTab", (["in"], cty.c_int, "hwndTab")),
    COMMETHOD(
        [],
        cty.HRESULT,
        "SetTabOrder",
        (["in"], cty.c_int, "hwndTab"),
        (["in"], cty.c_int, "hwndInsertBefore"),
    ),
    COMMETHOD(
        [],
        cty.HRESULT,
        "SetTabActive",
        (["in"], cty.c_int, "hwndTab"),
        (["in"], cty.c_int, "hwndMDI"),
        (["in"], TBATFLAG, "tbatFlags"),
    ),
    COMMETHOD(
        [],
        cty.HRESULT,
        "ThumbBarAddButtons",
        (["in"], cty.c_int, "hwnd"),
        (["in"], cty.c_uint, "cButtons"),
        (["in"], cty.POINTER(tagTHUMBBUTTON), "pButton"),
    ),
    COMMETHOD(
        [],
        cty.HRESULT,
        "ThumbBarUpdateButtons",
        (["in"], cty.c_int, "hwnd"),
        (["in"], cty.c_uint, "cButtons"),
        (["in"], cty.POINTER(tagTHUMBBUTTON), "pButton"),
    ),
    COMMETHOD(
        [],
        cty.HRESULT,
        "ThumbBarSetImageList",
        (["in"], cty.c_int, "hwnd"),
        (["in"], cty.POINTER(IUnknown), "himl"),
    ),
    COMMETHOD(
        [],
        cty.HRESULT,
        "SetOverlayIcon",
        (["in"], cty.c_int, "hwnd"),
        (["in"], ctyw.HICON, "hIcon"),
        (["in"], WSTRING, "pszDescription"),
    ),
    COMMETHOD(
        [],
        cty.HRESULT,
        "SetThumbnailTooltip",
        (["in"], cty.c_int, "hwnd"),
        (["in"], WSTRING, "pszTip"),
    ),
    COMMETHOD(
        [],
        cty.HRESULT,
        "SetThumbnailClip",
        (["in"], cty.c_int, "hwnd"),
        (["in"], cty.POINTER(ctyw.tagRECT), "prcClip"),
    ),
]


################################################################
# code template for ITaskbarList3 implementation
# class ITaskbarList3_Impl(object):
#     def SetProgressValue(self, hwnd, ullCompleted, ullTotal):
#         '-no docstring-'
#         #return
#
#     def SetProgressState(self, hwnd, tbpFlags):
#         '-no docstring-'
#         #return
#
#     def RegisterTab(self, hwndTab, hwndMDI):
#         '-no docstring-'
#         #return
#
#     def UnregisterTab(self, hwndTab):
#         '-no docstring-'
#         #return
#
#     def SetTabOrder(self, hwndTab, hwndInsertBefore):
#         '-no docstring-'
#         #return
#
#     def SetTabActive(self, hwndTab, hwndMDI, tbatFlags):
#         '-no docstring-'
#         #return
#
#     def ThumbBarAddButtons(self, hwnd, cButtons, pButton):
#         '-no docstring-'
#         #return
#
#     def ThumbBarUpdateButtons(self, hwnd, cButtons, pButton):
#         '-no docstring-'
#         #return
#
#     def ThumbBarSetImageList(self, hwnd, himl):
#         '-no docstring-'
#         #return
#
#     def SetOverlayIcon(self, hwnd, hIcon, pszDescription):
#         '-no docstring-'
#         #return
#
#     def SetThumbnailTooltip(self, hwnd, pszTip):
#         '-no docstring-'
#         #return
#
#     def SetThumbnailClip(self, hwnd, prcClip):
#         '-no docstring-'
#         #return
#


class Library(object):
    name = "TaskbarLib"
    _reg_typelib_ = ("{683BF642-E9CA-4124-BE43-67065B2FA653}", 1, 0)


class TaskbarList(CoClass):
    _reg_clsid_ = GUID("{56FDF344-FD6D-11D0-958A-006097C9A090}")
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ("{683BF642-E9CA-4124-BE43-67065B2FA653}", 1, 0)


TaskbarList._com_interfaces_ = [ITaskbarList3]


class _RemotableHandle(cty.Structure):
    pass


class __MIDL_IWinTypes_0009(cty.Union):
    pass


__MIDL_IWinTypes_0009._fields_ = [
    ("hInproc", cty.c_int),
    ("hRemote", cty.c_int),
]

# The size provided by the typelib is incorrect.
# The size and alignment check for __MIDL_IWinTypes_0009 is skipped.

_RemotableHandle._fields_ = [
    ("fContext", cty.c_int),
    ("u", __MIDL_IWinTypes_0009),
]


# The size provided by the typelib is incorrect.
# The size and alignment check for _RemotableHandle is skipped.


class __MIDL___MIDL_itf_taskbarlib_0006_0001_0001(cty.Structure):
    pass


__MIDL___MIDL_itf_taskbarlib_0006_0001_0001._fields_ = [
    ("Data1", cty.c_ulong),
    ("Data2", cty.c_ushort),
    ("Data3", cty.c_ushort),
    ("Data4", cty.c_ubyte * 8),
]

# The size provided by the typelib is incorrect.
# The size and alignment check for __MIDL___MIDL_itf_taskbarlib_0006_0001_0001 is skipped.

tagTHUMBBUTTON._fields_ = [
    ("dwMask", cty.c_ulong),
    ("iId", cty.c_uint),
    ("iBitmap", cty.c_uint),
    ("hIcon", cty.POINTER(IUnknown)),
    ("szTip", cty.c_ushort * 260),
    ("dwFlags", cty.c_ulong),
]

# The size provided by the typelib is incorrect.
# The size and alignment check for tagTHUMBBUTTON is skipped.

__all__ = [
    "ITaskbarList",
    "__MIDL___MIDL_itf_taskbarlib_0006_0001_0001",
    "_RemotableHandle",
    "TBPF_PAUSED",
    "TBPFLAG",
    "tagTHUMBBUTTON",
    "TaskbarList",
    "TBPF_NOPROGRESS",
    "ITaskbarList3",
    "TBPF_INDETERMINATE",
    "TBATF_USEMDITHUMBNAIL",
    "TBPF_ERROR",
    "TBPF_NORMAL",
    "ITaskbarList2",
    "TBATF_USEMDILIVEPREVIEW",
    "TBATFLAG",
    "__MIDL_IWinTypes_0009",
]