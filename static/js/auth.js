//图片验证码
$(function () {
    var $captchaDom=$('.image_captcha');
    $captchaDom.click(function () {
        $captchaDom.attr('src','/auth/img_captcha'+'?random='+Math.random());
    });
});

//短信验证码
$(function () {
    var $sms_right=$('.sms_right');
    function send_sms() {
        var telephone=$('input[name="telephone"]').val();
        if(!telephone|| telephone.length !=11){
            window.messageBox.showError('手机号码输入格式错误');
            return;
        }
        $.get({
            'url':'/auth/sms_captcha/',
            'data':{
                'telephone':telephone
            },
            'success':function (result) {
                console.log(result);
                $sms_right.addClass('sms_disabled');
                $sms_right.unbind('click');
                var num=10;
                var timer=setInterval(function () {
                    $sms_right.html(num+"s" );
                    num--;
                    if (num<=0){
                        clearInterval(timer);
                        $sms_right.html('发送验证码');
                        $sms_right.removeClass('sms_disabled');
                        $sms_right.click(send_sms)
                    }
                },1000);
            },
            'fail':function (error) {
                console.log(error);
            }
        });
    }
    $sms_right.click(send_sms);
});

//ajax注册功能实现
$(function () {
    var telephoneInput=$('input[name="telephone"]');
    var usernameInput=$('input[name="username"]');
    var passwordInput=$('input[name="password"]');
    var password_repeatInput=$('input[name="password_repeat"]');
    var img_captchaInput=$('input[name="img_captcha"]');
    var sms_captchaInput=$('input[name="sms_captcha"]');
    var buttonBtn=$('.login_btn');
    buttonBtn.click(function (event) {
        //禁止传统的表单发送数据
        event.preventDefault();
        var telephone=telephoneInput.val();
        var username=usernameInput.val();
        var password=passwordInput.val();
        var password_repeat=password_repeatInput.val();
        var img_captcha=img_captchaInput.val();
        var sms_captcha=sms_captchaInput.val();
        if(!telephone|| telephone.length !=11){
            window.messageBox.showError('手机号码输入格式错误');
            return;
        }
        xfzajax.post({
            'url': '/auth/register/',
            'data':{
                'telephone':telephone,
                'username':username,
                'password':password,
                'password_repeat':password_repeat,
                'img_captcha':img_captcha,
                'sms_captcha':sms_captcha
            },
            'success':function(result){
                if (result['code'] === 200){
                    //js中通过window.location= '/'重定向至首页
                    window.location='/';
                }else {
                    var message=result['message'];
                    window.messageBox.showError(message)
                }
            },
            'fail':function (fail) {
                console.log(fail)
            }
        });
    });
});