function add(){
    console.log('ddddddddd');
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

 