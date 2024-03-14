import asyncio
import logging
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
from interceptor import addons


async def main():
    logging.getLogger().setLevel(logging.INFO)
    opts = options.Options(mode=["wireguard"])

    m = DumpMaster(opts)
    m.addons.add(*addons)

    try:
        await m.run()
    except KeyboardInterrupt:
        m.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
