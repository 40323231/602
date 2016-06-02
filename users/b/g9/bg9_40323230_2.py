from flask import Blueprint, request
 
bg9_40323230_2 = Blueprint('bg9_40323230_2', __name__, url_prefix='/bg9_40323230_2', template_folder='templates')
 
head_str = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 繪圖</title>
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
    #chamber = "M 0, 0 L 0, -20 z"
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
        # 注意, cgoChamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole0 為原點位置
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
 
def circle(x, y):
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 50)
'''
    for i in range(2, 10):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*40)+") \n"
    return outstring
 
def twocircle(x, y):
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    x = 50
    y = 0
    degree = 12
    # 78, 66, 54, 42, 30, 18, 6度
    #必須有某些 chain 算座標但是不 render
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節也是 virtual chain
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''', True)
#x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    # 這裡要上下各多留一節虛擬 chain, 以便最後進行連接 (x7, y7) 與 (x22, y22)
    for i in range(2, int(repeat)+1):
        #if i < 7 or i > 23:        
        if i <= 7 or i >= 23:
            # virautl chain
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+", True) \n"
            #outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
        else:
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
 
    p = -150
    k = 0
    degree = 20
    # 70, 50, 30, 10
    # 從 i=5 開始, 就是 virautl chain
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節不是 virtual chain
    outstring += '''
#mychain = chain()
 
p1, k1 = mychain.basic_rot('''+str(p)+","+str(k)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        if i >= 5 and i <= 13:
            # virautl chain
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+", True) \n"
            #outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+") \n"
        else:
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+") \n"
 
    # 上段連接直線
    # 從 p5, k5 作為起點
    first_degree = 10
    repeat = 11
    outstring += '''
m1, n1 = mychain.basic_rot(p4, k4, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "m"+str(i)+", n"+str(i)+"=mychain.basic_rot(m"+str(i-1)+", n"+str(i-1)+", "+str(first_degree)+")\n"
 
    # 下段連接直線
    # 從 p12, k12 作為起點
    first_degree = -10
    repeat = 11
    outstring += '''
r1, s1 = mychain.basic_rot(p13, k13, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "r"+str(i)+", s"+str(i)+"=mychain.basic_rot(r"+str(i-1)+", s"+str(i-1)+", "+str(first_degree)+")\n"
 
    # 上段右方接點為 x7, y7, 左側則為 m11, n11
    outstring += "mychain.basic(x7, y7, m11, n11)\n"
    # 下段右方接點為 x22, y22, 左側則為 r11, s11
    outstring += "mychain.basic(x22, y22, r11, s11)\n"
 
    return outstring
@bg9_40323230_2.route('/circle')
def drawcircle():
    return head_str + chain_str + circle(0, 0) + tail_str
 
 
@bg9_40323230_2.route('/circle1/<degree>', defaults={'x': 0, 'y': 0})
@bg9_40323230_2.route('/circle1/<x>/<degree>', defaults={'y': 0})
@bg9_40323230_2.route('/circle1/<x>/<y>/<degree>')
#@bg9_40323230_2.route('/circle1/<int:x>/<int:y>/<int:degree>')
def drawcircle1(x,y,degree):
    return head_str + chain_str + circle1(int(x), int(y), int(degree)) + tail_str
 
 
def eighteenthirty(x, y):
    '''
從圖解法與符號式解法得到的兩條外切線座標點
(-203.592946177111, 0.0), (0.0, 0.0), (-214.364148466539, 56.5714145924675), (-17.8936874260919, 93.9794075692901)
(-203.592946177111, 0.0), (0.0, 0.0), (-214.364148466539, -56.5714145924675), (-17.8936874260919, -93.9794075692901)
左邊關鍵鍊條起點 (-233.06, 49.48), 角度 20.78, 圓心 (-203.593, 0.0)
右邊關鍵鍊條起點 (-17.89, 93.9), 角度 4.78, 圓心 (0, 0)
    '''
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    x = 50
    y = 0
    degree = 20
    first_degree = 20.78+90
    startx = 44.0532
    starty = -165.17
    repeat = 360 / degree
    # 先畫出左邊第一關鍵節
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(startx)+","+str(starty)+", "+str(first_degree)+''')
 
'''
    # 接著繪製左邊的非虛擬鍊條
    for i in range(2, int(repeat)+1):
        if i >=2 and i <=11:
            # virautl chain
            #outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+","+str(first_degree+degree-i*degree)+", True) \n"
        else:
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
 
    # 接著處理右邊的非虛擬鍊條
    # 先畫出右邊第一關鍵節
 
    p = 0
    k = 50
    degree = 12
    first_degree = 4.78+90
    repeat = 360 / degree
    # 第1節不是 virtual chain
    outstring += '''
#mychain = chain()
 
p1, k1 = mychain.basic_rot('''+str(p)+","+str(k)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        if i >=18:
            # virautl chain
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+","+str(first_degree+degree-i*degree)+", True) \n"
            #outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
        else:
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
 
    # 上段連接直線
    # 從 x1, y1 作為起點
    first_degree = 10.78 +90 
    repeat = 10
    outstring += '''
m1, n1 = mychain.basic_rot(x1, y1, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "m"+str(i)+", n"+str(i)+"=mychain.basic_rot(m"+str(i-1)+", n"+str(i-1)+", "+str(first_degree)+")\n"
 
    # 下段連接直線
    # 從 x11, y11 作為起點
    first_degree = -10.78 +90
    repeat = 10
    outstring += '''
r1, s1 = mychain.basic_rot(x11, y11, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "r"+str(i)+", s"+str(i)+"=mychain.basic_rot(r"+str(i-1)+", s"+str(i-1)+", "+str(first_degree)+")\n"
 
    return outstring
 
 
@bg9_40323230_2.route('/circle2/<degree>', defaults={'x': 0, 'y': 0})
@bg9_40323230_2.route('/circle2/<x>/<degree>', defaults={'y': 0})
@bg9_40323230_2.route('/circle2/<x>/<y>/<degree>')
#@bg9_40323230_2.route('/circle2/<int:x>/<int:y>/<int:degree>')
def drawcircle2(x,y,degree):
    return head_str + chain_str + circle2(int(x), int(y), int(degree)) + tail_str
 
 
@bg9_40323230_2.route('/twocircle/<x>/<y>')
@bg9_40323230_2.route('/twocircle', defaults={'x':0, 'y':0})
def drawtwocircle(x,y):
    return head_str + chain_str + twocircle(int(x), int(y)) + tail_str
 
 
@bg9_40323230_2.route('/eighteenthirty/<x>/<y>')
@bg9_40323230_2.route('/eighteenthirty', defaults={'x':0, 'y':0})
def draweithteenthirdy(x,y):
    return head_str + chain_str + eighteenthirty(int(x), int(y)) + tail_str
 
 
@bg9_40323230_2.route('/snap')
# http://svg.dabbles.info/snaptut-base
def snap():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
    <script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
    <script type="text/javascript" src="/static/snap.svg-min.js"></script>
 
    <script>
    window.onload=function(){
    brython(1);
    }
    </script>
</head>
<body>
 
<svg width="800" height="800" viewBox="0 0 800 800" id="svgout"></svg>
 
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window, document
 
# 透過 window 與 JSConstructor 從 Brython 物件 snap 擷取 Snap 物件的內容
snap = JSConstructor(window.Snap)
 
s = snap("#svgout")
# 建立物件時, 同時設定 id 名稱
r = s.rect(10,10,100,100).attr({'id': 'rect'})
c = s.circle(100,100,50).attr({'id': 'circle'})
r.attr('fill', 'red')
c.attr({ 'fill': 'blue', 'stroke': 'black', 'strokeWidth': 10 })
r.attr({ 'stroke': '#123456', 'strokeWidth': 20 })
s.text(180,100, '點按一下圖形').attr({'fill' : 'blue',  'stroke': 'blue', 'stroke-width': 0.2 })
 
g = s.group().attr({'id': 'tux'})
 
def hoverover(ev):
    g.animate({'transform': 's1.5r45,t180,20'}, 1000, window.mina.bounce)
 
def hoverout(ev):
    g.animate({'transform': 's1r0,t180,20'}, 1000, window.mina.bounce) 
 
# callback 函式
def onSVGLoaded(data):
    #s.append(data)
    g.append(data)
    #g.hover(hoverover, hoverout )
    g.text(300,100, '拿滑鼠指向我')
 
# 利用 window.Snap.load 載入 svg 檔案
tux = window.Snap.load("/static/Dreaming_tux.svg", onSVGLoaded)
g.transform('t180,20')
 
# 與視窗事件對應的函式
def rtoyellow(ev):
    r.attr('fill', 'yellow')
 
def ctogreen(ev):
    c.attr('fill', 'green')
 
# 根據物件 id 綁定滑鼠事件執行對應函式
document['rect'].bind('click', rtoyellow)
document['circle'].bind('click', ctogreen)
document['tux'].bind('mouseover', hoverover)
document['tux'].bind('mouseleave', hoverout)
</script>
</body>
</html>
'''
    return outstring
 
 
@bg9_40323230_2.route('/snap_link')
# http://svg.dabbles.info/
def snap_link():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
    <script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
    <script type="text/javascript" src="/static/snap.svg-min.js"></script>
 
    <script>
    window.onload=function(){
    brython(1);
    }
    </script>
</head>
<body>
 
<svg width="800" height="800" viewBox="0 0 800 800" id="svgout"></svg>
 
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window, document
 
# 透過 window 與 JSConstructor 從 Brython 物件 snap 擷取 Snap 物件的內容
snap = JSConstructor(window.Snap)
 
# 使用 id 為 "svgout" 的 svg 標註進行繪圖
s = snap("#svgout")
 
offsetY = 50
 
# 是否標訂出繪圖範圍
#borderRect = s.rect(0,0,800,640,10,10).attr({ 'stroke': "silver", 'fill': "silver", 'strokeWidth': "3" })
 
g = s.group().transform('t250,120')
r0 = s.rect(150,150,100,100,20,20).attr({ 'fill': "orange", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c0 = s.circle(225,225,10).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "4"  }).attr({ 'id': 'c0' })
g0 = s.group( r0,c0 ).attr({ 'id': 'g0' })
#g0.animate({ 'transform' : 't250,120r360,225,225' },4000)
g0.appendTo( g )
g0.animate({ 'transform' : 'r360,225,225' },4000)
# 讓 g0 可以拖動
g0.drag()
 
r1 = s.rect(100,100,100,100,20,20).attr({ 'fill': "red", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c1 = s.circle(175,175,10).attr({ 'fill': "silver", 'stroke': "black" , 'strokeWidth': "4"}).attr({ 'id': 'c1' })
g1 = s.group( r1,c1 ).attr({ 'id': 'g1' })
g1.appendTo( g0 ).attr({ 'id': 'g1' })
g1.animate({ 'transform' : 'r360,175,175' },4000)
 
r2 = s.rect(50,50,100,100,20,20).attr({ 'fill': "blue", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c2 = s.circle(125,125,10).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "4" }).attr({ 'id': 'c2' })
g2 = s.group(r2,c2).attr({ 'id': 'g2' })
 
g2.appendTo( g1 );
g2.animate( { 'transform' : 'r360,125,125' },4000);
 
r3 = s.rect(0,0,100,100,20,20).attr({ 'fill': "yellow", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c3 = s.circle(75,75,10).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "4" }).attr({ 'id': 'c3' })
g3 = s.group(r3,c3).attr({ 'id': 'g3' })
 
g3.appendTo( g2 )
g3.animate( { 'transform' : 'r360,75,75' },4000)
 
r4 = s.rect(-50,-50,100,100,20,20).attr({ 'fill': "green", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c4 = s.circle(25,25,10).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "4" }).attr({ 'id': 'c4' })
g4 = s.group(r4,c4).attr({ 'id': 'g4' });
g4.appendTo( g3 )
g4.animate( { 'transform' : 'r360,25,25' },4000)
</script>
</body>
</html>
'''
    return outstring
 
 
@bg9_40323230_2.route('/snap_gear')
def snap_gear():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
    <script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
    <script type="text/javascript" src="/static/snap.svg-min.js"></script>
 
    <script>
    window.onload=function(){
    brython(1);
    }
    </script>
</head>
<body>
 
<svg width="800" height="800" viewBox="0 0 800 800" id="svgout"></svg>
 
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window, document
 
# 透過 window 與 JSConstructor 從 Brython 物件 snap 擷取 Snap 物件的內容
snap = JSConstructor(window.Snap)
 
s = snap("#svgout")
# 畫直線
s.line(0, 0, 100, 100).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "1"  }).attr({ 'id': 'line1' })
</script>
</body>
</html>
'''
    return outstring
