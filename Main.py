import plistlib, sys, os, aiohttp, asyncio

async def main():
    print("Options:")
    print("1. Download latest driver")
    print("2. Exit\n")
    response = input("Input your option (1, 2): ")

    try:
        intresponse = int(response)
    except ValueError:
        print("Invalid input")
        await main()

    if response not in ["1", "2"]:
        print("Invalid input")
        await main()
    else:
        if intresponse == 1:
            await getLatest()
        if intresponse == 2:
            print("Good day/night!")
            sys.exit(0)

async def getLatest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    url = "https://gfe.nvidia.com/mac-update"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            webpage = await response.text()

    pl = webpage.encode("utf-8")
    plist = plistlib.readPlistFromBytes(pl)

    total_size = 0
    data = b""
    async with aiohttp.ClientSession() as downloader:
        async with downloader.get(url) as downloaded:
            assert downloaded.status == 200
            while True:
                chunk = await downloaded.content.read(4*1024) 
                data += chunk
                total_size += len(chunk)
                if not chunk:
                    break

    name = "WebDriver-{}.pkg".format(plist["updates"][0]["version"])              
    with open(name, 'wb') as package:
        package.write(data)
    
    print("Version {} downloaded in the place where you ran this script. Exiting...".format(plist["updates"][0]["version"]))
    print("Good day/night!")
    sys.exit(0)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())