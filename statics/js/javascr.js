

function filter(category) {
    price_from = document.getElementById("price_from").textContent
    price_to = document.getElementById("price_to").textContent
    let show_color = document.getElementById('show_color') 
    var color = new Array();  
    for (var i = 0; i < show_color.children.length; i++) {
        if (show_color.children[i].checked) {  
            color.push(show_color.children[i].nextSibling.textContent);
        }
    } 
    let show_size = document.getElementById('show_size') 
    var size = new Array();  
    for (var i = 0; i < show_size.children.length; i++) {
        if (show_size.children[i].checked) {
            size.push(show_size.children[i].nextSibling.textContent);
        }
    } 
    $.ajax({
        type: 'GET',
        async: true,
        url: 'filter',
        data: {
            ajax: true,
            price_from: price_from,
            price_to: price_to,
            color: color,
            size: size,
            category: category,
        },
        success: function (data) {
            $("body").html(data)
        },
        error: function (xhr, status, e) {
        },
        dataType: '',
    });
}
function rangeSlider(id, value) {
    document.getElementById(id).innerHTML = value;
} 
function add_item(product_id) { 
    quantity = $('#' + product_id).val(); 
    $.ajax({
        type: 'GET',
        async: true,
        url: 'add_item',
        data: {
            ajax: true,
            quantity: quantity,
            product_id: product_id,
        },
        success: function (data) {
            $("body").html(data)
        },
        error: function (xhr, status, e) {
            // console.log(status);
        },
        dataType: '',
    });
}
 
