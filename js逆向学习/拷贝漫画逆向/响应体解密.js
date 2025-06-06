function decrypt(response) {

    const CryptoJS = require('crypto-js');

    // a = response.results.substring(0, 16)
    // b = response.results.substring(16, response.results.length)

    a = response.substring(0, 16)
    b = response.substring(16, response.length)

    f1 = function (t, e) {
        t = this.words = t || []
            this.sigBytes = null != e ? e : 4 * t.length
    }

    f2 = function (t) {
        for (var e = t.length, r = [], i = 0; i < e; i += 2)
            r[i >>> 3] |= parseInt(t.substr(i, 2), 16) << 24 - i % 8 * 4;
        return new f1(r, e / 2)
    }

    f3 = function (t) {
        var e = t.words
            , r = t.sigBytes
            , i = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
        // f3.clamp();
        for (var n = [], o = 0; o < r; o += 3)
            for (var s = (e[o >>> 2] >>> 24 - o % 4 * 8 & 255) << 16 | (e[o + 1 >>> 2] >>> 24 - (o + 1) % 4 * 8 & 255) << 8 | e[o + 2 >>> 2] >>> 24 - (o + 2) % 4 * 8 & 255, a = 0; a < 4 && o + .75 * a < r; a++)
                n.push(i.charAt(s >>> 6 * (3 - a) & 63));
        var c = i.charAt(64);
        if (c)
            for (; n.length % 4;)
                n.push(c);
        return n.join("")
    }

    f4 = function (t) {
        for (var e = t.length, r = [], i = 0; i < e; i++)
            r[i >>> 2] |= (255 & t.charCodeAt(i)) << 24 - i % 4 * 8;
        return new f1(r, e)
    }

    f5 = function (t) {
        return f4(unescape(encodeURIComponent(t)))
    }

    const data = f3(f2(b))
    const iv = f5(a)
    const password = 'xxxmanga.woo.key'
    const key = f5(password)
    const dict = {'iv': iv, 'mode': CryptoJS.mode.CBC, 'padding': CryptoJS.pad.Pkcs7}

    new_data = JSON.parse(CryptoJS.AES.decrypt(data, key, dict).toString(CryptoJS.enc.Utf8).toString())

    return new_data

}