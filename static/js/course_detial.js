// 课程播放功能
$(function () {
    var spanVal=$('.video-container span');
    var video=spanVal.attr('data-video-url');
    var coverurl=spanVal.attr('data-cover-url');
    var courseid=spanVal.attr('data-course-id');
    console.log(video);
    console.log(coverurl);
    //初始化播放器，并且将视频地址的参数传递进去。
    //通过cyberplayer获取palyercontainer,并通过.setup()对其进行设置；
    var player=cyberplayer("playercontainer").setup({
        width:'100%',
        height:'100%',
        file:video,
        image:coverurl,
        //记载完毕后是否自动开始
        autostart:false,
        //扩大的方式？？？
        stretching:'uniform',
        //播放完后是否重复
        repeat:false,
        volume:100,
        //是否显示控制条
        controls:true,
        //设置播放方式，如果删掉就会优先使用h5的播放方式；
        // primary:'flash',
        //是否采用token加密的方式
        tokenEncrypt:true,
        //AccessKey
        ak:'5b8849ddc6504318abcea39fe620948e'
    });
    //给player绑定一个事件，‘beforePlay’表示播放之前执行后面的函数。先拿到token才能播放视频
    //before() 方法在被选元素前插入指定的内容。
    player.on('beforePlay',function (e) {
        if(!/m3u8/.test(e.file)){
            return;
        }
        console.log(e.file);
        xfzajax.get({
            'url':'/course/course_token/',
            'data':{
                'video':video,
                'courseid':courseid
            },
            'success':function (result) {
                if(result['code'] === 200){
                    // console.log(result)
                    var token=result['data']['token'];
                    console.log('=====================');
                    console.log(token);
                    console.log('=====================');
                    //e.file表示文件的名字
                    player.setToken(e.file,token)
                }else {
                    window.messageBox.showInfo(result['message']);
                    player.stop()
                }
            }
        });
    });
});