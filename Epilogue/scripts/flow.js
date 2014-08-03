(function() {

    showIndex = function() {
        $(".content-page").hide();
        $(".content-page#" + pageNum).show();
    }

    getNext = function() {
        pageNum++;
        showIndex();
    }

    $(function() {
        showIndex();
        $("button").click(getNext())
        $("#flower")
    });

}());
