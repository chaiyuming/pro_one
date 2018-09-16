#将报错信息封装，以便随时继承调用
class FormMixin(object):
    def get_error(self):
        if hasattr(self,'errors'):
            # errors可以获取验证表单forms.py文件中注册时的错误信息
            # print(type(form.errors))
            # .get_json_data将错误信息转成字典形式
            # print(form.errors.get_json_data())
            errors_dict = self.errors.get_json_data()
            # popitem()可以获取字典中的任意一项，该处用户获取errors_info中的任意一项错误信息,该信息以元祖的形式被提取出。
            # ('sms_captcha', [{'message': '请输入四位数字的短信验证码', 'code': 'required'}])
            print(errors_dict)
            errors_tuple = errors_dict.popitem()
            print(errors_tuple)
            # [{'code': 'required', 'message': '必须填入密码'}]
            errors_list = errors_tuple[1]
            print(errors_list)
            # {'code': 'required', 'message': '必须填入密码'}
            errors_info = errors_list[0]
            # 请再次输入密码
            message = errors_info['message']
            # print(errors_message)
            return message
        else:
            return None
