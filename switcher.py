#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===========================================================
Author: Peltux
Date: 2026/03/09|2026/03/09
Version: v1.0
Description: 切换扬声器输出设备快捷切换
-----------------------------------------------------------
此脚本旨在切换扬声器输出设备快捷切换，适用于 Windows 10/11 系统。

依赖库:
    - pycaw: 用于查询扬声器设备（可选）
    - comtypes: 用于访问 Windows COM 接口，进行音频设备控制
    - winotify: 用于显示 Windows 通知
    - keyboard: 用于监听键盘事件（可选）

使用方法:
    python switcher.py
    - 修改 devName 和 devID 变量（可通过运行以下脚本获得）
    --------------------------- 用户可复制的脚本 ---------------------------

    # 导入需要的库
    from pycaw.pycaw import AudioUtilities
    from pycaw.constants import AudioDeviceState

    # 获取所有音频设备
    devices = AudioUtilities.GetAllDevices()

    print("已启用的扬声器设备列表:\n")

    # 过滤出状态为 Active 且是输出设备（扬声器）
    for dev in devices:
        if dev.id.startswith("{0.0.0.00000000}") and dev.state == AudioDeviceState.Active:
            print("Name:", dev.FriendlyName)
            print("ID:", dev.id)
            print("State:", dev.state)
            print("-" * 40)

    --------------------------- 结束用户可复制的脚本 ---------------------------

许可证:
    MIT License
===========================================================
"""

import comtypes
from ctypes import *
from comtypes import GUID, COMMETHOD, IUnknown, CLSCTX_ALL
from winotify import Notification

devName_a = "扬声器 (2- Realtek(R) Audio)"
devName_b = "头戴式耳机 (HyperX Virtual Surround Sound)"
devID_a = "{0.0.0.00000000}.{a31e70e2-4ee2-4b7b-888f-672c41b9daec}"
devID_b = "{0.0.0.00000000}.{9c837a18-3ffb-422a-ad09-de62cc8cf150}"

CLSID_PolicyConfigClient = GUID("{870AF99C-171D-4F9E-AF0D-E63DF40C2BC9}")


class IPolicyConfig(IUnknown):
    _iid_ = GUID("{F8679F50-850A-41CF-9C72-430F290290C8}")
    _methods_ = [
        COMMETHOD([], HRESULT, "GetMixFormat"),
        COMMETHOD([], HRESULT, "GetDeviceFormat"),
        COMMETHOD([], HRESULT, "ResetDeviceFormat"),
        COMMETHOD([], HRESULT, "SetDeviceFormat"),
        COMMETHOD([], HRESULT, "GetProcessingPeriod"),
        COMMETHOD([], HRESULT, "SetProcessingPeriod"),
        COMMETHOD([], HRESULT, "GetShareMode"),
        COMMETHOD([], HRESULT, "SetShareMode"),
        COMMETHOD([], HRESULT, "GetPropertyValue"),
        COMMETHOD([], HRESULT, "SetPropertyValue"),
        COMMETHOD([], HRESULT, "SetDefaultEndpoint",
                  (["in"], c_wchar_p, "deviceId"),
                  (["in"], c_int, "role")),
        COMMETHOD([], HRESULT, "SetEndpointVisibility"),
    ]


def set_default(device_id):
    policy = comtypes.CoCreateInstance(
        CLSID_PolicyConfigClient,
        IPolicyConfig,
        CLSCTX_ALL
    )

    for role in range(3):
        policy.SetDefaultEndpoint(device_id, role)


def switch():
    import winreg

    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\AudioSwitcher")

    try:
        state, _ = winreg.QueryValueEx(key, "state")
    except FileNotFoundError:
        state = 0

    if state == 0:
        set_default(devID_a)
        winreg.SetValueEx(key, "state", 0, winreg.REG_DWORD, 1)
        toast = Notification(
            app_id="Audio Switcher",
            title="音频切换\n ",
            msg="已切换到 " + devName_a
        )
        toast.show()
    else:
        set_default(devID_b)
        winreg.SetValueEx(key, "state", 0, winreg.REG_DWORD, 0)
        print("已切换到 头戴式耳机 (HyperX Virtual Surround Sound) ")
        toast = Notification(
            app_id="Audio Switcher",
            title="音频切换\n ",
            msg="已切换到 " + devName_b
        )
        toast.show()


if __name__ == "__main__":
    switch()