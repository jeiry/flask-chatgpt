new Vue({
    delimiters: ["((", "))"],
    el: '#app',
    data: function () {
        return {
            role:'user',
            input:'',
            list:[
            ],
            inputM:'gpt-3.5-turbo',
            options:[
                'gpt-3.5-turbo',
                'gpt-3.5-turbo-16k',
                'gpt-4',
                'gpt-4-32k'
            ],
            isloading:false,
            completion_text:''
        }
    },
    mounted() {
        // setInterval(() => {
        //     this.load()
        // }, 2000);
        let that = this
        setInterval(function () {
            if(that.isloading == true){
                that.check()
            }
        }, 1000)
    },
    methods: {
        sent() {
            let that = this
            that.completion_text = ""
            if(that.role != 'system'){
                this.isloading = true
            }
            axios.post('sent', {
                params: {
                    role:that.role,
                    input:that.input,
                    inputM:that.inputM
                }
            })
                .then(function (response) {
                    let res = response.data
                    console.log(res);
                    if (res.status == 1) {
                        that.list.push({"role": that.role,"content": that.input})
                        that.input = ""
                    } else {
                        that.$message({
                            type: 'info',
                            message: res.msg
                        });
                    }
                })
                .catch(function (error) {

                });
        },
        check(){
            var that = this
            axios.get('check', {
                params: {
                }
            })
                .then(function (response) {
                    let res = response.data
                    console.log(res);
                    if (res.status == 1) {
                        // tempText
                        if(res.isstop == false){
                            that.completion_text = res.completion_text
                        }else{
                            that.isloading = false
                            if(that.completion_text != ''){
                                that.list.push({"role": "assistant","content": that.completion_text})
                            }
                            that.completion_text = ""
                        }
                    } else {
                        that.$message({
                            type: 'info',
                            message: res.msg
                        });
                    }
                })
                .catch(function (error) {

                });

        },
        reset(){
            this.completion_text = ""
            this.list = []
            this.isloading = false
            axios.get('reset', {
                params: {
                }
            })
                .then(function (response) {
                    let res = response.data
                    console.log(res);
                    if (res.status == 1) {
                    } else {
                        that.$message({
                            type: 'info',
                            message: res.msg
                        });
                    }
                })
                .catch(function (error) {

                });
        },
        change(){
            console.log(this.inputM)
            this.reset()
        },
        getParameters() {
            let uri = window.location.href.split('?');
            if (uri.length == 2) {
                let vars = uri[1].split('&');
                let getVars = {};
                let tmp = '';
                vars.forEach(function (v) {
                    tmp = v.split('=');
                    if (tmp.length == 2)
                        getVars[tmp[0]] = tmp[1];
                });
                return getVars
                // console.log(getVars);
            }
        }
    }
})
