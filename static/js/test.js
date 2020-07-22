window.onload = function () {
        page();
        $('#footPage a').click(function () {
            page()
        })

        function page() {
            var page_url = "/haircut/admin/data/page/user?page=" + this.text;
            let axiosApp = newAxios({
                timeout: 10000,
                baseURL: "http://192.168.32.1/",
                withCredentials: true,
                headers: {
                    post: {'Content-Type': 'application/x-www-form-urlencoded'}
                }
            })
            axiosApp.get(
                page_url
                , res => {
                    if (res.data.status == 1000) {
                        var current_page = res.data['current_page'];
                        var pager = res['pager'];
                        var len = pager.length;
                        paramsDate(res.data)
                        let htmlString = '<a class="prev" data="'+ res.data.lw + '" val="'+ parseInt(current_page)-1 +'">&lt;&lt;</a>'
                        for (let j = 0; j < len; j++) {
                            if (j + 1 < current_page) {
                                htmlString += '<a class=\"num\" lw="'+ res.data.lw +'">'+ pager[j] +'</a>'
                            } else if (j + 1 > current_page) {
                                 htmlString += '<a class=\"num\" up="'+ res.data.up +'">'+ pager[j] +'</a>'
                            } else {
                                htmlString += '<span class="current">'+ pager[j] +'</span>'
                            }
                        }
                        htmlString += '<a class="next" up="'+ res.data.up +' val='+ parseInt(current_page)+1 +'>&gt;&gt;</a>'
                        document.getElementById('footPage').innerHTML = htmlString
                        console.log(data);
                        console.log(htmlString);
                    }
                }
            )
        }


        var paramsDate = (resDict) => {

        }

    }