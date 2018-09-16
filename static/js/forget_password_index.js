//发送短信验证码
$(function () {
    var smsright=$('.sms_right');
    function send_sms () {
       var telephone=$("input[name='telephone']").val();
        $.get({
            'url':'/auth/rest_pwd/',
            'data':{
                'telephone':telephone
            },
            'success':function (result) {
                console.log('=========');
                console.log(result);
                console.log('=========');
                smsright.addClass('sms_disabled');
                smsright.unbind('click');
                var num = 10;
                var timer=setInterval(function () {
                    smsright.html(num + 's');
                    num --;
                    if(num <=0){
                        clearInterval(timer);
                        smsright.html('发送验证码');
                        smsright.removeClass('sms_disabled');
                        smsright.click(send_sms);
                    }
                },1000);
            },
            'fail':function (error) {
                console.log(error);
            }
        });
    }
    smsright.click(send_sms);
});

// 短信验证页面
$(function () {
   var submitBtn=$('.submit-btn');
   // console.log('=====');
   // console.log(submitBtn);
   submitBtn.click(function (ev) {
       ev.preventDefault();
        var telephone=$("input[name='telephone']").val();
        var sms_captcha=$("input[name='sms_captcha']").val();
        if(!telephone|| telephone.length !=11) {
            window.messageBox.showError('手机号码输入格式错误');
            return;
        }
        xfzajax.post({
            'url':'/auth/forget_password/',
            'data':{
                'telephone':telephone,
                'sms_captcha':sms_captcha
            },
            'success':function (result) {
                console.log(result);
                if(result['code'] === 200){
                    window.location='/auth/modifypassword/?pk='+result['data']['user_id'];
                }else{
                    window.messageBox.showError(result['message']);
                }
            }
        });
   });
});

