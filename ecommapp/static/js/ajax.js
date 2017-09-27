// #disable checkout button when cart is empty

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



$(".cart-btn").click(function(){
    $.ajax({
            type: "POST",
            url: $(".cart-btn").attr("data-ajax-url"),
            data:{
                 "quantity":$(".quantity").val(),
                 "product":$(".cart-btn").attr("data-product-id"),
                 "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
                "s":console.log($("input[name='csrfmiddlewaretoken']").val())
                     },
              success: function(result){
                           $.ajax({
                                         type: "GET",
                                         url: $(".cart-btn").attr("data-ajax-url"),
                                          success: function(result){
                                            console.log(result);
                                          $(".cart-list").html(result.mesg);
                                           for(i=0;i<result.length;i++){
                                             prod=result[i].Product_name;
                                             $(".cart-list").append("<ul>"+prod+"</ul>");}

                                          }
                                          });


                                                         } 
              });
});


$(".cart-btn").click(function(){
    $.ajax({
            type: "POST",
            url: $(".cart-btn").attr("data-ajax-url"),
            data:{
                 "product":$(".cart-btn").attr("data-product-id"),
                 "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
                "s":console.log($("input[name='csrfmiddlewaretoken']").val())
                     },
              success: function(result){
                           $.ajax({
                                         type: "GET",
                                         url: $(".cart-btn").attr("data-ajax-url"),
                                          success: function(result){
                                            console.log(result);
                                          $(".cart-list").html(result.mesg);
                                           for(i=0;i<result.length;i++){
                                             prod=result[i].Product_name;
                                             $(".cart-list").append("<ul>"+prod+"</ul>");}

                                          }
                                          });
   } 
       });
});
$.ajax({
             type: "GET",
             url: "/cart/",
              success: function(result){
                    console.log(result);
                $(".cart-list").text(result.message);
              for(i=0;i<result.length;i++){
                 prod=result[i].Product_name;
                 $(".cart-list").append("<ul>"+prod+"</ul>");
                
}
             }

              
              });


