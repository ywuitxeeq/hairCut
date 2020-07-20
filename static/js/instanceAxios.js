const newAxios = (baseConfig) => {
    /**
     * baseConfig = {
            timeout: 10000,
            baseURL: "http://192.168.32.1/",
            withCredentials: true,
            headers : {
                common: {Authorization: "Authorization"},
                post: {'Content-Type': 'application/x-www-form-urlencoded'}
            }
        }
     * /**   支持多种请求方式
     axios(config)
     axios.request(config)
     axios.get(url,[config])
     axios.delete(url,[config])
     axios.head(url,[config])
     axios.post(url,data,[config])
     axios.put(url,data,[config])
     axios.patch(url,data,[config])
     多个请求
     axios.all()

     example:
        obj.get("xxx/login", {
            params: {"abc":"123"},

        }, successCallback, errorCallback)

         obj.post("xxx/login", data, {
            transformRequest: obj.transformRequest,
            headers: {
                'Content-Type': 'application/json'
            }
         },successCallback(res){
            obj.defaults.headers.common['Authorization'] = res['AUTH_TOKEN'];
         }, errorCallback)

        obj.all([obj.instance.get(url, config), obj.instance.post(url, config)], successCallback, errorCallback)
        // form data文件
            const data = new FormData();
            data.append('file', file);
            obj.post('/xxx/file', data, {

                // 改变请求头
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            }, successCallback, errorCallback)
     * **/


    baseConfig = baseConfig || {}
    let ins = axios.create(baseConfig)

    let obj = {
        get: (url, config, successCallback, errorCallback) => {

           if (typeof config === "function"){
                successCallback = config
                config = {}
            }else {
                config = config ? obj.checkContentType(config) :{}
            }
            successCallback = successCallback || function (res) {}
            errorCallback = errorCallback || function (res) {}
            ins.get(url, config).then(successCallback).catch(errorCallback)
        },
        request: (config, successCallback, errorCallback) => {
            successCallback = successCallback || function (res) {
            }
            errorCallback = errorCallback || function (res) {
            }
            config = config ? obj.checkContentType(config) :{}
            ins.request(config).then(successCallback).catch(errorCallback)
        },
        delete: (url, config, successCallback, errorCallback) => {

           if (typeof config == "function"){
                successCallback = config
                config = {}
            }else {
               config = config ? obj.checkContentType(config) :{}
            }
            successCallback = successCallback || function (res) {}
            errorCallback = errorCallback || function (res) {}
            ins.delete(url, config).then(successCallback).catch(errorCallback)
        },
        head: (url, config, successCallback, errorCallback) => {
            if (typeof config == "function"){
                successCallback = config
                config = {}
            }else {
                config = config? obj.checkContentType(config):{}
            }
            successCallback = successCallback || function (res) {}
            errorCallback = errorCallback || function (res) {}

            ins.head(url, config).then(successCallback).catch(errorCallback)
        },
        post: (url, data, config, successCallback, errorCallback) => {
            if (typeof config == "function"){
                successCallback = config
                config = {}
            }else {
                config = config? obj.checkContentType(config):{}
            }
            successCallback = successCallback || function(res){}
            errorCallback = errorCallback || function (res){}
            ins.post(url, data, config).then(successCallback).catch(errorCallback)
        },
        put: (url, data, config, successCallback, errorCallback) => {
            if (typeof config == "function"){
                successCallback = config
                config = {}
            }else {
                config = config? obj.checkContentType(config):{}
            }
            successCallback = successCallback || function(res){}
            errorCallback = errorCallback || function (res){}
            ins.put(url, data, config).then(successCallback).catch(errorCallback)
        },
        patch: (url, data, config, successCallback, errorCallback) => {
             if (typeof config === "function"){
                successCallback = config
                config = {}
            }else {
                config = config? obj.checkContentType(config):{}
            }
            successCallback = successCallback || function(res){}
            errorCallback = errorCallback || function (res){}
            ins.patch(url, data, config).then(successCallback).catch(errorCallback)
        },
        all: (reqArr,successCallback, errorCallback) => {
            /**
             * @params:reqArr = [obj.instance.get(url, config), obj.instance.post(url, config)]
             *
             * */
             successCallback = successCallback || function (res) {
            }
            errorCallback = errorCallback || function (res) {
            }
            ins.all(reqArr).then(successCallback).catch(errorCallback)
        },
        transformRequest: [function (data, headers) {
            // 对 data url编码 发送 改变默认的 json
            var post = headers.post['Content-Type']
            var patch = headers.patch['Content-Type']
            var put = headers.put['Content-Type']
            if (post.toLowerCase().indexOf("application/x-www-form-urlencoded") !== -1) {
                return obj.uriComponent(data)
            } else if (post.toLowerCase().indexOf("application/json") !== -1) {
                return obj.uriComponentJson(data)
            }

            if (put.toLowerCase().indexOf("application/x-www-form-urlencoded") !== -1) {
                return obj.uriComponent(data)
            } else if (post.toLowerCase().indexOf("application/json") !== -1) {
                return obj.uriComponentJson(data)
            }

            if (patch.toLowerCase().indexOf("application/x-www-form-urlencoded") !== -1) {
                return obj.uriComponent(data)
            } else if (post.toLowerCase().indexOf("application/json") !== -1) {
                return obj.uriComponentJson(data)
            }

            return data

        }],
        "instance": ins,
        uriComponent(data) {

            let str = '';
            for (let key in data) {
                str += encodeURIComponent(key) + '=' + encodeURIComponent(data[key]) + '&'
            }
            return str.slice(0, str.length - 1);
        },
        uriComponentJson(data) {
            return JSON.stringify(data)
        },
        checkContentType(config){
            let headers = config['headers']
            if (headers){
                if (!config['headers']['post']){
                    config['headers']['post'] = {}
                }

                if (!config['headers']['patch']){
                    config['headers']['patch'] = {}
                }


                if (!config['headers']['put']){
                    config['headers']['put'] = {}
                }
                var str = "axios headers config example"
                var obj = { headers: {
                    "common": {Accept: "application/json, text/plain, */*", "Authorization": "Authorization"},
                    "post": {"Content-Type": "application/xxx;charset=urf8"},
                    "patch": {"Content-Type": "application/xxx;charset=urf8"},
                    "put": {"Content-Type": "application/xxx;charset=urf8"},
                    "delete": {},
                    "get": {},
                    "head": {},
                }}
                if (headers['Content-Type']){
                    console.log(str, obj)
                    config['headers']['post']['Content-Type'] = headers['Content-Type']
                    config['headers']['put']['Content-Type'] = headers['Content-Type']
                    config['headers']['patch']['Content-Type'] = headers['Content-Type']
                } else if (headers['content-type']) {
                     console.log(str, obj)
                    config['headers']['post']['Content-Type'] = headers['content-type']
                    config['headers']['put']['Content-Type'] = headers['content-type']
                    config['headers']['patch']['Content-Type'] = headers['content-type']
                }
            }

            return config
        }
    }

    return obj
}

