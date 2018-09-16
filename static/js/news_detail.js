$(function () {
    var submitBtn=$('#submit-comment-btn');
    var contentVal=$('.comment-textarea');
    submitBtn.click(function () {
        //返回属性的值，即获取属性值
        var news_id=submitBtn.attr('data-news-id');
        var content=contentVal.val();
        xfzajax.post({
            'url':'/add_comment/',
            'data':{
                'news_id':news_id,
                'content':content
            },
            'success':function (result) {
                if(result['code']===200){
                    // console.log(result)
                    var comment =result['data'];
                    var commentGroup=$('.comment-list-group');
                    //将获得到的数据comment变成idcomment-data的模板
                    var tpl=template('comment-data',{'comment':comment});
                    commentGroup.prepend(tpl);
                    console.log(news_id);
                    contentVal.val('');
                } else {
                    window.messageBox.showError(result['message'])
                }
            }
        })
    });
});