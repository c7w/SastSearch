var searchBox = document.querySelectorAll('.search-box input[type="text"] + span');
searchBox.forEach(function (elm) {
    elm.addEventListener("click", function () {
        elm.previousElementSibling.value = ""
    })
});
// (function () {
//     var rowNode = $("div.post-content p");
//     var keyword = document.getElementById("input").value.split(" ");
//     rowNode.each(function () {
//         var newHtml = $(this).html();
//         for (var i in keyword) {
//             newHtml = newHtml.replace(keyword[i], '<span style="color:lightpink;">' + keyword[i] + "</span>")
//         }
//         $(this).html(newHtml)
//     })
// }());

function set_background_image(option = 'NotSet') {
    // Read from cookies
    if (option == 'NotSet') {
        option = 'Mori'
        for (let entry of document.cookie.split(';').map(x => x.trim()) ){
            const dict = entry.split('=');
            if (dict[0] == 'bgimg') {
                option = dict[1];
                break;
            }
        }
    }
    
    // Const options
    const options = {
        'Yoru': {
            'url': "https://i.loli.net/2021/08/03/17CeYrRoJ89NiWU.jpg",
            'color': 'rgb(5,7,22);'
        },
        'Umi': {
            'url': 'https://i.loli.net/2021/08/03/fcPC5LObS1NT9l7.jpg',
            'color': 'rgb(214,230,238);'
        },
        'Mori': {
            'url': 'https://i.loli.net/2021/08/03/4gZ7yAOhbrT3qHF.jpg',
            'color': 'rgb(190,206,107);'
        }
    };
    
    const sel = options[option];
    document.body.style.setProperty("--bg-image", "url('" + sel['url'] + "')");
    // Write to cookies
    document.cookie = "bgimg=" + option;
}

set_background_image();
