from urllib.request import urlopen
from datetime import datetime
from os.path import abspath
from pprint import pprint
from json import loads
from PIL import Image
import ctypes

P = "https://"
MainUrl = "cn.bing.com"

NowDate = datetime.isoformat(datetime.now())
# 访问必应壁纸API
GetJsonText = (
    urlopen("https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN")
    .read()
    .decode("utf-8")
)

GetDict: dict = loads(GetJsonText)
with open("WallPaper.log", "a", encoding="utf-8", newline="\n") as LogFile:
    LogFile.write(NowDate + "\n")
    pprint(object=GetDict, stream=LogFile)
    LogFile.write("\n" * 3)

TodayImageUrl = P + MainUrl + GetDict["images"][0]["url"]
data = urlopen(TodayImageUrl)
Image.open(data).save("TodayWallpaper.BMP")
ctypes.windll.user32.SystemParametersInfoW(
    20, 0, abspath("TodayWallpaper.BMP"), 0
)  # 设置桌面
