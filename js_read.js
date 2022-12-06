
/*
 * 검색 객체
 */
var search_domain = window.location.host;
var FULL_URL = "//" + window.location.hostname;
var langType = LANG_TYPE;
Search.searchPage = 2;

//dev와 qa에서 동작을 위한 처리 추가
if(search_domain.match("qa-")) {
    search_domain = search_domain.replace("qa-", "");
} else if(search_domain.match("dev-")) {
    search_domain = search_domain.replace("dev-", "");
}

if(search_domain == 'm-cn.yna.co.kr' || search_domain == "cb.yna.co.kr"){
    langType = 'cn';
}

// 이미지 타입 변환
String.prototype.P2 = function() {
	return this.toString().replace('_T.','_P2.').replace('_P4.','_P2.').replace('_P1.','_P2.');
};
String.prototype.P1 = function() {
	return this.toString().replace('_T.','_P1.').replace('_P4.','_P1.').replace('_P2.','_P1.');
};

var SearchBasic = {

    CurrentKeyword: undefined,
    CurrentSuggest: undefined,
    SuggestTimeout: undefined,

    LastPage: undefined,
    Total: undefined,
    Page: undefined,
    Count: undefined,
    StartPage: undefined,

    Language: undefined,

    // 이름기반으로 해당되는 ctype 가져오기 - 검색용 html 문서에만 해당
    GetCtype: function (str) {
    	if(typeof str !== 'undefined'){
    		str = str.toLowerCase();
    	}
        if (!str)
            return '*';
        if (str.indexOf('all') >= 0)
            return '*';
        if (str.indexOf('article') >= 0)
            return 'A';
        else if (str.indexOf('photo') >= 0)
            return 'P';
        else if (str.indexOf('graphic') >= 0)
            return 'G';
        else if (str.indexOf('mpic') >= 0)
            return 'M';
        else if (str.indexOf('video') >= 0)
            return 'M';
        else if (str.indexOf('press') >= 0)
            return 'R';
        else if (str.indexOf('issue') >= 0)
            return 'I';
        else if (str.indexOf('people') >= 0)
            return 'H';
        else if (str.indexOf('blog') >= 0)
            return 'B';
        else if (str.indexOf('efestival') >= 0)
            return 'E';
        return '';
    },
    GetCountMain: function (ctype) {
        var search_domain = window.location.host;
        var count = 0;

        if (!ctype)
            return 0;
        switch (ctype) {
            case 'A':
            case 'R':
            case 'B':
            case 'E':
                count = 4;
                if(SearchBasic.Language.toLowerCase() == "kr"){
                    count = 5;
                }
                return count;
            case 'P':
            case 'G':
                if(search_domain == "m-" + langType + ".yna.co.kr"){
                    return 6;
                }
            case 'M':
                return 4;
            case 'I':
                return 6;
            case 'H':
                return 4;
        }
        return 0;
    },
    // 컨텐츠 화면에서 컨텐츠별 표시 개수
    GetCount: function (ctype) {
        var search_domain = window.location.host;
        if (!ctype)
            return 0;
        switch (ctype) {
            case 'A':
                if(search_domain == "m-" + langType + ".yna.co.kr"){
                    return 16;
                }
            case 'H':
                return 10;
            case 'P':
            case 'G':
            case 'M':
                return 16;
            case 'I':
                return 12;
            case 'R':
            case 'B':
            case 'E':
                return 20;
        }
        return 10;
    },
    changeImage : function(image) {
    	return image ? image.replace(/^\/contents/,'').replace(/\/+/g, '/') : '';
    },
    markUpReplace : function(text) {
        return text ? text.replace(/(<[^>]+>)/ig, "") : "";

    },
    // 연관검색어 처리
    SetRelateKeywords: function () {
        var ctype = Search.Query['ctype'];
        Search.LoadRelateKeywords(Search.Query['query'], 'SearchBasic.RelatedKeywords');
        if (ctype == 'H' || ctype == 'I') {
            $('#search_detail_inbox').show();   // 걍 보여주기로.
            $('.center1, .right1').hide();
        }
        else {
            if (ctype == 'R' || ctype == 'E' || ctype == 'B')
                $('.center1, .right1').hide();

            $('#search_detail_inbox').show();
        }
    },
    RelatedKeywords: function (json) {
        var h = '';
        if (json['result']) {
            for (var i = 0; i < json['result'].length; i++) {
                h += '<a href="javascript:SearchBasic.GoSearch({query:\'' + json['result'][i]['keyword'] + '\'});">' + json['result'][i]['keyword'] + '</a>';
            }
        }
        if (h) {
            $('.HdivbbbLayer2').find('.word_area2').html(h);
            $('.HdivbbbLayer2').show();
        }
    },
    MoveSuggestKeyword: function (e, ul) {
        if (Search.OffSuggest)
            return;
        var keyword = $('#keyword').val();
        if (keyword) {
            if (ul) {
                var cr = Search.CurrentSuggest;
                if (cr)
                    cr.find('li').removeClass('keyWord'); // css('background-color', '');
                ul.find('li').addClass('keyWord'); // css('background-color', '#ddddff');
                Search.CurrentSuggest = ul;
                //$('#keyword').val(Search.CurrentSuggest.find('li a').text());
            }
            // 위/아래 방향키 처리
            else if (e && (e.keyCode == 38 || e.keyCode == 40)) {
                var cr = Search.CurrentSuggest;
                var next = '';
                if (e.keyCode == 38) {
                    next = cr ? cr.prev() : $('#suggest .words ul').eq(0);
                }
                else if (e.keyCode == 40) {
                    next = cr ? cr.next() : $('#suggest .words ul').eq(0);
                }
                if (next && next.size() > 0) {
                    if (cr)
                        cr.find('li').removeClass('keyWord'); // css('background-color', '');
                    next.find('li').addClass('keyWord'); // css('background-color', '#ddddff');
                    Search.CurrentSuggest = next.eq(0);
                    $('#keyword').val(Search.CurrentSuggest.find('li a').text());
                }
                e.preventDefault();
            }

        }
    },
    // 자동완성 검색어 처리
    SetSuggestKeywords: function (e, down) {
        var keyword = $('#keyword').val();
        keyword = keyword.replace(/\\/g, '');
        if (keyword) {
            Search.LoadSuggestKeywords(keyword, 'SearchBasic.Suggest');
        }
        else {
            Search.CurrentSuggest = undefined;
            $('#suggest .words').html('');
            $('#suggest').hide();
        }
    },
    Suggest: function (json) {
        if (json['result'] && json['result'].length > 0) {
            var h = '';
            var query = '^(' + json['query'].replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/^\s*|\s*$/g, '').replace(/\s+/g, '\\s*') + ')';
            var reg = new RegExp(query, 'i');
            for (var i = 0; i < json['result'].length; i++) {
                h += '<ul class="_resultBox">\r\n';
                //h += '  <li><a href="javascript:SearchBasic.GoSearch({reset:true, query:\'' + json['result'][i]['keyword'] + '\'});" title="">' + json['result'][i]['keyword'].replace(json['query'], '<font style="color:#ff0000;">' + json['query'] + '</font>') + '</a></li>\r\n';
                h += '  <li><a href="javascript:SearchBasic.GoSearch({reset:true, query:\'' + json['result'][i]['keyword'] + '\'});" title="">' + json['result'][i]['keyword'].replace(reg, '<span class="ac_kwd">$1</span>') + '</a></li>\r\n';
                h += '</ul>\r\n';
            }
            $('#suggest .words').html(h).find('._resultBox').hover(function () { SearchBasic.MoveSuggestKeyword(null, $(this)); });
            $('#suggest').show();
        }
        else {
            $('#suggest .words').html('');
            $('#suggest').hide();
        }
    },

    // QueryString에 있는 값들
    GetOptions: function () {

        var o = Search.LoadOptions();   // QueryString 값 로딩. Search.Options 에도 저장됨.
        var p = Search.Query;
        o['page_size'] = p['ctype'] ? SearchBasic.GetCount(p['ctype']) : undefined;
        return o;
    },
    // 설정된 조건으로 검색
    GoSearch: function (options, popup, tag) {
        if(!SearchBasic.SetParameters(options)) {
        	alert(SEARCH_NULL);
        	return;
        }

        var p = Search.Options;
        var param = '';
        var fullUrl = window.location.href;
        var urlPath = window.location.pathname;
        var pathName = "";

        if(urlPath.indexOf("/gate/big5/") > -1) {
        	pathName = urlPath.split("/gate/big5/")[1];
        	pathName = pathName.split("/search/index")[0];
        }

        for (var n in p) {
            if (!p[n] || (n != 'query' && p[n] == '*'))
                continue;
            if (n == 'page_no' && p[n] == 1)
                continue;
            if (n == 'sort' && p[n] == 'date')
                continue;
            p[n] = (typeof (p[n]) == 'string') ? p[n].replace(/^\s*|\s*$/g, '') : p[n];
            if (!p[n])
                continue;
            if (param)
                param += '&';
            param += (n + '=' + encodeURIComponent(p[n]));
        }

        if(location.pathname.indexOf("/search/index") > -1) {
        	if(typeof popup !== 'undefined'){
                tag.attr("href", "index?"+param).attr("target", "_blank");
            } else {
                document.location.href = '?' + param;
            }
        } else {
            if(search_domain == "m-" + langType + ".yna.co.kr" || pathName.match("m-cn")) {
            	console.log(search_domain);
            	if(search_domain === "cb.yna.co.kr") {
            		location.href = "//" + search_domain + "/gate/big5/m-cn.yna.co.kr/search/index?" + param;
           	 	} else {
           	 		location.href = '//' + window.location.host + '/search/index?' + param;
           	 	}
            }
        }
    },
    SetOptions: function (o) {
        if (!o)
            o = {};
        else if (typeof (o) == 'number')
            o = { 'page_no': Number(o) }

        var keyword = $('#keyword').val();

        o['query'] = o['query'] ? o['query'] : keyword;
        // reset 이 있으면 아무 조건 없은 기본 조건으로 검색
        if (o['reset']) {
            o['reset'] = undefined;
            return o;
        }

        o['sort'] = $('input[name=sort]:checked').val();
        o['url'] = Search.Query['url'];
        if (!o['ctype'])
            o['ctype'] = Search.Query['ctype'];
        if (!o['lang'])
            o['lang'] = Search.Query['lang'];
        if (!o['page_no'])
            o['page_no'] = Search.Query['page_no'];
        o['scope'] = Search.Query['ctype'] == 'H' ? Search.Query['scope'] : $('input[name=scope]:checked').val();
        o['period'] = $('input[name=period]:checked').val();
        // 전체 검색일때는 넣지 않음.
        if (o['period'] != 'all') {
            if (!o['from'])
                o['from'] = $('input[name=from]').val() ? $('input[name=from]').val() : Search.Query['from'];
            if (!o['to'])
                o['to'] = $('input[name=to]').val() ? $('input[name=to]').val() : Search.Query['to'];
        }
        if ($('#writer').size() > 0)
            o['writer'] = $('#writer').val();
        var list = $('input[name=div_code]:checked');

        // 전체 항목을 선택했을 경우 아무것도 선택하지 않은 것으로 처리
        if (list.size() > 0 && $('input[name=div_code]').not(':checked').size() > 0) {
            var div = '';
            for (var i = 0; i < list.size(); i++) {
                div += list.eq(i).val() + ' ';
            }
            if (div)
                o['div_code'] = div;
        }
        return o;
    },
    SetParameters: function (o) {
        if (!o)
            o = {};
        else if (typeof (o) == 'number')
            o = { 'page_no': Number(o) };

        Search.Reset();

        // keyword2 - 국문 pc, search-keyword2 - 다국어 모바일, txt-sch-keyword02 - 다국어 pc
        var keyword = '';
        var fullParam = ""; //MEPS-14032
        var urlPath = window.location.pathname;
        var pathName = "";
        var period = "";

        if(urlPath.indexOf("/gate/big5/") > -1) {
        	pathName = urlPath.split("/gate/big5/")[1];
        	pathName = pathName.split("/search/index")[0];
        }

        if(window.location.href.indexOf("m-" + langType) > -1 || pathName.match("m-cn")) {
            keyword = $('#txt-sch-keyword02, #keyword, .search-keyword2').val(); // 다국어 모바일 일 때만 따로 처리
        } else {
            keyword = $('#txt-sch-keyword02, #keyword2').val(); // 국문, 다국어 pc 일 때 처리
        }

        // reset 인 경우는 통합검색으로 감.
        if (o['reset']) {
            //Search.SetKeyword(o['query'] ? o['query'] : $('#keyword').val());
        	o['query'] = o['query'] !== undefined ? o['query'] : keyword;

        	if(o['query'] == "") return false;
        	Search.SetLanguage(o['lang']);
            Search.SetKeyword(o['query']);
            return true;
        }

        if(keyword == "") return false;

        // 옵션내 키워드로 재설정(하이브리드 앱 때문에 분기 처리)
        if(/YonhapnewsApp/ig.test(navigator.userAgent)) {
        	fullParam = new URLSearchParams(window.location.search);

            Search.SetKeyword(fullParam.get("query"));
            Search.SetCtype(Search.Query['ctype']);
            Search.SetLanguage(Search.Query['lang']);
            Search.SetOrder(fullParam.get("sort"));
            Search.Set('url', Search.Query['url']);
            Search.SetScope(fullParam.get("scope"));

            period = fullParam.get("period");
        } else {
            Search.SetKeyword(keyword);
            Search.SetCtype(Search.Query['ctype']);
            Search.SetLanguage(Search.Query['lang']);
            Search.SetOrder($('input[name=sort]:checked').val());
            Search.Set('url', Search.Query['url']);
            Search.SetScope(Search.Query['ctype'] == 'H' ? Search.Query['scope'] : $('input[name=scope]:checked').val());

            period = $('input[name=period]:checked').val();
        }

        // 전체 검색일때는 넣지 않음.
        if (period != 'all') {
            if(/YonhapnewsApp/ig.test(navigator.userAgent)) {
                Search.SetFromTo(fullParam.get("from"), fullParam.get("to"));
                Search.Set('period', fullParam.get("period"));
            } else {
                // Search.SetFromTo($('input[name=from]').val() ? $('input[name=from]').val() : Search.Query['from'],
                // $('input[name=to]').val() ? $('input[name=to]').val() : Search.Query['to']);
                Search.SetFromTo($('input[name=from]').val(), $('input[name=to]').val());
                Search.Set('period', period);
            }
        }
        else {
            Search.SetFromTo('', '');
        }
        Search.SetWriter($('#writer').val());

        var list = $('input[name=div_code]:checked');

        // 전체 항목을 선택했을 경우 아무것도 선택하지 않은 것으로 처리
        if (list.size() > 0 && $('input[name=div_code]').not(':checked').size() > 0) {
            for (var i = 0; i < list.size(); i++) {
                Search.AddDivCode(list.eq(i).val());
            }
        }
        for (var n in o) {
            Search.Set(n, o[n]);
        }
        return true;
    },
    // 화면에 설정된 값을 파라미터로 만들기
    GetParameters: function (o) {
        if (!o)
            o = {};
        else if (typeof (o) == 'number')
            o = { 'page_no': Number(o) }

        var keyword = $('#keyword').val();

        o['query'] = o['query'] ? o['query'] : keyword;
        // reset 이 있으면 아무 조건 없은 기본 조건으로 검색
        if (o['reset']) {
            o['reset'] = undefined;
            return o;
        }

        o['sort'] = $('input[name=sort]:checked').val();
        o['url'] = Search.Query['url'];
        if (!o['ctype'])
            o['ctype'] = Search.Query['ctype'];
        if (!o['lang'])
            o['lang'] = Search.Query['lang'];
        if (!o['page_no'])
            o['page_no'] = Search.Query['page_no'];
        o['scope'] = Search.Query['ctype'] == 'H' ? Search.Query['scope'] : $('input[name=scope]:checked').val();
        o['period'] = $('input[name=period]:checked').val();
        // 전체 검색일때는 넣지 않음.
        if (o['period'] != 'all') {
            if (!o['from'])
                o['from'] = $('input[name=from]').val() ? $('input[name=from]').val() : Search.Query['from'];
            if (!o['to'])
                o['to'] = $('input[name=to]').val() ? $('input[name=to]').val() : Search.Query['to'];
        }
        if ($('#writer').size() > 0)
            o['writer'] = $('#writer').val();
        var list = $('input[name=div_code]:checked');

        // 전체 항목을 선택했을 경우 아무것도 선택하지 않은 것으로 처리
        if (list.size() > 0 && $('input[name=div_code]').not(':checked').size() > 0) {
            var div = '';
            for (var i = 0; i < list.size(); i++) {
                div += list.eq(i).val() + ' ';
            }
            if (div)
                o['div_code'] = div;
        }
        return o;
    },
    Search: function (options) {
        var lo = {};
        if (!options)
            options = Search.LoadOptions();
        $('#HdivLoad').show();
        Search.Search(options);
    },
    MakeHTML: function (json, col) {
        var search_domain = window.location.host;
        var fullUrl = window.location.href;
        var urlPath = window.location.pathname;
        var pathName = "";

        // dev와 qa에서 동작을 위한 처리 추가
        if(search_domain.match("qa-")) {
            search_domain = search_domain.replace("qa-", "");
        } else if(search_domain.match("dev-")) {
            search_domain = search_domain.replace("dev-");
        }

        if(urlPath.indexOf("/gate/big5/") > -1) {
        	pathName = urlPath.split("/gate/big5/")[1];
        	pathName = pathName.split("/search/index")[0];
        }

        $('#HdivLoad').hide();
        //모바일 페이지에서만 실행

        if(search_domain == "m-" + langType + ".yna.co.kr" || pathName.match("m-cn")) {
            SearchBasic.MobileTab(json);
            SearchBasic.MobileUrl(json);
            SearchBasic.Mobilemore(json);
        }
        // MEPS-18598
        if (json['ctype'] == 'C')
        	json['ctype'] = 'H';

        SearchBasic.MakeArticle(json, pathName);
        SearchBasic.MakePhoto(json, pathName);
        if(!search_domain.match("m-en")) SearchBasic.MakeMpic(json, pathName);
        else $(".enVideo").hide();
        SearchBasic.MakeGraphic(json, pathName);
        SearchBasic.MakePeople(json);
        SearchBasic.MakeIssue(json);
        SearchBasic.MakePress(json);
        SearchBasic.MakeEfestival(json);
        SearchBasic.MakeBlog(json);
        SearchBasic.Makehref(json);
        SearchBasic.SetAllTotal(json, pathName);

        if(search_domain == "m-" + langType + ".yna.co.kr") {
            layerOpen($('.btn-share'), $('#sharePop'));
        }

        if(window.location.href.match("sort=weight")) {
            $(".search-option2").find("#order02").attr("checked", "checked"); // 모바일
            $(".search-result").find("#order02").attr("checked", "checked");
            $("label[for=order02]").addClass("on"); // pc
        } else {
            $(".search-option2").find("#order01").attr("checked", "checked"); // 모바일
            $(".search-result").find("#order01").attr("checked", "checked"); // pc
            $("label[for=order01]").addClass("on");
        }
    },
    GetURL: function (cid, keyword) {
        if (/^AKR.*/.test(cid) || /^XKR.*/.test(cid)) {
            return '/view/' + cid  + '?section=search';
        }
        else if (/^A.*/.test(cid)) {
            return '/view/' + cid;
        }
        else if (/^P.*/.test(cid)) {
            return '/view/' + cid;
        }
        else if (/^G.*/.test(cid)) {
            return '/view/' + cid;
        }
        else if (/^M.*/.test(cid)) {
        	// /popup/video?cid=" + cid // 팝업 url 형식
            return '/view/' + cid;

        }
        else if (/^I.*/.test(cid)) {
            return '/view/' + cid + "?section=search";
        }
        else if (/^C.*/.test(cid)) {
            return "https://www.helloarchive.co.kr/person/preview/" + cid + '?from=search';
        }
        return '';
    },
    GetSokbo: function (cid) {
        var url = '';
        if(SearchBasic.Language == 'kr'){
            url = 'http://www.yonhapnews.co.kr/bulletin/' + cid.substring(3, 7) + '/' + cid.substring(7, 9) + '/' + cid.substring(9, 11) + '/0200000000' + cid + '.HTML?from=search';
        }else{
            url = '#none';
        }
        return
    },
    Show: function (cid, keyword) {
        var url = FULL_URL + SearchBasic.GetURL(cid, keyword);
        if (/^M.*/.test(cid)) {
            var m_width = 782;
            var m_height = 803;
            window.open(url, 'ContentsPopup', 'width=' + m_width + ', height=' + m_height + ' ,scrollbars=no, resizable=no');
        }
        else if (/C.*/.test(cid)) {
            var url = "https://www.helloarchive.co.kr/person/preview/" + cid + '?from=search';
            window.open(url, 'Buy', 'width=1350,height=850,resizeble=no, scrollbars=yes, toolbar=no, status=no, menubar=no');
        }
        else {
            document.location.href = url;
        }
    },
    SetTotal: function (id, total) {
        var search_domain = window.location.host;
        var str_total = '';

        if(SearchBasic.Language.toLowerCase() != "kr"){
            str_total = '(' + total + ')';
        } else {
            str_total = '[ 총 ' + total + '건 ]';
        }

        $(id).find('span.cnt').html(str_total);
        $(id).find('span.total').html(str_total);

        $(".search-result").find('span.total').html(str_total);

    },
    SetAllTotal: function (json, pathName) {
        var search_domain = window.location.host;
        var langCtype = json['ctype'];
        var totalObj = "";

        // dev와 qa에서 동작을 위한 처리 추가
        if(search_domain.match("qa-")) {
            search_domain = search_domain.replace("qa-", "");
        } else if(search_domain.match("dev-")) {
            search_domain = search_domain.replace("dev-");
        }

        if( json['ctype'] == langCtype){
            if (search_domain == "m-" + langType + ".yna.co.kr" || pathName.match("m-cn")) {
                totalObj = $('.title04 .cnt');
            }else {
                totalObj = $('.tit .total');
            }
            var totalNumber = 0;
            $.each(totalObj, function(){
                var item = $(this);
                var string = item.text();
                SearchBasic.Mobilemore(string);
                if(string === "()") return;
                var parse = string.split('(')[1];
                totalNumber = (totalNumber+parseInt(parse.split(')')[0]));
            });

            if (search_domain == "m-" + langType + ".yna.co.kr" || pathName.match("m-cn")) {
                if(langType === "en")
                    $(".search-result").html("Search Results " + "(" + totalNumber + ")");
                else if(langType === "cn")
                    $(".search-result").html("搜索结果 " + "(" + totalNumber + ")");
                else if(langType === "ck")
                    $(".search-result").html("搜索结果 " + "(" + totalNumber + ")");
                else if(langType === "jp")
                    $(".search-result").html("検索結果 " + "(" + totalNumber + ")");
                else if(langType === "ar")
                    $(".search-result").html("نتيجة البحث " + "(" + totalNumber + ")");
                else if(langType === "sp")
                    $(".search-result").html("Resultados de búsqueda " + "(" + totalNumber + ")");
                else if(langType === "fr")
                    $(".search-result").html("Résultat de la recherche " + "(" + totalNumber + ")");
            }else{
                $(".search-result").find('span.total').html("(" + totalNumber + ")");
            }
        }
    },
    _show: function (ele) {
        ele.css('opacity', 0).show().animate({ opacity: 1 }, 300);
    },

    //모바일 탭 이동 제어
    MobileTab : function (json){
        var navList = $(".tab-inner ul li a");
        navList.click(function (e) {
            e.preventDefault();
            return false;
        });
    },
    MobileUrl : function (json) {
        var search_domain = window.location.host; //현재주소
        var search_url = "/search/index?query=";
        var langCtype = json['ctype'];
        var langCtype02 = "";
        //검색어를 입력창에 고정
        $(".search-keyword2").val(Search.Query.query);

        // 전체보기일 때 상세검색 가리기
        if(langType === "en")
            langCtype02 = "A,P,G";
        else
            langCtype02 = "A,P,M";

        // A,P,G,M,I,C,R
        // json['ctype'] == langCtype02
        if(json['ctype'].length > 1){
            $(".btn-zone02").hide();
        }

        var naviList = $(".tab-type02 ul li button");

        //탭 클릭 시 이동 링크(인수인계자 확인 이런 형식으로 url이 붙어야함 사용하지는 않음 확인만)
        var page_no = 1;
        var all = "//" + search_domain + search_url + Search.Query.query + "&lang=" + LANG_TYPE.toUpperCase();
        var article = "//" + search_domain + search_url + Search.Query.query + "&ctype=A" + "&lang=" + LANG_TYPE.toUpperCase();
        var photo = "//" + search_domain + search_url + Search.Query.query + "&ctype=P" + "&lang=" + LANG_TYPE.toUpperCase();
        var graphic = "//" + search_domain + search_url + Search.Query.query + "&ctype=G" + "&lang=" + LANG_TYPE.toUpperCase();
        var video = "//" + search_domain + search_url + Search.Query.query + "&ctype=M" + "&lang=" + LANG_TYPE.toUpperCase();

        //-------------------------------------------------------------------------------------

        //탭 링크 이동
        naviList.eq(0).click(function () {
           SearchBasic.GoSearch({
               ctype: SearchBasic.GetCtype($(this).attr('id')),
               page_no: 1,
               query: Search.Query.query
           })
        });

        if(json['ctype'] == langCtype){
            $(".tab-inner ul li").removeClass('on');
            $(".tab-inner ul li").eq(0).addClass('on');
        }

        naviList.eq(1).click(function () {
            console.log(Search.Query.query);
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'A'
            });
        });
        $(".news-list-zone .btn").click(function () {
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'A'
            });
        });

        naviList.eq(2).click(function () {
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'P'
            });
        });
        $(".image-photo-zone .btn").click(function () {
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'P'
            });
        });

     // 하이브리드 앱에서 검색 시 그래픽 탭을 클릭하면 영상 탭으로 클릭이 되는 현상을 수정하기 위해 클릭한 탭만 클릭이 되도록 바꿈
        naviList.eq(3).click(function () {
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'G'
            });
        });

        $(".graphic-photo-zone .btn").click(function () {
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'G'
            });
        });

        naviList.eq(4).click(function () {
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'M'
            });
        });

        $(".video-list-zone .btn").click(function () {
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'M'
            });
        });

        //영문을 제외한 다국어에 그래픽의 데이터가 들어올 시 if문 삭제필요함
        /*naviList.eq(3).click(function () {
            if(LANG_TYPE == 'en'){
                SearchBasic.GoSearch({
                    page_no: 1,
                    query: Search.Query.query,
                    ctype: 'G'
                })
            } else {
                SearchBasic.GoSearch({
                 page_no: 1,
                 query: Search.Query.query,
                 ctype: 'M'
                 })
            }
         });

         $(".graphic-photo-zone .btn").click(function () {
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'G'
            });
         });

         if(LANG_TYPE == 'en') {
            naviList.eq(4).click(function () {
                SearchBasic.GoSearch({
                    page_no: 1,
                    query: Search.Query.query,
                    ctype: 'M'
                });
            });
         }

         $(".video-list-zone .btn").click(function () {
            SearchBasic.GoSearch({
                page_no: 1,
                query: Search.Query.query,
                ctype: 'M'
             });
         })*/
    },
    MakeArticle: function (json, pathName) {
        // 국문 pc 기사 all & 기사 탭 동적 리스트 생성
        var search_domain = window.location.host;
        var article_type = LANG_TYPE;
        if (article_type == "cn"){
            article_type = "ck";
        }
        var jsonLangType = article_type.toUpperCase() + "_ARTICLE";
        if (json['KR_ARTICLE'] || json['KQ_ARTICLE']) {
            var data = json['KR_ARTICLE'] || json['KQ_ARTICLE'];
            SearchBasic.SetTotal('#article_list', data['totalCount']);
            if (json['ctype'] != 'A') {
                if (data['totalCount'] > SearchBasic.GetCountMain('A')) {
                   /* $('#article_list .search_more').click(function () {
                        SearchBasic.GoSearch({ ctype: 'A', page_no: 1 });
                    }).show();*/

                    $("#article_list .search_more").show();
                    $('#article_list .search_more a').attr("href","javascript:SearchBasic.GoSearch({ctype: 'A', page_no: 1})");
                }
                else {
                    $('#article_list .search_more').hide();
                }
            }
            else {
                $('#article_list .search_more').hide();
                var paging = $(SearchBasic.MakePaging(data, 10));
                $('#article_list').next().html(paging).show();
            }

            var html = '<ul>';
            var list = data['result'];
            var cnt = json['ctype'] == 'A' ? list.length : SearchBasic.GetCountMain('A');

            for (var i = 0; i < list.length && i < cnt; i++) {
                html += '<li>\r\n';
                //html += '   <a href="javascript:SearchBasic.Show(\'' + list[i]['CONTENTS_ID'] + '\', \'' + data['query'] + '\');" class="' + (i % 2 == 0 ? 'acbx' : 'acbxbg') + '">\r\n';
                html += '   <a href="' + '//' + search_domain + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '">';
                html += '   <span class="tt2">' + list[i]['TITLE'] + '</span>\r\n';
                html += '   <span class="fl" style="display: block;">\r\n';
    			//MEPS-15414
                if (list[i]['INNER_FILE_INFO'] && /.+[.](jpe?g|png|bmp|gif)$/i.test(list[i]['INNER_FILE_INFO']) ) {
                    html += '    <img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['INNER_FILE_INFO']) + '"/>\r\n';
                }
                html += '       <span class="cts">' + list[i]['TEXT_BODY'] + '</span>\r\n';
                html += '       <span class="pbdt">' + Search.DateFormat('yyyy-MM-dd HH:mm', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>\r\n';
                html += '   </span>\r\n';
                html += '   </a>\r\n';
                html += '</li>\r\n';
            }
            html += '</ul>';
            $('#article_list .cts_atclst').html(html);
            SearchBasic._show($('#article_list'));
        }else if(json[jsonLangType]){
            // 다국어 모바일 기사 탭 동적 리스트 생성
            var jsonType = '', data = '';
            data = json[jsonLangType];
            if (article_type == "ck"){
                article_type = "cn";
            }

            // dev와 qa에서 동작을 위한 처리 추가
            if(search_domain.match("qa-")) {
                search_domain = search_domain.replace("qa-", "");
            } else if(search_domain.match("dev-")) {
                search_domain = search_domain.replace("dev-");
            }

            //모바일 아티클 목록 리스트 생성
            if(search_domain == "m-" + article_type + ".yna.co.kr" || pathName.match("m-cn")){
                var langCtype = json['ctype'];

                if(json['ctype'] == 'A'){
                    var tabInner = $(".tab-inner ul li");
                    tabInner.removeClass("on");
                    tabInner.eq(1).addClass("on");
                    //선택한 탭 보이기( 모든 탭 동일)
                    $(".news-list-zone").show();
                    function article(){
                         $(".list-padd, .news-list-zone .btn").remove();
                        var list = data['result'];
                        $(".articlelist-zone-more .title04 .cnt, .search-result").html("(" + data['totalCount'] + ")");

                        if(langType === "en")
                            $(".search-result").html("Search Results " + "("  + data['totalCount'] + ")");
                        else if(langType === "cn")
                            $(".search-result").html("搜索结果" + "(" + data['totalCount'] + ")");
                        else if(langType === "jp")
                            $(".search-result").html("検索結果 " + "(" + data['totalCount'] + ")");
                        else if(langType === "ar")
                            $(".search-result").html("نتيجة البحث " + "(" + data['totalCount'] + ")");
                        else if(langType === "sp")
                            $(".search-result").html("Resultados de búsqueda " + "(" + data['totalCount'] + ")");
                        else if(langType === "fr")
                            $(".search-result").html("Résultat de la recherche " + "(" + data['totalCount'] + ")");

                        var cnt = json['ctype'] == 'A' ? list.length : SearchBasic.GetCountMain('A');
                        var html = "";
                        for (var i = 0; i < list.length && i < cnt; i++) {
                            html += '<li>\r\n';
                            html += '   <article>\r\n';
                            html += '       <div class="txt-con">\r\n';
                            //html += '           <span class="tag"><a href="#">#</a></span>\r\n';
                            html += '           <h2 class="tit"><a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a></h2>\r\n';
                            html += '           <span class="date datefm-' + SearchBasic.Language + '01">' + SearchBasic.MakeDate('A', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>\r\n';
                            html += '           <div class="btn-con">\r\n';
                            html += '               <button class="btn-share"><span> + "Share" + </span></button>\r\n';
                            html += '           </div>\r\n';
                            html += '       </div>\r\n';
                            html += '   </article>\r\n';
                            html += '</li>\r\n';
                        }
                        $(".news-list-zone .list-article ul").append(html);
                        if(data['totalCount'] < 16){
                            $('.btn-more').hide();
                        }
                    }
                    article();
                }else if(json['ctype'] == langCtype){
                    // 다국어 모바일 all 탭 기사 동적 리스트 생성
                    $(".list-padd").remove();
                    var list = data['result'];
                    $(".news-list-zone .title04 .cnt").html("(" + data['totalCount'] + ")");
                    var cnt = json['ctype'] == 'A' ? list.length : SearchBasic.GetCountMain('A');
                    var html = "";
                    for (var i = 0; i < list.length && i < cnt; i++) {
                        html += '<li>\r\n';
                        html += '   <article>\r\n';
                        html += '       <div class="txt-con">\r\n';
                        //html += '           <span class="tag"><a href="#">#</a></span>\r\n';
                        html += '           <h2 class="tit"><a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a></h2>\r\n';
                        html += '           <span class="date datefm-' + SearchBasic.Language + '01">' + SearchBasic.MakeDate('A', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>\r\n';
                        html += '           <div class="btn-con">\r\n';
                        html += '               <button class="btn-share"><span> + "Share" + </span></button>\r\n';
                        html += '           </div>\r\n';
                        html += '       </div>\r\n';
                        html += '   </article>\r\n';
                        html += '</li>\r\n';
                    }
                    $(".news-list-zone .list-article ul").html(html);
                    $(".news-list-zone").show();
                }
            }else {
                // 다국어 pc all & 기사 탭 동적 리스트 생성
                SearchBasic.SetTotal('#tabArticle', data['totalCount']);
                if (json['ctype'] != 'A') {
                    if (data['totalCount'] > SearchBasic.GetCountMain('A')) {
                    	if (data['totalCount'] > SearchBasic.GetCountMain('A')) {
                            // 자동으로 클릭하게 해서 href에 링크 새롭게 갱신
                            $('#tabArticle .btn-more a').trigger("click");
                            $('#tabArticle .btn-more a').click(function () {
                                SearchBasic.GoSearch({ctype: 'A', page_no: 1}, true, $(this));
                            });

                            // $("#tabArticle .btn-more a").attr("href","javascript:SearchBasic.GoSearch({ctype: 'A', page_no: 1},true, 'tabArticle')");
                        }
                    }
                    else {
                        $('#tabArticle .btn-more').hide();
                    }
                }

                else {
                    $('#tabArticle .btn-more').hide();
                    if($(".paging").length == 0) {
	                    var paging = $(SearchBasic.MakePaging(data, 10));
	                    var pagingDom = $('<div class="paging"></div>');
	                    pagingDom.html(paging);
	                    $('#tabArticle').after(pagingDom.show());
	                }
                }

                var html = '<ul>';
                var list = data['result'];
                    var cnt = json['ctype'] == 'A' ? list.length : SearchBasic.GetCountMain('A');
                    for (var i = 0; i < list.length && i < cnt; i++) {
                    	var thumb = list[i]['INNER_FILE_INFO'];
                        html += '<li>\r\n';
                        html += '   <article>\r\n';
                        if (thumb != "" && thumb != null && thumb != undefined) {
                        	html += '       <figure>\r\n';
                        	html += '           <a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search"><img src="' + IMG_DOMAIN + SearchBasic.changeImage(thumb) + '" alt="' + SearchBasic.markUpReplace(list[i]['TITLE']) + '"></a>\r\n';
                            html += '       </figure>\r\n';
                        }
                        html += '       <div class="txt-con">\r\n';
                        //html += '           <span class="tag"><a href="#">#</a></span>\r\n';
                        html += '           <h2 class="tit"><a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search"  target="_blank">' + list[i]['TITLE'] + '</a></h2>\r\n';
                        html += '           <span class="lead">' + list[i]['TEXT_BODY'] + '</span>\r\n';
                        html += '           <span class="date datefm-' + SearchBasic.Language + '01">' + SearchBasic.MakeDate('A', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>\r\n';
                        html += '       </div>\r\n';
                        html += '   </article>\r\n';
                        html += '</li>\r\n';
                }
                html += '</ul>';

                if (list.length == 0) {
                    $('#tabArticle .btn-more').hide();
                    $('#tabArticle p .undefined-list-zone').show();
                }
                $('#tabArticle .smain-list-type01').html(html);
                // 검색엔진에서 이미지를 잘못 주는 경우가 있기 때문에 404 일 경우 figure 태그 remove 시킴
                $("#tabAreaAll").find("li figure img").on("error", function() {
                   $(this).parents("figure").remove();
                });
                SearchBasic._show($('#tabArticle'));
            }
        }
    },
    MakePhoto: function (json, pathName) {
        // 국문 pc 포토 all & 포토 탭 동적 리스트 생성
        var search_domain = window.location.host;
        var photo_type = LANG_TYPE;
        if (photo_type == "cn"){
            photo_type = "ck";
        }
        var jsonLangType = photo_type.toUpperCase() + "_PHOTO";
        if (json['KR_PHOTO'] || json['KQ_PHOTO'] || json['KR_PHOTO_YNA']) {
            var data = json['KR_PHOTO'] || json['KQ_PHOTO'] || json['KR_PHOTO_YNA'];
            SearchBasic.SetTotal('#photo_list', data['totalCount']);
            // 통합검색일 경우에만 표시
            if (json['ctype'] != 'P') {
                if (data['totalCount'] > SearchBasic.GetCountMain('P')) {
                    /*$('#photo_list .search_more').click(function () {
                        SearchBasic.GoSearch({ ctype: 'P', page_no: 1 });
                    }).show();*/

                    $("#photo_list .search_more").show();
                    $('#photo_list .search_more a').attr("href","javascript:SearchBasic.GoSearch({ctype: 'P', page_no: 1})");
                }
                else {
                    $('#photo_list .search_more').hide();
                }
            }
            else {
                $('#photo_list .search_more').hide();
                var paging = $(SearchBasic.MakePaging(data, 10));
                $('#photo_list').next().html(paging).show();
            }
            var html = '';
            var list = data['result'];
            var cnt = json['ctype'] == 'P' ? list.length : SearchBasic.GetCountMain('P');
            for (var i = 0; i < list.length && i < cnt; i++) {
                html += '<div class="search_pho_list_list_c">\r\n';
                html += '   <table class="list">\r\n';
                html += '       <tr>\r\n';
                html += '       <td align="center" valign="middle">\r\n';
                //html += '           <a href="javascript:SearchBasic.Show(\'' + list[i]['CONTENTS_ID'] + '\', \'' + data['query'] + '\');">';
                html += '           <a href="' + FULL_URL + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">';
                html += '               <img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH']  + '/' + list[i]['THUMBNAIL_FILE_NAME'].P2()) + '" alt="' + list[i]['TITLE'] + '" />';
                html += '           </a>\r\n';
                html += '       </td>\r\n';
                html += '       </tr>\r\n';
                html += '   </table>\r\n';
                html += '   <div class="txt">\r\n';
                //html += '       <a href="javascript:SearchBasic.Show(\'' + list[i]['CONTENTS_ID'] + '\', \'' + data['query'] + '\');">' + list[i]['TITLE'] + '</a>\r\n';
                html += '       <a href="' + FULL_URL + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a>\r\n';
                html += '       <p class="pbdt_s">' + Search.DateFormat('yyyy-MM-dd HH:mm', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</p>\r\n';
                html += '   </div>\r\n';
                html += '</div>\r\n';
            }
            $('#photo_list_2').html(html);
            SearchBasic._show($('#photo_list'));
        }else if(json[jsonLangType]) {
            // 다국어 모바일 포토 탭 동적 리스트 생성
            var jsonType = '', data = '';
            data = json[jsonLangType];
            if (photo_type == "ck"){
                photo_type = "cn";
            }

            // dev와 qa에서 동작을 위한 처리 추가
            if(search_domain.match("qa-")) {
                search_domain = search_domain.replace("qa-", "");
            } else if(search_domain.match("dev-")) {
                search_domain = search_domain.replace("dev-");
            }

            if (search_domain == "m-" + photo_type + ".yna.co.kr" || pathName.match("m-cn")) {
                var langCtype = json['ctype'];

                if (json['ctype'] == 'P') {
                    var tabInner = $(".tab-inner ul li");
                    tabInner.removeClass("on");
                    tabInner.eq(2).addClass("on");
                    $(".image-photo-zone").show();
                    $(".title04").css("border-top","0px");
                    $(".PG").addClass("photo-grid-wrap");
                    function photo() {
                        $(".image-photo-zone .first, .image-photo-zone .btn").remove();
                        var html = '<ul class="list-photo04 photo-grid">';
                        var list = data['result'];
                        $(".image-photo-zone .title04 .cnt").html("(" + data['totalCount'] + ")");

                        if(langType === "en")
                            $(".search-result").html("Search Results " + "(" + data['totalCount'] + ")");
                        else if(langType === "cn")
                            $(".search-result").html("搜索结果 " + "(" + data['totalCount'] + ")");
                        else if(langType === "jp")
                            $(".search-result").html("検索結果 " + "(" + data['totalCount'] + ")");
                        else if(langType === "ar")
                            $(".search-result").html("نتيجة البحث " + "(" + data['totalCount'] + ")");
                        else if(langType === "sp")
                            $(".search-result").html("Resultados de búsqueda " + "(" + data['totalCount'] + ")");
                        else if(langType === "fr")
                            $(".search-result").html("Résultat de la recherche " + "(" + data['totalCount'] + ")");

                        var cnt = json['ctype'] == 'P' ? list.length : SearchBasic.GetCountMain('P');
                        for (var i = 0; i < list.length && i < cnt; i++) {
                            html += '<li>\r\n';
                            html += '   <article>\r\n';
                            if (typeof(list[i]['THUMBNAIL_FILE_PATH']) != "undefined") {
                                html +=
                                    '<figure class="img-cover">' +
                                    '<a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' +
                                    '<img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH']  + '/' + list[i]['THUMBNAIL_FILE_NAME'].P2()) + '" alt="' + list[i]['TITLE'] + '">' +
                                    '</a>' +
                                    '</figure>' +
                                    '<h1 class="tit">' +
                                    '<a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a>' +
                                    '</h1>' +
                                    '<span class="date">' + SearchBasic.MakeDate('P', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>' +
                                    '<div class="btn-con">' +
                                    '<button class="btn-share" data-snslink="' + getViewURL(list[i]['CONTENTS_ID']) + '">' + '<span>' + '</span>' + '</button>' +
                                    '</div>';

                            }
                            html += '   </article>\r\n';
                            html += '</li>\r\n';
                        }
                        html += '</ul>';
                        $(".image-photo-zone .list-photo").append(html);
                        if(data['totalCount'] < 16){
                            $('.btn-more').hide();
                        }
                    }
                    photo();
                }else if(json['ctype'] == langCtype){
                    // 다국어 모바일 all 탭 포토 동적 리스트 생성
                    var html = '<ul class="list-photo04">';
                    var list = data['result'];
                    $(".image-photo-zone .title04 .cnt").html("(" + data['totalCount'] + ")");
                    var cnt = json['ctype'] == 'P' ? list.length : SearchBasic.GetCountMain('P');
                    for (var i = 0; i < list.length && i < cnt; i++) {
                        html += '<li>\r\n';
                        html += '   <article>\r\n';
                        if (typeof(list[i]['THUMBNAIL_FILE_PATH']) != "undefined") {
                            html +=    '<a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' +
                                           '<figure class="img-cover">' +
                                               '<img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + '/' + list[i]['THUMBNAIL_FILE_NAME'].P2()) + '" alt="' + list[i]['TITLE'] + '">' +
                                           '</figure>' +
                                           '<h4 class="tit">' + list[i]['TITLE'] + '<h4>'+
                                       '</a>\r\n';
                        }
                        html += '   </article>\r\n';
                        html += '</li>\r\n';
                    }
                    html += '</ul>';
                    $(".image-photo-zone .list-photo04").html(html);
                    $(".image-photo-zone").show();
                    $(".image-photo-zone .list-photo04 li").css("width","33.333%");
                }
            } else {
                // 다국어 pc all & 포토 탭 동적 리스트 생성
                SearchBasic.SetTotal('#tabPhoto', data['totalCount']);
                if (json['ctype'] != 'P') {
                	if (data['totalCount'] > SearchBasic.GetCountMain('P')) {
                        $('#tabPhoto .btn-more a').trigger("click");
                        $('#tabPhoto .btn-more a').click(function () {
                            SearchBasic.GoSearch({ctype: 'P', page_no: 1}, true, $(this));
                            //location.href= "//" + LANG_TYPE + ".yna.co.kr/search/index?query=" + $("#txt-sch-keyword02").val() + "&lang=" + LANG_TYPE;
                        });

                        // $("#tabPhoto .btn-more a").attr("href","javascript:SearchBasic.GoSearch({ctype: 'P', page_no: 1},true)");
                    }
                    else {
                        $('#tabPhoto .btn-more').hide();
                    }
                }
                else {
                    $('#tabPhoto .btn-more').hide();
                    if($(".paging").length == 0) {
	                    var paging = $(SearchBasic.MakePaging(data, 10));
	                    var pagingDom = $('<div class="paging"></div>');
	                    pagingDom.html(paging);
	                    $('#tabPhoto').after(pagingDom.show());
                    }
                }

                var html = '<ul>';
                var list = data['result'];
                var cnt = json['ctype'] == 'P' ? list.length : SearchBasic.GetCountMain('P');
                for (var i = 0; i < list.length && i < cnt; i++) {
                    html += '<li>\r\n';
                    html += '   <article class="thumb-article">\r\n';
                    if (typeof(list[i]['THUMBNAIL_FILE_PATH']) != "undefined") {
                        html += '       <figure class="img-con img-cover">\r\n';
                        html += '           <a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search"><img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH']  + '/' + list[i]['THUMBNAIL_FILE_NAME'].P2()) + '" alt="' + list[i]['TITLE'] + '"></a>\r\n';
                        html += '       </figure>\r\n';
                    }
                    html += '       <div class="txt-con">\r\n';
                    html += '           <h3 class="tit">\r\n';
                    html += '               <a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a>\r\n';
                    html += '           </h4>\r\n';
                    html += '           <span class="thumb-date">' + SearchBasic.MakeDate('P', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>\r\n';
                    html += '       </div>\r\n';
                    html += '   </article>\r\n';
                    html += '</li>\r\n';
                }
                html += '</ul>';

                //데이터 없는 경우
                if (list.length == 0) {
                    $('#tabPhoto .btn-more').hide();
                    $('#tabPhoto p .undefined-list-zone').show();
                }

                $('#tabPhoto .thumb-list').html(html);
                SearchBasic._show($('#tabPhoto'));
            }
        }

        imgCrop();
    },
    MakeMpic: function (json, pathName) {
        // 국문 pc 영상 all & 영상 탭 동적 리스트 생성
        var video_type = LANG_TYPE;
        if (video_type == "cn"){
            video_type = "ck";
        }
        var search_domain = window.location.host;
        var jsonLangType = video_type.toUpperCase() + "_MPIC";
        if (json['KR_MPIC']) {
            var data = json['KR_MPIC'];

            SearchBasic.SetTotal('#mpic_list', data['totalCount']);

            // 통합검색일 경우에만 표시
            if (json['ctype'] != 'M') {
                if (data['totalCount'] > SearchBasic.GetCountMain('M')) {
                    /*$('#mpic_list .search_more').click(function () {
                        SearchBasic.GoSearch({ ctype: 'M', page_no: 1 });
                    }).show();*/

                    $("#mpic_list .search_more").show();
                    $('#mpic_list .search_more a').attr("href","javascript:SearchBasic.GoSearch({ctype: 'M', page_no: 1})");
                }
                else {
                    $('#mpic_list .search_more').hide();
                }
            }
            else {
                $('#mpic_list .search_more').hide();
                var paging = $(SearchBasic.MakePaging(data, 10));
                $('#mpic_list').next().html(paging).show();
            }
            var html = '';
            var list = data['result'];
            var cnt = json['ctype'] == 'M' ? list.length : SearchBasic.GetCountMain('M');

            // javascript:SearchBasic.Show(\'' + list[i]['CONTENTS_ID'] + '\', \'' + data['query'] + '\'); // 기존 팝업 형태
            for (var i = 0; i < list.length && i < cnt; i++) {
                html += '<div class="search_pho_list_list_c">\r\n';
                html += '   <table class="list"><tr><td align="center" valign="middle">\r\n';
                html += '   <a href="' + FULL_URL + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">';
                html += '   <img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + '/' + list[i]['THUMBNAIL_FILE_NAME'].P2()) + '" alt="' + list[i]['TITLE'] + '" />';
                html += '   </a></td></tr></table>\r\n';
                html += '   <div class="txt">\r\n';
                html += '       <a href="' + FULL_URL + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a>\r\n';
                html += '       <p class="pbdt_s">' + Search.DateFormat('yyyy-MM-dd HH:mm', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</p>\r\n';
                html += '   </div>\r\n';
                html += '</div>\r\n';
            }
            $('#mpic_list_2').html(html);
            SearchBasic._show($('#mpic_list'));
        }else if(json[jsonLangType]) {
            // 다국어 모바일 영상 탭 동적 리스트 생성
            var jsonType = '', data = '';
            data = json[jsonLangType];
            if (video_type == "ck"){
                video_type = "cn";
            }

            // dev와 qa에서 동작을 위한 처리 추가
            if(search_domain.match("qa-")) {
                search_domain = search_domain.replace("qa-", "");
            } else if(search_domain.match("dev-")) {
                search_domain = search_domain.replace("dev-");
            }

            if (search_domain == "m-" + video_type + ".yna.co.kr" || pathName.match("m-cn")) {
                var langCtype = json['ctype'];

                if (json['ctype'] == 'M') {
                    var tabInner = $(".tab-inner ul li");
                    tabInner.removeClass("on");
                    if(LANG_TYPE !== 'en'){
                        tabInner.eq(3).addClass("on");
                    }else {
                        tabInner.eq(4).addClass("on");
                    }
                    $(".video-list-zone").show();
                    $(".title04").css("border-top","0px");

                    function video() {
                        $(".video-list-zone .list-padd, .video-list-zone .btn").remove();
                        var html = '<ul class="list-video02">';
                        var list = data['result'];
                        $(".video-list-zone .title04 .cnt").html("(" + data['totalCount'] + ")");

                        if(langType === "en")
                            $(".search-result").html("Search Results " + "(" + data['totalCount'] + ")");
                        else if(langType === "cn")
                            $(".search-result").html("搜索结果 " + "(" + data['totalCount'] + ")");
                        else if(langType === "jp")
                            $(".search-result").html("検索結果 " + "(" + data['totalCount'] + ")");
                        else if(langType === "ar")
                            $(".search-result").html("نتيجة البحث " + "(" + data['totalCount'] + ")");
                        else if(langType === "sp")
                            $(".search-result").html("Resultados de búsqueda " + "(" + data['totalCount'] + ")");
                        else if(langType === "fr")
                            $(".search-result").html("Resultat de la recherche " + "(" + data['totalCount'] + ")");

                        var cnt = json['ctype'] == 'M' ? list.length : SearchBasic.GetCountMain('M');
                        for (var i = 0; i < list.length && i < cnt; i++) {

                            var distTime = list[i]['DIST_TIME'];
                            var distTime2 = distTime.toString();
                            var runTime1 = distTime2.substr(0, 2);
                            var runTime2 = distTime2.substr(2, 4);
                            var runTime = runTime1 + " : " + runTime2;

                            html += '<li>\r\n';
                            html += '   <article>\r\n';
                            if (typeof(list[i]['THUMBNAIL_FILE_PATH']) != "undefined") {
                                html += '<a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' +
                                            '<figure class="img-cover">' +
                                                '<img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + '/' + list[i]['THUMBNAIL_FILE_NAME'].P1()) + '" alt="' + list[i]['TITLE'] + '">' +
                                                '<span class="btn-play"></span>' +
                                                '<span class="runtime">' + runTime + '</span>' +
                                            '</figure>' +
                                            '<h4 class="tit">' + list[i]['TITLE'] + '<h4>' +
                                        '</a>\r\n';
                            }
                            html += '   </article>\r\n';
                            html += '</li>\r\n';
                        }
                        html += '</ul>';
                        $(".video-list-zone .list-video").append(html);
                        if(data['totalCount'] < 16){
                            $('.btn-more').hide();
                        }
                    }
                    video();
                }else if(json['ctype'] == langCtype){
                    // 다국어 모바일 all 탭 영상 동적 리스트 생성
                    var html = '<ul class="list-video02">';
                    var list = data['result'];
                    $(".video-list-zone .title04 .cnt").html("(" + data['totalCount'] + ")");
                    var cnt = json['ctype'] == 'M' ? list.length : SearchBasic.GetCountMain('M');
                    for (var i = 0; i < list.length && i < cnt; i++) {

                        var distTime = list[i]['DIST_TIME'];
                        var distTime2 = distTime.toString();
                        var runTime1 = distTime2.substr(0,2);
                        var runTime2 = distTime2.substr(2,4);
                        var runTime = runTime1 + " : " + runTime2;

                        html += '<li>\r\n';
                        html += '   <article>\r\n';
                        if (typeof(list[i]['THUMBNAIL_FILE_PATH']) != "undefined") {
                            html += '<a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' +
                                        '<figure class="img-cover">' +
                                            '<img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + '/' + list[i]['THUMBNAIL_FILE_NAME'].P1()) + '" alt="' + list[i]['TITLE'] + '">' +
                                            '<span class="btn-play"></span>'+
                                            '<span class="runtime">' + runTime + '</span>'+
                                        '</figure>' +
                                        '<h4 class="tit">' + list[i]['TITLE'] + '<h4>'+
                                    '</a>\r\n';
                        }
                        html += '   </article>\r\n';
                        html += '</li>\r\n';
                    }
                    html += '</ul>';
                    $(".video-list-zone .list-video").html(html);
                    $(".video-list-zone").show();
                }
            } else {
                // 다국어 pc all & 영상 탭 동적 리스트 생성
                SearchBasic.SetTotal('#tabVideo', data['totalCount']);

                if (json['ctype'] != 'M') {
                	if (data['totalCount'] > SearchBasic.GetCountMain('M')) {
                        $('#tabVideo .btn-more a').trigger("click");
                        $('#tabVideo .btn-more a').click(function () {
                            SearchBasic.GoSearch({ctype: 'M', page_no: 1}, true, $(this));
                        });

                        // $("#tabVideo .btn-more a").attr("href","javascript:SearchBasic.GoSearch({ctype: 'M', page_no: 1},true)");
                    }
                    else {
                        $('#tabVideo .btn-more').hide();
                    }
                }
                else {
                    $('#tabVideo .btn-more').hide();
                    if($(".paging").length == 0) {
	                    var paging = $(SearchBasic.MakePaging(data, 10));
	                    var pagingDom = $('<div class="paging"></div>');
	                    pagingDom.html(paging);
	                    $('#tabVideo').after(pagingDom.show());
                    }
                }

                var html = '<ul>\r\n';
                var list = data['result'];
                var cnt = json['ctype'] == 'M' ? list.length : SearchBasic.GetCountMain('M');
                for (var i = 0; i < list.length && i < cnt; i++) {
                    html += '<li>\r\n';
                    html += '   <article>\r\n';
                    if (typeof(list[i]['THUMBNAIL_FILE_PATH']) != "undefined") {
                        html += '       <figure class="img-con">\r\n';
                        html += '           <a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">';
                        html += '               <img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + '/' + list[i]['THUMBNAIL_FILE_NAME'].P1()) + '" alt="' + list[i]['TITLE'] + '">\r\n';
                        html += '               <span class="runtime">00:00</span>\r\n';
                        html += '           </a>\r\n';
                        html += '       </figure>\r\n';
                    }
                    html += '           <div class="txt-con">\r\n';
                    html += '               <h4 class="tit">\r\n';
                    html += '                   <a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a>\r\n';
                    html += '               </h4>\r\n';
                    html += '               <span class="thumb-date view"><strong class="count">' + 286 + '</strong> ' + SearchBasic.MakeDate('M', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>\r\n';
                    html += '           </div>\r\n';
                    html += '   </article>\r\n';
                    html += '</li>\r\n';
                }
                html += '</ul>\r\n';

                //데이터 없는 경우
                if (list.length == 0) {
                    $('#tabVideo .btn-more').hide();
                    $('#tabVideo p .undefined-list-zone').show();
                }

                $('#tabVideo .box-video-list').html(html);
                SearchBasic._show($('#tabVideo'));


            }
        }
    },

    MakeGraphic: function (json, pathName) {
        // 국문 pc 그래픽 all & 그래픽 탭 동적 리스트 생성
        var graphic_type = LANG_TYPE;
        if (graphic_type == "cn"){
            graphic_type = "ck";
        }
        var search_domain = window.location.host;
        var jsonLangType = graphic_type.toUpperCase() + "_GRAPHIC";
        if (json['KR_GRAPHIC']) {
            var data = json['KR_GRAPHIC'];

            SearchBasic.SetTotal('#graphic_list', data['totalCount']);

            // 통합검색일 경우에만 표시
            if (json['ctype'] != 'G') {
                if (data['totalCount'] > SearchBasic.GetCountMain('G')) {
                   /* $('#graphic_list .search_more').click(function () {
                        SearchBasic.GoSearch({ctype: 'G', page_no: 1});
                    }).show();*/

                    $("#graphic_list .search_more").show();
                    $('#graphic_list .search_more a').attr("href","javascript:SearchBasic.GoSearch({ctype: 'G', page_no: 1})");
                }
                else {
                    $('#graphic_list .search_more').hide();
                }
            }
            else {
                $('#graphic_list .search_more').hide();
                var paging = $(SearchBasic.MakePaging(data, 10));
                $('#graphic_list').next().html(paging).show();
            }
            var html = '';
            var list = data['result'];
            var cnt = json['ctype'] == 'G' ? list.length : SearchBasic.GetCountMain('G');
            for (var i = 0; i < list.length && i < cnt; i++) {
                html += '<div class="search_pho_list_list_c">\r\n';
                html += '   <table class="list"><tr><td align="center" valign="middle">\r\n';
                //html += '   <a href="javascript:SearchBasic.Show(\'' + list[i]['CONTENTS_ID'] + '\', \'' + data['query'] + '\');">';
                html += '   <a href="' + FULL_URL + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">';
                html += '   <img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + '/' + list[i]['THUMBNAIL_FILE_NAME'].P2()) + '" alt="' + list[i]['TITLE'] + '" />';
                html += '   </a></td></tr></table>\r\n';
                html += '   <div class="txt">\r\n';
                //html += '       <a href="javascript:SearchBasic.Show(\'' + list[i]['CONTENTS_ID'] + '\', \'' + data['query'] + '\');">' + list[i]['TITLE'] + '</a>\r\n';
                html += '       <a href="' + FULL_URL + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a>\r\n';
                html += '       <p class="pbdt_s">' + Search.DateFormat('yyyy-MM-dd HH:mm', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</p>\r\n';
                html += '   </div>\r\n';
                html += '</div>\r\n';
            }
            $('#graphic_list_2').html(html);
            SearchBasic._show($('#graphic_list'));
        }else if(json[jsonLangType]) {
            // 다국어 모바일 그래픽 탭 동적 리스트 생성
            var jsonType = '', data = '';
            data = json[jsonLangType];
            if (graphic_type == "ck"){
                graphic_type = "cn";
            }

            // dev와 qa에서 동작을 위한 처리 추가
            if(search_domain.match("qa-")) {
                search_domain = search_domain.replace("qa-", "");
            } else if(search_domain.match("dev-")) {
                search_domain = search_domain.replace("dev-");
            }

            if (search_domain == "m-" + graphic_type + ".yna.co.kr" || pathName.match("m-cn")) {
                var langCtype = json['ctype'];

                if (json['ctype'] == 'G') {
                    var tabInner = $(".tab-inner ul li");
                    tabInner.removeClass("on");
                    tabInner.eq(3).addClass("on");
                    $(".graphic-photo-zone").show();
                    $(".title04").css("border-top","0px");
                    $(".PG").addClass("photo-grid-wrap");

                    function graphic() {
                        $(".graphic-photo-zone .first, .graphic-photo-zone .btn").remove();
                        var html = '<ul class="list-photo04 photo-grid">';
                        var list = data['result'];
                        $(".graphic-photo-zone .title04 .cnt").html("(" + data['totalCount'] + ")");

                        if(langType === "en")
                            $(".search-result").html("Search Results " + "(" + data['totalCount'] + ")");
                        else if(langType === "cn")
                            $(".search-result").html("搜索结果 " + "(" + data['totalCount'] + ")");
                        else if(langType === "jp")
                            $(".search-result").html("検索結果 " + "(" + data['totalCount'] + ")");
                        else if(langType === "ar")
                            $(".search-result").html("نتيجة البحث " + "(" + data['totalCount'] + ")");
                        else if(langType === "sp")
                            $(".search-result").html("Resultados de búsqueda " + "(" + data['totalCount'] + ")");
                        else if(langType === "fr")
                            $(".search-result").html("Résultat de la recherche " + "(" + data['totalCount'] + ")");

                        var cnt = json['ctype'] == 'G' ? list.length : SearchBasic.GetCountMain('G');
                        for (var i = 0; i < list.length && i < cnt; i++) {
                            html += '<li>\r\n';
                            html += '   <article>\r\n';
                            if (typeof(list[i]['THUMBNAIL_FILE_PATH']) != "undefined") {
                                html += '<figure class="img-cover">' +
                                            '<a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' +
                                                '<img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + '/' + list[i]['THUMBNAIL_FILE_NAME'].P2()) + '" alt="' + list[i]['TITLE'] + '">' +
                                            '</a>' +
                                        '</figure>' +
                                        '<h1 class="tit">' +
                                            '<a href="' + FULL_URL + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a>' +
                                        '</h1>' +
                                        '<span class="date">' + SearchBasic.MakeDate('G', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>' +
                                            '<div class="btn-con">' +
                                                '<button class="btn-share" data-snslink="' + getViewURL(list[i]['CONTENTS_ID']) + '">' + '<span>' + '</span>' + '</button>' +
                                            '</div>';
                            }
                            html += '   </article>\r\n';
                            html += '</li>\r\n';
                        }
                        html += '</ul>';
                        $(".graphic-photo-zone .list-graphic").append(html);
                        if(data['totalCount'] < 16){
                            $('.btn-more').hide();
                        }
                    }
                    graphic();
                }else if(json['ctype'] == langCtype){
                    // 다국어 모바일 all 탭 그래픽 동적 리스트 생성
                    var html = '<ul class="list-photo04">';
                    var list = data['result'];
                    $(".graphic-photo-zone .title04 .cnt").html("(" + data['totalCount'] + ")");
                    var cnt = json['ctype'] == 'G' ? list.length : SearchBasic.GetCountMain('G');
                    for (var i = 0; i < list.length && i < cnt; i++) {
                        html += '<li>\r\n';
                        html += '   <article>\r\n';
                        if (typeof(list[i]['THUMBNAIL_FILE_PATH']) != "undefined") {
                            html += '<a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' +
                                        '<figure class="img-cover">' +
                                            '<img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + '/'  + list[i]['THUMBNAIL_FILE_NAME'].P2()) + '" alt="' + list[i]['TITLE'] + '">' +
                                        '</figure>' +
                                        '<h4 class="tit">' + list[i]['TITLE'] + '<h4>'+
                                    '</a>\r\n';
                        }
                        html += '   </article>\r\n';
                        html += '</li>\r\n';
                    }
                    html += '</ul>';
                    $(".graphic-photo-zone .list-photo04").html(html);
                    $(".graphic-photo-zone").show();
                    $(".graphic-photo-zone .list-photo04 li").css("width","33.333%");
                }
            } else {
                // 다국어 pc all & 그래픽 탭 동적 리스트 생성
                SearchBasic.SetTotal('#tabGraphic', data['totalCount']);

                if (json['ctype'] != 'G') {
                	if (data['totalCount'] > SearchBasic.GetCountMain('G')) {
                        $('#tabGraphic .btn-more a').trigger("click");
                        $('#tabGraphic .btn-more a').click(function () {
                            SearchBasic.GoSearch({ctype: 'G', page_no: 1}, true, $(this));
                        });

                        // $("#tabGraphic .btn-more a").attr("href","javascript:SearchBasic.GoSearch({ctype: 'G', page_no: 1},true)");
                    }
                    else {
                        $('#tabGraphic .btn-more').hide();
                    }
                }
                else {
                    $('#tabGraphic .btn-more').hide();
                    if($(".paging").length == 0) {
	                    var paging = $(SearchBasic.MakePaging(data, 10));
	                    var pagingDom = $('<div class="paging"></div>');
	                    pagingDom.html(paging);
	                    $('#tabGraphic').after(pagingDom.show());
                    }
                }
                var html = '<ul>';
                var list = data['result'];
                var cnt = json['ctype'] == 'G' ? list.length : SearchBasic.GetCountMain('G');
                for (var i = 0; i < list.length && i < cnt; i++) {
                    html += '<li>\r\n';
                    html += '\  <article class="thumb-article">\r\n';
                    if (typeof(list[i]['THUMBNAIL_FILE_PATH']) != "undefined") {
                        html += '       <figure class="img-con img-cover">\r\n';
                        html += '           <a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search"><img src="' + IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + '/' + list[i]['THUMBNAIL_FILE_NAME'].P2()) + '" alt="' + list[i]['TITLE'] + '"></a>\r\n';
                        html += '       </figure>\r\n';
                    }
                    html += '       <div class="txt-con">\r\n';
                    html += '           <h4 class="tit">\r\n';
                    html += '               <a href="' + DOMAIN + SearchBasic.GetURL(list[i]['CONTENTS_ID'], data['query']) + '?section=search">' + list[i]['TITLE'] + '</a>\r\n';
                    html += '           </h4>\r\n';
                    html += '           <span class="thumb-date">' + SearchBasic.MakeDate('G', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>\r\n';
                    html += '       </div>\r\n';
                    html += '   </article>\r\n';
                    html += '</li>\r\n';
                }

                html += '</ul>';

                //데이터 없는 경우
                if (list.length == 0) {
                    $('#tabGraphic .btn-more').hide();
                    $('#tabGraphic p .undefined-list-zone').show();
                }

                $('#tabGraphic .thumb-list').html(html);
                SearchBasic._show($('#tabGraphic'));
            }
        }

        imgCrop();
    },
    MakePeople: function (json) {
        if (json['KR_PEOPLE']) {
            var data = json['KR_PEOPLE'];

            SearchBasic.SetTotal('#people_list', data['totalCount']);

            // 통합검색일 경우에만 표시
            if (json['ctype'] != 'H') {
                if (data['totalCount'] > SearchBasic.GetCountMain('H')) {
                    $('#people_list .search_more').click(function () {
                        SearchBasic.GoSearch({ ctype: 'H', page_no: 1 });
                    }).show();
                }
                else {
                    $('#people_list .search_more').hide();
                }
            }
            else {
                $('#people_list .search_more').hide();
                var paging = $(SearchBasic.MakePaging(data, 10));
                $('#people_list').next().html(paging).show();
            }
            var html = '';
            var list = data['result'];
            var cnt = json['ctype'] == 'H' ? list.length : SearchBasic.GetCountMain('H');
            var name = '';
            var img = '';
            var office = '';
            var charged = '';
            for (var i = 0; i < list.length && i < cnt; i++) {
                charged = list[i]['CHARGED_YN'];

                name = list[i]['NAME'];
                if (list[i]['CHNCHAR_NAME'])
                    name += '(' + list[i]['CHNCHAR_NAME'] + ')';
                img = !list[i]['THUMBNAIL_FILE_PATH'] || !list[i]['THUMBNAIL_FILE_NAME'] ?
                    R_DOMAIN + '/www/home_n/v01/img/20110726_peo_none.gif'
                    : IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + "/" + list[i]['THUMBNAIL_FILE_NAME'].P2());
                if (list[i]['OFFICE_NAME'])
                    office = '[現]' + SearchBasic.MakeOfficeName(list[i]['OFFICE_NAME'], list[i]['OFFICE_DEPT_NAME'], list[i]['OFFICE_POSITION']);
                else if (list[i]['EXOFFICE_NAME'])
                    office = '[前]' + SearchBasic.MakeOfficeName(list[i]['EXOFFICE_NAME'], list[i]['EXOFFICE_DEPT_NAME'], list[i]['EXOFFICE_POSITION']);
                else
                    office = '';
                html += '<div class="people_pop">\r\n';
                if (charged == 'Y')
                    html += '<dl><dt><img src="' + img + '" alt="' + name + '" onclick="SearchBasic.Show(\'' + list[i]['CONTENTS_ID'] + '\');" style="cursor:pointer;"/></dt>\r\n';
                else
                    html += '<dl><dt><img src="' + img + '" alt="' + name + '"/></dt>\r\n';
                html += '    <dd><span>' + name + '</span>';
                html += office;
                if (charged == 'Y')
                    html += '    <p><img src="//r.yna.co.kr/www/home_n/v01/img/20110721_people_ic_pay.gif" alt="유료" /></p>\r\n';
                else
                    html += '    <p><img src="//r.yna.co.kr/www/home_n/v01/img/20110721_people_ic_free.gif" alt="세부정보없음" /></p>\r\n';
                html += '   </dd>\r\n';
                html += '</dl>\r\n';
                html += '</div>\r\n';
            }
            $('#people').html(html);
            SearchBasic._show($('#people_list'));


        }
    },

    MakeOfficeName: function (name, dept, position) {
        var nameList = name.split('^');
        var deptList = dept.split('^');
        var posiList = position.split('^');
        var h = '';
        for (var i = 0; i < nameList.length && i < 1; i++) {
            if (h)
                h += ', ';
            h += nameList[i] + ' ' + deptList[i] + ' ' + posiList[i];
        }
        return h;
    },
    MakeIssue: function (json) {
        if (json['KR_ISSUE']) {
            var data = json['KR_ISSUE'];

            SearchBasic.SetTotal('#issue_list', data['totalCount']);

            // 통합검색일 경우에만 표시
            if (json['ctype'] != 'I') {
                if (data['totalCount'] > SearchBasic.GetCountMain('I')) {
                    $('#issue_list .search_more').click(function () {
                        SearchBasic.GoSearch({ ctype: 'I', page_no: 1 });
                    }).show();
                }
                else {
                    $('#issue_list .search_more').hide();
                }
            }
            else {
                $('#issue_list .search_more').hide();
                var paging = $(SearchBasic.MakePaging(data, 10));
                $('#issue_list').next().html(paging).show();
            }
            var html = '';
            var list = data['result'];
            var cnt = json['ctype'] == 'I' ? list.length : SearchBasic.GetCountMain('I');
            var img = '';
            var url = '';
            for (var i = 0; i < list.length && i < cnt; i++) {
                //url = 'http://www.yonhapnews.co.kr/section/7305010000.html?c=A&id=' + list[i]['ISSUE_ID'] + '&from=search';
                url = FULL_URL + SearchBasic.GetURL(list[i]['ISSUE_ID']);
                img = !list[i]['THUMBNAIL_FILE_PATH'] || !list[i]['THUMBNAIL_FILE_NAME'] ?
                    R_DOMAIN + '/www/home_n/v01/img/20110805_n_img.jpg'
                    : IMG_DOMAIN + SearchBasic.changeImage(list[i]['THUMBNAIL_FILE_PATH'] + "/" + list[i]['THUMBNAIL_FILE_NAME'].P2());
                html += '<div class="issue_list_box">\r\n';
                html += '   <a href="' + url + '" title="' + list[i]['ISSUE_NAME'] + '?section=search" target="_blank">\r\n';
                html += '       <img src="' + img + '" height="106" width="170" alt="' + list[i]['ISSUE_NAME'] + '" /></a>\r\n';
                html += '   <h5><a href="' + url + '" title="' + list[i]['ISSUE_NAME'] + '?section=search" target="_blank">' + list[i]['ISSUE_NAME'] + '</a></h5>\r\n';
                html += '   <p class="issue_list_con">' + list[i]['ISSUE_DESC'].replace(/^(.{50})(.+)$/, '$1...') + '</p>\r\n';
                html += '   <p class="info">' + SearchBasic.MakeDate('I', list[i]['START_DATE']) + '</p>\r\n';
                html += '</div>\r\n';
            }

            $('#issue_lists').html(html);
            SearchBasic._show($('#issue_list'));
        }
    },
    MakePress: function (json) {
        if (json['KR_PRESS']) {
            var data = json['KR_PRESS'];
            SearchBasic.SetTotal('#press_list', data['totalCount']);

            // 통합검색일 경우에만 표시
            if (json['ctype'] != 'R') {
                if (data['totalCount'] > SearchBasic.GetCountMain('R')) {
                    $('#press_list .search_more').click(function () {
                        SearchBasic.GoSearch({ ctype: 'R', page_no: 1 });
                    }).show();
                }
                else {
                    $('#press_list .search_more').hide();
                }
            }
            else {
                $('#press_list .search_more').hide();
                var paging = $(SearchBasic.MakePaging(data, 10));
                $('#press_list').next().html(paging).show();
            }
            var html = '';
            var list = data['result'];
            var cnt = json['ctype'] == 'R' ? list.length : SearchBasic.GetCountMain('R');
            var url = '';
            for (var i = 0; i < list.length && i < cnt; i++) {
                url = '//' + search_domain + '/view/' + list[i]["CONTENTS_ID"] + "?section=search";
                html += '<ul>\r\n';
                html += '   <li>\r\n';
                html += '    <a href="' + url + '" class="h4" target="_blank">' + list[i]['TITLE'] + '</a>\r\n';
                html += '       <span class="bar">|</span><span class="date">' + SearchBasic.MakeDate('R', list[i]['DIST_DATE'] + list[i]['DIST_TIME']) + '</span>\r\n';
                html += '   </li>\r\n';
                html += '</ul>\r\n';
            }

            $('#press_list_2').html(html);
            SearchBasic._show($('#press_list'));


        }
    },
    MakeEfestival: function (json) {
        if (json['KR_EFESTIVAL']) {
            var data = json['KR_EFESTIVAL'];
            SearchBasic.SetTotal('#efestival_list', data['totalCount']);

            // 통합검색일 경우에만 표시
            if (json['ctype'] != 'E') {
                if (data['totalCount'] > SearchBasic.GetCountMain('E')) {
                    $('#efestival_list .search_more').click(function () {
                        SearchBasic.GoSearch({ ctype: 'E', page_no: 1 });
                    }).show();
                }
                else {
                    $('#efestival_list .search_more').hide();
                }
            }
            else {
                $('#efestival_list .search_more').hide();
                var paging = $(SearchBasic.MakePaging(data, 10));
                $('#efestival_list').next().html(paging).show();
            }
            var html = '';
            var list = data['result'];
            var cnt = json['ctype'] == 'E' ? list.length : SearchBasic.GetCountMain('E');
            var img = '';
            for (var i = 0; i < list.length && i < cnt; i++) {
                //http://efestival.yonhapnews.co.kr/efestival/v/index.jsp?vgnextoid=f29445b4a861b310VgnVCM1000005106010aRCRD&vgnextchannel=d70857ac13e2a010VgnVCM1000005106010aRCRD
                html += '<ul>\r\n';
                html += '   <li>\r\n';
                html += '   <a href="http://efestival.yonhapnews.co.kr/efestival/v/index.jsp?vgnextoid=' + list[i]['RECORDID'].replace(/^\s*|\s*$/g, '') + '&vgnextchannel=d70857ac13e2a010VgnVCM1000005106010aRCRD&&section=search" target="_blank" class="h4">[' + list[i]['EVENT_NAME'] + ']</a>\r\n';
                html += '   <span class="bar">|</span><span class="date">' + SearchBasic.MakeDate('E', list[i]['START_DATE']) + ' ~ ' + SearchBasic.MakeDate('E', list[i]['END_DATE']) + '</span>\r\n';
                html += '   <span class="bar">|</span><span class="date">' + list[i]['EVENT_LOC'] + '</span>\r\n';
                html += '   </li>\r\n';
                html += '</ul>\r\n';
            }

            $('#efestival_list_2').html(html);
            SearchBasic._show($('#efestival_list'));
        }

    },
    MakeBlog: function (json) {
        if (json['KR_BLOG']) {
            var data = json['KR_BLOG'];
            SearchBasic.SetTotal('#blog_list', data['totalCount']);

            // 통합검색일 경우에만 표시
            if (json['ctype'] != 'B') {
                if (data['totalCount'] > SearchBasic.GetCountMain('B')) {
                    $('#blog_list .search_more').click(function () {
                        SearchBasic.GoSearch({ ctype: 'B', page_no: 1 });
                    }).show();
                }
                else {
                    $('#blog_list .search_more').hide();
                }
            }
            else {
                $('#blog_list .search_more').hide();
                var paging = $(SearchBasic.MakePaging(data, 10));
                $('#blog_list').next().html(paging).show();
            }
            var html = '';
            var list = data['result'];
            var cnt = json['ctype'] == 'B' ? list.length : SearchBasic.GetCountMain('B');
            var img = '';
            for (var i = 0; i < list.length && i < cnt; i++) {
                html += '<ul>\r\n';
                html += '   <li>\r\n';
                html += '       <a href="http://blog.yonhapnews.co.kr/' + list[i]['BLOGID'] + '/post/' + list[i]['POSTSN'] + '?section=search" target="_blank" class="h4">' + list[i]['POSTTITLE'] + '</a>\r\n';
                html += '       <span class="bar">|</span><span class="date">' + SearchBasic.MakeDate('B', list[i]['POSTREGDT']) + '</span>\r\n';
                html += '   </li>\r\n';
                html += '</ul>\r\n';
            }

            $('#blog_list_2').html(html);
            SearchBasic._show($('#blog_list'));


        }

    },

    MakeDate: function (ctype, date) {
        var change_date = '';
        var year = date.substring(0, 4);
        var month = date.substring(4, 6) - 1;
        var day = date.substring(6, 8);
        var hours = date.substring(8, 10);
        var minutes = date.substring(10, 12);
        var seconds = date.substring(12, 14);
        var today = new Date(year, month, day, hours, minutes, seconds);
        change_date =  new Date(today);

        if(day <= 9) {
            day = day.replace("0", "");
        }

        if (!date)
            return '';
        switch (ctype) {
            case 'A':
            case 'M':
                // 아이폰에서 NaN, undefined 표시가 되고 있어서 주석처리 함
                if(LANG_TYPE === "en") return change_date.Format2(hours + ':mm MMM. dd', LANG_TYPE);
                if(LANG_TYPE === "ck") return change_date.Format2('MM月dd日 HH:mm', LANG_TYPE);
                if(LANG_TYPE === "jp") return change_date.Format2('MM.dd ' + hours + ':mm', LANG_TYPE);
                if(LANG_TYPE === "ar") return change_date.Format2('MM.dd HH:mm', LANG_TYPE);
                if(LANG_TYPE === "sp") return change_date.Format2(day + ' MMM ' + hours + ':mm', LANG_TYPE).toLowerCase();
                if(LANG_TYPE === "fr") return change_date.Format2('dd.MM à HHhmm', LANG_TYPE);
            case 'I':
                return Search.DateFormat('yyyy.MM.dd', date);
            case 'R':
                return Search.DateFormat('yyyy-MM-dd HH:mm', date);
            case 'E':
                return Search.DateFormat('yyyy-MM-dd (%D)', date);
            case 'B':
                return Search.DateFormat('yyyy-MM-dd HH:mm', date);
            case 'P':
            case 'G':
                if(LANG_TYPE === "en") return change_date.Format2(hours + ':mm MMM. dd', LANG_TYPE);
                if(LANG_TYPE === "ck") return change_date.Format2('MM月dd日 HH:mm', LANG_TYPE);
                if(LANG_TYPE === "jp") return change_date.Format2('MM.dd HH:mm', LANG_TYPE);
                if(LANG_TYPE === "ar") return change_date.Format2('MM.dd HH:mm', LANG_TYPE);
                if(LANG_TYPE === "sp") return change_date.Format2(day + ' MMM ' + hours + ':mm', LANG_TYPE).toLowerCase();
                if(LANG_TYPE === "fr") return change_date.Format2('dd.MM à HHhmm', LANG_TYPE);

        }
        return '';
    },
    MakePaging: function (json, pageCount) {
            if (!pageCount)
                pageCount = 10;
            var total = Number(json['totalCount']);
            var page = Number(json['page_no']);
            var count = Number(json['page_size']);

            var h = '';
            var startPage = Math.floor((page - 1) / pageCount) * pageCount + 1;

            var lastPage = Math.ceil(total / count);
            var firstPage = 1;
            var prevPage = startPage - 1;
            if (prevPage < 1)
                prevPage = 1;
            if(SearchBasic.Language.toLowerCase() == 'kr') {
                if (total > 0) {
                    h += '<a href="" data-page="' +prevPage+ '" class="prev"><img src="http://img.yonhapnews.co.kr/basic/svc/12_images/uni_icoPre2012.gif" border="0" alt="" /></a>\r\n';
                    for (var i = startPage; i < startPage + pageCount && i <= lastPage; i++) {
                        if (i == page)
                            h += '<a href="" data-page="' + i + '" class="bbb">' + i + '</a>\r\n';
                        else
                            h += '<a href="" data-page="' + i + '">' + i + '</a>\r\n';
                    }
                    if (startPage + pageCount <= lastPage)
                        h += '<a href=""  data-page="' +(startPage + pageCount)+ '" class="next"><img src="http://img.yonhapnews.co.kr/basic/svc/12_images/uni_icoNxt2012.gif" border="0" alt=""/></a>\r\n';
                    else
                        h += '<a href="" data-page="' +lastPage+ '" class="next"><img src="http://img.yonhapnews.co.kr/basic/svc/12_images/uni_icoNxt2012.gif" border="0" alt=""/></a>\r\n';
                }
            }else{
                if (total > 0) {
                    h += '<a href="" data-page="' + firstPage + '" class="first"><span> + First + </span></a>\r\n';
                    h += '<a href="" data-page="' + (page - 1) + '" class="prev"><span> + Previous + </span></a>\r\n';
                    for (var i = startPage; i < startPage + pageCount && i <= lastPage; i++) {
                        if (i == page)
                            h += '<a href="" data-page="' + i + '" class="on">' + i + '</a>\r\n';

                        else
                            h += '<a href="" data-page="' + i + '">' + i + '</a>\r\n';
                    }
                    h += '<a href="" data-page="' + (page + 1) + '" class="next"><span> + Next + </span></a>\r\n';
                    h += '<a href="" data-page="' + lastPage + '" class="last"><span> + "Last" + </span></a>\r\n';
                }
            }
            SearchBasic.LastPage = lastPage;
            SearchBasic.Total = total;
            SearchBasic.Page = page;
            SearchBasic.Count = count;
            SearchBasic.StartPage = startPage;
            return h;
    },
    Mobilemore: function (json) {
        var langArticle = ""; // 기사 일 때
        var langPhoto = ""; // 포토 일 때
        var langMpic = ""; // 영상 일 때
        var langGraphic = ""; // 그래픽 일 때

        //모바일 더보기 설정
        if(json["ctype"] === "A") {
            langArticle = json[LANG_TYPE.toUpperCase() + "_ARTICLE"];
            Search.totalCount = langArticle["totalCount"];
        } else if(json["ctype"] === "P") {
            langPhoto = json[LANG_TYPE.toUpperCase() + "_PHOTO"];
            Search.totalCount = langPhoto["totalCount"];
        } else if(json["ctype"] === "M") {
            langMpic = json[LANG_TYPE.toUpperCase() + "_MPIC"];
            Search.totalCount = langMpic["totalCount"];
        } else if(json["ctype"] === "G") {
            langGraphic = json[LANG_TYPE.toUpperCase() + "_GRAPHIC"];
            Search.totalCount = langGraphic["totalCount"];
        }

        $(".btn-zone02 .btn-more").unbind().click(function (e) {
            if(Math.ceil(Search.totalCount / Search.Options.page_size) === Search.searchPage) {
                $(this).hide();
            }

            Search.SetPage( Search.searchPage++ );
            Search.Search();
        });

        if(Search.Options.page_size === Search.totalCount) {
            $(".btn-zone02 .btn-more").hide();
        }
    },
    Makehref: function () {
        $(".paging a, .paging_search a").click(function () {
            event.preventDefault();
            var page = parseInt($(this).attr("data-page"));

            if(page > 999) {
                page = 999;
            }

            SearchBasic.GoSearch(page);
        })
    },
    SuggestOff: function () {
        Search.OffSuggest = true;
        $('#suggest').hide();
    },

    Reset: function () {
        if(SearchBasic.Language == "kr"){
            //$('input[name=period][value=all]').click();
            $('#writer').val('');
            $('input[name=div_code]').each(function () { this.checked = false; });
            $('input[name=sort][value=date]').click();
            $('input[name=scope][value=""]').click();
        }
        $('input[name=period][value=all]').click();
        $('input[name=scope][value=""]').click();
    },
    CheckLogin: function () {
        var userId = $cookie('YNA_MEMBER_ID');
        if (userId != null) {
            $('#ankLogin').text('로그아웃').attr('href', 'https://app.yonhapnews.co.kr/yna/basic/2013_member/logout.html?template=2971');
        }
        else {
            $('#ankLogin').text('로그인').attr('href', 'https://app.yonhapnews.co.kr/yna/basic/2013_member/login.html?template=2971');
        }
    },
    EncodQuery : function () {

    },
    // 초기화
    Init: function () {
        //검색언어 설정
        SearchBasic.Language = Search.Query['lang'];
        if(SearchBasic.Language == null || SearchBasic.Language == ''){
            SearchBasic.Language = LANG_TYPE.toUpperCase();
        }
        SearchBasic.Reset();

        var opt = SearchBasic.GetOptions();

        //국문 - 다국어 구분
        if(SearchBasic.Language == "KR"){
            /*
            $('#keyword2').on('keyup', function() {
                if($(this).val().length > 20) {
                    $(this).val($(this).val().substring(0, 20));
                    alert("에러: 검색어 최대길이는 20자 입니다.");
                    return;
                }
            });
            */
            //로그인 체크
            SearchBasic.CheckLogin();
            Search.OnException = function (json) {
                $('#HdivLoad').hide();
                alert('에러:' + json['EXCEPTION']);
                return;
            };
            Search.OnNoKeyword = function () {
                $('#HdivLoad').hide();
                alert(SEARCH_NULL);
                $('#keyword').focus();
            };

            // 검색결과 노드 가리기
            $('#articleList, #photoList, #graphicList, #mpicList, #issue_list, #people_list, #press_list, #efestival_list, #blog_list, .paging_search').hide();
            // 브라우져 내장 자동완성 기능 끄기
            $('#keyword').attr('autocomplete', 'off');

            // 상세옵션내 키워드 표시
            $('#keyword2').val(Search.Options['query']);

            // 검색버튼 바인딩
            $('#searchButton').unbind().click(function () {
                SearchBasic.GoSearch({
                    query: $('#txt-sch-keyword02,#keyword').val(),
                    reset: true,
                    page_no: 1
                });
            });

            // 키워드박스 자동완성 처리
            $('#keyword').keyup(function (e) {
                if (e.keyCode == 38 || e.keyCode == 40) {
                    SearchBasic.MoveSuggestKeyword(e);
                    return;
                }
                else if (e.keyCode != 8 && e.keyCode < 40) {
                    //e.preventDefault();
                    //return;
                }
                else {
                    clearTimeout(SearchBasic.SuggestTimeout);
                    SearchBasic.SuggestTimeout = setTimeout(function () {
                        SearchBasic.SetSuggestKeywords();
                    }, 100);
                }
            });
            $('#keyword').keypress(function (e) {
                if (e.keyCode == 38 || e.keyCode == 40)
                    return;
                else if (e.keyCode != 8 && e.keyCode < 40) {
                    //e.preventDefault();
                    //return;
                }
                else {
                    clearTimeout(SearchBasic.SuggestTimeout);
                    SearchBasic.SuggestTimeout = setTimeout(function () {
                        SearchBasic.SetSuggestKeywords();
                    }, 100);
                }
            });

            // 자동완성 레이어 설정
            var suggest = $('#suggest');
            suggest.css({
                'z-index': '100',
                'background-color': '#ffffff'
            });

            // 레이어 가려지는 문제 임시조치.
            suggest.remove();
            $(document.body).append(suggest);

            /* 20150123 removed
             var keyword = $('.s_srchbar');
             suggest.css({
             'left': (keyword.offset().left + 4) + 'px',
             'top': (keyword.offset().top + keyword.height() + 4) + 'px'
             });

             // 자동완성 레이어 위치 가변처리
             $(window).resize(function () {
             var keyword = $('.s_srchbar');
             $('#suggest').css({
             'left': (keyword.offset().left + 4) + 'px',
             'top': (keyword.offset().top + keyword.height() + 4) + 'px'
             });
             });
             */

            $('#search_container').css('background', '');
            $('#search_container').css('position', '');

            // 자동완성기능 끄기
            $('#suggest .funoff').attr('href', 'javascript:SearchBasic.SuggestOff();');

            // 검색어 표시
            $('.search_navi_result').find('.point').text(Search.Query['query'] ? Search.Query['query'] : '');
            $('.search_navi_result').show();

            // 정렬방식
            if (opt['sort'])
                $('input[name=sort][value=' + opt['sort'] + ']').click();

            // 검색이동
            var list = $('.search_menu1 li');
            list.removeClass('current');
            list.find('a').removeAttr('href');

            //현재 선택 탭
            var onClass = "current";
            if(SearchBasic.Language.toLowerCase() != "kr")
                onClass = "on";
                var ctype = Search.Query['ctype'];
                // ctype 이 없으면 통합검색
                if (!ctype)
                    list.eq(0).addClass(onClass);


                for (var i = 0; i < list.size(); i++) {
                    if (ctype && SearchBasic.GetCtype(list.eq(i).attr('id')) == ctype)
                        list.eq(i).addClass(onClass);

                    list.eq(i).click(function () {
                        SearchBasic.GoSearch({
                            ctype: SearchBasic.GetCtype($(this).attr('id')),
                            page_no: 1
                        });

                    });
                }

            // 작성자
            $('#writer').keydown(function (e) {
                if (e.keyCode == 13) {
                    SearchBasic.GoSearch({
                        page_no: 1
                    });
                }
            });

            if (Search.Options['writer'])
                $('#writer').val(Search.Options['writer']);

            // 검색대상 이외의 영역을 클릭하면 가리기
            $(document.body).click(function (e) {
                if(langType !== "kr") {
                    if ($('#div_code').find($(e.srcElement)).size() == 0) $('#div_list').hide();
                } else {
                    if ($('#div_code').find($(e.target)).length == 0) $('#div_list').hide();
                }

                if ($('#suggest').find($(e.srcElement)).size() == 0 && $('.s_srchbar').find($(e.srcElement)).size() == 0) $('#suggest').hide();
            });
            $(document.body).keydown(function (e) {
                if (e.keyCode == 27) {
                    $('#div_list').hide();
                    $('#suggest').hide();
                }
            });
            $(".jqTransformSelectOpen").click(function () {
                event.preventDefault();
            });
            // 검색대상 버튼
            $('#div_code > div').click(function () {
                $('#div_list').toggle();
                return false;
            });
            // 전체선택
            $('#div_all').click(function () {
                //if ($(this).is(':checked'))
                if (this.checked)
                    $('input[name=div_code]').each(function () { this.checked = true; });
                else
                    $('input[name=div_code]').each(function () { this.checked = false; });
            });

            // 분야세팅
            if (Search.Query['div_code']) {
                var list = Search.Query['div_code'].split(/[^0-9,]+/);
                for (var i = 0; i < list.length; i++) {
                    $('input[name=div_code][value="' + list[i] + '"]').click();
                }
            }

            // 검색영역 및 정렬 바인딩
            //$('#search_detail_inbox').find('input[type=radio]').not('[name=period]').click(function () { SearchBasic.GoSearch({ 'page_no': 1 }); });

            // 상세검색 URL 바인딩
            $('.s_srch_fword dd').not('.logo').find('a').attr('href', 'http://app.yonhapnews.co.kr/YNA/Basic/article/new_search/YIBW_showSearchDetail_New.aspx');

            // 오늘날짜 표시
            $('#today').text(Search.DateFormat('yyyy.MM.dd (%D)'));
            $('.right12').text('예: ' + Search.DateFormat('yyyyMMdd'));
        }else{
            // 검색결과 노드 가리기
            //$('#articleList, #photoList, #graphicList, #mpicList, #issue_list, #people_list, #press_list, #efestival_list, #blog_list, .paging_search').hide();
            $('#tabArticle, #tabPhoto, #tabGraphic, #tabVideo').hide();

            //키워드 표시
            var search_domain = window.location.host;

            // dev와 qa에서 동작을 위한 처리 추가
            if(search_domain.match("qa-")) {
                search_domain = search_domain.replace("qa-", "");
            } else if(search_domain.match("dev-")) {
                search_domain = search_domain.replace("dev-");
            }

            var urlPath = window.location.pathname;
            var pathName = "";

            if(urlPath.indexOf("/gate/big5/") > -1) {
            	pathName = urlPath.split("/gate/big5/")[1];
            	pathName = pathName.split("/search/index")[0];
            }

            if(search_domain == "m-" + langType + ".yna.co.kr" || pathName.match("m-cn")) {
                $(".search-keyword2, .search-keyword").val(Search.Options['query']);
            }else {
                $("#txt-sch-keyword02").val(Search.Options['query']);
                $('#keyword-label').hide('');
            }

            // 검색어 표시
            $('.search-result').find('.point').text(Search.Query['query'] ? Search.Query['query'] : '');
            $('.search-result').show();

            //총 검색수 표시
            $('.search-result').find('.total').text("(00)");

            // 검색이동
            var list = $('.tab-type03 li, .page-search .tab-type02 li');
            list.removeClass('on');
            list.find('a').removeAttr('href');

            // 검색버튼 바인딩

            $('#searchButton').unbind().click(function () {
                if($("#txt-sch-keyword02").val() == "") {
                    alert(SEARCH_NULL);
                }else {
                	if($('#txt-sch-keyword02,.keyword2').val().length > 40) {
                		alert(SEARCH_LENGTH_TEXT);
                	} else {
                		SearchBasic.GoSearch({
                            query: $('#txt-sch-keyword02,.keyword2').val(),
                            reset: true,
                            page_no: 1,
                            lang : SearchBasic.Language
                        });
                	}
                }
            });
        }

        // 키워드박스 엔터기 처리
        $('#keyword,#keyword2, #txt-sch-keyword02').keydown(function (e) {
            var id = $(this).attr('id');
            if (e.keyCode == 13) {
                var opt = { page_no: 1 };
                // 상단 박스 일경우
                if (id == 'keyword')
                    opt['reset'] = true;
                else if(id === "txt-sch-keyword02") {
                    opt["lang"] = SearchBasic.Language;
                    opt["reset"] = true;
                }



                SearchBasic.GoSearch(opt);
            }
            else if (id == 'keyword') { // 상단 박스에서만 자동완성
                if (e.keyCode == 38 || e.keyCode == 40) {
                    //Search.MoveSuggestKeyword(e);
                    return;
                }
                else if (e.keyCode != 8 && e.keyCode < 45) {
                    //e.preventDefault();
                    //return;
                }
                else {
                    clearTimeout(SearchBasic.SuggestTimeout);
                    SearchBasic.SuggestTimeout = setTimeout(function () {
                        SearchBasic.SetSuggestKeywords(e);
                    }, 100);
                }
            }
        });

        // 검색영역
        if (opt['scope'])
            $('input[name=scope][value=' + opt['scope'] + ']').click();

        //현재 선택 탭
        var onClass = "current";
        if(SearchBasic.Language.toLowerCase() != "kr"){
            onClass = "on";
            var ctype = Search.Query['ctype'];
            // ctype 이 없으면 통합검색
            if (!ctype)
                list.eq(0).addClass(onClass);

            for (var i = 0; i < list.size(); i++) {
                if (ctype && SearchBasic.GetCtype(list.eq(i).attr('id')) == ctype)
                    list.eq(i).addClass(onClass);

                if(!/YonhapnewsApp/i.test(navigator.userAgent)) {
                    list.eq(i).click(function () {
                        SearchBasic.GoSearch({
                            ctype: SearchBasic.GetCtype($(this).attr('id')),
                            page_no: 1
                        });
                    });
                }
            }
        }

        // 옵션내 검색버튼(국문 pc 쪽, 확실하지는 않음)
        $('#search_click,button[name=filterSearch]').unbind().click(function () {
            SearchBasic.GoSearch({
                page_no: 1
            });
        });

        function caledarString() {
            var string = $(".calendar-inputWrap input").val();
            sessionStorage.setItem("calendarDate", string);
            var fromString = "";
            var toString = "";
            var del = /[ \{\}\[\]\/?.,;:|\)*~`!^\-_+┼<>@\#$%&\'\"\\(\=]/gi;
            string = string.replace(del, '');
            string = string.replace('to', '');
            string = string.toString();
            fromString = string.substr(0, 8);
            toString = string.substr(8, 16);
            $('input[name=from]').val(fromString);
            $('input[name=to]').val(toString);
        }

        // 커스텀 기간을 설정했을 경우 유지가 되도록
        var urlFull = window.location.href;

        if(urlFull.match("&period=diy")) {
            if(urlFull.match("m-")) {
                $(".custom-box").find(".input-box").addClass("on");
            } else {
                if(langType !== "kr") {
                    var calendarFrom = "", calendarTo = "";
                    var calendarDate = sessionStorage.getItem("calendarDate");
                    calendarDate = calendarDate.split("to");

                    calendarFrom = calendarDate[0].replace("/", "-");
                    calendarFrom = calendarFrom.replace("/", "-").trim();

                    calendarTo = calendarDate[1].replace("/", "-");
                    calendarTo = calendarTo.replace("/", "-").trim();

                    $(".display-date").addClass("on");
                    $(".calendar-inputWrap input").asDatepicker('setDate',[{from : calendarFrom ,to : calendarTo}]);
                }
            }
        } else {
            sessionStorage.removeItem("calendarDate");
        }

        var MobileKeyword = {
            init : function() {
                jQuery.ajax({
                    url: SEARCH_KEYWORD_API,
                    type: 'GET',
                    dataType: 'json',
                    success:function(data){
                        var keyword = data['DATA'];
                        var html = "";
                        if(keyword.length === 5) {
                            for (var i = 0; i < keyword.length; i++) {
                                html += '<a href="' + DOMAIN + "/search/index?query=" + encodeURIComponent(keyword[i]['KEYWORD']) + "&lang=" + LANG_TYPE.toUpperCase() + '">' + '#' + keyword[i]['KEYWORD'] + '</a>';
                            }
                        }
                        if(html){
                            $('.recom').html(html);
                        }
                    }
                });
            }
        };

        var body = $('body');
        var today = new Date();
        var yyyy = today.getFullYear();
        var mm = today.getMonth()+1;
        var dd = today.getDate();

        if(dd<10) {
            dd='0'+dd
        }
        if(mm<10) {
            mm='0'+mm
        }
        today = yyyy + mm + dd;

        body.off('.calendar-row span');
        body.on('click', '.calendar-row span', function () {
            setTimeout(function () {
                caledarString();
            }, 1000);
        });

        if(search_domain == "m-" + langType + ".yna.co.kr" || window.location.href.match("m-")) {
            MobileKeyword.init();
            if(location.pathname == "/search/index"){
                $('.btn-right, .search-input-right').remove();
            }

            $('button[name=filterSearch]').unbind().click(function (e) {
            	var searchKeyword = "";

                if($(".search-keyword").val() == ""){
                    alert(SEARCH_NULL);
                    e.preventDefault();
                }else {
                    if (location.pathname !== "/search/index") {
                        SearchBasic.GoSearch({
                            query: $(".search-keyword").val(),
                            lang: LANG_TYPE.toUpperCase()
                        });
                    } else {
                    	if($(".search-keyword2").val() !== undefined) {
                    		searchKeyword = ".search-keyword2";
                    	} else {
                    		searchKeyword = ".search-keyword";
                    	}

                        SearchBasic.GoSearch({
                            query: $(".search-keyword2").val()
                        });
                    }
                }
            });

            //다국어 모바일 상세 검색 버튼 클릭 이벤트
            /*$('.search-input .search-option1 > span .inp-label').click(function () {
                $('.search-input .search-option1 > span').siblings().find('.inp-label').removeClass('on');
                $(this).addClass('on');
            });
            $('.search-input .search-option2 > span .inp-label').click(function () {
                $('.search-input .search-option2 > span').siblings().find('.inp-label').removeClass('on');
                $(this).addClass('on');
            });
            $('.search-input .search-option3 > span .inp-label').click(function () {
                $('.search-input .search-option3 > span').siblings().find('.inp-label').removeClass('on');
                $(this).addClass('on');
                if ($('.search-input .search-option3 > span .inp-label').eq(4).hasClass('on')) {
                    $(".custom-box .input-box").addClass('on');
                    $('input[name=to]').val(today);
                } else {
                    $(".custom-box .input-box").removeClass('on');
                }
            });*/

            $('.search-input .search-option3 > span .inp-label').on("click", function () {
                $('.search-input .search-option3 > span').siblings().find('.inp-label').removeClass('custom-input');
                $(this).addClass('custom-input');

                if($('.search-input .search-option3 > span .inp-label').eq(4).hasClass('custom-input'))
                    $(".custom-box .input-box").addClass('on');
                 else
                    $(".custom-box .input-box").removeClass('on');
            });
        }

        // 검색기간 바인딩
        $('#search_detail_inbox, .search_detail_inbox, .option-box, .search-input').find('input[type=radio][name=period]').click(function () {
            var type = $(this).val();
            var calendarDate = "", calendarFrom = "", calendarTo = "";

            if (type == 'diy') {
                if(!window.location.href.match("m-")) {
                    $('input[name=from],input[name=to]').removeAttr('readonly');
                    $('input[name=from]').focus();

                    if(langType !== "kr") {
                        var calendarInput = $(".calendar-inputWrap input").val();
                        sessionStorage.setItem("calendarDate", calendarInput);
                        calendarDate = calendarInput.split("to");

                        calendarFrom = calendarDate[0].replace("/", "");
                        calendarFrom = calendarFrom.replace("/", "").trim();

                        calendarTo = calendarDate[1].replace("/", "");
                        calendarTo = calendarTo.replace("/", "").trim();

                        $('input[name=from]').val(calendarFrom);
                        $('input[name=to]').val(calendarTo);
                    }
                } else {
                    $('input[name=from]').val(yyyy + "" + mm + "" + dd);
                    $('input[name=to]').val(yyyy + "" + mm + "" + dd);

                    $('input[name=from],input[name=to]').removeAttr('readonly');
                    $('input[name=from]').focus();
                }
            }
            else if (type == 'all') {
                $('input[name=from],input[name=to]').attr('readonly', 'readonly');
                $('input[name=from]').val('');
                $('input[name=to]').val('');
            }
            else {
            	var d = Search.GetPeriod(type);

                if(!window.location.href.match("m-")) {
                    $('input[name=from],input[name=to]').attr('readonly', 'readonly');
                    var d = Search.GetPeriod(type);
                    $('input[name=from]').val(d['from']);
                    $('input[name=to]').val(d['to']);
                } else {
                    $('input[name=from]').val(d['from']);
                    $('input[name=to]').val(d['to']);
                }
            }
        });
        $('input[name=from],input[name=to]').attr('readonly', 'readonly');

        // 검색기간 세팅
        if (Search.Query['period']) {
            $('input[name=period][value=' + Search.Query['period'] + ']').click();
            if (Search.Query['period'] == 'diy') {
                if (Search.Query['from'])
                    $('input[name=from]').val(Search.Query['from']);
                if (Search.Query['to'])
                    $('input[name=to]').val(Search.Query['to']);
            }
        }

        // 날짜는 숫자만
        $('input[name=from],input[name=to]').keyup(function () {
            var v = this.value.replace(/[^0-9]+/g, '').replace(/^([0-9]{8}).*/, '$1');
            this.value = v;
        });

        // 검색
        $('#HdivLoad').show();
        Search.Search(opt);
        if(SearchBasic.Language == "kr")
            SearchBasic.SetRelateKeywords(); // 가장 마지막에 실행해야 함. 앞에 넣으면 에러남!!!
    }
};

// 함수구현
Search.MakeHTML = SearchBasic.MakeHTML;

$(document.body).ready(function () {
    SearchBasic.Init();
});