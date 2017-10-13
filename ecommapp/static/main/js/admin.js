
  ///////////////////////////////////////////
  // Change product status through admin for orders
  ///////////////////////////////////////////

  $(".status-change-btn").click(function(){
    var orderId = $(this).attr("data-order-id");
    var productId = $(this).attr("data-product-id");
    var url = $(this).attr("data-url");
    var selector = "#status-list-" + orderId + "-" + productId;
    var status = $(selector).val();
    console.log(status);
    $.ajax({
      type: "POST",
      url: url,
      data:{
           "order_id":orderId,
           "order_product_id":productId,
           "status": status,
           "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val()
         },
      success: function(){
             location.reload();

           }
    });
  });
