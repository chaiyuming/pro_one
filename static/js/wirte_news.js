/*
//上传到服务器
$(function () {
    var uploadBtn=$('#upload-btn');
    //change表示按钮上绑定了图片的所有的信息
    uploadBtn.change(function (event) {
        //this表示当前的按钮，.files[0]表示当前选中的文件。
        var file=this.files[0];
        //构建表单体，FormData对象可以让我们组织一个使用XMLHttpRequest对象
        发送的键值对的集合。它主要用于发送表单数据,但是可以独立于使用表单传输的数据。
        var formData=new FormData();
        //('upfile',file)相当于upfile=file
        formData.append('upfile',file);
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data':formData,
            //processData:为true时表示会将表单中的数据进行处理
            'processData':false,
            //为true时，会指定一些js的contentType
            'contentType':false,
            'success':function (result) {
                if(result['code'] ===200){
                    console.log(result);
                    //data:{url: "/media/footer设置.png"},result['data']['url']获取到的是/media/footer设置.png。
                    var url=result['data']['url'];
                    var thumbnailInput=$("input[name='thumbnail']");
                    thumbnailInput.val(url)
                }
            }
        });
    });
});
*/
//进度条配置
$(function () {
    var progress_group=$('#progress-group');
    var progress_bar=$('.progress-bar');
    var uploadBtn = $('#upload-btn');
    function progress(response) {
        // console.log(response);
        //获取当前上传进度，范围：0～100。
        var percent=response.total.percent;
        //toFixed(n)表示保留小数点的个数，0表示不保留小数点。
        var progressText=percent.toFixed(0)+'%';
        progress_bar.css({'width':progressText});
        progress_bar.text(progressText);
        uploadBtn.unbind('change');

    }
    function error(err) {
        console.log(err);
        window.messageBox.showError(err.message);
        //表示当出现错误时，进度条隐藏
        progress_group.hide()
    }
    function complete(response) {
        // console.log(response);
    //  response包含了hash值以及key(文件名)
        var key=response.key;
        //七牛云的测试域名，以后进公司写项目要换成公司的域名
        var domain='http://pbfsh0l77.bkt.clouddn.com/';
        var url=domain + key;
        var thumbnailInput= $('input[name="thumbnail"]');
        thumbnailInput.val(url);
        //表示当完成时，进度条隐藏
        progress_group.hide();
    //    文件上传完以后，进度归零
        progress_bar.css({'width':'0'});
        progress_bar.text('0%');
    }
    //上传到千牛云
    //change表示按钮上绑定了图片的所有的信息
    function upload_file() {
        //this表示当前的按钮，.files[0]表示当前选中的文件。
        var file = this.files[0];
        //通过ajx获取token
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if (result['code'] === 200) {
                    //获取result中data中的token
                    var token = result['data']['token'];
                    // console.log(token);
                    //获取文件的名字
                    var key =file.name;
                    var putExtra = {
                        fname: key,
                        params: {},
                        //mimeType: null || array，用来限制上传文件类型，为 null 时表示不对文件类型限制；限制类型放到数组里： ["image/png", "image/jpeg", "image/gif"]
                        mimeType: ['image/png', 'image/jpeg', 'image/gif','video/x-ms-wmv']
                        // mimeType: null
                    };
                    var config = {
                        //config.useCdnDomain: 表示是否使用 cdn 加速域名，为布尔值，true 表示使用，默认为 false。
                        useCdnDomain: true,
                        //region: 选择上传域名区域；当为 null 或 undefined 时，自动分析上传域名区域
                        region: qiniu.region.z0
                    };
                    //qiniu.upload 返回一个 observable(可自定义) 对象用来控制上传行为，observable 对像通过 subscribe 方法可以被 observer 所订阅，订阅同时会开始触发上传，同时返回一个 subscription 对象，该对象有一个 unsubscribe 方法取消订阅，同时终止上传行为
                    var observable =qiniu.upload(file,key,token,putExtra,config);
                    //observer 为一个 object，用来设置上传过程的监听函数，有三个属性 next、error、complete
                    observable.subscribe ({
                        'next':progress,
                        'error':error,
                        'complete':complete
                    });
                    progress_group.show();

                }
            }
        });
    }
    //相当于uploadBtn.change(function () {......}
    uploadBtn.change(upload_file);
});

//富文本编辑器
$(function () {
    //此处UE为html文件中导入ueditor的js文件自带的。
    //window.ue是将ue这个变量变为全局变量
    window.ue = UE.getEditor('editor',{
        initialFrameHeight:400,
        serverUrl:'/ueditor/upload/'
    });
});


//发布新闻内容/编辑新闻内容
$(function () {
   var sumbitBtn=$('#sumbit-btn');
    sumbitBtn.click(function (event) {
        event.preventDefault();
        //表示的时当前的按钮
        var btn=$(this);
        var title=$('input[name="title"]').val();
        var desc=$('input[name="desc"]').val();
        var thumbnail=$('input[name="thumbnail"]').val();
        var category=$('select[name="category"]').val();
        //新闻内容是从富文本中获取，window.ue.getContent()可获取编辑器html的内容。
        var content=window.ue.getContent();
        var news_id=btn.attr('data-new-id');
        var url='';
        if(news_id){
            url='/cms/edit_news/';
        }else {
            url='/cms/write_news/';
        }
    //    获取完所有变量以后，通过ajax方式发送给服务器。
        xfzajax.post({
            'url':url,
            'data':{
                'title':title,
                'desc':desc,
                'thumbnail':thumbnail,
                'category':category,
                'content':content,
                'pk':news_id
            },
            'success':function (result) {
                if (result['code']===200){
                    xfzalert.alertSuccess('恭喜，新闻发布成功',function () {
                        window.location.reload();
                    });
                }
            }
        });
    });
});