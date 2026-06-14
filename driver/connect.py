import logging
import asyncio
import multiprocessing

from pymobiledevice3.lockdown import create_using_usbmux, LockdownClient
from pymobiledevice3.services.amfi import AmfiService
from pymobiledevice3.exceptions import NoDeviceConnectedError


async def get_usbmux_lockdownclient():
    while True:
        try:
            lockdown = await create_using_usbmux()
        except NoDeviceConnectedError:
            print("请连接设备后按回车...")
            input()
        else:
            break
    while True:
        lockdown = await create_using_usbmux()
        if lockdown.all_values.get("PasswordProtected"):
            print("请解锁设备后按回车...")
            input()
        else:
            break
    return await create_using_usbmux()


def get_version(lockdown: LockdownClient):
    return lockdown.all_values.get("ProductVersion")


async def get_developer_mode_status(lockdown: LockdownClient):
    return await lockdown.get_developer_mode_status()


async def reveal_developer_mode(lockdown: LockdownClient):
    await AmfiService(lockdown).reveal_developer_mode_option_in_ui()


async def enable_developer_mode(lockdown: LockdownClient):
    await AmfiService(lockdown).enable_developer_mode()
