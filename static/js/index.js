//新闻分页代码展示
$(function () {
    var moreBtn=$('.more_news');
    // var page=2;,为避免选中分类时，点击加载更多出现相应内容，应将page绑定到加载更多按钮上。
    moreBtn.click(function () {
        var liTags=$('.news_inner li.active');
        var category_id=liTags.attr('news_category_id');
        //因为从前端获取的为字符串，这里需将其转化为数字格式
        var page=parseInt(moreBtn.attr('data_page'));
        xfzajax.get({
            'url':'/news_list/',
            'data':{
                'p':page,
                'category_id':category_id
            },
            'success':function (result){
               var newses=result['data'];
               if(newses.length>0){
                   var newsGroup=$('.news_group');
               // console.log(newses)
                // 接下来就要用到arttemplate前端模板引擎
                    var tpl=template('news_item',{'newses':newses});
                    newsGroup.append(tpl);
                    //page+=1是当点击加载更多按钮时，每点击一次页数就会自动加1
                    page+=1;
               //     将page绑定到加载更多按钮上
                   moreBtn.attr('data_page',page)
               }else{
                   window.messageBox.showError('已全部加载');
               }
            }
        });
    });
});

//新闻分类代码展示
$(function () {
    var listBtn=$('.news_inner');
    libtn=listBtn.children();
    var moreBtn=$('.more_news');
    //点击时就会发送网络请求
    libtn.click(function () {
    //    在发送网络请求之前，先得知道点击的是哪个li标签
        var li=$(this);
    //    获取到li标签后，就可以获取到分类的id
        var categoryId=li.attr('news_category_id');
    //    拿到id以后就开始发送网络请求
        xfzajax.get({
            'url':'/news_list/',
            'data':{
                'category_id':categoryId
            },
            'success':function (result) {
                //获取新闻信息
                var newses=result['data'];
            //       然后将新闻信息渲染到arttemplate中
                var tpl=template('news_item',{'newses':newses});
                //ul标签的值
                var newsGroup=$('.news_group');
                // .empty()可以将newsGruop下的标签清除掉
                newsGroup.empty();
                //然后将获取到的数据放入
                newsGroup.append(tpl);
                li.addClass('active').siblings().removeClass('active');
            //    当每次点击分类后都应该将date_page重置为2
                moreBtn.attr('data_page',2);
            }
        });
    });
});