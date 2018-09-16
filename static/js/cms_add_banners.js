//这个函数是给关闭按钮添加关闭事件
function RemoveBanner(bannerItem) {
    //通过传递进来的参数找到.close_banner标签
    var closeBanner=bannerItem.find('.close_banner');
    //获取bannerid
    var banners_id=bannerItem.attr('data-banner-id');
    closeBanner.click(function () {
        //如果有bannerid说明这个轮播图是已经存在的，不是临时的，那么就可以执行下面的弹出提示
        if(banners_id){
            //alertConfirm是有提示的功能
            xfzalert.alertConfirm({
                'text':'您确定删除这个轮播图嘛？',
                //confirmCallback是点击确认按钮时，会执行里面的函数
                'confirmCallback':function () {
                //    通过ajax执行删除内容；
                    xfzajax.post({
                        'url':'/cms/delete_banners/',
                        'data':{
                            //对视图函数中定义的banner_id进行赋值
                            'banner_id':banners_id
                        },
                        'success':function (result) {
                            if(result['code']===200){
                                //将存进来的bannerItem参数删掉；
                                bannerItem.remove();
                                window.messageBox.showSuccess('轮播图删除成功！')
                            }
                        }
                    });
                }
            });
        //    else表示的是临时存在的情况
        }else{
            bannerItem.remove();
        }
    });
}
//添加轮播图图片事件
//上传到自己的服务器
function addiamge(bannerItem){
    var BannerImage=bannerItem.find('.banner-image');
    var AddImage=bannerItem.find('.add_image');
    BannerImage.click(function () {
        AddImage.click();
    });
    AddImage.change(function () {
        var file= this.files[0];
        var formData=new FormData();
        formData.append('upfile',file);
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data':formData,
            'processData':false,
            'contentType':false,
            'success':function (result) {
                if(result['code'] ===200){
                    // console.log(result);
                    //获取到上传的图片的图片地址
                    url=result['data']['url'];
                    BannerImage.attr('src',url)
                }
            }
        });
    });
}
//添加\编辑轮播图内容事件
function addbanner(bannerItem) {
    var saveBtn=bannerItem.find('.save-btn');
    var BannerImage=bannerItem.find('.banner-image');
    var priorityInput=bannerItem.find("input[name='priority']");
    var linktoInput=bannerItem.find("input[name='link_to']");
    var bannerid=bannerItem.attr('data-banner-id');
    var url='';
    if(bannerid){
            url ='/cms/edit_banners/'
        }else {
        url ='/cms/add_banners/'
    }
    saveBtn.click(function () {
        var image_url=BannerImage.attr('src');
        var priority=priorityInput.val();
        var link_to=linktoInput.val();
        console.log(priority);
        // console.log('点击');
        xfzajax.post({
            'url':url,
            'data':{
                'image_url':image_url,
                'priority':priority,
                'link_to':link_to,
                'pk':bannerid
            },
            'success':function (result) {
                if(result['code'] === 200){
                    if(!bannerid){
                        //因为add_banners视图中返回了banner_id,所以此时需要获取banner_id.
                        console.log(result);
                        //这里的bannerid不需要用用var定义，它会自动从data数据中获取。
                        bannerid=result['data']['banner_id'];
                        bannerItem.attr('data-banner-id',bannerid);
                        window.messageBox.showSuccess('添加成功！');
                    }else{
                        window.messageBox.showSuccess('修改成功！');
                    }
                    var priorityspan=$('.priority-span');
                    priorityspan.text('优先级'+ priority);
                }
            }
        });
    });
}
//共用部分定义成函数
function createbannerItem(banner) {
    //如果传入了banner就会显示if里面的内容，如果没有传入banner就会显示else里面的内容，.banners.html中的部分同理。
    var tpl=template('Add_Banners',{'banner':banner});
    var bannerListGroup=$('.banner_list_group');
    //因为if和else中各定义了一个bannerItem，重复定义了，所以先给bannerItem赋值，变成一个变量；
    var bannerItem=null;
    if(banner){
        bannerListGroup.append(tpl);
        bannerItem=bannerListGroup.find('.banner-item:last');
    }else{
        bannerListGroup.prepend(tpl);
        bannerItem=bannerListGroup.find('.banner-item:first');
    }
    RemoveBanner(bannerItem);
    addiamge(bannerItem);
    addbanner(bannerItem);
}
//// 网页加载完毕后就执行获取轮播图列表的事件
$(function () {
   // 因为这里只是需要展示显示的功能，所以不需要传入data数据。
   xfzajax.get({
       'url':'/cms/banner_list/',
       'success':function (result) {
           if(result['code']===200){
               //获取到所有的banner
               var banners=result['data']['banners'];
               // console.log(banner);
               for (var i=0; i<banners.length; i++){
                   var banner=banners[i];
                   createbannerItem(banner)
                   // var tpl=template('Add_Banners',{'banner':banner});
                   // var bannerListGroup=$('.banner_list_group');
                   // bannerListGroup.append(tpl);
                   // var bannerItem=bannerListGroup.find('.banner-item:last');
                    // RemoveBanner(bannerItem);
                    // addiamge(bannerItem);
                    // addbanner(bannerItem);
               }
           }
       }
   })
});


//点击添加轮播图页面展示
$(function () {
   var AddBtn=$('#add_banner');
   var bannerListGroup=$('.banner_list_group');
   AddBtn.click(function () {
        // var tpl=template('Add_Banners');
        // var bannerListGroup=$('.banner_list_group');
        // bannerListGroup.prepend(tpl);
        //当tpl添加到bannerListGroup后，通过bannerListGroup.find找到.banner_item标签，
        //因为prepend方式是将tpl添加到最前面，而:first表示找到最前面一个标签，刚好对应添加进来的tpl
        // var bannerItem=bannerListGroup.find('.banner-item:first');
       var length=bannerListGroup.children().length;
       if (length >=6){
           AddBtn.addClass('disabled');
            window.messageBox.showInfo('最多只能添加6张图！')
       }else{
          createbannerItem();
       }

        // RemoveBanner(bannerItem);
        // addiamge(bannerItem);
        // addbanner(bannerItem);
   });
});