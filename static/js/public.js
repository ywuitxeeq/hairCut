const localStorageUtils = {
    setParam: function (name, value) {
        if (value) {
            localStorage.setItem(name, value);
        }
    },
    getParam: function (name) {
        return localStorage.getItem(name);
    },
    removeParam: function (key) {
        return localStorage.removeItem(key);
    }
};

const dateHelp = (t) => {
    /*
    t 分钟
    * */
    let curData = new Date();
    curData.setSeconds(curData.getSeconds() + t * 60);
    return curData.getTime()
};


const setCookie = (name, value, seconds) => {
    seconds = seconds || 0; //seconds有值就直接赋值，没有为0。
    var expires = "";
    if (seconds != 0) { //设置cookie生存时间
        var date = new Date();
        date.setTime(date.getTime() + (seconds * 1000));
        expires = "; expires=" + date.toGMTString();
    }
    document.cookie = name + "=" + escape(value) + expires + "; path=/"; //转码并赋值
}



