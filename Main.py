import plistlib, time, sys, os, urllib
from urllib.request import urlopen

def main():
    print("Options:")
    print("1. Download latest driver")
    print("2. Exit\n")
    response = input("Input your option (1, 2, 3)")

    responseList = ["1", "2", "3"]

    if response not in responseList:
        print("Invalid choice")
        time.sleep(1)
        subprocess.call(["printf", "'\033c'"])
        main()
    else:
        if response == 1:
            getLatest()
        if response == 2:
            print("Good day/night!")
            sys.exit(0)

def getLatest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pl = urlopen("https://gfe.nvidia.com/mac-update").read()
    plist = plistlib.readPlistFromBytes(pl)
    url = plist["updates"][0]["downloadURL"]
    name = "WebDriver-{}.pkg".format(plist["updates"][0]["version"])
    urllib.request.urlretrieve(url, name)
    print("Version {} downloaded in the place where you ran this script. Exiting...".format(plist["updates"][0]["version"]))
    print("Good day/night!")
    sys.exit(0)

main()