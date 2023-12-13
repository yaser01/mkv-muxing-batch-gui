# -*- coding: mbcs -*-
import ctypes.wintypes
from ctypes import *
from comtypes import CoClass, COMMETHOD, GUID, IUnknown, wireHWND
from ctypes import HRESULT
from ctypes.wintypes import tagRECT

from packages.Startup import GlobalFiles

_lcid = 0  # change this if required
typelib_path = GlobalFiles.TaskBarLibFilePath
WSTRING = c_wchar_p



class ITaskbarList(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID('{56FDF342-FD6D-11D0-958A-006097C9A090}')
    _idlflags_ = []


class ITaskbarList2(ITaskbarList):
    _case_insensitive_ = True
    _iid_ = GUID('{602D4995-B13A-429B-A66E-1935E44F4317}')
    _idlflags_ = []


class ITaskbarList3(ITaskbarList2):
    _case_insensitive_ = True
    _iid_ = GUID('{EA1AFB91-9E28-4B86-90E9-9E9F8A5EEFAF}')
    _idlflags_ = []


ITaskbarList._methods_ = [
    COMMETHOD([], HRESULT, 'HrInit'),
    COMMETHOD(
        [],
        HRESULT,
        'AddTab',
        (['in'], c_int, 'hwnd')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'DeleteTab',
        (['in'], c_int, 'hwnd')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ActivateTab',
        (['in'], c_int, 'hwnd')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetActivateAlt',
        (['in'], c_int, 'hwnd')
    ),
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
        HRESULT,
        'MarkFullscreenWindow',
        (['in'], c_int, 'hwnd'),
        (['in'], c_int, 'fFullscreen')
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
TBPFLAG = c_int  # enum
# values for enumeration 'TBATFLAG'
TBATF_USEMDITHUMBNAIL = 1
TBATF_USEMDILIVEPREVIEW = 2
TBATFLAG = c_int  # enum


class tagTHUMBBUTTON(Structure):
    pass


ITaskbarList3._methods_ = [
    COMMETHOD(
        [],
        HRESULT,
        'SetProgressValue',
        (['in'], c_int, 'hwnd'),
        (['in'], c_ulonglong, 'ullCompleted'),
        (['in'], c_ulonglong, 'ullTotal')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetProgressState',
        (['in'], c_int, 'hwnd'),
        (['in'], TBPFLAG, 'tbpFlags')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'RegisterTab',
        (['in'], c_int, 'hwndTab'),
        (['in'], wireHWND, 'hwndMDI')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'UnregisterTab',
        (['in'], c_int, 'hwndTab')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetTabOrder',
        (['in'], c_int, 'hwndTab'),
        (['in'], c_int, 'hwndInsertBefore')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetTabActive',
        (['in'], c_int, 'hwndTab'),
        (['in'], c_int, 'hwndMDI'),
        (['in'], TBATFLAG, 'tbatFlags')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ThumbBarAddButtons',
        (['in'], c_int, 'hwnd'),
        (['in'], c_uint, 'cButtons'),
        (['in'], POINTER(tagTHUMBBUTTON), 'pButton')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ThumbBarUpdateButtons',
        (['in'], c_int, 'hwnd'),
        (['in'], c_uint, 'cButtons'),
        (['in'], POINTER(tagTHUMBBUTTON), 'pButton')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'ThumbBarSetImageList',
        (['in'], c_int, 'hwnd'),
        (['in'], POINTER(IUnknown), 'himl')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetOverlayIcon',
        (['in'], c_int, 'hwnd'),
        (['in'], ctypes.wintypes.HICON, 'hIcon'),
        (['in'], WSTRING, 'pszDescription')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetThumbnailTooltip',
        (['in'], c_int, 'hwnd'),
        (['in'], WSTRING, 'pszTip')
    ),
    COMMETHOD(
        [],
        HRESULT,
        'SetThumbnailClip',
        (['in'], c_int, 'hwnd'),
        (['in'], POINTER(tagRECT), 'prcClip')
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


class TaskbarList(CoClass):
    _reg_clsid_ = GUID('{56FDF344-FD6D-11D0-958A-006097C9A090}')
    _idlflags_ = []
    _typelib_path_ = typelib_path
    _reg_typelib_ = ('{683BF642-E9CA-4124-BE43-67065B2FA653}', 1, 0)


TaskbarList._com_interfaces_ = [ITaskbarList3]


class __MIDL_IWinTypes_0009(Union):
    pass


__MIDL_IWinTypes_0009._fields_ = [
    ('hInproc', c_int),
    ('hRemote', c_int),
]

# The size provided by the typelib is incorrect.
# The size and alignment check for __MIDL_IWinTypes_0009 is skipped.


class __MIDL___MIDL_itf_taskbarlib_0006_0001_0001(Structure):
    pass


__MIDL___MIDL_itf_taskbarlib_0006_0001_0001._fields_ = [
    ('Data1', c_ulong),
    ('Data2', c_ushort),
    ('Data3', c_ushort),
    ('Data4', c_ubyte * 8),
]

# The size provided by the typelib is incorrect.
# The size and alignment check for __MIDL___MIDL_itf_taskbarlib_0006_0001_0001 is skipped.


class Library(object):
    name = 'TaskbarLib'
    _reg_typelib_ = ('{683BF642-E9CA-4124-BE43-67065B2FA653}', 1, 0)


tagTHUMBBUTTON._fields_ = [
    ('dwMask', c_ulong),
    ('iId', c_uint),
    ('iBitmap', c_uint),
    ('hIcon', POINTER(IUnknown)),
    ('szTip', c_ushort * 260),
    ('dwFlags', c_ulong),
]

# The size provided by the typelib is incorrect.
# The size and alignment check for tagTHUMBBUTTON is skipped.


class _RemotableHandle(Structure):
    pass


_RemotableHandle._fields_ = [
    ('fContext', c_int),
    ('u', __MIDL_IWinTypes_0009),
]

# The size provided by the typelib is incorrect.
# The size and alignment check for _RemotableHandle is skipped.

__all__ = [
    'ITaskbarList2', 'tagTHUMBBUTTON', 'TBPFLAG', 'ITaskbarList3',
    'ITaskbarList', 'TBATFLAG', '_RemotableHandle', 'TBPF_NORMAL',
    'TBPF_NOPROGRESS', 'TBPF_INDETERMINATE',
    'TBATF_USEMDILIVEPREVIEW',
    '__MIDL___MIDL_itf_taskbarlib_0006_0001_0001', 'TBPF_ERROR',
    'TBPF_PAUSED', '__MIDL_IWinTypes_0009', 'TBATF_USEMDITHUMBNAIL',
    'TaskbarList'
]


