
sendRequest = (url, method, data) => {
    let r = axios({
        method: method,
        url: url,
        data: data,
        xsrfCookieName:'csrftoken',
        xsrfHeaderName:'X-CSRFToken',
        headers:{
            'X-Requested-With': 'XMLHttpRequest',
        }
    });
    return r;
}

const AppBuySell = Vue.createApp({
    data() {
        return {
            typeToken: 'st1',
            typeOrder: 'buytoken',
            opacityOrder: 0,
            total: 0,
        }
    },
    watch: {
        opacityOrder: function(){
            document.getElementById('loadinggif-part').style.animation = 'fadeIn 1s forwards';
            vm = this;
            sendRequest('/buy-sells/get-order/?op=' + this.opacityOrder + '&tk=' + this.typeToken, 'get')
                .then((response) => {
                    if(response['status'] == 200){
                        vm.total = response.data.total;
                        document.getElementById('loadinggif-part').style.animation = 'fadeOut 1s forwards';
                    }else if(response['status'] == 400){
                        document.getElementById('loadinggif-part').style.animation = 'fadeOut 1s forwards';
                    }
                })
        }
    },
});
AppBuySell.mount('#request-realtime')
