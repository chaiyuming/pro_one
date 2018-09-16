//富文本编辑器
$(function () {
   window.ue = UE.getEditor('editor',{
       initialFrameHeight:400,
       serverUrl:'/ueditor/upload/'
   });
});

//发布/编辑课程前端代码
$(function () {
    var CourseBtn=$('#course-button');
    CourseBtn.click(function (event) {
        event.preventDefault();
        //表示当前的编辑按钮
        var current=$(this);
        var course_id=current.attr('course-data-id');
       var title=$("input[name='title']").val();
       var category_id=$('#course-category').val();
       var teacher_id=$('#course-teacher').val();
       var video_url=$('#course-adress').val();
       var cover_url=$('#course-cover').val();
       var durarion=$('#course-time').val();
       var price=$('#course-price').val();
       var profile=window.ue.getContent();
       var url='';
       if(course_id){
           url='/cms/course_edit/';
       }else {
           url='/cms/pub_course/';
       }
       xfzajax.post({
           'url':url,
           'data':{
               'title':title,
               'video_url':video_url,
               'cover_url':cover_url,
               'category_id':category_id,
               'teacher_id':teacher_id,
               'durarion':durarion,
               'price':price,
               'profile':profile,
               'pk':course_id
           },
           'success':function (result) {
               console.log(result);
               if (result['code'] === 200){
                   xfzalert.alertSuccess('课程发布成功',function () {
                       console.log('===========');
                       window.location.reload()
                   })
               }else {
                   var message=result['message'];
                    window.messageBox.showError(message)
               }
           }
       });
    });
});

//添加课程分类
$(function () {
   var addBtn=$('.add-course-category');
   addBtn.click(function () {
       xfzalert.alertOneInput({
           'title':'添加课程分类',
           'placeholder':'请输入课程分类',
           'confirmCallback':function (inputValue) {
               xfzajax.post({
                   'url':'/cms/add_course_category/',
                   'data':{
                       'category_name':inputValue
                   },
                   'success':function (result) {
                       if(result['code']===200){
                           xfzalert.close();
                           window.location.reload();
                       }else{
                           xfzalert.close();
                           window.messageBox.showError(result['message']);
                       }
                   }
               })
           }
       });
   });
});

//课程分类编辑按钮
$(function () {
  var  editBtn=$('.edit-btn');
  editBtn.click(function () {
     var currentBtn=$(this);
     var tr=currentBtn.parent().parent();
     var pk=tr.attr('data-id');
     var name=tr.attr('data-name');
     xfzalert.alertOneInput({
         'title':'请重新输入分类',
         'value':name,
         'placeholder':'请输入分类名称',
         'confirmCallback':function (inputValue) {
             xfzajax.post({
                 'url':'/cms/edit_course_category/',
                 'data':{
                     'pk':pk,
                     'name':inputValue
                 },
                 'success':function (result) {
                     if(result['code'] === 200){
                         console.log('==================');
                         console.log(pk);
                         console.log(name);
                         console.log('==================');
                           // xfzalert.close();
                         window.location.reload();
                       }
                 }
             });
         }
     });
  });
});
//课程分类删除按钮

$(function () {
    var deleteBtn=$('.delete-btn');
    deleteBtn.click(function () {
        var currentBtn=$(this);
        var tr=currentBtn.parent().parent();
        var pk=tr.attr('data-id');
        xfzalert.alertConfirm({
            'title':'您确认删除吗？',
            'text':'您确认删除这个分类吗？',
            'confirmCallback':function () {
                xfzajax.post({
                    'url':'/cms/delete_course_category/',
                    'data':{
                        'pk':pk
                    },
                    'success':function (result) {
                        if(result['code']===200){
                            window.location.reload();
                        }
                    }
                });
            }
        });
    });
});