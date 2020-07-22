const tokenCheck = {

    init(hairCutAppAxios) {
        this.interval = null
        if (hairCutAppAxios){
            this.hairCutAppAxios = hairCutAppAxios
        }else {
            this.hairCutAppAxios = this.instanceAxios()
        }
        this.initAuthorization();
        this.run()
    },
    run() {
        this.checkTokenExpire()
    },
    initAuthorization(){
        if (localStorageUtils.getParam("Authorization")) {
        var infoArr = localStorageUtils.getParam("Authorization").split("@")

        this.hairCutAppAxios.instance.defaults.headers.common['Authorization'] = infoArr[0]
    }
    },
    instanceAxios(){

        return  newAxios({
            timeout: 10000,
            baseURL: baseUrl,
            withCredentials: true,
            headers : {
                common: {Authorization: "Authorization"},
                post: {'Content-Type': 'application/x-www-form-urlencoded'}
            }
        })
    },
    checkTokenExpire() {
        // clearInterval
        var intervalTime = 1000 * 15;

        if (!this.interval) {
            var This = this

            var flagAlter = true;
            let interval = setInterval(function () {
                var authorization = localStorageUtils.getParam("Authorization");
                if (!authorization) {
                    clearInterval(interval);
                    This.interval = null;
                    return
                }
                var tokeArr = authorization.split("@")
                var T = parseInt(tokeArr[1])
                var T2 = parseInt(tokeArr[2])
                var notTime = (new Date()).getTime();

                if (T < notTime) {
                    localStorageUtils.removeParam("Authorization")
                    clearInterval(interval);
                    This.interval = null
                } else if ((T - notTime) < (T - T2)) {
                    if (flagAlter) {
                        var t = (T - notTime) / 60000
                        var yes = confirm("token 还有" + parseInt(t) + "分钟过期是否激活");
                        flagAlter = false;
                        if (yes) {
                            This.activeToken()
                            clearInterval(interval);
                            This.interval = null
                        } else {
                            clearInterval(interval);
                            This.interval = null
                        }

                    }

                }

            }, intervalTime)

            this.interval = interval;

        }
    },
    activeToken() {
        var authorization = this.hairCutAppAxios.instance.defaults.headers.common.Authorization;
        var This = this
        this.hairCutAppAxios.get(
            "account/active_token",
            {
                params: {token: authorization}
            }, res => {
                if (res.data.status == 1000) {
                    this.hairCutAppAxios.instance.defaults.headers.common.Authorization = res.data.token;
                    This.localValue(res.data.token, res.data['expire'])
                    setCookie("authorization", res.data.token, res.data['expire'] * 60)
                } else {
                    window.location = hairCutAppAxios.baseURL + "/haircut/admin/login.html"
                }
            }
        )

    },
    localValue(token, expire) {

        var value = token + "@" + dateHelp(expire) + "@" + dateHelp(expire - 5);

        localStorageUtils.setParam("Authorization", value)

        this.checkTokenExpire()

    },
}



