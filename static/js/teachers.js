
//富文本编辑器
$(function () {
    window.ue=UE.getEditor('editor',{
        initialFrameHeight:400,
        serverUrl:'/ueditor/upload/'
    });
});

//上传七牛云
$(function () {
   var dataBtn=$('#data-btn');
   var progressBtn=$('#progress-group');
   var progressBar=$('.progress-bar');
   function progress(response) {
       var percent=response.total.percent;
       var progressVal=percent.toFixed(0)+'%';
       progressBar.css({'width':progressVal});
       progressBar.text(progressVal);
       //再上传的时候禁止点击上传按钮
       dataBtn.unbind('change');
       console.log('========================');
        console.log(response);
    }
    function error(error) {
        window.messageBox.showError(error.message);
        //上传错误的时候，进度条需要被隐藏
        progressBtn.hide()
    }
    function complete(response) {
        var key=response.key;
        var domain='http://pbfsh0l77.bkt.clouddn.com/';
        var url=domain + key;
        var avatarVal=$('input[name="avatar"]');
        avatarVal.val(url);
        //上传完之后进度条要隐藏，且值要归0
        progressBtn.hide();
        progressBar.css({'width':'0'});
        progressBar.text('0%');
    }
   dataBtn.change(function () {
       //表示当前的文件
       var file=this.files[0];
       xfzajax.get({
            'url':'/cms/qntoken/',
           'success':function (result) {
               if(result['code'] === 200){
                   // console.log('===========');
                   // console.log(result['data']);
                   // console.log('===========');
                   var token=result['data']['token'];
                   var key=file.name;
                   var  putExtra={
                       fname:key,
                       params:{},
                       mimeType:['image/png','image/jpeg','image/gif']
                   };
                   var config={
                        useCdnDomain:true,
                       region:qiniu.region.z0
                   };
                    var observable = qiniu.upload(file,key,token,putExtra,config);
                   observable.subscribe ({
                        'next':progress,
                       'error':error,
                       'complete':complete
                   });
                progressBtn.show();
               }
           }
       })

   })
});
//添加教师代码
$(function () {
    var submitBtn=$('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();
        //编辑时需要获取当前标签,以及当前的pk
        var current=$(this);
        var username=$("input[name='username']").val();
        var jobtitle=$("input[name='jobtitle']").val();
        var avatar=$("input[name='avatar']").val();
        var categoey=$('#teacher-category').val();
        //获取uediter中的内容
        var profile=window.ue.getContent();
        console.log('=======================');
        console.log(profile);
        console.log('=======================');
        var teacher_id=current.attr('teacher-list-id');
        var url='';
        if (teacher_id){
            url='/cms/edit_teacher_list/';
        }else{
            url='/cms/teacher/';
        }
        xfzajax.post({
            'url':url,
            'data':{
                'username':username,
                'jobtitle':jobtitle,
                'avatar':avatar,
                'profile':profile,
                'category':categoey,
                'pk':teacher_id
            },
            'success':function (result) {
                if(result['code']===200){
                    console.log('----+++++++======');
                        xfzalert.alertSuccess('添加成功',function () {
                            window.location.reload();
                        });
                }
            }
        });
    });
});

//教师分组前端代码
$(function () {
   var addBtn=$('.add-teacher-category');
   addBtn.click(function () {
       console.log('___=============');
       xfzalert.alertOneInput({
           'title':'添加教师分组',
           'placeholder':'请输入教师分组',
           'confirmCallback':function (inputValue) {
               xfzajax.post({
                   'url':'/cms/add_teacher_category/',
                    'data':{
                       'group_name':inputValue
                    },
                   'success':function (result) {
                       if(result['code'] === 200){
                           console.log('============+++++++++');
                           xfzalert.close();
                           // window.messageBox.showSuccess('添加成功');
                           window.location.reload();
                       }else {
                           xfzalert.close();
                           window.messageBox.showError(result['message']);
                       }
                   }
               });
           }
       });
   });
});

//  教师分组中编辑按钮前端代码
$(function () {
    var editBtn=$('.edit-btn');
    editBtn.click(function () {
        var currentBtn=$(this);
        var tr=currentBtn.parent().parent();
        var category_id=tr.attr('data-id');
        var category_name=tr.attr('data-name');
        xfzalert.alertOneInput({
            'title':'请重新输入分组',
            'value':category_name,
            'placeholder':'请输入分类名称',
            'confirmCallback':function (inputValue) {
                xfzajax.post({
                    'url':'/cms/edit_teacher_category/',
                    'data':{
                        'pk':category_id,
                        'name':inputValue
                    },
                    'success':function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }
                    }
                });
            }
        });
    });
});

//  教师分组中删除按钮前端代码
$(function () {
    var deleteBtn=$('.delete-btn');
    deleteBtn.click(function () {
       var currentBtn=$(this);
       var tr=currentBtn.parent().parent();
       var group_id=tr.attr('data-id');
       xfzalert.alertConfirm({
           'title':'您确定删除吗？',
           'text':'您确认删除这个分组吗？',
           'confirmCallback':function () {
               xfzajax.post({
                   'url':'/cms/delete_teacher_group/',
                   'data':{
                       'pk':group_id
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
//  删除某个教师列表
$(function () {
    var delBtn=$('.delete-list-btn');
    delBtn.click(function () {
       var current=$(this);
       var current_id=current.attr('teacher-list-id');
        xfzalert.alertConfirm({
            'title':'您确认删除吗？',
            'text':'您确认删除这条教師信息嗎？',
            'confirmCallback':function () {
                xfzajax.post({
                    'url':'/cms/delete_teacher_list/',
                    'data':{
                        'pk':current_id
                    },
                    'success':function (result) {
                        if(result['code']  ===200){
                            window.location.reload()
                        }
                    }
                })
            }
        })

    });
});





