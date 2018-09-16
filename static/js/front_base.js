$(function () {
    //判断只有当调用了template模板的才执行里面的代码
    //if (template)直接这样写回报template is not defined错误。
    // if (template){
    if (typeof template != 'undefined'){
        // template.defaults.imports+过滤器的名字，可参考arttemplate
        //dateValue是字符串形式，需要转换为时间的格式
        template.defaults.imports.timeSince=function (dateValue) {
            //转换为时间的格式
            var date= new Date(dateValue);
            //转换成时间戳
            var dates=date.getTime();
        //    获取当前时间的时间戳
            var nows=(new Date()).getTime();
            //dates和nows都是毫秒需要转换成秒
            var timestamp=(nows-dates)/1000;
            if (timestamp < 60){
                return '刚刚';
            }else if(timestamp >= 60 && timestamp < 60*60){
                var minutes=parseInt(timestamp / 60);
                return minutes+'分钟前';
            }else if (timestamp >=60*60 && timestamp <60*60*24){
                var hours=parseInt(timestamp/60/60);
                return hours+ '小时前';
            }else if(timestamp >=60*60*24 && timestamp <60*60*24*30){
                var days=parseInt(timestamp/60/60/24);
                return days+'天前';
            } else{
                // '%Y-%m-%d %H:%m'
                var year=date.getFullYear();
                var month=date.getMonth();
                var day=date.getDay();
                var hour=date.getHours();
                var minute=date.getMinutes();
                return  year+'-'+ month +'-' + day + '-' + '  ' + hour + ':' +minute;
            }
        }
    }
});

$(function () {
    var url=window.location.href;
    var protocol=window.location.protocol;
    var host=window.location.host;
    var domain=protocol+'//'+host;
    var path=url.replace(domain,'');
    var menulis=$('.nav-menu li');
    for(index=0;index<menulis.length;index++){
        var li=$(menulis[index]);
        var a =li.children('a');
        var href=a.attr('href');
        if (href===path){
            li.addClass('active');
        }
    }
});