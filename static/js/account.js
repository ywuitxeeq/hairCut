window.onload = function () {
    var baseURL = "http://192.168.32.1/"
    let hairCutAppAxios = newAxios({
        timeout: 10000,
        baseURL: baseURL,
        withCredentials: true,
        headers: {
            common: {Authorization: ""},
            post: {'Content-Type': 'application/x-www-form-urlencoded'}
        }
    })

    if (localStorageUtils.getParam("Authorization")) {
        var infoArr = localStorageUtils.getParam("Authorization").split("@")

        hairCutAppAxios.instance.defaults.headers.common['Authorization'] = infoArr[0]
    }

    let app = new Vue(
        {
            el: "#app",
            data: {
                login: false,
                modify: false,
                retrieve: false,
                register: false,
                interval: null,
                is_login: null,
                username: ''
            },

            methods: {

                submit(data) {
                    let success = data.success
                    let error = data.error
                    delete data.success
                    delete data.error
                    switch (data.method) {
                        case "post":
                            hairCutAppAxios.post(
                                data.uri, data, {
                                    transformRequest: hairCutAppAxios.transformRequest
                                }, success, error
                            )
                            break
                    }
                },
                checkTokenExpire() {
                    // clearInterval
                    var intervalTime = 60000 * 2;

                    if (!this.interval) {
                        var This = this
                        var flagAlter = true;
                        let interval = setInterval(function () {
                            var authorization = localStorageUtils.getParam("Authorization");
                            if (!authorization) {

                                clearInterval(interval);
                                This.interval = null;
                                localStorageUtils.removeParam('log')
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
                                        localStorageUtils.removeParam('log')
                                    }

                                }

                            }

                        }, intervalTime)

                        this.interval = interval;

                    }
                },
                activeToken() {
                    var authorization = hairCutAppAxios.instance.defaults.headers.common.Authorization;
                    var This = this
                    hairCutAppAxios.get(
                        "account/active_token",
                        {
                            params: {token: authorization}
                        }, res => {
                            console.log(res.data.status == 1000)
                            if (res.data.status == 1000) {
                                hairCutAppAxios.instance.defaults.headers.common.Authorization = res.data.token;
                                This.localValue(res.data.token, res.data['expire'])
                                setCookie("authorization", res.data.token, res.data['expire'] * 60)
                            }
                        }
                    )

                },
                localValue(token, expire) {

                    var value = token + "@" + dateHelp(expire) + "@" + dateHelp(expire - 5);
                    localStorageUtils.setParam("Authorization", value)

                    this.checkTokenExpire()
                },

                web_change(event) {
                    var old_tex = document.getElementById("baseTitle").text
                    var new_text
                    if (typeof event != 'string') {
                        new_text = event.target.text
                    } else {
                        new_text = event
                    }
                    document.getElementById("baseTitle").text = new_text;
                    this.register = false;
                    this.login = false;
                    this.retrieve = false;
                    this.modify = false;

                    switch (new_text) {
                        case "登陆":
                            if (!localStorageUtils.getParam('log')) {
                                this.changeAddr('/account/login')
                                this.login = true;
                            } else {
                                document.getElementById("baseTitle").text = "修改密码"
                                this.modify = true;
                            }

                            break
                        case "注册":
                            // let foot = document.getElementById('foot');
                            // foot.style.cssText = "top:686px";
                            if (!localStorageUtils.getParam('log')) {
                                this.changeAddr('/account/register');
                                this.register = true;
                            } else {
                                document.getElementById("baseTitle").text = "修改密码"
                                this.modify = true;
                            }
                            break
                        case "找回密码":
                            if (!localStorageUtils.getParam('log')) {
                                this.changeAddr('/account/retrieve')
                                this.retrieve = true;
                            } else {
                                document.getElementById("baseTitle").text = "修改密码"
                                this.modify = true;
                            }
                            break
                        case "修改密码":
                            if (localStorageUtils.getParam('log')) {
                                this.changeAddr('/account/modify')
                                this.modify = true;
                            } else {
                                if (old_tex == "修改密码") {
                                    return
                                }
                                this.web_change(old_tex)
                            }

                            break
                    }
                },

                changeAddr(str) {
                    let paramsArr = window.location.href.split("?")
                    let new_atr = ''

                    if (paramsArr.length == 2) {
                        new_atr = "?" + paramsArr[1]

                    }
                    let state = {title: '', url: paramsArr[0]}
                    history.pushState(state, '', str + new_atr);
                }

            },

            components: {

                login: {
                    template: "#login",
                    // props: ["checkTokenExpire"],  // 父传子
                    data: function () {
                        return {
                            username: '',
                            password: '',
                            nameError: '',
                            pwdError: '',
                        }
                    },
                    methods: {
                        submit(event) {
                            this.nameError = ''
                            this.pwdError = ''
                            let flag = this.checkUsername(this.username);
                            if (!flag['ret']) {
                                this.nameError = flag['msg']
                                return
                            }
                            flag = this.checkPassword(this.password)
                            if (!flag['ret']) {
                                this.pwdError = flag['msg']
                                return null
                            }
                            this.$emit("submit", {
                                username: this.username,
                                password: this.password,
                                uri: "account/login",
                                method: "post",
                                success: this.success,
                            }) // 向父主组发送信息
                        },
                        checkUsername(name) {
                            if (name.length < 6) {
                                return {
                                    ret: false,
                                    msg: "用户名太短"
                                }
                            } else if (!isNaN(Number(name))) {
                                return {
                                    ret: false,
                                    msg: "账号不能全是数字"
                                }
                            }
                            return {
                                ret: true,
                            }
                        },
                        checkPassword(pwd) {
                            if (pwd.length < 6) {
                                return {
                                    ret: false,
                                    msg: "密码太短"
                                }
                            } else if (!isNaN(Number(pwd))) {
                                return {
                                    ret: false,
                                    msg: "密码不能全是数字"
                                }
                            }
                            return {
                                ret: true,
                            }
                        },
                        success(data) {
                            if (data.data.status == 1000) {
                                hairCutAppAxios.instance.defaults.headers.common['Authorization'] = data.data.token;
                                app.localValue(data.data.token, data.data['expire'])
                                localStorageUtils.setParam("log", true)
                                setCookie("authorization", data.data.token, data.data['expire'] * 60)
                                app.username = data.data.username
                                setTimeout(function () {
                                    window.location = baseURL + 'haircut/index'
                                }, 500)
                            } else if (data.data.status == 1006) {
                                setTimeout(function () {
                                    window.location = baseURL + 'haircut/index'
                                }, 500)
                            } else {
                                this.nameError = data.data['errorMsg']
                                this.pwdError = this.nameError
                            }
                        },
                    }
                },

                register: {
                    template: "#register",
                    data: function () {
                        return {
                            username: '',
                            password: '',
                            re_password: "",
                            phone: '',
                            email: '',
                            question: "",
                            answer: "",
                            nameError: '',
                            pwdError: "",
                            emailError: "",
                            placeholder: "是否要输入密保答案",
                        }
                    },
                    methods: {
                        submit(event) {
                            let result;

                            result = this.checkUsername(this.username)
                            if (!result.ret) {
                                this.nameError = result.msg;
                                return
                            }

                            if (this.password != this.re_password) {
                                this.pwdError = "两次密码不一致"
                                return
                            }

                            result = this.checkPassword(this.password)
                            if (!result.ret) {
                                this.pwdError = result.msg
                                return
                            }

                            result = this.checkPassword(this.re_password)
                            if (!result.ret) {
                                this.pwdError = result.msg
                                return
                            }

                            result = this.checkEmail(this.email);
                            if (!result.ret) {
                                this.emailError = result.msg;
                                return
                            }

                            result = this.checkPhone(this.phone);
                            if (!result.ret) {
                                this.phone = ''
                                return null
                            }
                            var data = {
                                username: this.username,
                                password: this.password,
                                re_password: this.re_password,
                                email: this.email,
                                phone: this.phone,
                                success: this.success,
                                uri: "account/register",
                                method: "post",
                            }
                            if (this.question) {
                                if (this.answer) {
                                    data.question = this.question
                                    data.answer = this.answer
                                } else {
                                    this.placeholder = "请填写答案"
                                    return
                                }
                            } else {
                                this.answer = ''
                                this.placeholder = "是否要输入密保答案"
                            }
                            this.$emit("submit", data)
                        },

                        checkPhone(phone) {
                            if (!(/^1(3|4|5|6|7|8|9)\d{9}$/.test(phone))) {
                                return {
                                    ret: false,
                                    msg: "手机号有错"
                                }
                            }
                            return {
                                ret: true
                            }
                        },

                        checkEmail(email) {

                            this.emailError = ''
                            let em = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/
                            if (!em.test(email)) {
                                return {
                                    ret: false,
                                    msg: "邮箱错误"
                                }
                            }
                            return {
                                ret: true
                            }
                        },

                        checkPassword(pwd) {
                            this.pwdError = ''
                            if (pwd.length < 6) {
                                return {
                                    ret: false,
                                    msg: "密码太短"
                                }
                            } else if (!isNaN(Number(pwd))) {
                                return {
                                    ret: false,
                                    msg: "密码不能全是数字"
                                }
                            }
                            return {
                                ret: true,
                            }
                        },

                        checkUsername(name) {
                            this.nameError = '';
                            if (name.length < 6) {
                                return {
                                    ret: false,
                                    msg: "用户名太短"
                                }
                            } else if (!isNaN(Number(name))) {
                                return {
                                    ret: false,
                                    msg: "账号不能全是数字"
                                }
                            }
                            return {
                                ret: true,
                            }
                        },

                        success(data) {
                            if (data.data.status === 1000) {
                                app.changeAddr(data.data.href);
                                app.register = false;
                                app.login = true;
                            } else {
                                alert(data.data['errorMsg'])
                            }
                        }
                    }

                },

                modify: {
                    template: "#modify",
                    data: function () {
                        return {
                            password: '',
                            new_password: '',
                            re_password: '',
                            email: '',
                            phone: '',
                            oldPwdError: "",
                            pwdError: '',
                            emailError: '',
                            phoneError: '',

                        }
                    },

                    methods: {
                        submit(event) {
                            let result;
                            result = this.checkPassword(this.password)
                            if (!result.ret) {
                                this.oldPwdError = result['msg']
                                return null
                            }
                            result = this.checkPassword(this.re_password)
                            if (!result.ret) {
                                this.pwdError = result['msg']
                                return null
                            }
                            result = this.checkPassword(this.new_password)
                            if (!result.ret) {
                                this.pwdError = result['msg']
                                return null
                            }

                            var data = {
                                password: this.password,
                                re_password: this.re_password,
                                new_password: this.new_password,
                                success: this.success,
                                uri: "account/modify",
                                method: "post",

                            }
                            if (this.email) {
                                result = this.checkEmail(this.email)
                                if (!result.ret) {
                                    this.emailError = result['msg']
                                    return null
                                }
                                data['email'] = this.email
                            }

                            if (this.phone) {
                                result = this.checkPhone(this.phone)
                                if (!result.ret) {
                                    this.phoneError = result['msg']
                                    return null
                                }
                                data['phone'] = this.phone
                            }

                            this.$emit('submit', data);
                        },

                        checkPhone(phone) {
                            if (!(/^1(3|4|5|6|7|8|9)\d{9}$/.test(phone))) {
                                return {
                                    ret: false,
                                    msg: "手机号有错"
                                }
                            }
                            return {
                                ret: true
                            }
                        },

                        checkEmail(email) {

                            this.emailError = ''
                            let em = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/
                            if (!em.test(email)) {
                                return {
                                    ret: false,
                                    msg: "邮箱错误"
                                }
                            }
                            return {
                                ret: true
                            }
                        },

                        checkPassword(pwd) {
                            this.pwdError = ''
                            if (pwd.length < 6) {
                                return {
                                    ret: false,
                                    msg: "密码太短"
                                }
                            } else if (!isNaN(Number(pwd))) {
                                return {
                                    ret: false,
                                    msg: "密码不能全是数字"
                                }
                            }
                            return {
                                ret: true,
                            }
                        },

                        success(data) {

                            this.emailError = '';
                            this.oldPwdError = '';
                            this.pwdError = '';
                            this.phoneError = '';

                            if (data.data.status == 1000) {
                                localStorageUtils.removeParam('log')
                                localStorageUtils.removeParam('Authorization')
                                setCookie("authorization", '', -1)
                                hairCutAppAxios.instance.defaults.headers.common['Authorization'] = ''
                                app.changeAddr(data.data.href)
                                app.modify = false
                                app.login = true

                            } else if (data.data.status == 1005) {
                                this.emailError = data.data['errorMsg']
                            } else if (data.data.status == 1006) {
                                this.phoneError = data.data['errorMsg']
                            } else if (data.data.status == 1004) {
                                this.oldPwdError = data.data['errorMsg']
                            } else {
                                this.pwdError = data.data['errorMsg']
                            }
                        },
                    }
                },

                retrieve: {
                    template: "#retrieve",
                    data: function () {
                        return {
                            username: '',
                            email: '',
                            phone: '',
                            question: '',
                            answer: '',
                            phoneError: '',
                            emailError: '',
                            nameError: '',
                            pwdError: '',
                            new_password: '',
                            re_password: '',

                        }
                    },
                    methods: {
                        submit(event) {
                            let result;
                            result = this.checkUsername(this.username)
                            if (!result.ret) {
                                this.nameError = result['msg']
                                return null
                            }

                            result = this.checkPhone(this.phone)
                            if (!result.ret) {
                                this.phoneError = result['msg']
                                return null
                            }

                            if (this.email) {
                                result = this.checkEmail(this.email)
                                if (!result.ret) {
                                    this.emailError = result['msg']
                                    return null
                                }
                            }


                            var data = {
                                username: this.username,
                                email: this.email,
                                phone: this.phone,
                                question: this.question,
                                answer: this.answer,
                                success: this.success,
                                new_password: this.new_password,
                                re_password: this.re_password,
                                uri: "account/retrieve",
                                method: "post",
                            }

                            this.$emit('submit', data)
                        },

                        checkPhone(phone) {
                            this.phoneError = ''
                            if (!(/^1(3|4|5|6|7|8|9)\d{9}$/.test(phone))) {
                                return {
                                    ret: false,
                                    msg: "手机号有错"
                                }
                            }
                            return {
                                ret: true
                            }
                        },

                        checkEmail(email) {

                            this.emailError = ''
                            let em = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/
                            if (!em.test(email)) {
                                return {
                                    ret: false,
                                    msg: "邮箱错误"
                                }
                            }
                            return {
                                ret: true
                            }
                        },

                        checkUsername(name) {
                            this.nameError = '';
                            if (name.length < 6) {
                                return {
                                    ret: false,
                                    msg: "用户名太短"
                                }
                            } else if (!isNaN(Number(name))) {
                                return {
                                    ret: false,
                                    msg: "账号不能全是数字"
                                }
                            }
                            return {
                                ret: true,
                            }
                        },

                        success(data){
                            if (data.data.status == 1000){
                                alert(data.data.msg)
                            }
                        }
                    }
                },

            },


        }
    )
    app.checkTokenExpire();

    app.is_login = localStorageUtils.getParam("log")
    app.username = document.getElementById("username").name;
    function checkBaseTitle() {
        let title = document.getElementById("baseTitle").text;
        switch (title) {
            case "登陆":
                app.login = true;
                break
            case "注册":
                //  let foot = document.getElementById('foot');
                // foot.style.cssText = "top:686px";
                app.register = true;
                break
            case "找回密码":
                app.retrieve = true;
                break
            case "修改密码":
                if (!localStorageUtils.getParam('log')) {
                    localStorageUtils.setParam('log', true)
                }

                app.modify = true;
                break
        }
    }

    checkBaseTitle()

}