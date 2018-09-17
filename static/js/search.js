// $(function () {
//         var searchBtn=$('.search-btn');
//         var q=$('.search-input').val();
//         var titleVal=$('.news_title');
//         searchBtn.click(function () {
//             xfzajax.get({
//                 'url':'/search/',
//                 'data':{
//                     'q':q
//                 },
//                 'success':function (result) {
//                     if (result['code']===200){
//                         var content=result['data']['content'];
//                         var re1=content.indexOf(q);
//                         var re2=titleVal.indexOf(q);
//                         if(re1 < 0 && re2 < 0){
//                             window.messageBox.showError(result['message'])
//                         }
//                     }
//                 }
//             });
//         });
//     });
//
//
//         $(function () {
//             var searchBtn=$('.search-btn');
//             var resultList=$('.result-list');
//             // 要么你就用 Ajax  用表单回自定义刷新
//             searchBtn.click(function (ev) {
//                 ev.preventDefault();
//                 var searchVal=$('.search-input').val();
//                 console.log(searchVal);
//                 if(searchVal.trim()){
//                     resultList.addClass('hide').siblings('div.recommend-list').removeClass('hide');
//                 }else {
//                     alert('bunengweikong')
//                 }
//             });
//         });
// ajax代码

$(function () {
    var searchBtn=$('.search-btn');
    searchBtn.click(function (ev) {
        ev.preventDefault();
        var searchVal=$('.search-input').val();
        xfzajax.get({
            'url':'/search_list/',
            'data':{
                'q':searchVal
            },
            'success':function (result) {
                console.log(result);
                if(result['code']===200){
                    var resultList=$('.result-list');
                    var news=result['data'];
                    var tpl =template('search_item',{'news':news});
                    var ulVal=$('.list-content-group');
                    ulVal.empty();
                    ulVal.append(tpl);
                    resultList.removeClass('hide').siblings().addClass('hide');
                    console.log('==========');
                    console.log(news);
                    //$.trim()函数会移除字符串开始和末尾处的所有换行符，空格(包括连续的空格)和制表符。如果这些空白字符在字符串中间时，它们将被保留，不会被移除。
                    // if (searchVal.trim()) {
                    //     resultList.addClass('hide').siblings().removeClass('hide');
                    // }
                }
            }
        });
    });
});