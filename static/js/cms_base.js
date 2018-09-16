$(function () {
   // 获取完整的url：比如，http://127.0.0.1:8000/cms/staffs/
   var url=window.location.href;
   //获取协议：http:
   var protocol=window.location.protocol;
   //获取域名，127.0.0.1:8000
   var host=window.location.host;
   var domain=protocol+'//'+host;
   var path=url.replace(domain,'');
   //得到所有的li标签
   var MenuLi=$('.sidebar-menu li');
   //循环遍历所有的li标签
   for(var index=0;index<MenuLi.length;index++){
       var li=$(MenuLi[index]);
       var liA=li.children('a');
       var href=liA.attr('href');
       if(href === path){
           li.addClass('active');
       }
   }
});