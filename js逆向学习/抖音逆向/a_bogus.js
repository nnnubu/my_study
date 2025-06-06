require('./env')

function a_bogus(args, ua) {

    gr_obj = new gr()

    env_lists = [[0.00390625, 1, 14], [0.00390625, 1, 12], [0.00390625, 1, 0], [0.00390625, 1, 4]]

    end_str = 'dhzx'

    params = args + end_str

    params_32 = gr_obj.sum(gr_obj.sum(params))  //已检查无误

    end_str_32 = gr_obj.sum(gr_obj.sum(end_str))    //已检查无误

    function generate_ua_str(ua) {

        a256 = (function () {
            let array = new Array(256);
            for (let i = 0; i < 256; i++) {
                array[i] = 255 - i;
            }
            return array;
        })();

        (function test1() {
            let change_index = 0
            env_list = env_lists[0]
            let f3 = String.fromCharCode.apply(null, env_list)   //这个其实就是'\x00\x01\x0E'之类的数据
            for (let index = 0; index < 256; index++) {
                let index_val = a256[index]
                let t1 = change_index * index_val
                let t2 = change_index + t1
                let t3 = index % 3
                let t4 = f3.charCodeAt(t3)
                let t5 = t2 + t4
                change_index = t5 % 256
                a256[index] = a256[change_index]
                a256[change_index] = index_val
            }
        }())

        return (function test2(ua) {
            let ua_str = ""
            let change_index = 0
            for (let index = 1; index <= ua.length; index++) {
                let index_val = a256[index]
                let t1 = change_index + index_val
                change_index = t1 % 256
                a256[index] = a256[change_index]
                a256[change_index] = index_val
                let t2 = ua.charCodeAt(index - 1)
                let t3 = (a256[index] + a256[change_index]) % 256
                let t4 = t2 ^ a256[t3]
                let ua_char = String.fromCharCode(t4)
                ua_str += ua_char
            }
            return ua_str
        })(ua)
    }

    ua_str = generate_ua_str(ua)

    function demo() {
        o = o6
        v = [
            ua_str,
            String.prototype.charCodeAt,
            0,
            9,
            170,
            19,
            256,
            115,
            6241,
            6383,
            "1.0.1.19-fix.01"
        ]
        s = [
            [
                {},
                {}
            ],
            {
                "0": ua_str,
                "1": "s3"
            },
            ua_str,
            "s3",
            "=",
            {
                "s0": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
                "s1": "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
                "s2": "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
                "s3": "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe",
                "s4": "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe"
            },
            "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe",
            "",
            null,
            1
        ]
        a = 88
        p = 2
        d()
        return v[0]
    }

    ua_encrypt = demo()

    t = {
        "reg": [
            1937774191,
            1226093241,
            388252375,
            3666478592,
            2842636476,
            372324522,
            3817729613,
            2969243214
        ],
        "chunk": [],
        "size": 0
    }   //用不上

    ua_32 = gr_obj.sum(ua_encrypt)

    start_time = Date.now()

    middle_time = start_time + Math.floor(Math.random() * (20 - 10 + 1)) + 5

    end_time = middle_time + Math.floor(Math.random() * (20 - 10 + 1)) + 5

    screen_info = {
        "innerWidth": 835,
        "innerHeight": 975,
        "outerWidth": 1920,
        "outerHeight": 1080,
        "availWidth": 1920,
        "availHeight": 1080,
        "sizeWidth": 1920,
        "sizeHeight": 1080,
        "platform": "Win32"
    }

    screen_str = `${screen_info.innerWidth}|${screen_info.innerHeight}|${screen_info.outerWidth}|${screen_info.outerHeight}|${screen_info.availWidth}|${screen_info.availHeight}|${screen_info.sizeWidth}|${screen_info.sizeHeight}|${screen_info.platform}`; //这个其实太长了，不过也不重要

    function generate8(count = 0, list = []) {
        count += 1
        let f1 = function () {
            s[6] = Math.random() * 65535
            s[7] = (Math.random() * 65535) & 255
            s[8] = s[6] >> 8
        }
        let f2 = function () {
            s[9] = (s[7] & s[4]) | (1 & s[5])
            s[10] = (s[7] & s[5]) | (1 & s[4])
            s[11] = (s[8] & s[4]) | (0 & s[5])
            s[12] = (s[8] & s[5]) | (0 & s[4])
            list = list.concat([s[9], s[10], s[11], s[12]])
        }
        if (count === 1 || count === 3) {
            // count === 1 ? (list1 = [s[9], s[10], s[11], s[12]]) : (list2 = [s[9], s[10], s[11], s[12]])
            count === 1 ? function () {
                f1()
                f2()
                list = generate8(count, list, s, v)
            }() : function () {
                f2()
                return list
            }()
        } else if (count === 2) {
            f1()
            s[7] = (Math.random() * 240) >> 0
            v[0] = ((Math.random() * 255) >> 0) & 77
            v[0] += 2 + 16 + 32 + 128
            s[8] = v[0]
            list = generate8(count, list, s, v)
        }
        return list
// [(s[7] & s[4]) | (1 & s[5]), (s[7] & s[5]) | (1 & s[4]), (s[8] & s[4]) | (0 & s[5]), (s[8] & s[5]) | (0 & s[4])]
// 要执行三遍，第一遍生成list1,第三遍生成list2
// 第二遍生成最后s的基础并把s[7]改了，然后第三遍s[8]要把值换成v[0] 得到最后结果
// 但是这里我可以把修改全放在第二遍
    }

    //前缀乱码
    function generate4() {
        s = [
            [
                {
                    "5": {
                        "aid": 6383,
                        "pageId": 6241,
                        "boe": false,
                        "ddrt": 8.5,
                        "paths": {
                            "include": [
                                {},
                                {},
                                {},
                                {},
                                {},
                                {},
                                {}
                            ],
                            "exclude": [
                                {}
                            ]
                        },
                        "track": {
                            "mode": 0,
                            "delay": 300,
                            "paths": []
                        },
                        "slU": "",
                        "dump": true,
                        "rpU": "",
                        "ic": 8.5
                    }
                },
                {},
                "dhzx",
                start_time,
                end_time - start_time,
                {
                    "name": "Chrome"
                },
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null
            ],
            {
                "0": [
                    1,
                    0
                ]
            },
            [
                1,
                0
            ],
            0,//有时候又是1或2,不过这个好像用不上
            170,
            85
        ]
        s[6] = Math.random() * 65535
        s[7] = s[6] & 255     //s[6] & 255    (Math.random() * 65535) & 255
        s[8] = (Math.random() * 40) >> 0    //(s[6] >> 8) & 255 //(Math.random() * 40) >> 0
        s[9] = (s[7] & s[4]) | (3 & s[5])
        s[10] = (s[7] & s[5]) | (3 & s[4])
        s[11] = (s[8] & s[4]) | (82 & s[5])
        s[12] = (s[8] & s[5]) | (82 & s[4])
        let array = [s[9], s[10], s[11], s[12]]
        let str = String.fromCharCode.apply(null, array)
        // let hexStr = str.split('').map(char => {
        //     let hex = char.charCodeAt(0).toString(16);
        //     return '/x' + hex.padStart(2, '0');
        // }).join('');
        return str
        // [(s[7] & s[4]) | (3 & s[5]), (s[7] & s[5]) | (3 & s[4]), (s[8] & s[4]) | (82 & s[5]), (s[8] & s[5]) | (82 & s[4])]
    }

    function generate43_append(str) {
        list43 = []
        for (let i = 0; i < str.length; i++) {
            list43 = list43.concat(str.charCodeAt(i))
        }
        return list43
    }

    function generate4_append(end_time) {
        str = ((end_time + 3) & 255) + Z[303]
        n1 = str.charCodeAt(0)
        n2 = str.charCodeAt(1)
        n3 = str.charCodeAt(2)
        n4 = str.charCodeAt(3)
        list4 = [n1, n2, n3, n4].filter(value => !isNaN(value));
        return list4
    }

    function generate1_append(list, list8) {
        // list1和generate8有关
        // temp = list8里面的每个值^一遍    然后再对s里面的多个数据进行^运算，所以目前的任务是分析s里面每个数据的生成方法 生成方法设置断点g[0].length == 1834  或 == 207
        t = list8.concat(list)
        temp = t[0]
        for (let i = 1; i < t.length; i++) {
            temp ^= t[i]
        }
        list1 = [temp]
        return list1
    }   //用样本

    list43 = generate43_append(screen_str)  //已检查无误

    list4 = generate4_append(end_time)  //已检查无误

    list = [
        o1[288],
        (start_time - 1721836800000) / 1000 / 60 / 60 / 24 / 14 >> 0,
        o2[40],
        (end_time - start_time + o1[375]) & 255,
        end_time & o1[387],
        end_time >> 8 & 255,
        end_time >> 16 & 255,
        end_time >> 24 & 255,
        end_time / 256 / 256 / 256 / 256 & 255,
        end_time / 256 / 256 / 256 / 256 / 256 & 255,
        env_list[1] % 256 & 255,
        env_list[1] / 256 & 255,
        //o4是样本 Array.isArray(s) && s.length == 37 可分析 这个o4[0]我怀疑是params_32[28]
        o4[4] & 255,
        o4[4] >> 8 & 255,
        o4[0],
        o4[1],
        o4[2],
        o4[3],
        env_list[2] & 255,
        env_list[2] >> 8 & 255,
        env_list[2] >> 16 & 255,
        env_list[2] >> 24 & 255,
        params_32[9],
        params_32[18],
        // o1[625],
        params_32[o1[625]],
        end_str_32[10],
        end_str_32[19],
        // o1[714],
        end_str_32[o1[714]],
        ua_32[11],   //这里结果是变化的，如果不对应该是env_list里取值问题，最后一个元素有时候是变化的
        ua_32[21],
        // o1[803],
        ua_32[o1[803]],
        middle_time & 255,
        middle_time >> 8 & 255,
        middle_time >> 16 & 255,
        middle_time >> 24 & 255,
        middle_time / 256 / 256 / 256 / 256 & 255,
        middle_time / 256 / 256 / 256 / 256 / 256 & 255,
        3,
        6241 & 255, //"pageId": 6241
        6241 >> 8 & 255,    //"aid": 6383,
        6241 >> 16 & 255,
        6241 >> 24 & 255,
        6383 & 255,
        6383 >> 8 & 255,
        6383 >> 16 & 255,
        6383 >> 24 & 255,
        // screen_info,
        // screen_str,
        // list43,
        // list43.length,
        list43.length,
        0,
        // list4,
        // list4.length,
        list4.length,
        0
    ]

    list50 = [
        list[9],
        list[18],
        list[28],
        list[32],
        list[44],
        list[4],
        list[41],
        list[19],
        list[10],
        list[23],
        list[12],
        list[37],
        list[24],
        list[39],
        list[3],
        list[22],
        list[35],
        list[21],
        list[5],
        list[42],
        list[1],
        list[27],   //list[14]
        list[6],
        list[44],
        list[30],
        list[14],
        list[33],
        list[34],
        list[2],
        list[43],
        list[15],
        list[45],
        list[29],
        list[25],
        list[16],
        list[13],
        list[8],
        list[38],
        list[26],
        list[17],
        list[36],
        list[20],
        list[11],
        list[0],
        list[31],
        list[7],
        list[46],
        list[47],
        list[48],
        list[49]
    ]

    function generate138_8() {
        // 剩下130长度数组的生成规律
        o = o5
        s = [
            [
                {
                    "5": {
                        "aid": 6383,
                        "pageId": 6241,
                        "boe": false,
                        "ddrt": 8.5,
                        "paths": {
                            "include": [
                                {},
                                {},
                                {},
                                {},
                                {},
                                {},
                                {}
                            ],
                            "exclude": [
                                {}
                            ]
                        },
                        "track": {
                            "mode": 0,
                            "delay": 300,
                            "paths": []
                        },
                        "slU": "",
                        "dump": true,
                        "rpU": "",
                        "ic": 8.5
                    }
                },
                {},
                "dhzx",
                start_time,
                end_time - start_time,
                {
                    "name": "Chrome"
                },
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null
            ],
            {
                "0": [
                    1,
                    0
                ]
            },
            [
                1,
                0
            ],
            0,//有时候又是1或2,不过这个好像用不上
            170,
            85
        ]
        v = []

        //这个数组列表由前面生成的50+43+4+1也有可能是+3+1
        list8 = generate8()

        s[2] = [].concat(list50, list43, list4, generate1_append(list, list8))

        s[3] = []
        // s[4] ~ s[10] = o[6] 索引每次加5取到o[36]
        // 第一次生成主体，s[4]到s[10],后面每生成一个长度为4的数组就加3
        for (let i = 4, j = 6; j <= 36; i++, j += 5) {
            s[i] = o[j];
        }
        list130 = []
        for (s[10]; list130.length < 128; s[10] += 3) {
            // -----------------------------------------------------------------------------------------
            s[11] = Math.random() * 1000 & 255
            s[12] = (s[11] & s[4]) | (s[2][s[10]] & s[5])
            s[13] = (s[11] & s[6]) | (s[2][s[10] + o[117]] & s[7])          // o[117] == 0
            s[14] = (s[11] & s[8]) | (s[2][s[10] + o[142]] & s[9])             // o[142] == 2
            s[15] = ((s[2][s[10]] & s[4]) | (s[2][s[10] + o[171]] & s[6])) | (s[2][s[10] + o[186]] & s[8])
            list130 = list130.concat([s[12], s[13], s[14], s[15]])
            // -----------------------------------------------------------------------------------------
            //[(s[11] & s[4]) | (s[2][s[10]] & s[5]),(s[11] & s[6]) | (s[2][s[10] + o[117]] & s[7]) ,(s[11] & s[8]) | (s[2][s[10] + o[142]] & s[9]) ,((s[2][s[10]] & s[4]) | (s[2][s[10] + o[171]] & s[6])) | (s[2][s[10] + o[186]] & s[8])]
        }

        // s[10] o[271] o[275] s[10] s[2] s[10] o[55]
        // 重复以上步骤,直到长度达到128,也就是s[10]的长度到96的时候
        // s[2][s[10]] 加上去
        list130 = list130.concat([s[2][s[10]]])
        // s[2][s[10] + o[243]] 加上去
        if (s[2].length === 98) {
            list130 = list130.concat([s[2][s[10] + o[243]]])
        }

        list138 = [].concat(list8, list130)
        return [list138, list8]
    }

    list138 = generate138_8()[0]

    list8 = generate138_8()[1]

    str_138 = String.fromCharCode.apply(null, list138)

    function demo2() {
        o = o3
        v = [
            0,
            "Ó",
            String.prototype.charCodeAt,
            0,
            1,
            null,
            list138,
            Array.prototype.concat,
            list8,
            list130
        ]
        s = [
            [
                {},
                {}
            ],
            {
                "0": "Ó",
                "1": str_138
            },
            "Ó",
            str_138,
            (function () {
                let array = new Array(256);
                for (let i = 0; i < 256; i++) {
                    array[i] = 255 - i;
                }
                return array;
            })(),
            0,
            null,
            "",
            256,
            0
        ]
        a = 91
        p = 3
        d()
    }

    demo2()

    list256 = s[4]

    function generate_a_bogus() {
        o = o3
        v = [
            '',
            String,
            String.fromCharCode,
            str_138,
            String.prototype.charCodeAt,
            0,
            list138,
            Array.prototype.concat
        ]
        s = [
            [
                {},
                {}
            ],
            {
                "0": "Ó",
                "1": str_138
            },
            "Ó",
            str_138,
            list256,
            249,
            249,
            "",
            256,
            256,
            1,
            0
        ]
        // 问题在这里面的长度为256的数组 //已在demo2解决
        a = 247
        p = 5

        d()
        w = v[0]
        str = generate4() + w
        o = o6
        data = [
            [
                str,
                String.prototype.charCodeAt,
                0,
                9,
                75,
                58,
                256,
                208
            ],
            [
                str,
                String.prototype.charCodeAt,
                0,
                9,
                27,
                76,
                256,
                241
            ]
        ]
        randomIndex = Math.floor(Math.random() * data.length);
        // 随机选择 data 数组中的一个列表，并将其赋值给 v  虽说关系貌似不大
        v = data[randomIndex];
        s = [
            [
                {},
                {}
            ],
            {
                "0": str,
                "1": "s4"
            },
            str,
            "s4",
            "=",
            {
                "s0": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
                "s1": "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
                "s2": "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
                "s3": "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe",
                "s4": "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe"
            },
            "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe",
            "",
            null,
            1
        ]
        p = 2
        a = 88

        d()
        return v[0]
    }

    return generate_a_bogus()
}