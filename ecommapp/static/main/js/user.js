//////////////////////////////////////////
  //return Order
  //////////////////////////////////////////

  $(".return-package-btn").click(function(){
    var orderId = $(this).attr("data-id");
    var productId = $(this).attr("data-product-id");
    var url = $(this).attr("data-url");
    var reason =$('#returnPackageModal'+orderId+' textarea').val();
    $.ajax({
      type: "POST",
      url: url,
      data:{
           "order_id":orderId,
           "order_product_id":productId,
           "reason":reason,
           "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val()
         },
      success: function(){
             location.reload();

           }
    });
  });