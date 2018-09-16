//添加员工中提交功能代码
$(function () {
    var submitBtn=$('.submit-btn');
    submitBtn.click(function (ev) {
        ev.preventDefault();
        var telephone=$("input[name='telephone']").val();
        xfzajax.post({
           'url':'/cms/add_staff/',
           'data':{
               'telephone':telephone
           },
            'success':function (result) {
                if(result['code'] === 200){
                    window.location.href='/cms/staff';
                }else {
                    window.messageBox.showError(result['message']);
                }
            }
        });
    });
});


//删除员工
$(function () {
    var deleteBtn=$('.delete-id');
    deleteBtn.click(function () {
        var current=$(this);
        var pk=current.attr('staff-data-id');
        console.log(pk);
        xfzalert.alertConfirm({
         'title':'您确认删除吗？',
            'text':'您确认删除这个员工吗？',
            'confirmCallback':function (){
             xfzajax.post({
                 'url':'/cms/delete_staff/',
                 'data':{
                     'telephone':pk
                 },
                 'success':function (result) {
                     if(result['code'] === 200){
                            console.log('=========');
                            window.location.reload();
                        }
                 }
             });
            }
     });
    });
});