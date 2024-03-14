import asyncio
import logging
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
import dumpers


async def main():
    logging.getLogger().setLevel(logging.INFO)
    opts = options.Options(mode=["wireguard"])

    m = DumpMaster(opts)
    m.addons.add(*dumpers.ADDONS)

    try:
        await m.run()
    except KeyboardInterrupt:
        m.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
