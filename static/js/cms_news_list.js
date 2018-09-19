//时间选择器代码
$(function () {
    var todayDate=new Date();
    var todaystr=todayDate.getFullYear()+'/'+(todayDate.getMonth()+1)+'/'+todayDate.getDate();
    var options={
        //设置日期格式
        'format':'yyyy/mm/dd',
        //clear/today等按钮是否显示
        'showButtonPanel':true,
        //选择事件后自动关闭
        'autoclose':true,
        //选择器选择的开始时间
        'startDate':'2018/6/20',
        'endDate':todaystr,
        //点击today按钮自动关联到今天的日期
        'todayBtn':'linked',
        //清除时间
        'clearBtn':true,
        'todayHighlight':true,
        //选择器语言的显示
        'language':'zh-CN'
    };
    //调用.datepivker({}),就可以实现时间选择器
    $("input[name='start']").datepicker(options);
    $("input[name='end']").datepicker(options);
});

//列表新闻中删除新闻按钮功能
$(function () {
    var DeleteNewsBtn=$('.delete-news-btn');
    DeleteNewsBtn.click(function () {
        var btn=$(this);
        var pk=btn.attr('delete-news-id');
        console.log(pk);
        xfzalert.alertConfirm({
            'title':'您确认删除吗',
            'text':'您确认删除这条新闻吗',
            'confirmCallback':function () {
                xfzajax.post({
                    'url':'/cms/delete_news/',
                    'data':{
                        'pk':pk
                    },
                    'success':function (result) {
                        if(result['code'] === 200){
                            // window.location.reload();
                            window.location = window.location.href;
                        }
                    }
                });
            }
        });
    });
});