from flask import Blueprint, request
 
bg9_40323233_1 = Blueprint('bg9_40323233_1', __name__, url_prefix='/bg9_40323233_1', template_folder='templates')
 
head_str = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 鏈條繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
 
</head>
<body>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id="plotarea" width="800" height="800"></canvas>
'''
 
tail_str = '''
</script>
</body>
</html>
'''
 
chain_str = '''
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-250, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180  
 
# 將繪製鏈條輪廓的內容寫成 class 物件
class chain():
    # 輪廓的外型設為 class variable
    chamber = "M -6.8397, -1.4894 \
            A 7, 7, 0, 1, 0, 6.8397, -1.4894 \
            A 40, 40, 0, 0, 1, 6.8397, -18.511 \
            A 7, 7, 0, 1, 0, -6.8397, -18.511 \
            A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    def __init__(self, fillcolor="green", border=True, strokecolor= "tan", linewidth=2, scale=1):
        self.fillcolor = fillcolor
        self.border = border
        self.strokecolor = strokecolor
        self.linewidth = linewidth
        self.scale = scale
 
    # 利用鏈條起點與終點定義繪圖
    def basic(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, self.scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, v=False):
        # 若 v 為 True 則為虛擬 chain, 不 render
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.v = v
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)*self.scale
        y2 = y1 + 20*math.sin(rot*deg)*self.scale
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        if v == False:
            cgo.render(basic1, x1, y1, self.scale, 0)
 
        return x2, y2
'''

# 傳繪 A 函式內容
def a(x, y, scale=1, color="green"):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain(scale='''+str(scale)+''', fillcolor="'''+str(color)+'''")
 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1)
'''
 
    return outstring
    
@bg9_40323233_1.route('/a')
def draw_a():
    return head_str + chain_str + a(0, 0) + tail_str
    
def circle36(x, y, degree=10):
    # 20 為鏈條輪廓之圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    #degree = 10
    first_degree = 90 - degree
    repeat = 360 / degree
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
    return outstring
    
@bg9_40323233_1.route('/circle36/<degree>', defaults={'x': 0, 'y': 0})
@bg9_40323233_1.route('/circle36/<x>/<degree>', defaults={'y': 0})
@bg9_40323233_1.route('/circle36/<x>/<y>/<degree>')
#@bg9_40323233_1.route('/circle36/<int:x>/<int:y>/<int:degree>')
def drawcircle36(x,y,degree):
    return head_str + chain_str + circle36(int(x), int(y), int(degree)) + tail_str
@bg9_40323233_1.route('/abc', defaults={'n1':15,'n2':20,'n3':18})
@bg9_40323233_1.route('/abc/<n1>/<n2>/<n3>')
def abc(n1,n2,n3):
    outstring = '''
<!DOCTYPE html>
<html> 
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>
<script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id='gear1' width='800' height='750'></canvas>
 
<script type="text/python">
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx, cy, m, n, pa, theta):
    # n 為齒數
    #n = 17
    # pa 為壓力角
    #pa = 25
    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth
    #m = 0.8*canvas.width/n
    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
 
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    #gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh, 請注意 rotate 角度為 degree
    # theta 為角度
    gearTooth.rotate(theta) 
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
 
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
 
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path
    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    # 接著繪製齒輪的基準線
    deg = math.pi/180
    Line = cobj(['M', cx, cy, 'L', cx+pr*math.cos(theta*deg), cy+pr*math.sin(theta*deg)], "PATH", {
          'strokeColor':'blue', 'lineWidth': 1})
    cgo.render(Line)
 
# 3個齒輪的齒數
n1 = '''+str(n1)+'''
n2 = '''+str(n2)+'''
n3 = '''+str(n3)+'''
 
# m 為模數, 根據畫布的寬度, 計算適合的模數大小
# Module = mm of pitch diameter per tooth
# 利用 80% 的畫布寬度進行繪圖
# 計算模數的對應尺寸
m = canvas.width*0.8/(n1+n2+n3)
 
# 根據齒數與模組計算各齒輪的節圓半徑
pr1 = n1*m/2
pr2 = n2*m/2
pr3 = n3*m/2
 
# 畫布左右兩側都保留畫布寬度的 10%
# 依此計算對應的最左邊齒輪的軸心座標
cx = canvas.width*0.1+pr1
cy = canvas.height/2
 
# pa 為壓力角
pa = 25
 
# 畫最左邊齒輪, 定位線旋轉角為 0, 軸心座標 (cx, cy)
spur(cx, cy, m, n1, pa, 0)
# 第2個齒輪將原始的定位線逆時鐘轉 180 度後, 與第1個齒輪正好齒頂與齒頂對齊
# 只要第2個齒輪再逆時鐘或順時鐘轉動半齒的角度, 即可完成囓合
# 每一個齒分別包括從齒根到齒頂的範圍, 涵蓋角度為 360/n, 因此所謂的半齒角度為 180/n
spur(cx+pr1+pr2, cy, m, n2, pa, 180-180/n2)
# 第2齒與第3齒的囓合, 首先假定第2齒的定位線在 theta 角為 0 的原始位置
# 如此, 第3齒只要逆時鐘旋轉 180 度後, 再逆時鐘或順時鐘轉動半齒的角度, 即可與第2齒囓合
# 但是第2齒為了與第一齒囓合時, 已經從原始定位線轉了 180-180/n2 度
# 而當第2齒從與第3齒囓合的定位線, 逆時鐘旋轉 180-180/n2 角度後, 原先囓合的第3齒必須要再配合旋轉 (180-180/n2 )*n2/n3
spur(cx+pr1+pr2+pr2+pr3, cy, m, n3, pa, 180-180/n3+(180-180/n2)*n2/n3)
</script>
'''
    return outstring
