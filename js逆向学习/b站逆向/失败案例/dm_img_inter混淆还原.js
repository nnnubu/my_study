 /*dm_img_inter:{
    'ds':[{"t":7,"c":"dnVpX2J1dHRvbiB2dWlfYnV0dG9uLS1kaXNhYmxlZCB2dWlfcGFnZW5hdGlvbi0tYnRuIHZ1aV9wYWdlbmF0aW9uLS1idG4tc2lkZQ","p":[258,86,86],"s":[0,0,0]}]
}*/

 //function1(336) = 'getElInfo' function1(270) = 'activityDetector' function1(282) = 'logstack' 刷新了几次，都是固定字符串
 //this('getElInfo') = function2    ds = function2(this['activityDetector']['logstack'],*args)

 //----------------需要还原的方程  function2(参数1，参数2)
 // 分析：可以只需要一个参数1，参数2可以是undefined，参数1是记录鼠标移动和点击事件的50次(x,y,prex,prey)鼠标移动之后的位置和移动之前的位置
 // 貌似是取最后一次事件的各项数据{
 //     "type": "mousemove",
 //     "x": 600,
 //     "y": 867,
 //     "preX": 600,
 //     "preY": 866,
 //     "changeDistance": 0,
 //     "timestamp": 3825685,
 //     "preType": "mousemove", 还要记录前一次的鼠标事件类型
 //     "target": {}
 // }

 //ds默认也可以为[],那么接下来分析wh和of

 //wh
 //'wh': _0xb3fd69([~~this[_0x286186(0x185)], ~~this[_0x286186(0x122)]])    👉   _0xb3fd69(this['winWidth'],this['winHeight'])
 //_0xb3fd69        a  = this['winWidth']   b = this['winHeight']   c = Math['floor'](Math['random']()*114)
 //                 [2*(a+b)+3*c,4*a-b+c,c]     [3691, 2472, 11]    a默认为1920    b默认为971
 //wh的生成就是，传入两个参数，分别为屏幕的宽度和高度，记作a，b，用数学方法生成一个随机数c最后返回的值就是这个上面一行的算式子

 //of
 //'of': _0x445907([~~this[_0x286186(0x16a)], ~~this['scrollLeft']])   👉    _0x445907([~~this['scrollTop'], ~~this['scrollLeft']])
 //                 a = this['scrollTop']   b = this['scrollLeft']  c = Math['floor'](Math['random']()*514)     a，b都默认为0
 //                 [3*a+2*b+c,4*(a-b)+2*c,c]   [190, 380, 190]
 //of的生成与wh的生成类似

 //     dict = {"ds": [],"wh": [3691,2472,11],"of": [190,380,190]}
 //dm_img_inter = JSON['stringify'](dict)