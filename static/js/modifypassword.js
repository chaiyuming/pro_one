//修改密码
$(function () {
    var submitBtn=$('.submit-btn');
    submitBtn.click(function (ev) {
        ev.preventDefault();
        var current=$(this);
        var password=$("input[name='password']").val();
        var repeat_password=$("input[name='repeat_password']").val();
        var pk=current.attr('data-id');
        xfzajax.post({
            'url':'/auth/modifypassword/',
            'data':{
                'password':password,
                'repeat_password':repeat_password,
                'pk':pk
            },
            'success':function (result) {
                if(result['code'] === 200){
                    window.messageBox.showSuccess('密码修改成功');
                    setTimeout(function () {
                        window.location='/auth/login/';
                    },1200);
                }else {
                    xfzalert.alertError(result['message']);
                }
            }
        })
    })
});