function addScript(url){
    document.write("<script language=javascript src="+url+"></script>");
}
addScript('./md5.js')

if (parent.callback) {
    //如果是在子框架内就把首页刷新
    parent.callback();
}

var loginApp = new Vue({
    el: '.login-main',
    data: {
        username: '',
        password: '',
        loading: false
    },
    methods: {
        login: function () {
            this.loading = true;
            if (this.username === "" || this.password === "") {
                this.$message.error("Please enter your username or password!");
                this.loading = false;
                return ;
            }
            this.password = hex_md5(this.password);
            this.$nextTick(function () {
                document.getElementById('login-form').submit();
            });
        }
    }
});