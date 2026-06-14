import signal
import logging
import coloredlogs
import os
import asyncio
import sys
import argparse


from init import init
from init import tunnel
from init import route

import run
import config



debug = os.environ.get("DEBUG", False)

coloredlogs.install(level=logging.INFO)
logging.getLogger('wintun').setLevel(logging.DEBUG if debug else logging.WARNING)
logging.getLogger('quic').setLevel(logging.DEBUG if debug else logging.WARNING)
logging.getLogger('asyncio').setLevel(logging.DEBUG if debug else logging.WARNING)
logging.getLogger('zeroconf').setLevel(logging.DEBUG if debug else logging.WARNING)
logging.getLogger('parso.cache').setLevel(logging.DEBUG if debug else logging.WARNING)
logging.getLogger('parso.cache.pickle').setLevel(logging.DEBUG if debug else logging.WARNING)
logging.getLogger('parso.python.diff').setLevel(logging.DEBUG if debug else logging.WARNING)
logging.getLogger('humanfriendly.prompts').setLevel(logging.DEBUG if debug else logging.WARNING)
logging.getLogger('blib2to3.pgen2.driver').setLevel(logging.DEBUG if debug else logging.WARNING)
logging.getLogger('urllib3.connectionpool').setLevel(logging.DEBUG if debug else logging.WARNING)



async def main():
    parser = argparse.ArgumentParser(description="iOS 虚拟定位模拟跑步")
    parser.add_argument("-m", "--minutes", type=int, default=0,
                        help="运行时长（分钟），不指定则无限运行")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    coloredlogs.install(level=logging.INFO)
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
        coloredlogs.install(level=logging.DEBUG)

    if args.minutes > 0:
        print(f"运行时长设置为 {args.minutes} 分钟")
        print("到达时长后会自动停止并恢复真实定位")
        print()

    await init.init()
    logger.info("init done")

    logger.info("trying to start tunnel")
    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    process, address, port = tunnel.tunnel()
    signal.signal(signal.SIGINT, original_sigint_handler)
    try:
        logger.debug(f"tunnel address: {address}, port: {port}")

        loc = route.get_route()
        logger.info(f"got route from {config.config.routeConfig}")

        try:
            duration = args.minutes * 60 if args.minutes > 0 else None

            if duration:
                print(f"已开始模拟跑步，速度大约为 {config.config.v} m/s")
                print(f"将在 {args.minutes} 分钟后自动停止")
            else:
                print(f"已开始模拟跑步，速度大约为 {config.config.v} m/s")
                print("会无限循环，按 Ctrl+C 退出")
            print("请勿直接关闭窗口，否则无法还原正常定位")

            await run.run(address, port, loc, config.config.v, duration_seconds=duration)
        except KeyboardInterrupt:
            logger.debug("get KeyboardInterrupt (inner)")
        except asyncio.TimeoutError:
            print()
            print(f"已运行 {args.minutes} 分钟，正在停止...")
        except Exception:
            logger.debug("unexpected error", exc_info=True)
        finally:
            logger.debug(f"Is process alive? {process.is_alive()}")
            logger.debug("Start to clear location")

    except KeyboardInterrupt:
        logger.debug("get KeyboardInterrupt (outer)")
    finally:
        logger.debug(f"Is process alive? {process.is_alive()}")
        logger.debug("terminating tunnel process")
        process.terminate()
        logger.info("tunnel process terminated")
        print("Bye")



if __name__ == "__main__":
    asyncio.run(main())
