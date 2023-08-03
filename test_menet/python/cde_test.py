import requests, random, aiohttp, asyncio

headers = {
    'Host': 'www.chinadrugtrials.org.cn',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://www.chinadrugtrials.org.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Referer':
    'http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

# cookies = {
#     'NID':
#     '511=TaV27o1S92YoVBFv_y8dJTQp7VVJ0qvn5m7iKJdCLPJVs0O9grw9SvSbNS6Wx3yeLeB4PPBjuAye-RKVQvNbRFw2VMtkGBvEftDoodg1Xt8WPCu2aBggv1FJXpp35H_AUil8J3pEWgA9oF7PrMyPb4huLU3OBv3HT2Ol5T0JmN0'
# }

# cookies = {
#     'FSSBBIl1UgzbN7N80S':
#     'dfK9XVCDmkTSBE280jPXyH44F9.VDn9uIa7W0jWClIYcgy.n6RyWc9_8yuOtrU_s',
#     'token':
#     '17EGmwgZNQrQ4Flfv1IIjEDF_akUrJrYdHiSczipXuQK9rrLxqscs5T2hdI',
#     'FSSBBIl1UgzbN7N80T':
#     '3WM_9B5E4AA517nB73dkBOuB414rvY9Y1pN14oGOKTvncxeinCHT4RVy5AJmRVf3BuXbsJTQ2c0SqfQeMi0.pPdHBblY6wl378NMeQWSmWls6mMKkSEfazubeCPoM2vtkVEZ45kLSGwTwYstzGKjNtbrjPzMzxR_pvgX2ZIIYT6K1rWvwCEqhZDO2Ez7aIV3VBErrIE3jkC_1t.CfhLXT0Wz.qq94LJ8nMalZM1PMJonpSRyKfCDnsL3vnwTVgf48Xn8PtLJpd3QZ1i450mHDY3sLTVdwJ38E2H5C6lM0XTK9CSEiUrlq116DJq82aUPOg.a7mse9ckI_061zEXE5iY4Jlc9f7FKATp_f9GIx5elk_q'
# }

# cookiea = {
#     'FSSBBIl1UgzbN7N80S':
#     'dfK9XVCDmkTSBE280jPXyH44F9.VDn9uIa7W0jWClIYcgy.n6RyWc9_8yuOtrU_s',
#     'token':
#     '17EGmwgZNQrQ4Flfv1IIjEDF_akUrJrYdHiSczipXuQK9rrLxqscs5T2hdI',
#     'FSSBBIl1UgzbN7N80T':
#     '3gCSCMskN9eTq3I9571EeU89NbKtTfx8q2lRNuJLlrtyAeAmGcP5Nzyn79GihGWseokzry3U6CR_1YSCx_RGkK1leJWmlCG0wZQ38seSH_pBsZ_FH5RMv5FimjoSfDriIKF9q_buVLwvj6MqRtaaEfFKz7EKs_KhB4Vz1wiKQYkmgam77UFG5Jsokn3gKr.70FCGQ3lEjlJHPRwBcW4a6UPyBSFqahXJsUwwCgIAKd8DtbJA8MWngwOznPfmtoqaJoknjvNPx7xj1O3Q9joj3D3eE3wgS0Q88DsGiQ.c_M0OMg0oeLmjj.uEO6Nu.WK9LuG51uoqF.QQhxcYlwrGLhVIPeCTjzMnceKCCckzujwVulG'
# }

cookies = {
    'FSSBBIl1UgzbN7N80S':
    'DOq1uowDqN08v.mu4G8N_6e3CTzANjx555A4kEo8LjrwCQANFmjtrgVkHOSk9sHD',
    'token':
    'nPN4dIqh9g21yh0qReXRw8BWgNTFYtMdZ2cPjMLnkCsNGGLTrV6mLvbzX7g',
    'FSSBBIl1UgzbN7N80T':
    '3fEAaFXNfmf2gsauozY7sYK9nB6IdaFep76c9S66ZAY7tWjVil2plUgvzJkZ1y93vZycWcB6UAXuNPPhmX78iT4h7XIaCU_VJabo2cWvu8NS5woFpirnDzW0cf6aRC5R1849PnYPKadXkoN5cExKYQlo02.RlrTIbKYleJ4r3FuCRHuz72Fbw2FsaZSK5Prwj6BvUkqNYnyQ52n_UU4HXVGqupbMgqHT6BDV662fIWx9CIng63XqM86DMf8r7zNBdY2qohWoiTEMLE0xxlwedoJ_1R_mPoMXhIkmfC4fYs76.Yxt5dN7lwi_wvvtWywQOTbdRE.wpyIR5DPI2sjfGlfkpue5AKv0zBQb7RfEvPM78.G'
}

url = "http://www.chinadrugtrials.org.cn/clinicaltrials.searchlistdetail.dhtml?_export=doc"
# url = 'https://sb-ssl.google.com/safebrowsing/clientreport/download?key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw'

payload = {'id': 'f30ed24e49f74c53a2bd240e4d01ba18'}


async def downlaod():
    # resp = requests.post(url,
    #                      headers=headers,
    #                      cookies=cookies,
    #                      data=payload,
    #                      verify=False,
    #                      timeout=30)
    # print(resp.status_code)

    session = aiohttp.ClientSession(cookies=cookies)

    resp = await session.post(url, json=payload, headers=headers)

    random_number = random.randint(100, 999)

    # if resp.status_code == 200:

    if resp.status == 200:
        file_path = './test/cde/cde_download_tmp_{}.doc'.format(random_number)

    else:
        file_path = './test/cde/cde_download_tmp_err_{}.html'.format(
            random_number)

    print('文件地址：{}'.format(file_path))

    # with open(file_path, "wb") as f:
    #     f.write(resp.content)

    content = await resp.read()

    with open(file_path, "wb") as f:
        f.write(content)

    print("end.............")


import collections


def format_data(data, replace_str=None):

    def replace_target(data):
        for match in replace_str:
            data = data.replace(match, '')
        return data

    def _format(data):

        if isinstance(data, str):
            data = replace_target(data)
            return data

        if isinstance(data, list):
            result = collections.deque()
            for d in data:
                d = _format(d)
                result.append(d)
            return list(result)

        if isinstance(data, dict):
            for key, value in data.items():
                value = _format(value)
                data[key] = value
            return data

        return data

    if not replace_str:
        return data

    data = _format(data)
    return data


from lxml.html import etree
import re


class TestParse:

    def parse_content(self):
        content = """<html>
    <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,Chrome=1" />
    <title>CTR20213351详细信息</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge,Chrome=1"/>

    <meta name="viewport"/>

    <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>

    <style></style>
    <meta id="9DhefwqGPrzGxEp9hPaoag" content="L4UKTblTUiTZjT`lT]hT^GTZfTZaT[UTbWT`I&amp;QAMSVVYGHWWS`G}GGKGXYJRST+V,_[O&gt;1P/(WoZ=@2&lt;q9-48^v0.M76wpI]35Qlua?)H:U\n;*tN`FrALsKbdce !#$%fghijkx{}~BDEG_GJLPSGJGZSPJLGJVUJH[GH)2)e)n&amp;&gt;?W&gt;R9P_OYWZVaS=UrLuZXWWURVt[&lt;S6P+V?V2M^KMN6KNPrSZYBO8KsVXL`SVQ,O3O+JOOKN:U8ScV9VMSUK]W]RsNPUsSPNCOSL7TuSuPY]Q%-}U{q3;@8Xp\8J{D3&lt;mE|,\E[3]`M^bHc:b`M^3Cc9&lt;),@)3)Z9@kFLK3rH|G(,?3r@8q(\,p)43kAa:&lt;BL83r,~ku~J*F\D3J`|8JuxMbq3sn9^pn|u|I,a{`{3pACH*FD3s(|},(|Zp`Ex3|uD^|&gt;~9FZxq3sBtA{43{IE~wz9&lt;Gq3JBD=wB{3t\L9,,tbCu|9|@t|,43pc?3{[va{6vXGk3FZ}t&lt;y}?3C)oc3tu,]]nKxu&gt;}IunD3{I*Xb`D=JI}^{z}+bF)m*u9^wzxm;BK4sB@Apy*3&lt;nD3(FLD;F:7rFkL*q3)B:2kyZ^F@~:Cco8&lt;Z48r6a^[c@oF@Z8Fy\?FF\*rk3k~9Gu[LFu)x(uZ|C3sBtb3)Fv:kZ*3,?M^(y9*r?~~&lt;Zkmw5@oGc?H&lt;)a`wIv3F(o7k&gt;~kkcKDFk3Jyv3&lt;mZ3)&gt;a8k)k3*H|I|~|+3FHLr&lt;c,&lt;&lt;cZ_3&lt;,EC]q3Cna3uH~6k&gt;)3G(@c{`C}w[EM|B]qC(CM]Itvw5~_3G`Ez{,@5p5Ka{I?3)&gt;)3*nCI(43;n}+p`EX{B,a]k3;5@swcLy|~-3(AqvoA4~Gy4-J?oL;q3,Z*ArH,Drq3r@EwFm@|),xq%*-)PCY_U@K_G5vyDNk6L8`u@S1KUlvGGa1fwjpSwNQYIlwUH8wdGCXxQaI`V1IA2OfKXNMsTBlFhbY1TOqms1Fd7O/3J/Ueo/lwPUy6It13TXX/o8otQ/eiruX-JO1PUrIpDBoIstdB_0tp^D1Q1gaFuTaIVr/pewT1BGNlwo8xLDCotIUIiPCxYUrwQwjQ3gJ2NvSo-QB1qgkw4I5k/21MXGCdP0j1nh/6dsjYaJkSeTSI67CSlHJptTXpfU8@As06i7uXTPuos%FJyP2P7nqnunonPn&amp;1onRnW7~7;n&gt;nZn@yOn}y#nFn8n)n%n:ysTSn5h6yWnKy~n(npn7wEyoFFnTw]nyeAy8a)nanAy%n;nw;6y1c5yun2F9nz1wyQw@;-y@wJyVy y;1s;R2(F6yBV yLyXywVQy*2gFuy}y{F(ygyKF&gt;F~1yyTFM2;F8FG1BcQ2s;z;$ypFoT60LFnF2TqyeA$9sy0FayF91FewWFhw$0S1LFq0qw0FVwGTB:M7kea0}wsw&amp;1;FsF|T;a9;UF}1eFT1J9{w%F FZwP7%egF0wKwSF%;Z1]FAFyFETcFp1FF:w{0O:|1$Fzw9wph7V*281V;}VVcs71wwen7Sw(;M1X2:aF11:7zT;ge6wLT#;|7)Vg1T1awu;J1Ew5k&gt;0gwXwOr%w#;*7#18:@75e&amp;wU;kw|zZwkwAaPze0&amp;Vek0eUw-zVhJk]1qh#e)1~172@9qV92er&gt;1RkkA~10:%;L7n1S1&gt;A@-nVs;%hX2y;{T(aXa(k#-E0RTA7c0U9LeS; :(;B26zEAg7M09VE;@a#V|ap2W0hVp1W;Fzoa*V-huzwzpas9Qh@r1Aoks9orcchT]Ae;n;Q2#T$k-;rhpa~1hcVh kukyhk;:eRVuh&amp;::V7T-hM7Ok*7T-gTVTU0Kay7B-Bh$:cerV::~2cz2;ezPa};716kS;#0#zKe%rzrZ0|c|:JrBVh7r-#Az0): V5rk07eVT5eE-o:a2R9Xkok$TMr99BV]cPkL:Vk@cUTJkUzqr-1U2EV{a7eWcgVMTo:u-Z21cq2qe~0Bh&gt;1cz;VSk2z00M-9eKcOz&amp;knAO-&gt;:;0neqTahcc@h~ATez9V-Ve{AMz9e$a$VK2%7L:{95akhLcK--:n;h-G2r0 ckVG-Sr8:B-5cce*c(9P9 -rkh1;cpeM-W:Qa|T aQc0;panAa-@rs0P:s;S7|VUr{Th9@cuz]-2rJ:&amp;:eaOk V67Ze]7yAn9]:Fc A1A-z7e29GeG:LznAke;-]c89M2S;0ee9:-&amp;1 c~z6-u-sTyhTV~hVzMc;kJAUhR-02Pc-rOAWA67AAhV%9Uc*-L-Tc9hFeF:RVz9RczVXAc2}aScSzkFr9p:PaJ-~Tka0zua;zJ9azLr7hGagTXa2ry-RVR-J-:ah1z:Z:oA)9;0rz%:2z(-wTL7oc:z}-KA(hnAVrocG1g25V#azcB9~zX:pa8zgrX:*VPa@98rE2$hqr;k9aeF{T2AXeprKVnh9VAk;7K9$c)aZ7]hz9(zGr09T9*eLT*:U-Qe5a6z|rLa&amp;0Qc}0F-y979yTscZ192L-8ARVFkp-A90-}aoAyr52F-qc#zah2VJ7JASApTE2ZArh{7&amp;rA0w:82B7qT~A2aar#r|AQT%7zVBaqAsaWTRzh:-T17$7g7WA]aR:W0z:TaV:X2n0XeQA&gt;cFzr-O01aAz@1(A*r(c6cM2Aw2V82a7Qaca-V(TTe1:rz12~z*z~VwaU2T7-A}c&amp;rU9&gt;V1AFc%z&gt;:ycoc1h;r@a{r~7R9|zW70-(V$:522:kcJ0TAZhW7uhOeO;K-PcRe#7:- 2h9e7{aT2Q-zcE7eeo9n0EVTF*A99w-1AAaL72TG96a :$02AwAPT:z:TrTQc&gt;A#rTr 2Xzsz-z)e(AKA5V@2*hAkX-XV}z$V0rPcr-pT9:1cncXhKh*-|9rA7A:r6rp99e::K:hcacW:0zS0yec:Ah(r:Vc7}r)T8:S:9a5TP:GeBe|VKaE920@ru7s-U7&gt;7(-{:]a:2&gt;2OVq-6hyTWha9hFJ-*9kh]:6e7zQ1&amp;78c]kMVLkF0p9c9&amp;7FV&gt;7Gc{-hAB0-0(:)T|cTA|e0790~Vo9)ho0;A&amp;aKe@2)F1e8rq9K9F0s9ATw9#rnrVzU-kaMcwTe9ZrW0krSh%rFa%V&amp;7*0eT7e97 hg:}:q-Frek%;q;Vr*0cVa2-rwVr007p2Va1hsVkA{ey;P0VTOAG9%cLk5k|9Sr2kWwT9zrR0:05kBT&amp;A%kR2wrakQe rh-7k{kZ;oeu2&amp;k:Tgh1c22o2Khh;9TZzA;)9}k~ehz{2 :&gt;VZ0Jz T&gt;;W2JTK;5-)zFe&gt;9grM0$cyzz:zk)cA:gePekr}k(aB9JeT-%0A;]Tuaw-Mk8AL0Zc$kTrr0a;2z8r&amp;kr06kK2u1kh5hZ9OVO-eh}kE;GT)eZhQ0&gt;kP1:2k0%;1h|;c7@hUhw;~7w1M1#9-rga]1u1-2]zBe-eszO;;1A7X1rV22zhE9E2{keV)aueJ-czR-;w::#;&amp;2U0o1Zz#wc2Gar2MA k7:E;wwV1n;OrG1PkawFk&amp;hr1|;8whheAJT}w*kw2|kcTnn~weeweX9ukGkOwnAuz5T@aGw1w;;&gt;w wzwo;(1%9WA80Gw&gt;hB;awBwq7E0u;sVy08nerQkVceA;T{h-AEwQ2p1*;Er]F#kqc7w}kg7UF)Tp1Qwywg1pF71)1}hS0{kzwMA0h)hP15-$FgV;k1FK;Ar$27;uk}FSF@F]FOh0FWFPF&amp;h:0*76FUh8w)FR1GVWyaykFk-ayAFLwaFBTz20yhT0a&gt;kA1K:w;TyPyywry]yEy20Wy)y:y-y|y7F5127Vy91@F-7PyZyz1{y(yMw~Aqy6w7yGwZyUF;y5FXyryRwRzcycnVzy1On9ncnkySyJn1FQe};yynnnFwyqn-TF:On*y&gt;nrn#y&amp;;X0]n]FcnOw6n|F$k6w8nsnLnhn6n n0y$nEngnXnGn$n{nUnSnQnJnMnBPh?7|)|Qyy)*Qyz(~Q}}xQyy)*1Ldif&lt;fc&lt;dRW+pw~a9+E]11p;p}^9KIwG7Gs2I`I6Zw1w|Z8[;\7w{qqqqqqqqqqqqqqqqqqqr1.I_S6UzhAiF5_JNCXV3rRymflqDP9eXTR_.f_U.oRk1A.gmblGNgNXUCOC50_DNpIb89mjOh6QsRlJPzgAZKnGzLheDITlSX8Hlhk674k128{L8azxWVZ_AVaiFfxGiKVwwSyGDnmrhV9BmUWWJueyk6SsWTYZobGBwrR4qUqYpspooYl8YTWJDSprml0wmV9JArShk0AxqfwWmV9isfSYc80QMty3bTK3U3p8PYbDU3rFfmjDUEYMkirEqKVPVJIWsMk0Au0OPjLcO.YGiKSf7EKW.M1y7haqqqqqqqqqqqqqqqqqK9CqqLtxmNkMI8PxB2u5vxAqV3DepKYwoYVrKpmmDV9JAq{qAJMgl_3SabrvUa_g6C8waDPtNGmS__VM8SuAGxZ4Df.F6bl.hXiec2.wnKYFgvVlJ1677516614416t1611661380hoKCrMAaiG1Jm25661D6152bb}R1eraz1P2h4W4LCK6h4r2XsbaRM72g6HjQtZn.OouthLXZ111hWZLOooM8eZZfnPoR3ABOKKDi3T2PcUKIe2gTsn3HJgL214QxEl7CPPMQQy4uknHHJQL9PtYtNGyPcntiR3zMkZBE6q.h1ejwOTZHsR.tDxPFPfB3bA5FCxXEOp0H6QkrT7ql80JVCcc7v1DpmR9p.sCpM822NUU7Q8TRNpbzwRme4ACSwImffYPRI3lf2VAk1Bl"><!--[if lt IE 9]><script r='m'>document.createElement("section")</script><![endif]--><script type="text/javascript" src="/4QbVtADbnLVIc/d.FxJzG50F.6152bb9.js?D9PVtGL=6152bb" r='m'></script><script type="text/javascript" r='m'>function _$ua(){return 7}function _$hT(_$h7,_$pe,_$jn,_$bm,_$vn,_$eu){_$h7=_$kF(_$i4(_$uP(_$h7)),2);var _$qI=_$in(_$uP(_$pe));_$pe=_$vW.call(_$qI,_$jI);_$jn=_$uP(_$jn);if(_$jn.length>0){_$jn=_$vW.call(_$jn,_$jI);_$pe=_$pe[_$nc()](_$jn);}var _$fq=_$ie();for (var _$oT=0;_$oT<_$h7.length;_$oT++ ){_$wc[_$fq+_$h7[_$oT]]=_$pe[_$oT];}_$bm=_$kF(_$uP(_$bm),2);_$qI=_$uP(_$vn);_$vn=_$vW.call(_$qI,_$jI);_$qI=_$uP(_$eu);_$eu=_$vW.call(_$qI,_$jI);_$vn=_$vn[_$nc()](_$eu);_$mh(_$bm,_$vn);}function _$q1(_$oT){var _$eu,_$qI=0,_$vn;_$oT=_$gl(_$oT);_$vn=_$oT.length;_$eu=new _$v0(_$vn);_$vn-=3;while (_$qI<_$vn){_$eu[_$qI]=_$vV.call(_$oT,_$qI++ );_$eu[_$qI]=_$vV.call(_$oT,_$qI++ );_$eu[_$qI]=_$vV.call(_$oT,_$qI++ );_$eu[_$qI]=_$vV.call(_$oT,_$qI++ );}_$vn+=3;while (_$qI<_$vn)_$eu[_$qI]=_$vV.call(_$oT,_$qI++ );return _$eu;}function _$qL(_$qI){for (var _$oT,_$eu,_$vn=_$qI.length-1;_$vn>0;_$vn-- ){_$oT=_$v8[_$nq()](_$tu()*_$vn);_$eu=_$qI[_$vn];_$qI[_$vn]=_$qI[_$oT];_$qI[_$oT]=_$eu;}return _$qI;}function _$gw(_$eu,_$pe,_$oT){_$pe=_$pe||0;if(_$oT===_$wa)_$oT=_$eu.length;var _$qI=new _$v0(_$v8[_$fr()](_$eu.length/40960)),_$h7=_$oT-40960,_$vn=0;while (_$pe<_$h7){_$qI[_$vn++ ]=_$qg[_$nx()](null,_$eu[_$ga()](_$pe,_$pe+=40960));}if(_$pe<_$oT)_$qI[_$vn++ ]=_$qg[_$nx()](null,_$eu[_$ga()](_$pe,_$oT));return _$qI.join(_$fv());}function _$ui(){return 8}function _$gl(_$qI){return _$k7(_$sI(_$qI));}function _$aw(){return 9}function _$jj(_$eu,_$vn){var _$qI=_$h0()[5];var _$oT=_$qI[_$vV.call(_$eu,_$vn)];if(_$oT<82)return 1;return 86-_$oT+1;}function _$iV(_$pe){var _$h7=_$pe.length,_$qI=new _$v0(_$h7),_$vn,_$oT,_$eu=_$mm();for (_$vn=0;_$vn<_$h7;_$vn++ ){_$oT=_$vV.call(_$pe,_$vn);if(_$oT>=32&&_$oT<127)_$qI[_$vn]=_$eu[_$oT-32];else _$qI[_$vn]=_$uJ.call(_$pe,_$vn);}return _$qI.join(_$nU());}function _$lE(){var _$oT=_$py();var _$eu=[];for (var _$fq=0;_$fq<6;_$fq++ ){_$eu[_$fq]=[];}_$h0=function(){return _$eu;};var _$h7=_$eu[0],_$vn=_$eu[1],_$jn=_$eu[2],_$pe=_$eu[3],_$ja=_$eu[4],_$qI=_$eu[5];_$jC(_$qI,0,255, -1);for (_$fq=0;_$fq<_$oT.length;_$fq++ ){var _$bm=_$vV.call(_$oT[_$fq],0);_$h7[_$bm]=_$fq<<2;_$vn[_$bm]=_$fq>>4;_$jn[_$bm]=(_$fq&15)<<4;_$pe[_$bm]=_$fq>>2;_$ja[_$bm]=(_$fq&3)<<6;_$qI[_$bm]=_$fq;}}function _$n1(){_$g4=_$wc[_$mI()][_$rS()]()[_$qo()](/[\r\n\s]/g,_$nU())!==_$pY();}function _$ov(_$eu){var _$qI;return function(_$oT,_$vn){if(_$qI===_$wa){_$qI=_$oN(_$eu);}return _$qI;};}function _$le(){return 406;}function _$in(_$oT){_$oT=_$vW.call(_$oT,_$fv());for (var _$qI=0;_$qI<_$oT.length-1;_$qI+=2){var _$eu=_$oT[_$qI];_$oT[_$qI]=_$oT[_$qI+1];_$oT[_$qI+1]=_$eu;}return _$oT.join(_$fv());}function _$mU(_$eu){var _$qI;return function(){if(_$qI===_$wa){_$qI=_$n5(_$eu);_$qI=_$uP(_$qI);}return _$qI;};}function _$iq(){var _$qI=new _$v0(256),_$vn=new _$v0(256),_$oT;for (var _$h7=0;_$h7<256;_$h7++ ){_$qI[_$h7]=_$qg(_$vn[_$h7]=_$h7);}var _$pe=_$th();for (_$h7=32;_$h7<127;_$h7++ )_$oT=_$h7-32,_$qI[_$h7]=_$uJ.call(_$pe,_$oT),_$vn[_$h7]=_$vV.call(_$pe,_$oT);_$pe=_$qI;_$fC=function(){return _$pe;};var _$eu=_$vW.call(_$gp(),_$nU());_$mm=function(){return _$eu;};}function _$f9(_$qI){var _$h7=_$sM();_$pe=_$uL();if(_$rX()){_$qI[_$jD(_$uA(),16)]=_$rR();}_$uB(_$qI);return _$rR();}function _$eU(){if(_$kF)/$/.test(_$lE());_$hT(_$uR(),_$uR(),_$uR(),_$uR(),_$uR(),_$uR());_$iq();_$v9=_$wc[_$cN()];_$tu=_$v8[_$fj()];_$tF=_$wc[_$nt()];_$c9=_$wc[_$cw()];_$nz=_$v8[_$mP()];_$vd=_$wc[_$m4()];try{_$vN=_$wc[_$du()];}catch(_$qI){}if(_$vN){try{_$vN[_$fp()]=_$fp();_$vN[_$jq()](_$fp());_$vN[_$eZ()]=_$du();}catch(_$qI){_$vN=_$wa;}}if( !_$en&& !_$nf){_$nf=0;_$en=0;_$eK=0;}if( !_$vd){_$vd=new _$a5();_$wc[_$m4()]=_$vd;}_$jK=_$d5(_$fJ());}function _$jG(){var _$eu=_$s4(_$cr(_$ch()))("9DhefwqGPrzGxEp9hPaoag"),_$h7=0,_$oT={};_$oT._$jF=_$pe;_$oT._$pc=_$qI;return _$oT;function _$vn(){var _$bm=_$vV.call(_$eu,_$h7);if(_$bm>=40){_$h7++ ;return _$bm-40;}var _$jn=39-_$bm;_$bm=0;for (var _$fq=0;_$fq<_$jn;_$fq++ ){_$bm*=87;_$bm+=_$vV.call(_$eu,_$h7+1+_$fq)-40;}_$h7+=_$jn+1;return _$bm+87;}function _$qI(){return _$vT.call(_$eu,_$h7);}function _$pe(){var _$jn=_$vn();var _$fq=_$vT.call(_$eu,_$h7,_$jn);_$h7+=_$jn;return _$fq;}}function _$oJ(){return 10}function _$tE(){return 4}function _$jp(){return "rAe||nao|yteep|oouatDseaMcEnplrnC||mnci|jteFId|aaeovecUrrsbItno|rnhtnteROaecpru";}function _$u2(){return 12}function _$aP(_$fq,_$rA,_$oT){var _$ja=_$v4();_$n1();var _$s7=0,_$sN=0;var _$vn=_$iV(_$k5());_$ja=_$v4();_$dD();var _$bw=_$rD();var _$tA=_$qH();var _$pK=_$qH();_$pK=_$pK[_$iP()](_$qH(true));var _$bm=_$qH();_$bm=_$bm[_$iP()](_$qH(true));var _$bA=_$qH()[_$iP()](_$qH(true));_$ja=_$v4();_$dD();var _$m1=_$rD();_$fq=_$d5(_$fq[_$eM()](_$s7));_$s7=0;_$ja=_$v4();var _$fo=_$rA[_$gv()](_$oT[1],_$oT[2]);var _$jn=_$rA[_$gv()](0,_$oT[0]);var _$b5=_$rA[_$gv()](_$oT[3],_$oT[4]);var _$r7=[_$bA,_$b5,[],_$jn,_$fo];if(_$wc[_$oN(_$u6(_$le()))]){_$qL(_$jn);}_$ja=_$v4();var _$eu,_$rE=0,_$p9=[_$wa,_$wa,_$wa,_$wa,_$wa,_$h7,_$pe,_$qI];_$eu=_$pe(1);_$ja=_$v4();_$pb(_$b5,_$bm);_$o2(_$oN(_$eu));return;function _$pg(){return _$fq[_$s7++ ];}function _$pe(_$dR){var _$ty=0,_$cD,_$fH,_$rz;if(_$dR===1){_$hx();if(_$fH<=4){return _$r7[_$fH][_$rz];}return _$p9[_$fH](_$rz);}_$cD=new _$v0(_$dR);while (_$ty<_$dR){_$hx();if(_$fH<=4){_$cD[_$ty++ ]=_$r7[_$fH][_$rz];}else{_$cD[_$ty++ ]=_$p9[_$fH](_$rz);}}return _$cD.join(_$nU());function _$hx(){_$fH=_$pg();_$rz=_$fH&0x1F;_$fH=_$fH>>5;if(_$rz==0x1f){_$rz=_$rN()+31;}}}function _$qH(_$ta){var _$hx,_$dR,_$fH,_$ty;_$dD();_$dR=_$rD();_$hx=_$rD();_$fH=_$s2(_$hx);if(_$dR===0&&_$hx===0)return[];var _$rz=_$fH[_$mx()](_$vn);if(_$ta){for (var _$cD=0;_$cD<_$dR;_$cD++ ){_$rz[_$cD]=_$n5(_$rz[_$cD]);}}return _$rz;}function _$s2(_$rz){var _$dR=_$s7;_$s7+=_$rz;return _$fq[_$b3()](_$dR,_$s7);}function _$rD(){var _$dR=_$nG(_$fq,_$s7);_$s7+=_$jj(_$fq,_$s7);return _$dR;}function _$qI(){var _$cD,_$rz,_$dR;_$cD=_$pe(1);_$pe(1);_$rz=_$pe(1);_$pe(1);_$dR=_$pe(1);_$wc[_$oN(_$cD)]=_$mE(_$rz,_$dR);}function _$dD(){if(_$sN=== -1)return;if(_$sN===0){_$s7++ ;if(_$fq[_$mV()](_$s7)===_$af()){_$s7++ ;}else if(_$fq[_$mV()](_$s7)===_$md()){_$sN= -1;_$s7++ ;return;}else{}}var _$dR;if( typeof(_$fq)===_$l2()){_$dR=_$vX(_$fq[_$eM()](_$s7+1,3));}else{_$dR=_$vX(_$gw(_$fq,_$s7+1,_$s7+4));}if(_$dR!==_$sN){}_$s7+=4;_$sN++ ;}function _$h7(_$cD){var _$dR=_$rN(),_$fH,_$su=new _$v0(_$cD),_$rz=new _$v0(_$dR),_$hx=new _$v0(_$cD+_$dR);if(_$cD==3){var _$oR=_$wc[_$jT()][_$nq()]((_$v4()-_$nR)/1000);_$nv=_$nv+_$wc[_$jT()][_$nq()](_$wc[_$jT()][_$eg()](_$oR/5.88+1));}_$fH=0;while (_$fH<_$dR)_$rz[_$fH++ ]=_$pe(1);_$fH=0;while (_$fH<_$cD)_$su[_$fH++ ]=_$pe(1);_$qL(_$su);_$fH=0;var _$aO=0,_$ty=0;while (_$aO<_$dR&&_$ty<_$cD){var _$ta=(_$tu()%100)*(_$dR-_$aO+1)/(_$cD-_$ty)>=50;var _$sK=_$tu()%10;if(_$ta){while (_$aO<_$dR&&_$sK>0){_$hx[_$fH++ ]=_$rz[_$aO++ ]; --_$sK;}}else{while (_$ty<_$cD&&_$sK>0){_$hx[_$fH++ ]=_$su[_$ty++ ]; --_$sK;}}}while (_$aO<_$dR)_$hx[_$fH++ ]=_$rz[_$aO++ ];while (_$ty<_$cD)_$hx[_$fH++ ]=_$su[_$ty++ ];return _$hx.join(_$nU());}function _$rN(){var _$dR=_$fq[_$s7];if((_$dR&0x80)===0){_$s7+=1;return _$dR;}if((_$dR&0xc0)===0x80){_$dR=((_$dR&0x3f)<<8)|_$fq[_$s7+1];_$s7+=2;return _$dR;}};;;;}function _$pb(_$eu,_$oT){for (var _$qI=0;_$qI<_$oT.length;_$qI++ ){_$wc[_$oN(_$eu[_$qI])]=_$ov(_$oT[_$qI]);}}function _$mE(_$eu,_$qI){var _$oT;return function(_$vn,_$h7){if(_$oT===_$wa){_$oT=_$lS(_$oN(_$eu),_$oN(_$qI));}return _$oT;};}function _$v4(){return new _$tV()[_$jg()]();}function _$sM(){return 5}function _$qB(_$qI,_$eu){_$en|=_$qI;if(_$eu)_$nf|=_$qI;}function _$nk(_$oT){var _$vn=_$qp&&new _$qp();if(_$vn){var _$h7=_$vn[_$be()];if( !_$h7){return;}var _$eu=_$h7[_$rS()]();var _$qI=_$vW.call(_$eu,_$j5());_$eu=_$qI[_$gB()]();if(_$eu===_$nU()&&_$qI.length>0)_$eu=_$qI[_$gB()]();if(_$aq.call(_$eu,_$mo())!== -1||_$vt(_$eu,_$fB())||_$eu===_$jz()){_$o3(_$oT,1);return true;}}}function _$sW(_$qI){_$uO(_$qI);_$qI[12]=_$ul();var _$vn=_$uA();_$pe=_$rR();var _$vn=_$um();_$vn=_$uW();_$tq(_$qI);return _$qI[_$jD(_$rX(),16)];}function _$ug(_$qI){var _$h7=_$uA();_$h7=_$rR();_$qI[_$jD(_$ui(),16)]=_$um();_$qI[12]=_$ul();return _$rX();}function _$i6(_$h7,_$qI){_$qI=_$vW.call(_$mW(_$qI),'|');_$h7=_$mW(_$h7);var _$eu,_$oT=_$vT.call(_$h7,0,2),_$vn;for (_$eu=0;_$eu<_$qI.length;_$eu++ ){_$vn=_$vT.call(_$h7,2+_$eu*2,2);_$wc[_$oT+_$vn]=_$wc[_$qI[_$eu]];}}function _$e2(_$qI){return _$qI[_$iR];}function _$oN(_$oT){var _$vn=_$oT.length,_$qI=new _$v0(_$vn),_$eu=0,_$h7=_$fC();while (_$eu<_$vn){_$qI[_$eu]=_$h7[_$vV.call(_$oT,_$eu++ )];}return _$qI.join(_$nU());}function _$uH(_$qI){_$uc(_$qI);var _$h7=_$ul();if(_$tE()){_$qI[_$jD(_$rc(),16)]=_$ae();}_$qI[6]=_$tE();_$qI[2]=_$ui();_$tm(_$qI);return _$ug(_$qI);}function _$me(_$qI){return function(){_$qI=(_$qI*17405+40643)>>9&0xFFFF;return _$qI;};}function _$uc(_$qI){var _$vn=_$oJ();_$h7=_$uA();var _$pe=_$ui();_$pe=_$um();_$qI[_$jD(_$uL(),16)]=_$ua();return _$oJ();}function _$b0(){var _$qI=_$uP(_$uR())[_$mx()](_$k5());for (var _$eu=0;_$eu<_$qI.length;_$eu++ )_$qI[_$eu]=_$vX(_$qI[_$eu]);return _$qI;}function _$sF(_$eu){var _$qI=[],_$oT,_$vn,_$h7,_$pe=_$vV.call(_$au(),0);for (_$oT=0;_$oT<_$eu.length;){_$vn=_$eu[_$oT];if(_$vn<0x80){_$h7=_$vn;}else if(_$vn<0xc0){_$h7=_$pe;}else if(_$vn<0xe0){_$h7=((_$vn&0x3F)<<6)|(_$eu[_$oT+1]&0x3F);_$oT++ ;}else if(_$vn<0xf0){_$h7=((_$vn&0x0F)<<12)|((_$eu[_$oT+1]&0x3F)<<6)|(_$eu[_$oT+2]&0x3F);_$oT+=2;}else if(_$vn<0xf8){_$h7=_$pe;_$oT+=3;}else if(_$vn<0xfc){_$h7=_$pe;_$oT+=4;}else if(_$vn<0xfe){_$h7=_$pe;_$oT+=5;}else{_$h7=_$pe;}_$oT++ ;_$qI.push(_$h7);}return _$gw(_$qI);}function _$uF(_$qI){var _$pe=_$u2();var _$pe=_$ae();if(_$uL()){_$h7=_$tE();}_$qI[_$jD(_$ul(),16)]=_$rX();_$qI[_$jD(_$uA(),16)]=_$rR();_$h7=_$ae();return _$qI[_$jD(_$uW(),16)];}function _$kp(){_$pm=_$vd[_$jM()];_$vd[_$jM()]=_$wa;_$vd._$kZ=_$v4();_$nR=_$vd._$kZ;_$qB(4,0);_$qB(2,_$nk(7));var _$h7=_$cQ();var _$eu=_$b0();var _$vn=_$b0();_$u6=_$qI;_$ee=_$vn[1];_$nv=_$vn[0];_$dB=_$vn[2];if(_$pm){_$aP(_$pm,_$h7,_$eu);_$pm=_$wa;}_$vd._$sm=_$v4();if(_$vd._$sm-_$vd._$kZ>12000){_$qB(1,1);_$o3(13,1);}else{_$qB(1,0);}_$qB(8,0);function _$oT(){return _$hr;}function _$qI(_$pe){return _$wc[_$oN(_$h7[_$pe])];}}function _$rR(){return 15}function _$vi(_$jn,_$vn){if( typeof _$jn===_$l2())_$jn=_$q1(_$jn);if( !_$vn)_$vn=_$py();var _$qI,_$eu=_$tt=0,_$oT=_$jn.length,_$pe,_$h7;_$qI=new _$v0(_$v8[_$eQ()](_$oT*4/3));_$oT=_$jn.length-2;while (_$eu<_$oT){_$pe=_$jn[_$eu++ ];_$qI[_$tt++ ]=_$vn[_$pe>>2];_$h7=_$jn[_$eu++ ];_$qI[_$tt++ ]=_$vn[((_$pe&3)<<4)|(_$h7>>4)];_$pe=_$jn[_$eu++ ];_$qI[_$tt++ ]=_$vn[((_$h7&15)<<2)|(_$pe>>6)];_$qI[_$tt++ ]=_$vn[_$pe&63];}if(_$eu<_$jn.length){_$pe=_$jn[_$eu];_$qI[_$tt++ ]=_$vn[_$pe>>2];_$h7=_$jn[ ++_$eu];_$qI[_$tt++ ]=_$vn[((_$pe&3)<<4)|(_$h7>>4)];if(_$h7!==_$wa){_$qI[_$tt++ ]=_$vn[(_$h7&15)<<2];}}return _$qI.join(_$nU());}function _$mW(_$jn){_$jn=_$vW.call(_$jn,'');var _$oT,_$eu=_$me(30035),_$qI=[],_$h7=_$jn.length,_$vn,_$pe;for (_$oT=0;_$oT<_$h7;_$oT++ ){_$qI.push(_$eu()%_$h7);}for (_$oT=_$h7-1;_$oT>=0;_$oT-- ){_$vn=_$qI[_$oT];_$pe=_$jn[_$oT];_$jn[_$oT]=_$jn[_$vn];_$jn[_$vn]=_$pe;}return _$jn.join('');}function _$pI(_$qI){if( !_$vN)return;if( typeof _$qI===_$nn()){_$qI=_$vQ(_$qI);}_$qI=_$c5()+_$vi(_$qI);return _$vN[_$qI];}function _$nM(){debugger;}function _$n9(){_$uJ=_$vQ.prototype.charAt;_$vV=_$vQ.prototype.charCodeAt;_$jo=_$vQ.prototype.codePointAt;_$vf=_$vQ.prototype.concat;_$q5=_$vQ.prototype.endsWith;_$fk=_$vQ.prototype.includes;_$aq=_$vQ.prototype.indexOf;_$ar=_$vQ.prototype.lastIndexOf;_$kv=_$vQ.prototype.localeCompare;_$go=_$vQ.prototype.match;_$mJ=_$vQ.prototype.normalize;_$hR=_$vQ.prototype.padEnd;_$ow=_$vQ.prototype.padStart;_$dS=_$vQ.prototype.repeat;_$vg=_$vQ.prototype.replace;_$bP=_$vQ.prototype.search;_$uN=_$vQ.prototype.slice;_$vW=_$vQ.prototype.split;_$n2=_$vQ.prototype.startsWith;_$vT=_$vQ.prototype.substr;_$vk=_$vQ.prototype.substring;_$hI=_$vQ.prototype.toLocaleLowerCase;_$mX=_$vQ.prototype.toLocaleUpperCase;_$uC=_$vQ.prototype.toLowerCase;_$eO=_$vQ.prototype.toSource;_$i7=_$vQ.prototype.toString;_$dF=_$vQ.prototype.toUpperCase;_$oO=_$vQ.prototype.trim;_$aL=_$vQ.prototype.trimLeft;_$qD=_$vQ.prototype.trimRight;_$iI=_$vQ.prototype.valueOf;}function _$jC(_$qI,_$eu,_$oT,_$vn){for (;_$eu<_$oT;_$eu++ ){_$qI[_$eu]=_$vn;}}function _$lS(_$vn,_$qI){_$vn=_$vn[_$mx()](_$bd());_$vn.push(_$qI);var _$h7=_$vn.length,_$oT=new _$v0(_$h7);for (var _$eu=0;_$eu<_$h7;_$eu++ ){_$oT[_$eu]=_$jm()[_$iP()](_$eu,_$i3());}return new _$e7(_$fO(),_$bt()+_$oT.join(_$bd())+_$fb())(_$vn);}function _$um(){return 1}function _$o3(_$oT,_$eu){if( !_$vN)return;if( typeof _$oT===_$nn()){_$oT=_$vQ(_$oT);}var _$qI=_$pI(_$oT);if(_$qI)_$eu=_$vX(_$qI)+_$eu;_$oT=_$c5()+_$vi(_$oT);_$vN[_$oT]=_$eu;}function _$cQ(){var _$oT=_$uP(_$uR());_$oT=_$kF(_$oT,2);var _$eu=_$iV(_$g2());for (var _$qI=0;_$qI<_$oT.length;_$qI++ ){_$oT[_$qI]=_$eu+_$oT[_$qI];}return _$oT;}function _$uA(){return 11}function _$tm(_$qI){_$qI[_$jD(_$uL(),16)]=_$ua();var _$pe=_$tE();_$vn=_$aw();_$qI[0]=_$um();return _$uW();}function _$uP(_$oT){var _$qI,_$pe=_$e2(_$oT),_$jn=new _$v0(_$pe-1);var _$eu=_$vV.call(_$oT,0)-40;for (var _$h7=0,_$vn=1;_$vn<_$pe; ++_$vn){_$qI=_$vV.call(_$oT,_$vn);if(_$qI>=40&&_$qI<127){_$qI+=_$eu;if(_$qI>=127)_$qI=_$qI-87;}_$jn[_$h7++ ]=_$qI;}return _$qg.apply(null,_$jn);}function _$n5(_$eu){var _$qI=_$d5(_$eu);return _$sF(_$qI);}function _$uE(_$qI){var _$vn=_$sM();_$pe=_$uL();_$qI[_$jD(_$rX(),16)]=_$u2();var _$vn=_$rc();_$h7=_$ae();return _$sM();}function _$ch(){return"_ZdslargmlZ[y pcrspl dslargmlZgb[y t_p v ; bmaskclr,ecrCjckclr@wGbZgb[9 t_p t ; v,amlrclr9 v,n_pclrLmbc,pckmtcAfgjbZv[9 pcrspl t9{{Z[[";}function _$uU(_$qI){var _$pe=_$ua();_$pe=_$oJ();var _$h7=_$aw();_$vn=_$ae()+_$sM();_$pe=_$oJ()+_$uA();_$sW(_$qI);_$qI[_$jD(_$qI[_$jD(_$tE(),16)],16)]=_$uE(_$qI);return _$uL();}function _$iv(){return "IspVv_sevXk587vq$a047t";}function _$qb(_$qI){return function(){return _$qI;};}function _$uO(_$qI){_$qI[14]=_$uW();_$qI[_$jD(_$ua(),16)]=_$oJ();var _$vn=_$aw();_$vn=_$ui();return _$um();}function _$d5(_$vn){var _$bm=_$vn.length,_$p9=new _$v0(_$v8[_$aW()](_$bm*3/4));var _$pK,_$qH,_$tA,_$sN;var _$jn=0,_$fq=0,_$oT=_$bm-3;var _$eu=_$h0();var _$r7=_$eu[0],_$dD=_$eu[1],_$pe=_$eu[2],_$h7=_$eu[3],_$ja=_$eu[4],_$qI=_$eu[5];for (_$jn=0;_$jn<_$oT;){_$pK=_$vV.call(_$vn,_$jn++ );_$qH=_$vV.call(_$vn,_$jn++ );_$tA=_$vV.call(_$vn,_$jn++ );_$sN=_$vV.call(_$vn,_$jn++ );_$p9[_$fq++ ]=_$r7[_$pK]|_$dD[_$qH];_$p9[_$fq++ ]=_$pe[_$qH]|_$h7[_$tA];_$p9[_$fq++ ]=_$ja[_$tA]|_$qI[_$sN];}if(_$jn<_$bm){_$pK=_$vV.call(_$vn,_$jn++ );_$qH=_$vV.call(_$vn,_$jn++ );_$p9[_$fq++ ]=_$r7[_$pK]|_$dD[_$qH];if(_$jn<_$bm){_$tA=_$vV.call(_$vn,_$jn);_$p9[_$fq++ ]=_$pe[_$qH]|_$h7[_$tA];}}return _$p9;}function _$rX(){return 0}function _$i4(_$oT){_$oT=_$vW.call(_$oT,_$fv());for (var _$qI=0;_$qI<_$oT.length-1;_$qI+=2){var _$eu=_$oT[_$qI];_$oT[_$qI]=_$oT[_$qI+1];_$oT[_$qI+1]=_$eu;}return _$oT.join(_$fv());}function _$kF(_$eu,_$pe){var _$vn=_$e2(_$eu),_$qI=new _$v0(_$ml(_$vn/_$pe)),_$oT=0,_$h7=0;for (;_$h7<_$vn;_$h7+=_$pe,_$oT++ )_$qI[_$oT]=_$vT.call(_$eu,_$h7,_$pe);return _$qI;}function _$pv(_$qI){_$qI[0]=_$uH(_$qI);_$qI[_$jD(_$qI[_$jD(_$rR()+_$rc(),16)],16)]=_$uF(_$qI);if(_$qI[_$jD(_$oJ()+_$uA(),16)]){_$f9(_$qI);}_$qI[1]=_$qI[_$jD(_$rR()+_$rc(),16)];return _$uU(_$qI);}function _$jD(_$eu,_$qI){return _$nz(_$eu)%_$qI;}var _$wa,_$vN;_$wc=window;_$vQ=String;_$n9();_$i6(_$iv(),_$jp());function _$nG(_$h7,_$pe){var _$qI=_$h0()[5];var _$vn=_$qI[_$vV.call(_$h7,_$pe)];if(_$vn<82)return _$vn;var _$eu=86-_$vn;_$vn=0;for (var _$oT=0;_$oT<_$eu;_$oT++ ){_$vn*=86;_$vn+=_$qI[_$vV.call(_$h7,_$pe+1+_$oT)];}return _$vn+82;}function _$m0(_$oT,_$vn){var _$eu=_$ie();for (var _$qI=0;_$qI<_$vn.length;_$qI++ ){_$wc[_$eu+_$oT[_$qI]]=_$qb(_$vn[_$qI]);}}function _$tq(_$qI){_$qI[8]=_$u2();_$qI[_$jD(_$rR(),16)]=_$rc();_$qI[9]=_$sM();return _$uL();}function _$uB(_$qI){var _$h7=_$rX();_$h7=_$u2();var _$vn=_$rc();_$pe=_$ae();_$qI[15]=_$uL();_$h7=_$oJ();return _$uA();}function _$mh(_$oT,_$vn){var _$eu=_$ie();for (var _$qI=0;_$qI<_$vn.length;_$qI++ ){_$wc[_$eu+_$oT[_$qI]]=_$mU(_$vn[_$qI]);}}function _$uW(){return 14}function _$uR(){return _$qy._$jF();}function _$jX(){var _$qI=_$uR();var _$eu=_$uR();_$qI=_$vW.call(_$uP(_$qI),_$jI);_$eu=_$vW.call(_$uP(_$eu),_$jI);_$m0(_$qI,_$eu);}_$qg=_$vQ.fromCharCode;_$ml=_$v8.ceil;_$jI=_$qg(96);var _$en,_$nf,_$eK;var _$rZ=1;_$iR=_$cr("qzs|u`v");;function _$vt(_$qI,_$eu){return _$uN.call(_$qI,0,_$eu.length)===_$eu;}function _$rc(){return 13}function _$o2(_$qI){if(_$qI===_$wa||_$qI===_$nU()){return;}var _$vn=_$wc[_$lO()][_$l3()],_$oT;if( !_$qS){_$qS=_$vn[_$jl()];}if(_$wc[_$li()]){_$oT=_$wc[_$li()](_$qI);}else{var _$eu=_$wc[_$mI()];_$oT=_$eu[_$hC()](_$wc,_$qI);}if(_$qS!==_$vn.push){_$vn.push=_$qS;}return _$oT;}function _$ae(){return 2}function _$sa(_$qI){var _$pe=_$uA();_$pe=_$rR();_$qI[3]=_$ae();_$qI[15]=_$uL();return _$ua();}function _$ul(){return 3}function _$kL(_$eu){var _$qI=arguments;return _$eu[_$qo()](/\{(.+?)\}/g,function(_$vn,_$oT){return _$qI[_$vX(_$oT)+1];});}function _$py(){return _$vW.call(_$it(),_$fv());};var _$qS;;_$qy=_$jG();_$jX();_$eU();function _$uL(){return 6}function _$ie(){return _$qg(95,36);}function _$cr(_$oT){var _$qI,_$pe=_$oT.length,_$jn=new _$v0(_$pe-1);var _$eu=_$vV.call(_$oT,0)-93;for (var _$h7=0,_$vn=1;_$vn<_$pe; ++_$vn){_$qI=_$vV.call(_$oT,_$vn);if(_$qI>=40&&_$qI<92){_$qI+=_$eu;if(_$qI>=92)_$qI=_$qI-52;}else if(_$qI>=93&&_$qI<127){_$qI+=_$eu;if(_$qI>=127)_$qI=_$qI-34;}_$jn[_$h7++ ]=_$qI;}return _$qg.apply(null,_$jn);}_$kp();;</script><script></script>
    <meta name="SiteName" content="国家药审"/>
    <meta name="SiteDomain" content="http://chinadrugtrials.org.cn"/>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta name="Keywords" content="查询详细信息"/>
    <meta name="ColumnKeywords" content="查询详细信息"/>
    <meta name="ColumnName" content="null"/>
    <meta name="ColumnType" content="null"/>
    <meta name="ColumnDescription" content="null"/>
    <meta name="ArticleTitle" content="CTR20213351详细信息"/>
    <meta name="Description" content="CTR20213351详细信息查询详细信息"/>
    <link href="/resource/css/bootstrap.min.css" rel="stylesheet">
    <link href="/resource/css/font-awesome.min.css" rel="stylesheet">
    <link href="/resource/css/bootstrap-select.min.css" rel="stylesheet">
    <link href="/skin/skin_01/style.css" rel="stylesheet">
    <link href="/resource/js/layer/skin/layer.css" rel="stylesheet">
    <link href="/resource/js/layer/skin/layer.ext.css" rel="stylesheet">
    <link href="/skin/origin.css" rel="stylesheet">
    <script type="text/javascript" src="/resource/js/jquery.min.js"></script>
    <script  src="/resource/js/clientmediatype.js"></script>
    </head>
    <body class="" ads="" style="background-color: rgb(244, 244, 244); min-height: 264px;">
        <header class="" style="">
        <div class="row " style="background-color: #3f69c4; box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);">
                <div class="container" style="">
                    <div class="column col-sm-3 col-md-3" style=""><div class="skin_01 eapblock " id="block1" style=""><style>
    /*内容样式片段*/
    .wrap_428 .widget-body{
        
    }
    </style>

    <div class="wrap_428">
        <div  class="widget-wrap">
            <div style="height: 80px;padding-top: 18px;">
        <img src="/website/img/logoFront.png" alt="">
    </div>
        </div>
    </div></div></div>
                    <div class="column col-sm-9 col-md-9" style="position: relative; padding-right: 140px;"><div class="skin_01 eapblock " id="block2" style=""><script type="text/javascript" src="/resource/js/leftnav/jquery.mmenu.all.min.js"></script>


    <div class="widget-menuwrap">
        <div id="hader-title" class="header-bg hidden-sm hidden-md hidden-lg">
            <a href="#widget-menu"></a>
            药物临床试验登记与信息公示平台
        </div>

        <nav id="widget-menu">
            <ul class="widget-nav clearfix">
                <li>
                    <a target="_self" href="/index.html">
                    首页
                    </a>
                </li>
                <li>
                    <a target="_self" href="/clinicaltrials.prosearch.dhtml">
                    试验公示和查询
                    </a>
                </li>
                <li>
                    <a target="_self" href="/clinicaltrials.index.dhtml">
                    试验登记
                    </a>
                </li>
                <li>
                    <a target="_self" href="/genericdrugs.index.dhtml">
                    备案平台
                    </a>
                </li>
                <li>
                    <a target="_self" href="/clinicaltrials.tongji.dhtml">
                    信息统计
                    </a>
                </li>
                <li>
                    <a target="_self" href="/helpLink.html">
                    帮助与链接
                    </a>
                </li>
                <li>
                    <a target="_self" href="/snipet/434.html">
                    关于平台
                    </a>
                </li>

            </ul>
        </nav>
    </div>



    <script type="text/javascript">
        var str;
        $(function() {
            str = $(".widget-menuwrap").html();
            window.onload=function() {
                initLayout();
                $(window).resize(function(){
                    initLayout();
                });
            };
        });
        function initLayout() {
            map_width=document.documentElement.clientWidth;
            if(map_width<768){
                $('nav#widget-menu').mmenu({
                    extensions	: [ 'effect-slide-menu', 'pageshadow','theme-white' ],
                    counters	: false,
                    slidingSubmenus: true,

                    navbar 		: {
                        title		: '网站导航'
                    },
                    navbars		: [
                        {

                            position	: 'top',
                            content		: [
                                'prev',
                                'title',
                                'close'
                            ]
                        }
                    ]
                });

            }else{
                $("#hader-title").remove();
                $("nav#widget-menu").remove();
                $(".widget-menuwrap").append(str);
            }
        }

    </script>
    </div><div class="skin_01 eapblock " id="block3" style="position: absolute; top: 15px; right: 65px; z-index:999;"><style>
    /*内容样式片段*/
    .wrap_435 .widget-body{
        
    }
    </style>

    <div class="wrap_435">
        <div  class="widget-wrap">
            <style>
    .inputBox {
    width: 50px;
    height: 50px;
    position: relative; z-index: 999;
    }
    .inputBox .search {
    position: absolute;
    margin: auto; 
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    width: 50px;
    height: 50px; text-align: center; color: #fff; line-height: 50px; font-size: 16px;
    background: #517bd6;
    border-radius: 50%;
    transition: all 1s;
    z-index: 4;
    box-shadow: 0 0 25px 0 rgba(0, 0, 0, 0.1);
    }
    .inputBox .search:hover {
    cursor: pointer;
    }
    .inputBox .search::before {
    content: url(/website/img/searchIcon.png);
    }
    .inputBox input {
    position: absolute;
    margin: auto;
    top: 0;
    right: 0;
    bottom: 0;
    /* left: 0; */
    width: 40px;
    height: 40px;
    outline: none;
    border: none;
    background: #fff;
    color: #777;
    border-radius: 30px;
    box-shadow: 0 0 25px 0 #517bd6, 0 0px 15px 0 rgba(0, 0, 0, 0.5);
    transition: all 1s;
    opacity: 0;
    z-index: 5;
    font-weight: bolder;
    }
    .inputBox input:hover {
    cursor: pointer;
    }
    .inputBox input:focus {
    width: 300px;
    padding: 0 80px 0 20px;
    opacity: 1;
    cursor: text;
    }
    .inputBox input:focus ~ .search {
    right: 0px;
    background: #f60;
    z-index: 6;
    }
    .inputBox input:focus ~ .search::before {
    content: "搜索"; 
    }
    .inputBox input::placeholder {
    color: #777;
    opacity: 0.8;
    }
    </style>
    <div class="inputBox">
        <input type="text" name="keywords" id="keywords" autocomplete="off" placeholder="查询药物试验 如输入糖尿病">
        <div class="search" id="goSearch"></div>
    </div>
    <script>
    $(function(){
        $("#goSearch").click(function(){
        window.location.href = encodeURI("/clinicaltrials.searchlist.dhtml?keywords="+$("#keywords").val());
        })
    })
    </script>
        </div>
    </div></div><div class="skin_01 eapblock " id="block4" style="position: absolute; top: 15px; right: 0px; z-index:999;"><style>
    /*内容样式片段*/
    .wrap_465 .widget-body{
        
    }
    </style>

    <div class="wrap_465">
        <div  class="widget-wrap">
            <script>
        function getCookie(name) {
            var cookies = document.cookie.split(";");
            for(var i=0;i<cookies.length;i++) {
                var cookie = cookies[i];
                var cookieStr = cookie.split("=");
                if(cookieStr && cookieStr[0].trim()==name) {
                    return  decodeURI(cookieStr[1]);
                }
            }
        }
        $(function () {
            if(getCookie("eap_username")!=undefined&&getCookie("eap_username")!=""){
            $.ajax({
            type: "get",
            url: "/clinicaltrials.getuserinfo.phtml",
            success: function(data){
                var jdata=jQuery.parseJSON(data);
                $("#topuser_name").html(jdata.user_name);
                $("#topname").html(jdata.name);
                $(".userinfo").css("display","block");
                $("#inBtn").css("display","none");
            }, error: function (xhr, textStatus, errorThrown) {
                if(xhr.status==401){
                    $(".userinfo").css("display","none");
                    $("#inBtn").css("display","block");
                }else{
                    $("#topuser_name").html("获取失败");
                    $("#topname").html("获取失败");
                    $(".userinfo").css("display","block");
                    $("#inBtn").css("display","none");
                }
            }
        });
            
            }else{
                console.log(2);
                $(".userinfo").css("display","none");
                $("#inBtn").css("display","block");
            }
            $("#inBtn").click(function(){
                window.location.href="/common.login.dhtml"
            })
            $("#dologout").click(function(){
                $.post("/common.login.logout.dhtml",
                "",
                function(data, textStatus){
                    $(".userinfo").css("display","none");
                    $("#inBtn").css("display","block");
                    localStorage.clear();
                    window.location.reload();
                });
            });
        })
    </script>
    <style>
        .inOutBtn{
            width: 50px; height: 50px; border-radius: 25px; background-color: #517bd6;
            text-align: center; cursor: pointer; 
            box-shadow: 0 0 25px 0 rgba(0, 0, 0, 0.1);
        line-height:50px;
        color:#fff
        }
        .inOutBtn img{
            display: block;
        }
        .userinfo{
            display: none;
        }
        .userinfo .dropdown-menu {
        min-width: 170px; margin-right: -60px; top: 95%;
        color: #fff;
        border-radius: 0;
        border: 0;
        text-align: center;
        padding: 0;
        background-color: #1991ec;
    }

    .userinfo .dropdown-menu li {
        line-height: 18px !important; padding: 12px;
        border-bottom: 1px #3aa6f8 solid;
    }

    .userinfo .dropdown-menu li:nth-of-type(odd) {
        background-color: #0e86e1;
    }

    .userinfo .dropdown-menu li a {
        color: #fff;
        padding: 0 !important;
    }

    .userinfo .dropdown-menu li a:hover {
        color: #fff;
        background-color: transparent;
    }
    .userinfo:hover .dropdown-menu {display: block;}
    </style>
    <div class="inOutBtn" id="inBtn">
        
        登录
    </div>

    <div class="dropdown pull-right userinfo">
        <a id="dLabel" role="button" aria-expanded="false" aria-haspopup="true" data-toggle="dropdown" data-target="#" >
        <div class="inOutBtn"><img src="/website/img/login.png" alt=""></div>
        </a>
        <ul class="dropdown-menu" aria-labelledby="dLabel">
        <li>当前账号：<span id="topuser_name"></span></li>
        <li  id="topname"></li>
        <li style="background-color: #e9a23e; border-bottom:0;"><a id="dologout" href="javascript:void(0)"><i class="fa fa-sign-out"></i>&nbsp;退 出 </a></li>
        </ul>
    </div> 
        </div>
    </div></div></div>
                </div>
            </div></header> 
        <main style="padding-top:15px;" class="">
        <div class="row clearfix">
                <div class="container">
                    <div class="col-md-12 column"></div>
                </div>
            </div><div class="row " style="">
                <div class="container" style="background-color: #fff; ">
                    <div class="column col-md-12" style="">
                        <div class='_main_content  skin_01' style=''><div class='_main_content null skin_01' style=''><link rel="alternate" type="application/rss+xml" href="/clinicaltrials.searchdetail.rss.dhtml?ckm_id=2c3156058a7b452e929810630dc8dc1d" title="RSS"/>
    <link href="/resource/component/clinicaltrials/css/lcsy.css" rel="stylesheet" media="screen">
    <link href="/resource/component/clinicaltrials/css/print.css" rel="stylesheet" media="print">
    <script>
    $(function(){
        if($(document).scrollTop()>=85){
        $(".goTop").show();
        }else{
        $(".goTop").hide();
        }
        $(window).scroll(function(){
        if($(document).scrollTop()>=85){
            $(".goTop").show();
        }else{
            $(".goTop").hide();
        }
        });
        $(".goTop").click(function () {
        $("html, body").animate({
            "scroll-top":0
        },"slow");
        });
    });
    //临床试验列表展开或关闭
    function open_close(id){
    var div = "#div_open_close_" + id;
    var input = "#" + id;
    var open_or_close = $(input).attr("class");
    //如果要检索的字符串值没有出现，则该方法返回 -1
    if(open_or_close.indexOf("down_icon") == -1){
    //没找到则是关闭状态,需要进行开启
    $(div).css("display","block");
    $(input).attr("class","down_icon2");
    }else{
    //找到则是展开状态,需要进行关闭
    $(div).css("display","none");
    $(input).attr("class","up_icon2");
    }
    }
    //打印
    function doPrint(){
    window.print();
    }
    function printit(){ 
    if (confirm('确定打印吗？')){
    var headhtml = "<html>" +
    "			<head>" +
    "				<title></title>" +
    "	    		<style>" +
    "		    		 .tabled , .tabled th , .tabled td{ border:1px solid;border-collapse: collapse; }" +
    "		    	</style>" +
    "			</head>" +
    "		<body>";
    var foothtml = "</body>";
    var newhtml = document.all.item('打印主题id').innerHTML;
    var oldhtml = document.body.innerHTML;
    document.body.innerHTML = headhtml + newhtml + foothtml;
    // 调用window.print方法打印新窗口
    $("#newsContent").show();
    window.print();
    // 将原来窗口body的html值回填展示
    document.body.innerHTML = oldhtml;
    return false;
    }
    if(getExplorer() == "IE"){
    pagesetup_null();
    }
    }
    function logdetail(id){
        $("#log_id").val(id)
        $("#logform")[0].submit();
    }

    //上/下/第一/最后一个试验
    function gotopage(currentpage){
        document.getElementById("currentpage").value = currentpage;
        document.getElementById("searchform").submit();
    }
    </script>

    <div class="onlyPrintVisible">
        药物临床试验登记与信息公示平台
    </div>
    <div class="btnNav marginBtm0" >
        <div class="container btnNavCon clearfix">
            <div class="currentPlace">
                <a href="/index.html">首页</a> &gt; <a href="/clinicaltrials.prosearch.dhtml">试验公示和查询</a> &gt; <a href="/clinicaltrials.searchlist.dhtml">公示列表</a> &gt;详细信息
            </div>
        </div>
    </div>


    <form action="/clinicaltrials.updatehistorypublic.dhtml" method="post" target="_blank" id="logform" style="display: inline;">
    <input type="hidden" name="id" id="log_id" value=""/>
    </form>								

    <div class="padding15 printHidden">

        <div class="pull-right">
            <form action="/clinicaltrials.searchlistdetail.dhtml?_export=doc" method="post" style="display: inline;">
                <input type="hidden" name="id" value="3f2a7f7fa9274298bf16dfa180a36c40"/>
                <button type="submit" class="btn btn-sm btn-info download"><span class="fa fa-download"></span> 下载</button>
                </form>
                <button type="button" class="btn btn-sm btn-info" onclick="window.location='/clinicaltrials.searchdetail.rss.dhtml?id=3f2a7f7fa9274298bf16dfa180a36c40'"><span class="fa fa-feed"></span> 订阅RSS</button>
                <button type="button" class="btn btn-sm btn-info" onclick="doPrint()"><span class="fa fa-print"></span> 打印</button>
        </div>

        查询条件： &nbsp;
        <span style="color: #f00;">
            无
        </span>
        
    </div>

    <div id= "toolbar_top" class="paddingSide15">

    <style>
    .f00{
        color:#F00
    }
    .radius_100{
        border-radius: 100px;
    }

    </style>
    <div class="row" style="border-top: 1px #dedede solid; text-align: center; padding: 40px 0; line-height: 32px; font-size: 16px;">


                <a href="javascript:void(0)" class="btn btn-default radius_100"  onclick="gotopage(3883);">
                    <span class="fa fa-angle-left"></span>
                    &nbsp;
                    上一个试验
                </a>

            &nbsp;&nbsp;&nbsp;
            目前是第 
            <span class="f00">3884</span> 个试验/共 
            <span class="f00">19402</span> 个试验
            &nbsp;&nbsp;&nbsp;

                <a href="javascript:void(0)" class="btn btn-default radius_100" onclick="gotopage(3885);" >
                    下一个试验
                    &nbsp;
                    <span class="fa fa-angle-right"></span>
                </a>

        

    </div>

        <form id="searchform" name="searchform" action="/clinicaltrials.searchlistdetail.dhtml" method="post">
            
            <input type="hidden" id="currentpage" name="currentpage" value="1"/>
            
            <input type="hidden" id="sort" name="sort"  value="desc"/>
            
            <input type="hidden" id="sort2" name="sort2" value=""/>
            <input type="hidden" id="rule" name="rule" value="CTR"/>
        </form>
    </div>


    <div class="paddingSide15">
        <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
            
            <div class="panel panel-default">
                <div class="panel-heading" role="tab" id="headingOne">
                    <h4 class="panel-title">
                        <a role="button" data-toggle="collapse"  href="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                            基本信息
                        </a>
                    </h4>
                </div>
                <div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">
                    <div class="panel-body">
                        <table class="searchDetailTable">
                            <tr>
                                <th width="15%">登记号</th>
                                <td width="35%">CTR20213351</td>
                                <th width="15%">试验状态</th>
                                <td width="35%">进行中</td>
                            </tr>
                            <tr>
                                <th>申请人联系人</th>
                                <td>杨双</td>
                                <th>首次公示信息日期</th>
                                <td>
                                2021-12-31
                                </td>
                            </tr>
                            <tr>
                                <th>申请人名称</th>
                                <td colspan="3">
                                    Merck Sharp & Dohme Corp./
                                    默沙东研发（中国）有限公司/
                                    MSD Ireland（Carlow）
                                </td>
                            </tr>
                        </table>
                            
                    </div>
                </div>
            </div>
            
            <div class="panel panel-default">
                <div class="panel-heading" role="tab" id="headingTwo">
                    <h4 class="panel-title">
                        <a class="collapsed" role="button" data-toggle="collapse"  href="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
                            公示的试验信息
                        </a>
                    </h4>
                </div>
                <div id="collapseTwo" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTwo">
                    <div class="panel-body">
                            <div class="searchDetailPartTit" style="margin-top: 0;">一、题目和背景信息</div>
                            <table class="searchDetailTable">
                                <tr>
                                    <th>登记号</th>
                                    <td colspan="3">CTR20213351</td>
                                </tr>
                                <tr>
                                    <th>相关登记号</th>
                                    <td colspan="3"></td>
                                </tr>
                                <tr>
                                    <th>药物名称</th>
                                    <td colspan="3">
                                        帕博利珠单抗注射液
                                        &nbsp;&nbsp;曾用名:MK-3475注射液,Pembrolizumab注射液
                                    </td>
                                </tr>
                                <tr>
                                    <th>药物类型</th>
                                    <td colspan="3">
                                    生物制品
                                    </td>
                                </tr>
                                <tr>
                                    <th>
                                        临床申请受理号
                                    </th>
                                    <td colspan="3">
                                        企业选择不公示
                                    </td>
                                </tr>
                                <tr>
                                    <th>适应症</th>
                                    <td colspan="3">肌层浸润性膀胱癌（MIBC）</td>
                                </tr>
                                <tr>
                                    <th>试验专业题目</th>
                                    <td colspan="3">一项在可耐受顺铂治疗的肌层浸润性膀胱癌受试者中评价围手术期Enfortumab Vedotin联合帕博利珠单抗（MK-3475）治疗对比吉西他滨联合顺铂新辅助治疗的III期、随机、开放性研究（KEYNOTE-B15/EV-304）</td>
                                </tr>
                                <tr>
                                    <th>试验通俗题目</th>
                                    <td colspan="3">可耐受顺铂治疗的MIBC中围手术期EV+帕博利珠单抗 vs 新辅助化疗</td>
                                </tr>
                                <tr>
                                    <th width="15%">试验方案编号</th>
                                    <td width="35%">KEYNOTE-B15 / EV-304</td>
                                    <th width="15%">
                                        方案最新版本号
                                    </th>
                                    <td width="35%">
                                        B15-02/EV-304
                                    </td>
                                </tr>
                                <tr>
                                    <th>版本日期:</th>
                                    <td>2022-04-04</td>
                                    <th>方案是否为联合用药</th>
                                    <td>是  </td>
                                </tr>
                            </table>
                            <div class="searchDetailPartTit">二、申请人信息</div>
                            <table class="searchDetailTable">
                                <tr>
                                    <th>申请人名称</th>
                                    <td colspan="5">
                                        <div class="input-group">
                                            <span class="input-group-addon">1</span>
                                            <input type="text" style="width: 500px;" class="form-control" readonly placeholder="" value="Merck Sharp & Dohme Corp.">
                                        </div>
                                        <div class="input-group">
                                            <span class="input-group-addon">2</span>
                                            <input type="text" style="width: 500px;" class="form-control" readonly placeholder="" value="默沙东研发（中国）有限公司">
                                        </div>
                                        <div class="input-group">
                                            <span class="input-group-addon">3</span>
                                            <input type="text" style="width: 500px;" class="form-control" readonly placeholder="" value="MSD Ireland（Carlow）">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <th width="15%" >联系人姓名</th>
                                    <td width="18%">杨双</td>
                                    <th width="15%">联系人座机</th>
                                    <td width="18%">020-38163955</td>
                                    <th width="15%">联系人手机号</th>
                                    <td width="19%"></td>
                                </tr>
                                <tr>
                                    <th>联系人Email</th>
                                    <td>shuang.yang3@merck.com</td>
                                    <th>联系人邮政地址</th>
                                    <td>北京市-北京市-朝阳区容达路21号</td>
                                    <th>联系人邮编</th>
                                    <td>100012</td>
                                </tr>
                            </table>	
                            <div class="searchDetailPartTit">三、临床试验信息</div>
                            <div class="sDPTit2">1、试验目的</div>
                            在≥18岁男性或女性，经组织学确认的肌层浸润性膀胱癌，临床分期为T2-T4aN0M0或T1-T4aN1M0的受试者中，比较A组（手术前enfortumab vedotin [EV] + 帕博利珠单抗和根治性膀胱切除术[RC] + 盆腔淋巴结清扫术[PLND]）与B组（吉西他滨+顺铂新辅助化疗和RC + PLND）的病理完全缓解（pCR）率，以及比较A组（围手术期EV+帕博利珠单抗和RC + PLND）与B组（吉西他滨+顺铂新辅助化疗和RC + PLND）的无事件生存期（EFS）
                            <div class="sDPTit2">2、试验设计</div>
                            <table class="searchDetailTable">
                                <tr>
                                    <th width="15%">试验分类</th>
                                    <td width="17%">
                                        安全性和有效性
                                    </td>
                            
                                    <th width="15%">试验分期</th>
                                    <td width="17%">
                                        III期
                                    </td>
                            
                                    <th width="15%">设计类型</th>
                                    <td width="17%">
                                        平行分组
                                    </td>
                                </tr>		
                                <tr>
                                    <th>随机化</th>
                                    <td>
                                        随机化
                                    </td>
                            
                                    <th>盲法</th>
                                    <td>
                                        开放
                                    </td>
                        
                                    <th>试验范围</th>
                                    <td>
                                        国际多中心试验
                                    </td>
                                </tr>
                            </table>
                            <div class="sDPTit2">3、受试者信息</div>
                            <table class="searchDetailTable">
                                <tr>
                                    <th width="15%">年龄</th>
                                    <td width="85%">
                                            18岁(最小年龄)至
                                            无上限
                                            (最大年龄)
                                    </td>
                                </tr>
                                <tr>
                                    <th width="15%">性别</th>
                                    <td width="35%">
                                            男+女
                                    </td>
                                </tr>
                                <tr>
                                    <th>健康受试者</th>
                                    <td colspan="3">
                                        无
                                    </td>
                                </tr>
                                <tr>
                                    <th>入选标准</th>
                                    <td colspan="3">
                                        <table class="subSearch">
                                            <tr>
                                                <td width="10%">
                                                1
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                通过BICR（中心病理学和/或中心影像学评估）确认诊断为尿路上皮癌（临床分期为T2-T4aN0M0或T1-T4aN1M0），主要组织学类型为尿路上皮癌（≥50%）并评估PD-L1表达水平（CPS≥10或CPS <10，对于无法评估的PD-L1，参见入选标准#4）。
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="10%">
                                                2
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                BICR通过影像学检查（胸部/腹部/盆腔的CT或MRI）确认的临床非转移性膀胱癌（N≤1，M0）
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="10%">
                                                3
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                泌尿科医生和/或肿瘤科医生认为适合进行RC + PLND，并同意接受附录9中引用的美国泌尿学会（AUA）/美国放射肿瘤学会（ASTRO）/美国临床肿瘤学会（ASCO）/泌尿外科肿瘤学会（SUO）指南所规定的根治性目的标准RC + PLND（如果适用，还包括前列腺切除术）
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="10%">
                                                4
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                行膀胱肿瘤TUR活检（在入组[签署ICF]前60天[+14天]内获得），提交中心病理学进行评估的组织样本，足以完成尿路上皮组织学确认和PD-L1表达检测。（如果无法评估样本中的PD-L1表达，则将该受试者分配至CPS <10组进行分层）
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="10%">
                                                5
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                男性或女性，签署书面知情同意时，年龄满18岁
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="10%">
                                                6
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                如果男性受试者同意在干预期间以及最后一次研究干预后一定时间内（每种研究干预体内消除所需最短时间）遵守以下要求，则可参加本研究。针对每种研究干预，避孕持续时间如下：
        Enfortumab Vedotin：180天
        吉西他滨/顺铂：95天
        帕博利珠单抗：0天（无要求）
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="10%">
                                                7
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                如果女性受试者没有怀孕或哺乳，并且至少符合以下情况之一，则可参加本研究。针对每种研究干预，避孕持续时间如下：
    -	Enfortumab Vedotin：180天
    -	吉西他滨/顺铂：180天
    -	帕博利珠单抗：120天
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="10%">
                                                8
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                提供参与本研究的书面知情同意书（受试者或监护人，如果适用）。
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="10%">
                                                9
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                ECOG体能状态为0或1。
                                                </td>
                                            </tr>
                                            <tr>
                                                <td width="10%">
                                                10
                                                </td>
                                                <td width="90%" style="text-align: left;">
                                                根据表6中定义，具有充分的器官功能。
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <th>排除标准</th>
                                    <td colspan="3">
                                            <table class="subSearch">
                                            <tr>
                                            <td width="10%">
                                            1
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            在本研究随机分组之前，已知尚有其他非尿路上皮来源的活动性恶性肿瘤或在本研究随机化前3年内接受积极抗癌治疗。
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            2
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            已经接受过针对MIBC的任何全身性治疗、放化疗和/或放疗。
    注：允许针对NMIBC的既往治疗-膀胱灌注治疗（例如，膀胱灌注卡介苗（BCG）或化疗）。不允许接受针对NMIBC的既往全身性治疗（包括但不限于使用帕博利珠单抗等抗PD-1/L1治疗）
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            3
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            通过影像学检查发现有≥N2疾病或转移性疾病（M1）
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            4
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            不耐受顺铂治疗，定义为符合以下任一标准：
    -	肾功能损伤，测定或计算所得CrCl <60 mL/min（通过以下方法之一计算：Cockcroft-Gault方法、MDRD公式或24小时尿液采集）
    -	ECOG体能状态≥2
    -	CTCAE v.5.0定义为≥2级周围神经病
    -	CTCAE v 5.0定义为≥2级听力损伤（没有相应临床症状的≥2级听力损伤听力异常，不需要被排除）；筛选时不要求进行听力测试；研究者可以自行决定是否进行该测试
    -	纽约心脏协会（NYHA）III级或更严重的心脏衰竭（https://manual.jointcommission.org/releases/TJC2016A/DataElem0439.html）
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            5
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            既往已接受过一种抗PD-1、抗PD-L1或抗PD-L2药物治疗或接受过另一种直接靶向刺激性或共抑制性T细胞受体的药物治疗（例如，CTLA-4、OX-40，CD137）。
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            6
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            既往在随机化之前3年内，接受过全身抗癌治疗，包括试验用药物（之前曾接受EV或其他基于MMAE的ADC的受试者将被排除）
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            7
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            已接受过任何膀胱放疗
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            8
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            已接受了部分膀胱切除术旨在切除任何NMIBC或MIBC
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            9
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            在第一次研究干预之前30天内接种了活疫苗或减毒活疫苗。允许接种灭活疫苗
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            10
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            目前正在参加或在第一次本研究干预之前4周内已经参加过,试验用药物的研究或使用了试验用器械
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            11
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            有≥2级感觉或运动神经病
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            12
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            诊断出免疫缺陷或第一次研究干预之前7天内接受慢性全身类固醇治疗（每天剂量超过10 mg泼尼松当量）或任何其他形式的免疫抑制治疗。在没有活动性自身免疫疾病的情况下，允许吸入或局部使用类固醇。允许肾上腺功能不全的受试者使用生理替代剂量（10 mg/天泼尼松当量）
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            13
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            对帕博利珠单抗和/或其任何辅料有重度（≥3级）超敏反应
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            14
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            已知对EV药物制剂中所含的任何辅料（包括组氨酸、海藻糖二水合物和聚山梨酯20）有重度（≥3级）超敏反应
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            15
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            对顺铂和/或吉西他滨和/或其任何辅料有重度（≥3级）超敏反应
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            16
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            有活动性角膜炎或角膜溃疡。如果研究者认为浅层点状角膜炎得到了适当治疗，则允许该病受试者参与研究
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            17
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            有活动性自身免疫疾病，在过去2年中进行了必需的全身性治疗（即，使用改善病情药物、皮质类固醇或免疫抑制药物）。替代治疗（例如，针对肾上腺、垂体功能不全等的甲状腺素、胰岛素或生理性皮质类固醇替代治疗）不被认为是全身性治疗，因此是允许的
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            18
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            有控制不佳的糖尿病病史。控制不佳的糖尿病定义为HbA1c≥8％或HbA1c为7％至<8％，且有没有其他可解释的相关糖尿病症状（多尿或烦渴）
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            19
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            既往存在需要类固醇治疗的（非感染性）肺部炎症病史或目前有肺部炎症
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            20
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            有需要全身性治疗的活动性感染。感染治愈后，可对受试者重新筛选一次。
    注：允许常规预防性抗菌用药，并且允许纳入接受预防性治疗的无症状性慢性感染受试者
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            21
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            已知有HIV感染史。除非当地卫生机构强制要求，否则不需要进行HIV检查
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            22
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            有已知乙型肝炎（定义为对HBsAg有反应性）或已知活动性丙型肝炎病毒感染（定义为检测到HCV-RNA[定性]）病史
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            23
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            具有任何可能混淆研究结果、干扰受试者参与全程研究的任何疾病、治疗或实验室异常的既往病史或当前证据，或者，根据研究者的判定，参与研究不符合受试者的最佳利益
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            24
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            已知有精神或药物滥用障碍，这些障碍将影响受试者配合完成研究要求的能力
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            25
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            在预计研究持续时间（从筛选访视至入选标准#6和#7所述时间段）内已怀孕或正在哺乳，或预期要怀孕或生育子女
                                            </td>
                                            </tr>
                                            <tr>
                                            <td width="10%">
                                            26
                                            </td>
                                            <td width="90%" style="text-align: left;">
                                            已经接受了同种异体组织/实体器官移植
                                            </td>
                                            </tr>
                                            </table>
                                    </td>
                                </tr>
                                
                            </table>
                            <div class="sDPTit2">4、试验分组</div>
                            
                            <table class="searchDetailTable">
                                <tr>
                                    <th width="15%">试验药</th>
                                    <td width="85%">
                                        <table class="subSearch">
                                            <tr>
                                                <th width="10%">序号</th>
                                                <th width="40%">名称</th>
                                                <th width="50%">用法</th>
                                            </tr>
                                            <tr>
                                                <td>
                                                1
                                                </td>
                                                <td>
                                                        中文通用名:帕博利珠单抗注射液<br>
                                                        英文通用名:Pembrolizumab Injection<br>
                                                        商品名称:可瑞达
                                                </td>
                                                <td >
                                                        剂型:注射剂<br>
                                                        规格:100mg/4ml<br>
                                                        用法用量:静脉输注，200mg，Q3W<br>
                                                        用药时程:17个周期
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                2
                                                </td>
                                                <td>
                                                        中文通用名:注射用enfortumab vedotin<br>
                                                        英文通用名:enfortumab vedotin for injection<br>
                                                        商品名称:NA
                                                </td>
                                                <td >
                                                        剂型:注射剂<br>
                                                        规格:30mg, 1 vial/kit<br>
                                                        用法用量:静脉输注，1.25 mg/kg，每周期第1和第8天<br>
                                                        用药时程:8个周期
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                3
                                                </td>
                                                <td>
                                                        中文通用名:帕博利珠单抗注射液<br>
                                                        英文通用名:Pembrolizumab Injection<br>
                                                        商品名称:可瑞达
                                                </td>
                                                <td >
                                                        剂型:注射剂<br>
                                                        规格:100mg/4ml<br>
                                                        用法用量:静脉输注，200mg，Q3W<br>
                                                        用药时程:17个周期
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                4
                                                </td>
                                                <td>
                                                        中文通用名:注射用enfortumab vedotin<br>
                                                        英文通用名:enfortumab vedotin for injection<br>
                                                        商品名称:NA
                                                </td>
                                                <td >
                                                        剂型:注射剂<br>
                                                        规格:30mg, 1 vial/kit<br>
                                                        用法用量:静脉输注，1.25 mg/kg，每周期第1和第8天<br>
                                                        用药时程:8个周期
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <th width="15%">对照药</th>
                                    <td width="35%">
                                        <table class="subSearch">
                                            <tr>
                                                <th width="10%">序号</th>
                                                <th width="40%">名称</th>
                                                <th width="50%">用法</th>
                                            </tr>
                                            <tr>
                                                <td>1</td>
                                                <td>
                                                        中文通用名:吉西他滨<br>
                                                        英文通用名:Gemcitabine<br>
                                                        商品名称:健泽
                                                </td>
                                                <td>
                                                        剂型:注射液<br>
                                                        规格:1000mg/支<br>
                                                        用法用量:静脉输注，第1天和第8天，1000 mg/m2<br>
                                                        用药时程:4个周期
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>2</td>
                                                <td>
                                                        中文通用名:注射用顺铂<br>
                                                        英文通用名:Cisplatin<br>
                                                        商品名称:NA
                                                </td>
                                                <td>
                                                        剂型:冻干粉<br>
                                                        规格:20mg/支<br>
                                                        用法用量:静脉输注，70 mg/m2
    Q3W<br>
                                                        用药时程:4个周期
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>3</td>
                                                <td>
                                                        中文通用名:注射用盐酸吉西他滨<br>
                                                        英文通用名:Gemcitabine Hydrochloride for Injection<br>
                                                        商品名称:健择
                                                </td>
                                                <td>
                                                        剂型:注射剂<br>
                                                        规格:1000mg/支<br>
                                                        用法用量:静脉输注，第1天和第8天，1000 mg/m2<br>
                                                        用药时程:4个周期
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>4</td>
                                                <td>
                                                        中文通用名:注射用顺铂<br>
                                                        英文通用名:Cisplatin for Injection<br>
                                                        商品名称:NA
                                                </td>
                                                <td>
                                                        剂型:冻干粉<br>
                                                        规格:20mg/支<br>
                                                        用法用量:静脉输注，70 mg/m2 Q3W<br>
                                                        用药时程:4个周期
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <div class="sDPTit2">5、终点指标</div>
                            
                            <table class="searchDetailTable">
                                <tr>
                                    <th width="15%">主要终点指标及评价时间</th>
                                    <td width="85%">
                                        <table class="subSearch">
                                            <tr>
                                                <th width="10%">序号</th>
                                                <th width="35%">指标</th>
                                                <th width="35%">评价时间</th>
                                                <th width="20%">终点指标选择</th>
                                            </tr>
                                            <tr>
                                                <td>1</td>
                                                <td>病理完全缓解（pCR）率：根据盲态中心病理学评估，来自RC + PLND的受检组织中无存活肿瘤细胞（pT0N0）</td>
                                                <td>最多约42个月</td>
                                                <td>
                                                有效性指标
                                                                                            </td>
                                            </tr>
                                            <tr>
                                                <td>2</td>
                                                <td>无事件生存期：从随机分组至首次发生以下事件的时间：
    术前发生无法根治手术的影像学疾病进展
    受试者因残留肌层浸润病灶和/或存在影像学病灶不能手术
    术中留有大体残留病灶
    术后局部或远处复发
    死亡</td>
                                                <td>最多约5年</td>
                                                <td>
                                                有效性指标
                                                                                            </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <th>次要终点指标及评价时间</th>
                                    <td>
                                            <table class="subSearch">
                                                <tr>
                                                    <th width="10%">序号</th>
                                                    <th width="35%">指标</th>
                                                    <th width="35%">评价时间</th>
                                                    <th width="20%">终点指标选择</th>
                                                </tr>
                                                <tr>
                                                <td>1</td>
                                                <td>总生存期（OS）：定义为从随机分组至任何原因死亡的时间</td>
                                                <td>最多约5年</td>
                                                <td>
                                                    有效性指标
                                                                                                </td>
                                                </tr>
                                                <tr>
                                                <td>2</td>
                                                <td>无病生存期（DFS）：定义为从术后基线扫描至首次发生以下任何一种情况的时间：
    -	BICR通过CT或MRI和/或活检评估发现有局部或远处复发
    -	任何原因死亡</td>
                                                <td>约从12个月到5 年</td>
                                                <td>
                                                    有效性指标
                                                                                                </td>
                                                </tr>
                                                <tr>
                                                <td>3</td>
                                                <td>病理降期（pDS）率：定义为根据中心病理学评估，来自RC + PLND的受检组织中疾病分期<pT2（包括pT0、pTis、pTa和pT1）且N0的受试者</td>
                                                <td>最多约42个月</td>
                                                <td>
                                                    有效性指标
                                                                                                </td>
                                                </tr>
                                                <tr>
                                                <td>4</td>
                                                <td>安全性和耐受性：
    -	受试者发生不良事件（AE）
    -	受试者因AE而停用研究药物
    -	受试者发生围手术期并发症</td>
                                                <td>最多约5年</td>
                                                <td>
                                                    安全性指标
                                                                                                </td>
                                                </tr>
                                                <tr>
                                                <td>5</td>
                                                <td>健康相关生活质量（HRQoL）较基线变化和至恶化时间：包括较基线变化EORTC QLQ-C30、BCI、EQ-5D-5L视觉模拟评分（VAS）、 EQ-5D-5L VAS</td>
                                                <td>最多约5年</td>
                                                <td>
                                                    有效性指标+安全性指标
                                                                                                </td>
                                                </tr>
                                            </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <div class="sDPTit2">
                                6、数据安全监查委员会（DMC）
                            </div>
                                    有
                            <div class="sDPTit2">
                                7、为受试者购买试验伤害保险
                            </div>	
                                
                                有

                            <div class="searchDetailPartTit">四、研究者信息</div>

                            <div class="sDPTit2">1、主要研究者信息</div>
                            <table class="searchDetailTable marginBtm10">
                                
                                <tr>
                                    <th width="5%" rowspan=3 style="text-align: center;">1</th>
                                    <th width="10%">姓名</th>
                                    <td width="18%">叶定伟</td>
                                    <th width="15%">学位</th>
                                    <td width="18%">博士</td>
                                    <th width="15%">职称</th>
                                    <td width="19%">主任医师</td>
                                </tr>
                                <tr>
                                    <th>电话</th>
                                    <td>021-64175590-1805</td>
                                    <th>Email</th>
                                    <td>dwyeli@163.com</td>
                                    <th>邮政地址</th>
                                    <td>上海市-上海市-东安路270号</td>
                                </tr>
                                <tr>
                                    <th>邮编</th>
                                    <td>200032</td>
                                    <th>单位名称</th>
                                    <td colspan="3">复旦大学附属肿瘤医院</td>
                                </tr>
                                
                            </table>
                            
                            <div class="sDPTit2">2、各参加机构信息</div>

                            <table class="searchDetailTable">
                                <tr>
                                    <th width="15%" class="text-center">序号</th>
                                    <th width="16%" class="text-center">机构名称</th>
                                    <th width="16%" class="text-center">主要研究者</th>
                                    <th width="16%" class="text-center">国家或地区</th>
                                    <th width="16%" class="text-center">省（州）</th>
                                    <th width="20%" class="text-center">城市</th>
                                </tr>
                                <tr>
                                    <td class="text-center">1</td>
                                    <td class="text-center">复旦大学附属肿瘤医院</td>
                                    <td class="text-center">叶定伟</td>
                                    <td class="text-center">中国</td>
                                    <td class="text-center">上海市</td>
                                    <td class="text-center">上海市</td>
                                </tr>
                                <tr>
                                    <td class="text-center">2</td>
                                    <td class="text-center">上海交通大学医学院附属仁济医院</td>
                                    <td class="text-center">薛蔚</td>
                                    <td class="text-center">中国</td>
                                    <td class="text-center">上海市</td>
                                    <td class="text-center">上海市</td>
                                </tr>
                                <tr>
                                    <td class="text-center">3</td>
                                    <td class="text-center">南京鼓楼医院</td>
                                    <td class="text-center">郭宏骞</td>
                                    <td class="text-center">中国</td>
                                    <td class="text-center">江苏省</td>
                                    <td class="text-center">南京市</td>
                                </tr>
                                <tr>
                                    <td class="text-center">4</td>
                                    <td class="text-center">湖南省肿瘤医院</td>
                                    <td class="text-center">韩惟青</td>
                                    <td class="text-center">中国</td>
                                    <td class="text-center">湖南省</td>
                                    <td class="text-center">长沙市</td>
                                </tr>
                                <tr>
                                    <td class="text-center">5</td>
                                    <td class="text-center">中山大学肿瘤防治中心</td>
                                    <td class="text-center">周芳坚</td>
                                    <td class="text-center">中国</td>
                                    <td class="text-center">广东省</td>
                                    <td class="text-center">广州市</td>
                                </tr>
                                <tr>
                                    <td class="text-center">6</td>
                                    <td class="text-center">南通市肿瘤医院</td>
                                    <td class="text-center">王小林</td>
                                    <td class="text-center">中国</td>
                                    <td class="text-center">江苏省</td>
                                    <td class="text-center">南通市</td>
                                </tr>
                                <tr>
                                    <td class="text-center">7</td>
                                    <td class="text-center">中山大学孙逸仙纪念医院</td>
                                    <td class="text-center">林天歆</td>
                                    <td class="text-center">中国</td>
                                    <td class="text-center">广东省</td>
                                    <td class="text-center">广州市</td>
                                </tr>
                                <tr>
                                    <td class="text-center">8</td>
                                    <td class="text-center">Fakultni Nemocnice Olomouc</td>
                                    <td class="text-center">Melichar, Bohuslav</td>
                                    <td class="text-center">捷克共和国</td>
                                    <td class="text-center">Olomouc</td>
                                    <td class="text-center">Olomouc</td>
                                </tr>
                                <tr>
                                    <td class="text-center">9</td>
                                    <td class="text-center">Fakultni Thomayerova nemocnice</td>
                                    <td class="text-center">Buchler, Tomas</td>
                                    <td class="text-center">捷克共和国</td>
                                    <td class="text-center">Praha 4</td>
                                    <td class="text-center">Praha 4</td>
                                </tr>
                                <tr>
                                    <td class="text-center">10</td>
                                    <td class="text-center">Fakultni nemocnice u sv. Anny v Brne</td>
                                    <td class="text-center">Katolicka, Jana</td>
                                    <td class="text-center">捷克共和国</td>
                                    <td class="text-center">Brno-mesto</td>
                                    <td class="text-center">Brno</td>
                                </tr>
                                <tr>
                                    <td class="text-center">11</td>
                                    <td class="text-center">CHU Jean Minjoz</td>
                                    <td class="text-center">Thiery-Vuillemin, Antoine</td>
                                    <td class="text-center">法国</td>
                                    <td class="text-center">Doubs</td>
                                    <td class="text-center">Besancon</td>
                                </tr>
                                <tr>
                                    <td class="text-center">12</td>
                                    <td class="text-center">Institut Universitaire du Cancer Toulouse - Oncopole</td>
                                    <td class="text-center">POUESSEL, Damien</td>
                                    <td class="text-center">法国</td>
                                    <td class="text-center">Haute-Garonne</td>
                                    <td class="text-center">Toulouse</td>
                                </tr>
                                <tr>
                                    <td class="text-center">13</td>
                                    <td class="text-center">CHU La Timone</td>
                                    <td class="text-center">Deville, Jean</td>
                                    <td class="text-center">法国</td>
                                    <td class="text-center">Bouches-du-Rhone</td>
                                    <td class="text-center">Marseille</td>
                                </tr>
                                <tr>
                                    <td class="text-center">14</td>
                                    <td class="text-center">Polyclinique du Bois</td>
                                    <td class="text-center">AMELA, Yaovi Eric</td>
                                    <td class="text-center">法国</td>
                                    <td class="text-center">Nord</td>
                                    <td class="text-center">Lille</td>
                                </tr>
                                <tr>
                                    <td class="text-center">15</td>
                                    <td class="text-center">CHU Limoges  Hopital Dupuytren</td>
                                    <td class="text-center">pestre munier, julia</td>
                                    <td class="text-center">法国</td>
                                    <td class="text-center">Haute-Vienne</td>
                                    <td class="text-center">Limoges</td>
                                </tr>
                                <tr>
                                    <td class="text-center">16</td>
                                    <td class="text-center">CHU de Brest -Site Hopital Morvan</td>
                                    <td class="text-center">Auberger, Benjamin</td>
                                    <td class="text-center">法国</td>
                                    <td class="text-center">Finistere</td>
                                    <td class="text-center">Brest</td>
                                </tr>
                                <tr>
                                    <td class="text-center">17</td>
                                    <td class="text-center">Centre Hospitalier Regional du Orleans</td>
                                    <td class="text-center">Meunier, Jerome</td>
                                    <td class="text-center">法国</td>
                                    <td class="text-center">Loiret</td>
                                    <td class="text-center">Orleans</td>
                                </tr>
                                <tr>
                                    <td class="text-center">18</td>
                                    <td class="text-center">Hopital Diaconesses Croix Saint Simon</td>
                                    <td class="text-center">Serrate, Camille</td>
                                    <td class="text-center">法国</td>
                                    <td class="text-center">Paris</td>
                                    <td class="text-center">Paris</td>
                                </tr>
                                <tr>
                                    <td class="text-center">19</td>
                                    <td class="text-center">Gustave Roussy</td>
                                    <td class="text-center">Loriot, Yohann</td>
                                    <td class="text-center">法国</td>
                                    <td class="text-center">Val-de-Marne</td>
                                    <td class="text-center">Villejuif</td>
                                </tr>
                                <tr>
                                    <td class="text-center">20</td>
                                    <td class="text-center">Caritas Krankenhaus St. Josef</td>
                                    <td class="text-center">Schnabel, Marco</td>
                                    <td class="text-center">德国</td>
                                    <td class="text-center">Bayern</td>
                                    <td class="text-center">Regensburg</td>
                                </tr>
                                <tr>
                                    <td class="text-center">21</td>
                                    <td class="text-center">Krankenhaus Martha Maria Halle-Doelau</td>
                                    <td class="text-center">Seseke, Florian</td>
                                    <td class="text-center">德国</td>
                                    <td class="text-center">Sachsen-Anhalt</td>
                                    <td class="text-center">Halle</td>
                                </tr>
                                <tr>
                                    <td class="text-center">22</td>
                                    <td class="text-center">Universitaetsklinikum Carl Gustav Carus</td>
                                    <td class="text-center">Propping, Stefan</td>
                                    <td class="text-center">德国</td>
                                    <td class="text-center">Sachsen</td>
                                    <td class="text-center">Dresden</td>
                                </tr>
                                <tr>
                                    <td class="text-center">23</td>
                                    <td class="text-center">Kath. Krankenhaus Marienhospital. Universitaetsklinik</td>
                                    <td class="text-center">Roghmann, Florian</td>
                                    <td class="text-center">德国</td>
                                    <td class="text-center">Nordrhein-Westfalen</td>
                                    <td class="text-center">Herne</td>
                                </tr>
                                <tr>
                                    <td class="text-center">24</td>
                                    <td class="text-center">Universitaetsklinikum Freiburg</td>
                                    <td class="text-center">Gratzke, Christian</td>
                                    <td class="text-center">德国</td>
                                    <td class="text-center">Baden-Wurttemberg</td>
                                    <td class="text-center">Freiburg</td>
                                </tr>
                                <tr>
                                    <td class="text-center">25</td>
                                    <td class="text-center">Universitaetsklinikum Muenster</td>
                                    <td class="text-center">Boegemann, Martin</td>
                                    <td class="text-center">德国</td>
                                    <td class="text-center">Nordrhein-Westfalen</td>
                                    <td class="text-center">Muenster</td>
                                </tr>
                                <tr>
                                    <td class="text-center">26</td>
                                    <td class="text-center">ATTIKON GENERAL UNIVERSITY HOSPITAL</td>
                                    <td class="text-center">Bamias, Aristotelis</td>
                                    <td class="text-center">希腊</td>
                                    <td class="text-center">Attiki</td>
                                    <td class="text-center">Chaidari</td>
                                </tr>
                                <tr>
                                    <td class="text-center">27</td>
                                    <td class="text-center">University General Hospital of Larissa</td>
                                    <td class="text-center">Kotsakis, Athanasios</td>
                                    <td class="text-center">希腊</td>
                                    <td class="text-center">Thessalia</td>
                                    <td class="text-center">Larissa</td>
                                </tr>
                                <tr>
                                    <td class="text-center">28</td>
                                    <td class="text-center">General Hospital of Athens</td>
                                    <td class="text-center">ZAGOURI, FLORA</td>
                                    <td class="text-center">希腊</td>
                                    <td class="text-center">Attiki</td>
                                    <td class="text-center">ATHENS</td>
                                </tr>
                                <tr>
                                    <td class="text-center">29</td>
                                    <td class="text-center">Ospedali Riuniti Umberto I GM Lancis G Salesi</td>
                                    <td class="text-center">Berardi, Rossana</td>
                                    <td class="text-center">意大利</td>
                                    <td class="text-center">Ancona</td>
                                    <td class="text-center">Ancona</td>
                                </tr>
                                <tr>
                                    <td class="text-center">30</td>
                                    <td class="text-center">AOU San Luigi Gonzaga di Orbassano</td>
                                    <td class="text-center">Buttigliero, Consuelo</td>
                                    <td class="text-center">意大利</td>
                                    <td class="text-center">Piemonte</td>
                                    <td class="text-center">Orbassano (TO)</td>
                                </tr>
                                <tr>
                                    <td class="text-center">31</td>
                                    <td class="text-center">IRCCS Ospedale San Raffaele</td>
                                    <td class="text-center">Necchi, Andrea</td>
                                    <td class="text-center">意大利</td>
                                    <td class="text-center">Milano</td>
                                    <td class="text-center">Milano</td>
                                </tr>
                                <tr>
                                    <td class="text-center">32</td>
                                    <td class="text-center">Azienda Ospedaliera Universitaria Integrata Verona - Ospedale Borgo Trento</td>
                                    <td class="text-center">Zivi, Andrea</td>
                                    <td class="text-center">意大利</td>
                                    <td class="text-center">Verona</td>
                                    <td class="text-center">Verona</td>
                                </tr>
                                <tr>
                                    <td class="text-center">33</td>
                                    <td class="text-center">Presidio Ospedaliero Santa Maria delle Grazie</td>
                                    <td class="text-center">Facchini, Gaetano</td>
                                    <td class="text-center">意大利</td>
                                    <td class="text-center">Napoli</td>
                                    <td class="text-center">Pozzuoli</td>
                                </tr>
                                <tr>
                                    <td class="text-center">34</td>
                                    <td class="text-center">Istituto Oncologico Veneto IRCCS-Oncologia Medica 1</td>
                                    <td class="text-center">Maruzzo, Marco</td>
                                    <td class="text-center">意大利</td>
                                    <td class="text-center">Padova</td>
                                    <td class="text-center">Padova</td>
                                </tr>
                                <tr>
                                    <td class="text-center">35</td>
                                    <td class="text-center">Narodowy Instytut Onkologii</td>
                                    <td class="text-center">Wiechno, Pawel</td>
                                    <td class="text-center">波兰</td>
                                    <td class="text-center">Mazowieckie</td>
                                    <td class="text-center">Warszawa</td>
                                </tr>
                                <tr>
                                    <td class="text-center">36</td>
                                    <td class="text-center">Wojewodzki Szpital im. Sw. Ojca Pio w Przemyslu</td>
                                    <td class="text-center">Kuc, Kamil</td>
                                    <td class="text-center">波兰</td>
                                    <td class="text-center">Podkarpackie</td>
                                    <td class="text-center">Przemysl</td>
                                </tr>
                                <tr>
                                    <td class="text-center">37</td>
                                    <td class="text-center">Szpital Wojewodzki im. Mikolaja Kopernika</td>
                                    <td class="text-center">Kwiatkowski, Mariusz</td>
                                    <td class="text-center">波兰</td>
                                    <td class="text-center">Zachodniopomorskie</td>
                                    <td class="text-center">Koszalin</td>
                                </tr>
                                <tr>
                                    <td class="text-center">38</td>
                                    <td class="text-center">CHLO, EPE - Hospital de Sao Francisco Xavier</td>
                                    <td class="text-center">Mourao, Ana</td>
                                    <td class="text-center">葡萄牙</td>
                                    <td class="text-center">Lisboa</td>
                                    <td class="text-center">Lisboa</td>
                                </tr>
                                <tr>
                                    <td class="text-center">39</td>
                                    <td class="text-center">Centro Hospitalar e Universitario de Coimbra</td>
                                    <td class="text-center">Nunes, Pedro</td>
                                    <td class="text-center">葡萄牙</td>
                                    <td class="text-center">Coimbra</td>
                                    <td class="text-center">Coimbra</td>
                                </tr>
                                <tr>
                                    <td class="text-center">40</td>
                                    <td class="text-center">Hospital Geral de Santo Antonio</td>
                                    <td class="text-center">Febra, Joana</td>
                                    <td class="text-center">葡萄牙</td>
                                    <td class="text-center">Porto</td>
                                    <td class="text-center">Porto</td>
                                </tr>
                                <tr>
                                    <td class="text-center">41</td>
                                    <td class="text-center">Inst. Portugues de Oncologia de Lisboa Francisco Gentil EPE</td>
                                    <td class="text-center">Cardoso, Catarina</td>
                                    <td class="text-center">葡萄牙</td>
                                    <td class="text-center">Lisboa</td>
                                    <td class="text-center">Lisboa</td>
                                </tr>
                                <tr>
                                    <td class="text-center">42</td>
                                    <td class="text-center">Cardiomed SRL Cluj-Napoca</td>
                                    <td class="text-center">Cainap, Calin</td>
                                    <td class="text-center">罗马尼亚</td>
                                    <td class="text-center">Cluj</td>
                                    <td class="text-center">Cluj-Napoca</td>
                                </tr>
                                <tr>
                                    <td class="text-center">43</td>
                                    <td class="text-center">Institutul Oncologic Prof.Dr. Ion Chiricuta Cluj-Napoca</td>
                                    <td class="text-center">Cebotaru, Cristina</td>
                                    <td class="text-center">罗马尼亚</td>
                                    <td class="text-center">Cluj</td>
                                    <td class="text-center">Cluj Napoca</td>
                                </tr>
                                <tr>
                                    <td class="text-center">44</td>
                                    <td class="text-center">Institutul Oncologic Prof.Dr. Ion Chiricuta Cluj-Napoca</td>
                                    <td class="text-center">Ciuleanu, Tudor</td>
                                    <td class="text-center">罗马尼亚</td>
                                    <td class="text-center">Cluj</td>
                                    <td class="text-center">Cluj-Napoca</td>
                                </tr>
                                <tr>
                                    <td class="text-center">45</td>
                                    <td class="text-center">SC Focus Lab Plus SRL</td>
                                    <td class="text-center">Iordan, Ingrid</td>
                                    <td class="text-center">罗马尼亚</td>
                                    <td class="text-center">Bucuresti</td>
                                    <td class="text-center">Bucuresti</td>
                                </tr>
                                <tr>
                                    <td class="text-center">46</td>
                                    <td class="text-center">Policlinica Oncomed SRL</td>
                                    <td class="text-center">Negru, Serban</td>
                                    <td class="text-center">罗马尼亚</td>
                                    <td class="text-center">Timis</td>
                                    <td class="text-center">Timisoara</td>
                                </tr>
                                <tr>
                                    <td class="text-center">47</td>
                                    <td class="text-center">S.C. Centrul de Oncologie Sf. Nectarie SRL</td>
                                    <td class="text-center">Schenker, Michael</td>
                                    <td class="text-center">罗马尼亚</td>
                                    <td class="text-center">Dolj</td>
                                    <td class="text-center">Craiova</td>
                                </tr>
                                <tr>
                                    <td class="text-center">48</td>
                                    <td class="text-center">SC Radiotherapy Center Cluj SRL</td>
                                    <td class="text-center">Ungureanu, Andrei</td>
                                    <td class="text-center">罗马尼亚</td>
                                    <td class="text-center">Cluj</td>
                                    <td class="text-center">Comuna Floresti</td>
                                </tr>
                                <tr>
                                    <td class="text-center">49</td>
                                    <td class="text-center">Hospital Clinico Universitario San Carlos de Madrid</td>
                                    <td class="text-center">Puente Vazquez, Javier</td>
                                    <td class="text-center">西班牙</td>
                                    <td class="text-center">Madrid</td>
                                    <td class="text-center">Madrid</td>
                                </tr>
                                <tr>
                                    <td class="text-center">50</td>
                                    <td class="text-center">Hospital Universitari de Girona Doctor Josep Trueta</td>
                                    <td class="text-center">Sala Gonzalez, Nuria</td>
                                    <td class="text-center">西班牙</td>
                                    <td class="text-center">Cataluna</td>
                                    <td class="text-center">Girona</td>
                                </tr>
                                <tr>
                                    <td class="text-center">51</td>
                                    <td class="text-center">Hospital Universitario Central de Asturias</td>
                                    <td class="text-center">Alvarez-Fernandez, Carlos</td>
                                    <td class="text-center">西班牙</td>
                                    <td class="text-center">Asturias</td>
                                    <td class="text-center">Oviedo</td>
                                </tr>
                                <tr>
                                    <td class="text-center">52</td>
                                    <td class="text-center">Xarxa Assistencial Universitaria Manresa</td>
                                    <td class="text-center">Domenech Santasusana, Montserrat</td>
                                    <td class="text-center">西班牙</td>
                                    <td class="text-center">Barcelona</td>
                                    <td class="text-center">Manresa</td>
                                </tr>
                                <tr>
                                    <td class="text-center">53</td>
                                    <td class="text-center">Hospital Universitario Insular de Gran Canaria</td>
                                    <td class="text-center">Gomez de Liano Lista, Alfonso</td>
                                    <td class="text-center">西班牙</td>
                                    <td class="text-center">Las Palmas</td>
                                    <td class="text-center">Las Palmas de Gran Canaria</td>
                                </tr>
                                <tr>
                                    <td class="text-center">54</td>
                                    <td class="text-center">Hospital Germans Trias i Pujol. ICO de Badalona</td>
                                    <td class="text-center">Font Pous, Albert</td>
                                    <td class="text-center">西班牙</td>
                                    <td class="text-center">Barcelona</td>
                                    <td class="text-center">Badalona</td>
                                </tr>
                                <tr>
                                    <td class="text-center">55</td>
                                    <td class="text-center">Hospital Virgen del Rocio</td>
                                    <td class="text-center">Perez Valderrama, Begona</td>
                                    <td class="text-center">西班牙</td>
                                    <td class="text-center">Sevilla</td>
                                    <td class="text-center">sevilla</td>
                                </tr>
                                <tr>
                                    <td class="text-center">56</td>
                                    <td class="text-center">CHUS - Hospital Clinico Universitario-Servicio de Oncologia</td>
                                    <td class="text-center">Anido Herranz, Urbano</td>
                                    <td class="text-center">西班牙</td>
                                    <td class="text-center">La Coruna</td>
                                    <td class="text-center">santiago de compostela</td>
                                </tr>
                                <tr>
                                    <td class="text-center">57</td>
                                    <td class="text-center">Hospital Universitari Vall d'Hebron-Departamento de Oncologia- VHIO</td>
                                    <td class="text-center">Morales Barrera, Rafael</td>
                                    <td class="text-center">西班牙</td>
                                    <td class="text-center">Cataluna</td>
                                    <td class="text-center">Barcelona</td>
                                </tr>
                                <tr>
                                    <td class="text-center">58</td>
                                    <td class="text-center">Lyell McEwin Hospital</td>
                                    <td class="text-center">Hocking, Christopher</td>
                                    <td class="text-center">澳大利亚</td>
                                    <td class="text-center">South Australia</td>
                                    <td class="text-center">Woodville South</td>
                                </tr>
                                <tr>
                                    <td class="text-center">59</td>
                                    <td class="text-center">Mater Hospital Brisbane</td>
                                    <td class="text-center">Oliveira, Niara</td>
                                    <td class="text-center">澳大利亚</td>
                                    <td class="text-center">Queensland</td>
                                    <td class="text-center">South Brisbane</td>
                                </tr>
                                <tr>
                                    <td class="text-center">60</td>
                                    <td class="text-center">Jewish General Hospital</td>
                                    <td class="text-center">McPherson, Victor</td>
                                    <td class="text-center">加拿大</td>
                                    <td class="text-center">QC</td>
                                    <td class="text-center">Montreeal</td>
                                </tr>
                                <tr>
                                    <td class="text-center">61</td>
                                    <td class="text-center">Moncton Hospital</td>
                                    <td class="text-center">Abdelsalam, Mahmoud</td>
                                    <td class="text-center">加拿大</td>
                                    <td class="text-center">NB</td>
                                    <td class="text-center">Moncton</td>
                                </tr>
                                <tr>
                                    <td class="text-center">62</td>
                                    <td class="text-center">Ottawa Hospital Research Institute</td>
                                    <td class="text-center">Bosse, Dominick</td>
                                    <td class="text-center">加拿大</td>
                                    <td class="text-center">ON</td>
                                    <td class="text-center">Ottawa</td>
                                </tr>
                                <tr>
                                    <td class="text-center">63</td>
                                    <td class="text-center">BC Cancer - Vancouver Center</td>
                                    <td class="text-center">Eigl, Bernie</td>
                                    <td class="text-center">加拿大</td>
                                    <td class="text-center">BC</td>
                                    <td class="text-center">Vancouver</td>
                                </tr>
                                <tr>
                                    <td class="text-center">64</td>
                                    <td class="text-center">Rambam Health Care Campus-Oncology</td>
                                    <td class="text-center">Peer, Avivit</td>
                                    <td class="text-center">以色列</td>
                                    <td class="text-center">Haifa</td>
                                    <td class="text-center">Haifa</td>
                                </tr>
                                <tr>
                                    <td class="text-center">65</td>
                                    <td class="text-center">Rabin Medical Center-Oncology</td>
                                    <td class="text-center">Rosenbaum, Eli</td>
                                    <td class="text-center">以色列</td>
                                    <td class="text-center">Petah-Tikva</td>
                                    <td class="text-center">Petah-Tikva</td>
                                </tr>
                                <tr>
                                    <td class="text-center">66</td>
                                    <td class="text-center">Sheba Medical Center-ONCOLOGY</td>
                                    <td class="text-center">Raanan, Berger</td>
                                    <td class="text-center">以色列</td>
                                    <td class="text-center">Ramat Gan</td>
                                    <td class="text-center">Ramat Gan</td>
                                </tr>
                                <tr>
                                    <td class="text-center">67</td>
                                    <td class="text-center">Hirosaki University Hospital</td>
                                    <td class="text-center">Narita, Takuma</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Aomori</td>
                                    <td class="text-center">Hirosaki</td>
                                </tr>
                                <tr>
                                    <td class="text-center">68</td>
                                    <td class="text-center">University of Tsukuba Hospital</td>
                                    <td class="text-center">Kandori, Shuya</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Ibaraki</td>
                                    <td class="text-center">Tsukuba</td>
                                </tr>
                                <tr>
                                    <td class="text-center">69</td>
                                    <td class="text-center">Tohoku University Hospital</td>
                                    <td class="text-center">Kawasaki, Yoshihide</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Miyagi</td>
                                    <td class="text-center">Sendai</td>
                                </tr>
                                <tr>
                                    <td class="text-center">70</td>
                                    <td class="text-center">Keio University Hospital</td>
                                    <td class="text-center">Matsumoto, Kazuhiro</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Tokyo</td>
                                    <td class="text-center">Tokyo</td>
                                </tr>
                                <tr>
                                    <td class="text-center">71</td>
                                    <td class="text-center">Tokyo Medical and Dental University Hospital</td>
                                    <td class="text-center">Fujii, Yasuhisa</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Tokyo</td>
                                    <td class="text-center">Tokyo</td>
                                </tr>
                                <tr>
                                    <td class="text-center">72</td>
                                    <td class="text-center">Kitasato University Hospital</td>
                                    <td class="text-center">Matsumoto, Kazumasa</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Kanagawa</td>
                                    <td class="text-center">Sagamihara</td>
                                </tr>
                                <tr>
                                    <td class="text-center">73</td>
                                    <td class="text-center">Kanagawa Cancer Center</td>
                                    <td class="text-center">Kishida, Takeshi</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Kanagawa</td>
                                    <td class="text-center">Yokohama</td>
                                </tr>
                                <tr>
                                    <td class="text-center">74</td>
                                    <td class="text-center">Yokohama City University Medical Center</td>
                                    <td class="text-center">Uemura, Hiroji</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Kanagawa</td>
                                    <td class="text-center">Yokohama</td>
                                </tr>
                                <tr>
                                    <td class="text-center">75</td>
                                    <td class="text-center">Kanazawa University Hospital</td>
                                    <td class="text-center">Izumi, Kouji</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Ishikawa</td>
                                    <td class="text-center">Kanazawa</td>
                                </tr>
                                <tr>
                                    <td class="text-center">76</td>
                                    <td class="text-center">Toyama University Hospital</td>
                                    <td class="text-center">Kitamura, Hiroshi</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Toyama</td>
                                    <td class="text-center">Toyama</td>
                                </tr>
                                <tr>
                                    <td class="text-center">77</td>
                                    <td class="text-center">Hamamatsu University Hospital</td>
                                    <td class="text-center">Miyake, Hideaki</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Shizuoka</td>
                                    <td class="text-center">Hamamatsu</td>
                                </tr>
                                <tr>
                                    <td class="text-center">78</td>
                                    <td class="text-center">Nagoya University Hospital</td>
                                    <td class="text-center">Sano, Tomoyasu</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Aichi</td>
                                    <td class="text-center">Nagoya</td>
                                </tr>
                                <tr>
                                    <td class="text-center">79</td>
                                    <td class="text-center">Gifu University Hospital</td>
                                    <td class="text-center">Koie, Takuya</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Gifu</td>
                                    <td class="text-center">Gifu</td>
                                </tr>
                                <tr>
                                    <td class="text-center">80</td>
                                    <td class="text-center">Osaka International Cancer Institute</td>
                                    <td class="text-center">Nakayama, Masashi</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Osaka</td>
                                    <td class="text-center">Osaka</td>
                                </tr>
                                <tr>
                                    <td class="text-center">81</td>
                                    <td class="text-center">Osaka City University Hospital</td>
                                    <td class="text-center">Kato, Minoru</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Osaka</td>
                                    <td class="text-center">Osaka</td>
                                </tr>
                                <tr>
                                    <td class="text-center">82</td>
                                    <td class="text-center">Okayama University Hospital</td>
                                    <td class="text-center">Edamura, Kohei</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Okayama</td>
                                    <td class="text-center">Okayama</td>
                                </tr>
                                <tr>
                                    <td class="text-center">83</td>
                                    <td class="text-center">Nagasaki University Hospital</td>
                                    <td class="text-center">Sakai, Hideki</td>
                                    <td class="text-center">日本</td>
                                    <td class="text-center">Nagasaki</td>
                                    <td class="text-center">Nagasaki</td>
                                </tr>
                                <tr>
                                    <td class="text-center">84</td>
                                    <td class="text-center">Seoul National University Hospital</td>
                                    <td class="text-center">Ku, Ja Hyeon</td>
                                    <td class="text-center">韩国</td>
                                    <td class="text-center">Seoul</td>
                                    <td class="text-center">Jongno-gu</td>
                                </tr>
                                <tr>
                                    <td class="text-center">85</td>
                                    <td class="text-center">Asan Medical Center</td>
                                    <td class="text-center">Hong, Bumshik</td>
                                    <td class="text-center">韩国</td>
                                    <td class="text-center">Seoul</td>
                                    <td class="text-center">Seoul</td>
                                </tr>
                                <tr>
                                    <td class="text-center">86</td>
                                    <td class="text-center">Chonnam National University Hwasun Hospital</td>
                                    <td class="text-center">Jung, Seung Il</td>
                                    <td class="text-center">韩国</td>
                                    <td class="text-center">Jeonranamdo</td>
                                    <td class="text-center">Hwasun-Gun</td>
                                </tr>
                                <tr>
                                    <td class="text-center">87</td>
                                    <td class="text-center">Kyungpook National University Chilgok Hospital</td>
                                    <td class="text-center">Kim, Tae Hwan</td>
                                    <td class="text-center">韩国</td>
                                    <td class="text-center">Taegu-Kwangyokshi</td>
                                    <td class="text-center">Daegu</td>
                                </tr>
                                <tr>
                                    <td class="text-center">88</td>
                                    <td class="text-center">Seoul National University Bundang Hospital</td>
                                    <td class="text-center">Oh, Jong Jin</td>
                                    <td class="text-center">韩国</td>
                                    <td class="text-center">Kyonggi-do</td>
                                    <td class="text-center">Seongnam-si</td>
                                </tr>
                                <tr>
                                    <td class="text-center">89</td>
                                    <td class="text-center">Gachon University Gil Medical Center</td>
                                    <td class="text-center">Park, Inkeun</td>
                                    <td class="text-center">韩国</td>
                                    <td class="text-center">Incheon</td>
                                    <td class="text-center">Incheon</td>
                                </tr>
                                <tr>
                                    <td class="text-center">90</td>
                                    <td class="text-center">Sarawak General Hospital</td>
                                    <td class="text-center">Ab Jalil, Hadi</td>
                                    <td class="text-center">马来西亚</td>
                                    <td class="text-center">Sarawak</td>
                                    <td class="text-center">Kuching</td>
                                </tr>
                                <tr>
                                    <td class="text-center">91</td>
                                    <td class="text-center">University Malaya Medical Centre</td>
                                    <td class="text-center">Saad, Marniza</td>
                                    <td class="text-center">马来西亚</td>
                                    <td class="text-center">Kuala Lumpur</td>
                                    <td class="text-center">Lembah Pantai</td>
                                </tr>
                                <tr>
                                    <td class="text-center">92</td>
                                    <td class="text-center">Sunway Medical Centre</td>
                                    <td class="text-center">Abdullah, Nik Muhd Aslan</td>
                                    <td class="text-center">马来西亚</td>
                                    <td class="text-center">Selangor</td>
                                    <td class="text-center">Petaling Jaya</td>
                                </tr>
                                <tr>
                                    <td class="text-center">93</td>
                                    <td class="text-center">Altay Regional Oncology Dispensary</td>
                                    <td class="text-center">Varlamov, Sergey</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Altayskiy kray</td>
                                    <td class="text-center">Barnaul</td>
                                </tr>
                                <tr>
                                    <td class="text-center">94</td>
                                    <td class="text-center">Scientific Research Oncology Institute n.a. N.N.Petrov</td>
                                    <td class="text-center">Nosov, Alexander</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Sankt-Peterburg</td>
                                    <td class="text-center">Saint Petersburg</td>
                                </tr>
                                <tr>
                                    <td class="text-center">95</td>
                                    <td class="text-center">St.Petersburg State Medical Univ. n.a. acad. I.P.Pavlov</td>
                                    <td class="text-center">Petrov, Sergey</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Sankt-Peterburg</td>
                                    <td class="text-center">Saint Petersburg</td>
                                </tr>
                                <tr>
                                    <td class="text-center">96</td>
                                    <td class="text-center">St.Petersburg Clinical Hospital RAS</td>
                                    <td class="text-center">Seyitkuliev, Artur</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Sankt-Peterburg</td>
                                    <td class="text-center">Saint Petersburg</td>
                                </tr>
                                <tr>
                                    <td class="text-center">97</td>
                                    <td class="text-center">National Medical Research Centre of Oncology named after N.N. Blokhin</td>
                                    <td class="text-center">Matveev, Vsevolod</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Moskva</td>
                                    <td class="text-center">Moscow</td>
                                </tr>
                                <tr>
                                    <td class="text-center">98</td>
                                    <td class="text-center">Sverdlovsk Regional Oncology Hospital</td>
                                    <td class="text-center">Shirokova, Oksana</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Sverdlovskaya oblast</td>
                                    <td class="text-center">Ekaterinburg</td>
                                </tr>
                                <tr>
                                    <td class="text-center">99</td>
                                    <td class="text-center">Sverdlovsky Regional Clinical hospital #1</td>
                                    <td class="text-center">Tevs, Dmitry</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Sverdlovskaya oblast</td>
                                    <td class="text-center">Ekaterinburg</td>
                                </tr>
                                <tr>
                                    <td class="text-center">100</td>
                                    <td class="text-center">National Medical Research Radiology Centre</td>
                                    <td class="text-center">Karyakin, Oleg</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Kaluzskaja oblast</td>
                                    <td class="text-center">Obninsk</td>
                                </tr>
                                <tr>
                                    <td class="text-center">101</td>
                                    <td class="text-center">Volgograd Regional Uronephrological Center</td>
                                    <td class="text-center">Perlin, Dmitry</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Volgogradskaya oblast</td>
                                    <td class="text-center">Volgograd</td>
                                </tr>
                                <tr>
                                    <td class="text-center">102</td>
                                    <td class="text-center">First Moscow State Medical University n.a. I.M.Sechenov</td>
                                    <td class="text-center">Enikeev, Dmitry</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Moskva</td>
                                    <td class="text-center">Moscow</td>
                                </tr>
                                <tr>
                                    <td class="text-center">103</td>
                                    <td class="text-center">Volga District Medical Center</td>
                                    <td class="text-center">Atduev, Vagif</td>
                                    <td class="text-center">俄罗斯</td>
                                    <td class="text-center">Nizhegorodskaya oblast</td>
                                    <td class="text-center">Nizhny Novgorod</td>
                                </tr>
                                <tr>
                                    <td class="text-center">104</td>
                                    <td class="text-center">Tan Tock Seng Hospital</td>
                                    <td class="text-center">CHIA, Puey Ling</td>
                                    <td class="text-center">新加坡</td>
                                    <td class="text-center">Central Singapore</td>
                                    <td class="text-center">Singapore</td>
                                </tr>
                                <tr>
                                    <td class="text-center">105</td>
                                    <td class="text-center">Steve Biko Academic Hospital</td>
                                    <td class="text-center">Khanyile, Richard</td>
                                    <td class="text-center">南非</td>
                                    <td class="text-center">Gauteng</td>
                                    <td class="text-center">Pretoria</td>
                                </tr>
                                <tr>
                                    <td class="text-center">106</td>
                                    <td class="text-center">Groote Schuur Hospital</td>
                                    <td class="text-center">Parkes, Jeannette</td>
                                    <td class="text-center">南非</td>
                                    <td class="text-center">Western Cape</td>
                                    <td class="text-center">Cape Town</td>
                                </tr>
                                <tr>
                                    <td class="text-center">107</td>
                                    <td class="text-center">Wits Clinical Research</td>
                                    <td class="text-center">Ruff, Paul</td>
                                    <td class="text-center">南非</td>
                                    <td class="text-center">Gauteng</td>
                                    <td class="text-center">Johannesburg</td>
                                </tr>
                                <tr>
                                    <td class="text-center">108</td>
                                    <td class="text-center">Regional Clinical Center of Urology and Nephrology n.a. V.I. Shapoval</td>
                                    <td class="text-center">Khareba, Gennadii</td>
                                    <td class="text-center">乌克兰</td>
                                    <td class="text-center">Kharkivska oblast</td>
                                    <td class="text-center">Kharkiv</td>
                                </tr>
                                <tr>
                                    <td class="text-center">109</td>
                                    <td class="text-center">MI Clinical oncology dispensary of Dnipropetrovsk regional council</td>
                                    <td class="text-center">Zvonarova, Nataliia</td>
                                    <td class="text-center">乌克兰</td>
                                    <td class="text-center">Dnipropetrovska oblast</td>
                                    <td class="text-center">Dnipro</td>
                                </tr>
                                <tr>
                                    <td class="text-center">110</td>
                                    <td class="text-center">MNPE Regional Center of Oncology</td>
                                    <td class="text-center">Nalbandian, Taron</td>
                                    <td class="text-center">乌克兰</td>
                                    <td class="text-center">Kharkivska oblast</td>
                                    <td class="text-center">Kharkiv</td>
                                </tr>
                                <tr>
                                    <td class="text-center">111</td>
                                    <td class="text-center">I.I. Mechnykov Dnipropetrovsk Regional Clinical Hospital</td>
                                    <td class="text-center">Stus, Viktor</td>
                                    <td class="text-center">乌克兰</td>
                                    <td class="text-center">Dnipropetrovska oblast</td>
                                    <td class="text-center">Dnipro</td>
                                </tr>
                                <tr>
                                    <td class="text-center">112</td>
                                    <td class="text-center">Lviv Oncology Regional Treatment and Diagnostic Center</td>
                                    <td class="text-center">Sabadash, Maksym</td>
                                    <td class="text-center">乌克兰</td>
                                    <td class="text-center">Lvivska oblast</td>
                                    <td class="text-center">Lviv</td>
                                </tr>
                                <tr>
                                    <td class="text-center">113</td>
                                    <td class="text-center">Zhytomyr Regional Oncology Center</td>
                                    <td class="text-center">Lipetska, Oksana</td>
                                    <td class="text-center">乌克兰</td>
                                    <td class="text-center">Zhytomyrska oblast</td>
                                    <td class="text-center">Zhytomyr</td>
                                </tr>
                                <tr>
                                    <td class="text-center">114</td>
                                    <td class="text-center">Municipal Non-profit Enterprise of Kharkiv Regional Council RCSDRPP</td>
                                    <td class="text-center">Neffa, Maryna</td>
                                    <td class="text-center">乌克兰</td>
                                    <td class="text-center">Kharkivska oblast</td>
                                    <td class="text-center">Kharkiv</td>
                                </tr>
                                <tr>
                                    <td class="text-center">115</td>
                                    <td class="text-center">MidLantic Urology</td>
                                    <td class="text-center">Belkoff, Laurence</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">PA</td>
                                    <td class="text-center">Bala Cynwyd</td>
                                </tr>
                                <tr>
                                    <td class="text-center">116</td>
                                    <td class="text-center">UT Southwestern Medical Center</td>
                                    <td class="text-center">Arafat, Waddah</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">TX</td>
                                    <td class="text-center">Dallas</td>
                                </tr>
                                <tr>
                                    <td class="text-center">117</td>
                                    <td class="text-center">UCLA Hematology/Oncology - Westwood (Building 200 Suite 140)-Department of Urology/Institute of Uro</td>
                                    <td class="text-center">Chamie, Karim</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">CA</td>
                                    <td class="text-center">Los Angeles</td>
                                </tr>
                                <tr>
                                    <td class="text-center">118</td>
                                    <td class="text-center">Saint Francis Cancer Center</td>
                                    <td class="text-center">Dyar, Stephen</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">SC</td>
                                    <td class="text-center">Greenville</td>
                                </tr>
                                <tr>
                                    <td class="text-center">119</td>
                                    <td class="text-center">University of Colorado, Anschutz Cancer Pavilion</td>
                                    <td class="text-center">Flaig, Thomas</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">CO</td>
                                    <td class="text-center">Aurora</td>
                                </tr>
                                <tr>
                                    <td class="text-center">120</td>
                                    <td class="text-center">University of California San Francisco</td>
                                    <td class="text-center">Koshkin, Vadim</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">CA</td>
                                    <td class="text-center">San Francisco</td>
                                </tr>
                                <tr>
                                    <td class="text-center">121</td>
                                    <td class="text-center">Icahn School of Medicine at Mount Sinai</td>
                                    <td class="text-center">Galsky, Matthew</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">NY</td>
                                    <td class="text-center">New York</td>
                                </tr>
                                <tr>
                                    <td class="text-center">122</td>
                                    <td class="text-center">Wake Forest Baptist Health</td>
                                    <td class="text-center">McCormack, Michael</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">NC</td>
                                    <td class="text-center">Winston-Salem</td>
                                </tr>
                                <tr>
                                    <td class="text-center">123</td>
                                    <td class="text-center">Duke University Medical Center</td>
                                    <td class="text-center">Hoimes, Christopher</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">NC</td>
                                    <td class="text-center">Durham</td>
                                </tr>
                                <tr>
                                    <td class="text-center">124</td>
                                    <td class="text-center">Urology of San Antonio</td>
                                    <td class="text-center">Zainfeld, Daniel</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">TX</td>
                                    <td class="text-center">San Antonio</td>
                                </tr>
                                <tr>
                                    <td class="text-center">125</td>
                                    <td class="text-center">University of Louisville, James Graham Brown Cancer Center</td>
                                    <td class="text-center">Kumar, Rohit</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">KY</td>
                                    <td class="text-center">Louisville</td>
                                </tr>
                                <tr>
                                    <td class="text-center">126</td>
                                    <td class="text-center">Stanford University</td>
                                    <td class="text-center">Srinivas, Sandy</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">CA</td>
                                    <td class="text-center">Stanford</td>
                                </tr>
                                <tr>
                                    <td class="text-center">127</td>
                                    <td class="text-center">University of California Irvine Medical Center</td>
                                    <td class="text-center">Uchio, Edward</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">CA</td>
                                    <td class="text-center">Orange</td>
                                </tr>
                                <tr>
                                    <td class="text-center">128</td>
                                    <td class="text-center">Oregon Health and Science University</td>
                                    <td class="text-center">Vuky, Jacqueline</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">OR</td>
                                    <td class="text-center">Portland</td>
                                </tr>
                                <tr>
                                    <td class="text-center">129</td>
                                    <td class="text-center">University of Iowa Hospital and Clinics</td>
                                    <td class="text-center">Zakharia, Yousef</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">IA</td>
                                    <td class="text-center">Iowa City</td>
                                </tr>
                                <tr>
                                    <td class="text-center">130</td>
                                    <td class="text-center">UF Health</td>
                                    <td class="text-center">Chatzkel, Jonathan</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">FL</td>
                                    <td class="text-center">Gainesville</td>
                                </tr>
                                <tr>
                                    <td class="text-center">131</td>
                                    <td class="text-center">Houston Methodist Urology Associates</td>
                                    <td class="text-center">Satkunasivam, Raj</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">TX</td>
                                    <td class="text-center">Houston</td>
                                </tr>
                                <tr>
                                    <td class="text-center">132</td>
                                    <td class="text-center">The University of Tennessee Medical Center</td>
                                    <td class="text-center">Mosley, James</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">TN</td>
                                    <td class="text-center">Knoxville</td>
                                </tr>
                                <tr>
                                    <td class="text-center">133</td>
                                    <td class="text-center">St Joseph Heritage Healthcare-Oncology</td>
                                    <td class="text-center">Park, David</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">CA</td>
                                    <td class="text-center">Fullerton</td>
                                </tr>
                                <tr>
                                    <td class="text-center">134</td>
                                    <td class="text-center">University of Wisconsin Hospital and Clinics</td>
                                    <td class="text-center">Emamekhoo, Hamid</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">WI</td>
                                    <td class="text-center">Madison</td>
                                </tr>
                                <tr>
                                    <td class="text-center">135</td>
                                    <td class="text-center">White Plains Hospital</td>
                                    <td class="text-center">Costin, Dan</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">NY</td>
                                    <td class="text-center">White Plains</td>
                                </tr>
                                <tr>
                                    <td class="text-center">136</td>
                                    <td class="text-center">Northwestern Memorial HealthCare</td>
                                    <td class="text-center">George, Christopher</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">IL</td>
                                    <td class="text-center">Geneva</td>
                                </tr>
                                <tr>
                                    <td class="text-center">137</td>
                                    <td class="text-center">Northwestern Medicine Cancer Center - Warrenville</td>
                                    <td class="text-center">George, Christopher</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">IL</td>
                                    <td class="text-center">Warrenville</td>
                                </tr>
                                <tr>
                                    <td class="text-center">138</td>
                                    <td class="text-center">Northwestern Medicine Cancer Center - Kishwaukee</td>
                                    <td class="text-center">George, Christopher</td>
                                    <td class="text-center">美国</td>
                                    <td class="text-center">IL</td>
                                    <td class="text-center">Kishwaukee</td>
                                </tr>
                            </table>
                        
                            <div class="searchDetailPartTit">五、伦理委员会信息</div>
                            <table class="searchDetailTable">
                                <tr>
                                    <th width="15%" style="text-align: center;">序号</th>
                                    <th width="30%" style="text-align: center;">名称</th>
                                    <th width="30%" style="text-align: center;">审查结论</th>
                                    <th width="25%" style="text-align: center;">批准日期/备案日期</th>
                                </tr>
                                <tr>
                                    <td style="text-align: center;">1</td>
                                    <td style="text-align: center;">复旦大学附属肿瘤医院伦理委员会</td>
                                    <td style="text-align: center;">
                                            同意
                                            
                                            
                                    </td>
                                    <td style="text-align: center;">2021-09-08</td>
                                </tr>
                                <tr>
                                    <td style="text-align: center;">2</td>
                                    <td style="text-align: center;">复旦大学附属肿瘤医院伦理委员会</td>
                                    <td style="text-align: center;">
                                            同意
                                            
                                            
                                    </td>
                                    <td style="text-align: center;">2022-07-20</td>
                                </tr>
                            </table>
                            <div class="searchDetailPartTit">六、试验状态信息</div>
                            <div class="sDPTit2">1、试验状态</div>
                            进行中
                            （招募中）
                                                    <div class="sDPTit2">2、试验人数</div>
                            <table class="searchDetailTable">
                                <tr>
                                    <th width="15%">目标入组人数</th>
                                    <td width="85%">
                                            
                                                国内:&nbsp;10&nbsp;；
                                                国际:&nbsp;784&nbsp;；
                                    </td>
                                </tr>
                                <tr>
                                    <th width="15%">已入组人数</th>
                                    <td width="85%">
                                            国内:&nbsp;6&nbsp;；
                                            国际:&nbsp;334&nbsp;；
                                    </td>
                                </tr>
                                <tr>
                                    <th>实际入组总人数</th>
                                    <td>
                                            国内:&nbsp;登记人暂未填写该信息；
                                            国际:&nbsp;登记人暂未填写该信息；
                                    </td>
                                </tr>
                            </table>
                            <div class="sDPTit2">3、受试者招募及试验完成日期</div>
                            <table class="searchDetailTable">
                                <tr>
                                    <th width="15%">第一例受试者签署知情同意书日期</th>
                                    <td width="85%">
                                            国内：2022-03-28；&nbsp;&nbsp;&nbsp;&nbsp;
                                            国际：2021-04-21；
                                    </td>
                                </tr>
                                <tr>
                                    <th>第一例受试者入组日期</th>
                                    <td>
                                            国内：2022-07-15；&nbsp;&nbsp;&nbsp;&nbsp;
                                            国际：2021-05-12；
                                    </td>
                                </tr>
                                <tr>
                                    <th>
                                            试验完成日期
                                    </th>
                                    <td>
                                            国内：登记人暂未填写该信息；&nbsp;&nbsp;&nbsp;&nbsp;
                                            国际：登记人暂未填写该信息；
                                    </td>
                                </tr>
                            </table>
                            <div class="searchDetailPartTit">七、临床试验结果摘要</div>
                            <table class="searchDetailTable">
                            <tr>
                                <th width="15%" class="text-center">序号</th>
                                <th width="45%" class="text-center">版本号</th>
                                <th width="40%" class="text-center">版本日期</th>
                            </tr>
                                <tr><td colspan="3"  style="text-align: center">暂未填写此信息</td></tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <div class="padding15 text-right printHidden">
        <form action="/clinicaltrials.searchlistdetail.dhtml?_export=doc" method="post" style="display: inline;">
            <input type="hidden" name="id" value="3f2a7f7fa9274298bf16dfa180a36c40"/>
            <button type="submit" class="btn btn-sm btn-info download"><span class="fa fa-download"></span> 下载</button>
        </form>
            <button type="button" class="btn btn-sm btn-info" onclick="window.location='/clinicaltrials.searchdetail.rss.dhtml?id=3f2a7f7fa9274298bf16dfa180a36c40'"><span class="fa fa-feed"></span> 订阅RSS</button>
            <button type="button" class="btn btn-sm btn-info" onclick="doPrint()"><span class="fa fa-print"></span> 打印</button>
    </div>

    <div class="goTop printHidden">
        <div class="upIcon"><span class="fa fa-angle-up"></span></div>
        TOP
    </div>
    <div id="toolbar_bottom" class="paddingSide15">

    <style>
    .f00{
        color:#F00
    }
    .radius_100{
        border-radius: 100px;
    }

    </style>
    <div class="row" style="border-top: 1px #dedede solid; text-align: center; padding: 40px 0; line-height: 32px; font-size: 16px;">


                <a href="javascript:void(0)" class="btn btn-default radius_100"  onclick="gotopage(3883);">
                    <span class="fa fa-angle-left"></span>
                    &nbsp;
                    上一个试验
                </a>

            &nbsp;&nbsp;&nbsp;
            目前是第 
            <span class="f00">3884</span> 个试验/共 
            <span class="f00">19402</span> 个试验
            &nbsp;&nbsp;&nbsp;

                <a href="javascript:void(0)" class="btn btn-default radius_100" onclick="gotopage(3885);" >
                    下一个试验
                    &nbsp;
                    <span class="fa fa-angle-right"></span>
                </a>

        

    </div>
    </div>
    </div></div></div>
                </div>
            </div></main>
        <footer class="" style=""> 
        <div class="row " style="margin-top:15px;"> 
            <div class="container" style="box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);"> 
            <div class="column col-md-12" style="">
    <div class="skin_01 eapblock " id="block5" style=""><style>
    /*内容样式片段*/
    .wrap_427 .widget-body{
        
    }
    </style>

    <div class="wrap_427">
        <div  class="widget-wrap">
            <style>
        html,body{height: auto;}
        ._main_content{padding:0!important}
        .copyRight{background-color: #3f69c4; position: relative;
        padding: 20px; line-height: 32px; text-align: center; color: #fff;}  
        .qrCode{
            position: absolute; right: 50px; top: 25px; line-height: 25px;
        }
    </style>
    <div class="copyRight">
    Copyright © 国家药品监督管理局药品审评中心 All Right Reserved.
    <br>
    地址： 中国 北京市朝阳区建国路128号 邮编：100022
    <br>
    总机：8610-68585566 传真：8610-68584189 备案序号：京ICP备09013725号-2
    <div class="qrCode">
        <img src="/website/img/qrCode.jpg" alt="">
        <br>
        手机版
    </div>

    </div>
        </div>
    </div></div>          </div> 
            </div> 
        </div></footer> 
    </body><script type="text/javascript" src="/resource/js/jquery.ui.touch-punch.min.js"></script>
    <script type="text/javascript" src="/resource/js/layer/layer.js"></script>
    <script type="text/javascript" src="/resource/js/layer/extend/layer.ext.js"></script>
    <!--[if lte IE 8]>
    <script type="text/javascript" src="/resource/js/respond.min.js"></script>
    <![endif]--><script type="text/javascript" src="/resource/js/bootstrap.min.js"></script>
    </html>"""
        info = {}

        content = content.replace("<pT2", "&lt;pT2")

        selector_new = etree.HTML(content)

        base_info_section = selector_new.xpath(
            '//div[@class="panel panel-default"]')[0]
        base_info_selector = etree.HTML(
            etree.tostring(base_info_section,
                           encoding='utf-8').decode('utf-8'))

        register_number = ''.join([
            cnt.xpath('string(.)') for cnt in base_info_selector.xpath(
                '//th[contains(string(.), "登记号")]//following-sibling::td[1]')
        ])
        applicant_contact_person = ''.join([
            cnt.xpath('string(.)') for cnt in base_info_selector.xpath(
                '//th[contains(string(.), "申请人联系人")]//following-sibling::td[1]'
            )
        ])
        name_of_applicant = ''.join([
            cnt.xpath('string(.)') for cnt in base_info_selector.xpath(
                '//th[contains(string(.), "申请人名称")]//following-sibling::td[1]')
        ])
        test_condition = ''.join([
            cnt.xpath('string(.)') for cnt in base_info_selector.xpath(
                '//th[contains(string(.), "试验状态")]//following-sibling::td[1]')
        ])
        first_publication = ''.join([
            cnt.xpath('string(.)') for cnt in base_info_selector.xpath(
                '//th[contains(string(.), "首次公示信息日期")]//following-sibling::td[1]'
            )
        ])
        base_info = {
            'register_number': register_number,
            'applicant_contact_person': applicant_contact_person,
            'name_of_applicant': name_of_applicant,
            'test_condition': test_condition,
            'first_publication': first_publication
        }

        title_and_background_section = selector_new.xpath(
            '//div[contains(string(.), "一、题目和背景信息") and @class="searchDetailPartTit"]/following-sibling::table[1]'
        )[0]
        title_and_background_selector = etree.HTML(
            etree.tostring(title_and_background_section,
                           encoding='utf-8').decode('utf-8'))
        register_number = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "登记号")]//following-sibling::td[1]')
        ])
        relevant_registration_number = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "相关登记号")]//following-sibling::td[1]')
        ])
        drug_name = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "药物名称")]//following-sibling::td[1]')
        ])
        drug_type = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "药物类型")]//following-sibling::td[1]')
        ])
        internet_content_provider = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "备案号")]//following-sibling::td[1]')
        ])
        indications = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "适应症")]//following-sibling::td[1]')
        ])
        experimental_subject = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "试验专业题目")]//following-sibling::td[1]'
            )
        ])
        experimental_popular_topic = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "试验通俗题目")]//following-sibling::td[1]'
            )
        ])
        test_scheme_number = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "试验方案编号")]//following-sibling::td[1]'
            )
        ])
        latest_solution_version_number = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "方案最新版本号")]//following-sibling::td[1]'
            )
        ])
        version_date = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "版本日期")]//following-sibling::td[1]')
        ])
        is_combination = ''.join([
            cnt.xpath('string(.)')
            for cnt in title_and_background_selector.xpath(
                '//th[contains(string(.), "方案是否为联合用药")]//following-sibling::td[1]'
            )
        ])
        title_and_background_info = {
            'register_number': register_number,
            'relevant_registration_number': relevant_registration_number,
            'drug_name': drug_name,
            'drug_type': drug_type,
            'internet_content_provider': internet_content_provider,
            'indications': indications,
            'experimental_subject': experimental_subject,
            'experimental_popular_topic': experimental_popular_topic,
            'test_scheme_number': test_scheme_number,
            'latest_solution_version_number': latest_solution_version_number,
            'version_date': version_date,
            'is_combination': is_combination
        }

        applicant_info_section = selector_new.xpath(
            '//div[contains(string(.), "二、申请人信息") and @class="searchDetailPartTit"]/following-sibling::table[1]'
        )[0]
        applicant_info_selector = etree.HTML(
            etree.tostring(applicant_info_section,
                           encoding='utf-8').decode('utf-8'))
        applicant_name = applicant_info_selector.xpath(
            '//th[contains(string(.), "申请人名称")]//following-sibling::td//input[@class="form-control"]/@value'
        )
        contact_person = ''.join([
            cnt.xpath('string(.)') for cnt in applicant_info_selector.xpath(
                '//th[contains(string(.), "联系人姓名")]//following-sibling::td[1]')
        ])
        contact_tel = ''.join([
            cnt.xpath('string(.)') for cnt in applicant_info_selector.xpath(
                '//th[contains(string(.), "联系人座机")]//following-sibling::td[1]')
        ])
        contact_phone = ''.join([
            cnt.xpath('string(.)') for cnt in applicant_info_selector.xpath(
                '//th[contains(string(.), "联系人手机号")]//following-sibling::td[1]'
            )
        ])
        contact_email = ''.join([
            cnt.xpath('string(.)') for cnt in applicant_info_selector.xpath(
                '//th[contains(string(.), "联系人Email")]//following-sibling::td[1]'
            )
        ])
        contact_post = ''.join([
            cnt.xpath('string(.)') for cnt in applicant_info_selector.xpath(
                '//th[contains(string(.), "联系人邮政地址")]//following-sibling::td[1]'
            )
        ])
        contact_post_code = ''.join([
            cnt.xpath('string(.)') for cnt in applicant_info_selector.xpath(
                '//th[contains(string(.), "联系人邮编")]//following-sibling::td[1]')
        ])
        applicant_info = {
            'applicant_name': applicant_name,
            'contact_person': contact_person,
            'contact_tel': contact_tel,
            'contact_phone': contact_phone,
            'contact_email': contact_email,
            'contact_post': contact_post,
            'contact_post_code': contact_post_code
        }

        clinical_trial_info_section = selector_new.xpath(
            '//div[contains(string(.), "三、临床试验信息") and @class="searchDetailPartTit"]/following-sibling::*'
        )

        clinical_trial_info_section_cnt = ''.join([
            etree.tostring(info, encoding='utf-8').decode('utf-8')
            for info in clinical_trial_info_section
        ])
        trial_objective = re.search(r"<div.*1、试验目的</div>(\s*.*\s*.*)",
                                    clinical_trial_info_section_cnt).group(1)

        clinical_trial_info_selector = etree.HTML(''.join([
            etree.tostring(info, encoding='utf-8').decode('utf-8')
            for info in clinical_trial_info_section
        ]))

        trial_design_section = clinical_trial_info_selector.xpath(
            '//div[contains(string(.), "2、试验设计") and @class="sDPTit2"]/following-sibling::table[1]'
        )[0]
        trial_design_selector = etree.HTML(
            etree.tostring(trial_design_section,
                           encoding='utf-8').decode('utf-8'))
        trial_type = ''.join([
            cnt.xpath('string(.)') for cnt in trial_design_selector.xpath(
                '//th[contains(string(.), "试验分类")]//following-sibling::td[1]')
        ])
        trial_stages = ''.join([
            cnt.xpath('string(.)') for cnt in trial_design_selector.xpath(
                '//th[contains(string(.), "试验分期")]//following-sibling::td[1]')
        ])
        design_type = ''.join([
            cnt.xpath('string(.)') for cnt in trial_design_selector.xpath(
                '//th[contains(string(.), "设计类型")]//following-sibling::td[1]')
        ])
        randomization = ''.join([
            cnt.xpath('string(.)') for cnt in trial_design_selector.xpath(
                '//th[contains(string(.), "随机化")]//following-sibling::td[1]')
        ])
        blind_method = ''.join([
            cnt.xpath('string(.)') for cnt in trial_design_selector.xpath(
                '//th[contains(string(.), "盲法")]//following-sibling::td[1]')
        ])
        trial_stretch = ''.join([
            cnt.xpath('string(.)') for cnt in trial_design_selector.xpath(
                '//th[contains(string(.), "试验范围")]//following-sibling::td[1]')
        ])
        trial_design_info = {
            'trial_type': trial_type,
            'trial_stages': trial_stages,
            'design_type': design_type,
            'randomization': randomization,
            'blind_method': blind_method,
            'trial_stretch': trial_stretch
        }

        subject_info_section = clinical_trial_info_selector.xpath(
            '//div[contains(string(.), "3、受试者信息") and @class="sDPTit2"]/following-sibling::table[1]'
        )[0]
        subject_info_selector = etree.HTML(
            etree.tostring(subject_info_section,
                           encoding='utf-8').decode('utf-8'))
        age = ''.join([
            cnt.xpath('string(.)') for cnt in subject_info_selector.xpath(
                '//th[contains(string(.), "年龄")]//following-sibling::td[1]')
        ])
        gender = ''.join([
            cnt.xpath('string(.)') for cnt in subject_info_selector.xpath(
                '//th[contains(string(.), "性别")]//following-sibling::td[1]')
        ])
        health_volunteer = ''.join([
            cnt.xpath('string(.)') for cnt in subject_info_selector.xpath(
                '//th[contains(string(.), "健康受试者")]//following-sibling::td[1]')
        ])
        inclusion_criteria = ''.join([
            cnt.xpath('string(.)') for cnt in subject_info_selector.xpath(
                '//th[contains(string(.), "入选标准")]//following-sibling::td[1]')
        ])
        exclusion_criteria = ''.join([
            cnt.xpath('string(.)') for cnt in subject_info_selector.xpath(
                '//th[contains(string(.), "排除标准")]//following-sibling::td[1]')
        ])
        subject_info = {
            'age': age,
            'gender': gender,
            'health_volunteer': health_volunteer,
            'inclusion_criteria': inclusion_criteria,
            'exclusion_criteria': exclusion_criteria
        }

        trial_group_section = clinical_trial_info_selector.xpath(
            '//div[contains(string(.), "4、试验分组") and @class="sDPTit2"]/following-sibling::table[1]'
        )[0]
        trial_group_selector = etree.HTML(
            etree.tostring(trial_group_section,
                           encoding='utf-8').decode('utf-8'))
        experimental_drug_selector = etree.HTML(
            etree.tostring(trial_group_selector.xpath(
                '//th[contains(string(.), "试验药")]//following-sibling::td[1]')
                           [0],
                           encoding='utf-8').decode('utf-8'))
        control_drug_selector = etree.HTML(
            etree.tostring(trial_group_selector.xpath(
                '//th[contains(string(.), "对照药")]//following-sibling::td[1]')
                           [0],
                           encoding='utf-8').decode('utf-8'))
        trial_group_info = {
            'experimental_drug':
            self.trial_group_info_handler(experimental_drug_selector),
            'control_drug':
            self.trial_group_info_handler(control_drug_selector)
        }

        endpoint_criteria_section = clinical_trial_info_selector.xpath(
            '//div[contains(string(.), "5、终点指标") and @class="sDPTit2"]/following-sibling::table[1]'
        )[0]
        endpoint_criteria_selector = etree.HTML(
            etree.tostring(endpoint_criteria_section,
                           encoding='utf-8').decode('utf-8'))
        primary_end_point_selector = etree.HTML(
            etree.tostring(endpoint_criteria_selector.xpath(
                '//th[contains(string(.), "主要终点指标及评价时间")]//following-sibling::td[1]'
            )[0],
                           encoding='utf-8').decode('utf-8'))
        secondary_end_point_selector = etree.HTML(
            etree.tostring(endpoint_criteria_selector.xpath(
                '//th[contains(string(.), "次要终点指标及评价时间")]//following-sibling::td[1]'
            )[0],
                           encoding='utf-8',
                           method='html').decode('utf-8'))
        endpoint_criteria_info = {
            'primary_end_point':
            self.endpoint_criteria_info_handler(primary_end_point_selector),
            'secondary_end_point':
            self.endpoint_criteria_info_handler(secondary_end_point_selector)
        }

        DMC = re.search(r"6、数据安全监查委员会（DMC）[\s.\S]*?</div>([.\s\S]*?)<div",
                        clinical_trial_info_section_cnt).group(1)
        insurance = re.search(r"7、为受试者购买试验伤害保险[.\s\S]*?</div>([.\s\S]*?)<div",
                              clinical_trial_info_section_cnt).group(1)

        clinical_trial_info = {
            'trial_objective': trial_objective,
            'trial_design_info': trial_design_info,
            'subject_info': subject_info,
            'trial_group_info': trial_group_info,
            'endpoint_criteria_info': endpoint_criteria_info,
            'DMC': DMC,
            'insurance': insurance
        }

        primary_researcher_section = clinical_trial_info_selector.xpath(
            '//div[contains(string(.), "1、主要研究者信息") and @class="sDPTit2"]/following-sibling::table[@class="searchDetailTable marginBtm10"]'
        )
        primary_researcher_selectors = [
            etree.HTML(etree.tostring(info, encoding='utf-8').decode('utf-8'))
            for info in primary_researcher_section
        ]
        primary_researcher_info = [
            self.primary_researcher_info_handler(selector)
            for selector in primary_researcher_selectors
        ]
        organization_info_section = clinical_trial_info_selector.xpath(
            '//div[contains(string(.), "2、各参加机构信息") and @class="sDPTit2"]/following-sibling::table[1]'
        )[0]
        organization_info_selector = etree.HTML(
            etree.tostring(organization_info_section,
                           encoding='utf-8').decode('utf-8'))
        organization_info = self.organization_info_handler(
            organization_info_selector)
        researcher_info = {
            'primary_researcher_info': primary_researcher_info,
            'organization_info': organization_info
        }

        ethics_committee_section = selector_new.xpath(
            '//div[contains(string(.), "五、伦理委员会信息") and @class="searchDetailPartTit"]/following-sibling::table[1]'
        )[0]
        ethics_committee_selector = etree.HTML(
            etree.tostring(ethics_committee_section,
                           encoding='utf-8').decode('utf-8'))
        ethics_committee_info = self.ethics_committee_info_handler(
            ethics_committee_selector)

        trial_population_section = clinical_trial_info_selector.xpath(
            '//div[contains(string(.), "2、试验人数") and @class="sDPTit2"]/following-sibling::table[1]'
        )[0]

        trial_population_selector = etree.HTML(
            etree.tostring(trial_population_section,
                           encoding='utf-8').decode('utf-8'))
        trial_population = {
            'target_group_people_nums':
            ''.join([
                cnt.xpath('string(.)')
                for cnt in trial_population_selector.xpath(
                    '//th[contains(string(.), "目标入组人数")]//following-sibling::td[1]'
                )
            ]),
            'already_group_people_nums':
            ''.join([
                cnt.xpath('string(.)')
                for cnt in trial_population_selector.xpath(
                    '//th[contains(string(.), "已入组人数")]//following-sibling::td[1]'
                )
            ]),
            'in_fact_group_people_nums':
            ''.join([
                cnt.xpath('string(.)')
                for cnt in trial_population_selector.xpath(
                    '//th[contains(string(.), "实际入组总人数")]//following-sibling::td[1]'
                )
            ]),
        }
        trial_status_info = {
            'trial_status':
            re.search(r"1、试验状态\s*.*</div>(\s*.*\s*.*\s*)?<div",
                      clinical_trial_info_section_cnt).group(1),
            'trial_population':
            trial_population
        }

        trial_end_date_section = clinical_trial_info_selector.xpath(
            '//div[contains(string(.), "受试者招募及试验完成日期") and @class="sDPTit2"]/following-sibling::table[1]'
        )[0]
        trial_end_date_selector = etree.HTML(
            etree.tostring(trial_end_date_section,
                           encoding='utf-8').decode('utf-8'))
        trial_end_date_info = {
            'approval_date':
            ''.join([
                cnt.xpath('string(.)')
                for cnt in trial_end_date_selector.xpath(
                    '//th[contains(string(.), "第一例受试者签署知情同意书日期")]//following-sibling::td[1]'
                )
            ]),
            'in_group_date':
            ''.join([
                cnt.xpath('string(.)')
                for cnt in trial_end_date_selector.xpath(
                    '//th[contains(string(.), "第一例受试者入组日期")]//following-sibling::td[1]'
                )
            ]),
            'end_date':
            ''.join([
                cnt.xpath('string(.)')
                for cnt in trial_end_date_selector.xpath(
                    '//th[contains(string(.), "试验完成日期")]//following-sibling::td[1]'
                )
            ])
        }

        trial_results_summary_section = clinical_trial_info_selector.xpath(
            '//div[contains(string(.), "七、临床试验结果摘要") and @class="searchDetailPartTit"]/following-sibling::table[1]'
        )[0]
        trial_results_summary_selector = etree.HTML(
            etree.tostring(trial_results_summary_section,
                           encoding='utf-8').decode('utf-8'))
        trial_results_summary_info = self.trial_results_summary_handler(
            trial_results_summary_selector)

        published_experimental_info = {
            'title_and_background_info': title_and_background_info,
            'applicant_info': applicant_info,
            'clinical_trial_info': clinical_trial_info,
            'researcher_info': researcher_info,
            'ethics_committee_info': ethics_committee_info,
            'trial_status_info': trial_status_info,
            'trial_end_date_info': trial_end_date_info,
            'trial_results_summary_info': trial_results_summary_info
        }

        content_section = selector_new.xpath('//div[@class="panel-group"]')[0]
        content = etree.tostring(content_section,
                                 encoding='utf-8').decode('utf-8')
        detail = {
            'base_info': base_info,
            'published_experimental_info': published_experimental_info,
            'content': content
        }

        info['detail'] = detail
        info['detail_url'] = 'url'

        data = format_data(info, replace_str=['\n', '  ', '\xa0', '\t', '\r'])

        return data

    def trial_group_info_handler(self, selector):
        colunms_map = {0: 'seq', 1: 'name', 2: 'usage'}
        result = self.parse_table_colums(selector=selector,
                                         colunms_map=colunms_map)
        return result

    def endpoint_criteria_info_handler(self, selector):
        colunms_map = {0: 'seq', 1: 'index', 2: 'comment_time', 3: 'end_point'}
        result = self.parse_table_colums(selector=selector,
                                         colunms_map=colunms_map)
        return result

    def parse_table_colums(self, selector, colunms_map):
        result = []

        all_trs = selector.xpath('//tr')
        for tr in all_trs[1:]:
            all_tds = tr.xpath('td')
            if len(all_tds) == 1:
                continue
            row = {}
            for col_index in range(0, len(all_tds)):
                key = colunms_map.get(col_index)
                row[key] = all_tds[col_index].xpath("string(.)")

            result.append(row)
        return result

    def primary_researcher_info_handler(self, selector):

        result = {
            'name':
            selector.xpath(
                'string(//th[contains(text(), "姓名")]/following-sibling::td[1])'
            ),
            'school':
            selector.xpath(
                'string(//th[contains(text(), "学位")]/following-sibling::td[1])'
            ),
            'title':
            selector.xpath(
                'string(//th[contains(text(), "职称")]/following-sibling::td[1])'
            ),
            'tel':
            selector.xpath(
                'string(//th[contains(text(), "电话")]/following-sibling::td[1])'
            ),
            'email':
            selector.xpath(
                'string(//th[contains(text(), "Email")]/following-sibling::td[1])'
            ),
            'post_address':
            selector.xpath(
                'string(//th[contains(text(), "邮政地址")]/following-sibling::td[1])'
            ),
            'postcode':
            selector.xpath(
                'string(//th[contains(text(), "邮编")]/following-sibling::td[1])'
            ),
            'organization':
            selector.xpath(
                'string(//th[contains(text(), "单位名称")]/following-sibling::td[1])'
            ),
        }

        return result

    def organization_info_handler(self, selector):
        colunms_map = {
            0: 'seq',
            1: 'organization_name',
            2: 'primary_researcher',
            3: 'country',
            4: 'province',
            5: 'city'
        }
        result = self.parse_table_colums(selector=selector,
                                         colunms_map=colunms_map)
        return result

    def trial_results_summary_handler(self, selector):
        colunms_map = {0: 'seq', 1: 'version', 2: 'version_date'}
        result = self.parse_table_colums(selector=selector,
                                         colunms_map=colunms_map)
        return result

    def ethics_committee_info_handler(self, selector):
        colunms_map = {
            0: 'seq',
            1: 'name',
            2: 'review_conclusion',
            3: 'approval_date'
        }
        result = self.parse_table_colums(selector=selector,
                                         colunms_map=colunms_map)
        return result


if __name__ == "__main__":

    # asyncio.run(downlaod())

    test_parse = TestParse()
    info = test_parse.parse_content()
