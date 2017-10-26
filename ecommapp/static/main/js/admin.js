
$(document).ready(function(){
  //prevent_defaults();
  bootstrapClass();
});

///////////////////////////
// stopping form submission
//////////////////////////

function prevent_defaults(){
  var form = $("#filter-form").get(0);
  form.addEventListener("submit",event => {
        event.preventDefault();
        submitFilters();
        console.log("form submission stopped");
    });
}



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


  ///////////////////////////////////////
  // Filter function for orders
  //////////////////////////////////////

  function submitFilters()
  {

  }

  ///////////////////////////////////
  //adding bootstrap class to django forms
  ////////////////////////////////////

  function bootstrapClass()
  {
    $(".provide-bootstrap-class input").addClass("form-control");
    $(".provide-bootstrap-class select").addClass("form-control");
  }
