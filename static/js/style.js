var searchBox = document.querySelectorAll('.search-box input[type="text"] + span');
searchBox.forEach(function (elm) {
    elm.addEventListener("click", function () {
        elm.previousElementSibling.value = ""
    })
});
(function () {
    var rowNode = $("div.post-content p");
    var keyword = document.getElementById("input").value.split(" ");
    rowNode.each(function () {
        var newHtml = $(this).html();
        for (var i in keyword) {
            newHtml = newHtml.replace(keyword[i], '<span style="color:lightpink;">' + keyword[i] + "</span>")
        }
        $(this).html(newHtml)
    })
}());