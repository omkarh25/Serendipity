import os
from datetime import date

today = date.today()
d1 = today.strftime("%d %b %y")
print("d1 =", d1)
newname = d1+'.txt'

straddleSrc = "C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\NiftyOrders.txt"
straddleDst = ("C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Backup\\NiftyOrdersRecord\\"+newname)

tradeSrc = "C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\tradeLog.txt"
tradeDst = ("C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Backup\\Tradelogs\\"+newname)

goldenSrc = "C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\GROrders.txt"
goldenDst = ("C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Backup\\goldenOrdersRecord\\"+newname)

goldenlogSrc = "C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Current\\goldenLog.txt"
goldenlogDst = ("C:\\Users\\amol37007\\OneDrive\\JsonTxt\\Backup\\goldenLog\\"+newname)

if os.path.isfile(straddleSrc):
    os.rename(straddleSrc,straddleDst)
    os.rename(tradeSrc,tradeDst)
else:
    print("No orders today !")

if os.path.isfile(goldenSrc):
    os.rename(goldenSrc,goldenDst)
    os.rename(goldenlogSrc,goldenlogDst)
else:
    print("No orders today !")

