// #disable checkout button when cart is empty
$.ajax({
    type: "GET",
    url: "/cart/cartitems",
    success: function(result) {
        console.log(result);
        $(".cart-list").text(result.message);
        for (i = 0; i < result.length; i++) {
            prod = result[i].Product_name;
            id = result[i].Product_id;
            quantity = result[i].Quantity;
            $(".cart-list").append("<ul>" + prod + quantity + "</ul>");
        }
    }
});
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
$(".cart-btn").click(function() {
    $.ajax({
        type: "POST",
        url: $(".cart-btn").attr("data-ajax-url"),
        data: {
            "quantity": $(".quantity").val(),
            "product": $(".cart-btn").attr("data-product-id"),
            "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function(result) {
            $.ajax({
                type: "GET",
                url: $(".cart-btn").attr("data-ajax-url"),
                success: function(result) {
                    console.log(result);
                    $(".cart-list").html(result.mesg);
                    for (i = 0; i < result.length; i++) {
                        prod = result[i].Product_name;
                        id = result[i].Product_id;
                        quantity = result[i].Quantity;
                        $(".cart-list").append("<ul>" + prod + quantity + "</ul>");
                    }
                }
            });
        }
    });
});
$(".rmv-cart-btn").click(function() {
    $.ajax({
        type: "POST",
        url: $(".rmv-cart-btn").attr("data-ajax-url"),
        data: {
            "product": $(".rmv-cart-btn").attr("data-product-id"),
            "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function(result) {
            $.ajax({
                type: "GET",
                url: $(".cart-btn").attr("data-ajax-url"),
                success: function(result) {
                    console.log(result);
                    $(".cart-list").html(result.mesg);
                    for (i = 0; i < result.length; i++) {
                        prod = result[i].Product_name;
                        id = result[i].Product_id;
                        quantity = result[i].Quantity;
                        $(".cart-list").append("<ul>" + prod + quantity + "</ul>");
                    }
                }
            });
        }
    });
});
//ajax for  username check
$('#id_username').keyup(function() {
    $.ajax({
        type: "POST",
        url: "/auth/validate/",
        data: {
            "username": $("#id_username").val(),
        },
        success: function(result) {
            $("#username_message").text(result.message);
        }
    })
});
$('#coupon').click(function() {
    $.ajax({
        type: "POST",
        url: "/cart/apply-coupon/",
        data: {
            "product": 2,
            "coupon_entered": "testcoupon",
        },
        success: function(result) {
            $("#username_message").text(result.message);
        }
    })
});
$(".order-can").click(function() {
    $.ajax({
        type: "POST",
        url: "/order/cancel-order/",
        data: {
            "order_id": 2,
        },
        success: function(result) {
            console.log(result)
        }
    })
});
