var CryptoJS = require('/usr/local/lib/node_modules/lib/node_modules/crypto-js')

// captchaKey = (Date.now() + (function () {
//     // var _0x43a4ae = _0x5bff;
//     for (var _0x537026 = [], _0x206d04 = '0123456789abcdef', _0x14331e = 0x0; _0x14331e < 0x24; _0x14331e++)
//         _0x537026[_0x14331e] = _0x206d04['substr'](Math["floor"](0x10 * Math['random']()), 0x1);
//     return _0x537026[0xe] = '4',
//         _0x537026[0x13] = _0x206d04['substr'](0x3 & _0x537026[0x13] | 0x8, 0x1),
//         _0x537026[0x8] = _0x537026[0xd] = _0x537026[0x12] = _0x537026[0x17] = '-',
//         _0x537026['join']('');
// }()))

function getcaptchaKey(time) {
    captchaKey = time + (function () {
        // var _0x43a4ae = _0x5bff;
        for (var _0x537026 = [], _0x206d04 = '0123456789abcdef', _0x14331e = 0x0; _0x14331e < 0x24; _0x14331e++)
            _0x537026[_0x14331e] = _0x206d04['substr'](Math["floor"](0x10 * Math['random']()), 0x1);
        return _0x537026[0xe] = '4',
            _0x537026[0x13] = _0x206d04['substr'](0x3 & _0x537026[0x13] | 0x8, 0x1),
            _0x537026[0x8] = _0x537026[0xd] = _0x537026[0x12] = _0x537026[0x17] = '-',
            _0x537026['join']('');
    }())
    return CryptoJS.MD5(captchaKey).toString()
}


// console.log(getcaptchaKey('1715572433057'))


function gettoken(time,captchaId,captchaKey) {
    token = CryptoJS.MD5(time + captchaId + "slide" + captchaKey) + ':' + (parseInt(time) + 300000) || ''
    return token
}

console.log(gettoken('1715572433057',"npElQbBkROS2qozzS8V96ate7TBObVDF","511e5c8e42b44a1cef851fa435fd158a"))