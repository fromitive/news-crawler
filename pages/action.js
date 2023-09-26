var header = document.getElementById("myHeader");
var sticky = header.offsetTop;
var initial_element=30;
var updated_element=30;
//처음 로드될때 보여지는 뉴스 개수
if(window.screen.width <= 480){
    initial_element=10;
    updated_element=10;
}

function fixScroll() {
    if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
    }
}

function sendNews(){
    var items=$(".news-table .selected")
    var data=new Array();
    for(let idx=0; idx < items.length; idx++){
        var news_item=new Object();
        newsTitle=$(items[idx]).find('.title')[0].textContent
        newsLink=$(items[idx]).find('td > a')[0].href
        news_item.newsTitle=newsTitle;
        news_item.newsLink=newsLink;
        data.push(news_item)
    }
    
    $.ajax({type:'post',
            url:"/news/send-news",
            data:JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success:function(data){
                alert(data);
    }});
}

// 뉴스선택 다시 부활 ;;
$( ".news-table tr" ).click(function(evt){
    $(this).toggleClass('selected'); 
});

$("#news-send1").click(function(evt){
    var items=$(".news-table .selected");
    //select list 초기화
    $("#modal-news-list").empty();
    for(let idx=0; idx < items.length; idx++){
        var newsTitleElmt='<li>'+$(items[idx]).find('.title')[0].textContent+'</li>';
        $("#modal-news-list").append(newsTitleElmt);
    }
    $('#modal-news-summary').text("발행할 뉴스 "+items.length+"개가 선택되었습니다. 뉴스는 아래와 같습니다.");

    $('.modal').show();
});

$("#news-send2").click(function(evt){
    sendNews();
});


$("#modal-close").click(function(){
    $('.modal').hide();
});

// 메뉴 fix
window.addEventListener('scroll',function(e){
    fixScroll();
});

//스크롤바가 제일 밑에 있을때, 컨텐츠 다시 더 보여주기
window.addEventListener('scroll',function(e){
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight-100) {
        initial_element+=updated_element;
        $(".news-table tbody tr:nth-child(-n+"+initial_element+")").removeAttr("Style")
    }
});

//뉴스뷰 초기화
window.addEventListener('load',function(e){
    $(".news-table tbody tr:nth-child(n+"+initial_element+")").css("display","none")
});