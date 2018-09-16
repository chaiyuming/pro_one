$(function () {
        var searchBtn=$('.search-btn');
        var q=$('.search-input').val();
        var titleVal=$('.news_title');
        searchBtn.click(function () {
            xfzajax.get({
                'url':'/search/',
                'data':{
                    'q':q
                },
                'success':function (result) {
                    if (result['code']===200){
                        var content=result['data']['content'];
                        var re1=content.indexOf(q);
                        var re2=titleVal.indexOf(q);
                        if(re1 < 0 && re2 < 0){
                            window.messageBox.showError(result['message'])
                        }
                    }
                }
            });
        });
    });


        $(function () {
            var searchBtn=$('.search-btn');
            var resultList=$('.result-list');
            // 要么你就用 Ajax  用表单回自定义刷新
            searchBtn.click(function (ev) {
                ev.preventDefault();
                var searchVal=$('.search-input').val();
                console.log(searchVal);
                if(searchVal.trim()){
                    resultList.addClass('hide').siblings('div.recommend-list').removeClass('hide');
                }else {
                    alert('bunengweikong')
                }
            });
        });


// ajax代码
        $(function () {
            var searchBtn=$('.search-btn');
            var resultList=$('.result-list');
            searchBtn.click(function (ev) {
                ev.preventDefault();
                var searchVal=$('.search-input').val();
                xfzajax.get({
                    'url':'/search/',
                    'data':{
                        'q':searchVal
                    },
                    'success':function (result) {
                        console.log(result);
                        if(result['code']===200){
                            console.log('==========');
                            console.log('result');
                            if (searchVal.trim()) {
                                resultList.addClass('hide').siblings('div.recommend-list').removeClass('hide');
                            }
                        }
                    }
                });
            });
    });