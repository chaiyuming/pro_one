// 添加分类
$(function () {
    var addBtn = $("#add-btn");
    addBtn.click(function () {
        //弹出对话框,alertOnrInput表示可以出入内容
        //xfzalert.alertOneInput表示调用xfzalert.alertOneInput这个函数
        xfzalert.alertOneInput({
            'title': '添加新闻分类',
            'placeholder': '请输入新闻分类',
            //confirmCalback表示点击确定按钮时会将输入的内容传递给某个函数
            //inputValue：表示在输入框中输入的内容
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/add_news_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            xfzalert.close();
                            window.location.reload();
                            // window.messageBox.showSuccess('添加成功！')
                        }else{
                            //表示当弹出message提示时，关闭xfzalert弹出页面
                            xfzalert.close();
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });
    });
});

//编辑分类
$(function () {
    var editBtn=$('.edit-btn');
    editBtn.click(function () {
        //获取当前的按钮
        var currentBtn=$(this);
        //获取tr标签内容
        var tr=currentBtn.parent().parent();
        var pk =tr.attr('data-pk');
        var name=tr.attr('data-name');
        xfzalert.alertOneInput({
            'title':'请重新输入分类',
            'value':name,
            'placeholder':'请输入分类名称',
            'confirmCallback':function (inputValue) {
                xfzajax.post({
                    'url':'/cms/edit_news_category/',
                    'data':{
                        'pk':pk,
                        'name':inputValue
                    },
                    'success':function (result) {
                        if (result['code'] === 200){
                            xfzalert.close();
                            window.location.reload();
                        }else{
                            //表示当弹出message提示时，关闭xfzalert弹出页面
                            xfzalert.close();
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });
    });
});

//删除分类
$(function () {
    var delBtn=$('.del-btn');
    delBtn.click(function () {
        var currentBtn=$(this);
        var tr=currentBtn.parent().parent();
        var pk =tr.attr('data-pk');
        xfzalert.alertConfirm({
            'title':'您确认删除吗',
            'text':'您确定要删除这个分类嘛',
            'confirmCallback':function () {
                xfzajax.post({
                    'url':'/cms/delete_news_category/',
                    'data':{
                        'pk':pk
                    },
                    'success':function (result) {
                        if (result['code'] === 200){
                            window.location.reload();
                        }
                    }
                });
            }
        });
    });
});
