$(function () {
    var q=$("input[name='q']").val();
    var searchresult=$('.main-container .list-group .result-list');
    console.log(q);
    if (q){
        searchresult.removeClass('add-class');
    }else {
        searchresult.addClass('add-class');
    }
});