$(document).ready(function(){
  billCalculate();
});



// #disable checkout button when cart is empty
// getting cookies
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
// csrf matching
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

// saving item in cart via add to cart cta for product-details page
// $("#add-to-cart-btn").click(function(){
//     $.ajax({
//             type: "POST",
//             url: $("#add-to-cart-btn").attr("data-ajax-url"),
//             data:{
//                  "quantity":"1",
//                  "product":$("#add-to-cart-btn").attr("data-product-id"),
//                  "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
//                 "s":console.log($("input[name='csrfmiddlewaretoken']").val())
//                      },
//               success: function(result){
//                            $.ajax({
//                                          type: "GET",
//                                          url: $("#add-to-cart-btn").attr("data-ajax-url"),
//                                           success: function(result){
//                                          console.log(result)
//
//                                           }
//                                           });
//                                         }
//               });
// });

$.ajax({
             type: "GET",
             url: "/cart/",
              success: function(result){
                console.log(result)
             for(i=0;i<result.length;i++){
                 prod=result[i].Product_name;
                 console.log(prod)


             }

              }
              });
/////////////////////////////////////
// for adding to cart on list page
//////////////////////////////////////

$(".cart-btn").click(function(){
    $.ajax({
            type: "POST",
            url: $(this).attr("data-ajax-url"),
            data:{
                 "quantity":"1",
                 "product":$(this).attr("data-product-id"),
                 "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
                "s":console.log($("input[name='csrfmiddlewaretoken']").val())
                     },
              success: function(result){
                           $.ajax({
                                         type: "GET",
                                         url: $(this).attr("data-ajax-url"),
                                          success: function(result){
                                         console.log(result)

                                          }
                                          });
                                        }
              });
});

/////////////////////////////////
// functionality for decreasing quantity via minus button
$(".reduce-quantity").click(function(){
  var val = $(this).siblings(".quantity-input").children().val();
  var id = $(this).siblings(".quantity-input").attr("data-id");
  var url = $(this).siblings(".quantity-input").attr("data-url");
  var inputElement = $(this).siblings(".quantity-input").children("input").get(0);
  if(val>1)
  {
    val--;
    $(this).siblings(".quantity-input").children().val(val);
  }
  updateCart(inputElement,id,url);
});

// functionality for increasing quantity via plus button
$(".increase-quantity").click(function(){
  var val = $(this).siblings(".quantity-input").children().val();
  var id = $(this).siblings(".quantity-input").attr("data-id");
  var url = $(this).siblings(".quantity-input").attr("data-url");
  var inputElement = $(this).siblings(".quantity-input").children("input").get(0);
  if(val<5)
  {
    val++;
    $(this).siblings(".quantity-input").children().val(val);
  }
  updateCart(inputElement,id,url);
});

//////////////////////////////
// updating and saving cart
///////////////////////////////
function updateCart(element,id,url)
{
  console.log("element = " + element);
  console.log("id = " + id);
  if(element.value>5)
    {
      element.value = 5;
    }
  else if(element.value<1)
  {
    element.value = 1;
  }
  $.ajax({
    type: "POST",
    url: url,
    data:{
         "quantity":element.value,
         "product":id,
         "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
        "s":console.log($("input[name='csrfmiddlewaretoken']").val())
         },
    success: function(){
      console.log("hurray quantity changed");
    }
  });

  billCalculate();
}

function removeFromCart(item)
{
  var id = $(item).attr("data-id");
  var url  = $(item).attr("data-url");

  $.ajax({
    type: "POST",
    url: url,
    data:{
         //"quantity":element.value,
         "product":id,
         "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
        "s":console.log($("input[name='csrfmiddlewaretoken']").val())
         },
    success: function(){
      console.log("item removed");
      $.get("/cart/checkout/",function(){
        console.log(reloaded);
      })
    }
    });

      location.reload();

}

/////////////////////////////////////////////
/////////Discount application
////////////////////////////////////////


$(".discount-form").each(function(){
    $(this).submit(function(evt){

      evt.preventDefault();
      var productId = $(this).attr("data-id");
      var discountUrl = $(this).attr("action");
      var discountCode = $(this).children("input").val();
      $.ajax({
        type: "POST",
        url: discountUrl,
        data:{
             //"quantity":element.value,
             "product":productId,
             "coupon_entered":discountCode.toString(),
             "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
            "s":console.log($("input[name='csrfmiddlewaretoken']").val())
             },
        success: function(){
          console.log("item removed");
          $.get("/cart/checkout/",function(){
            console.log(reloaded);
          })
        }
        });
    });
  });


  //////////////////////////////
  // Bill Estimation
  /////////////////////////////

  function billCalculate()
  {
    var $cost_element = $("#totalCost");
    var $deliveryCharges_element = $("#deliveryCharges");
    var $discount_element = $("#totalDiscount");
    var $billAmount_element = $("#totalBill");

    var $discount_value = $(".discount-value");
    var $cost_value = $(".product-price");
    var $quantity_value = $(".quantityValue");

    var totalDiscount = 0,totalBill = 0,totalCost = 0,deliveryCharges = 100;
    var totalelements = $("#cart-table tbody tr").length;
    $.each($cost_value,function(index,cost_value){
          let quantity = $quantity_value.get(index).value;
          cost = parseInt($(this).text())*quantity;
          console.log(cost);
          totalCost+= cost;
    });

    $.each($discount_value,function(index,discount_value){
          let quantity = $quantity_value.get(index).value;
          discount = parseInt($(this).text())*quantity;
          console.log(cost);
          totalDiscount+= discount;
    });

    console.log(totalCost);
    console.log(totalDiscount);

    totalBill = totalCost + deliveryCharges - totalDiscount;
    console.log(totalBill);

    $cost_element.text("₹"+totalCost);
    $deliveryCharges_element.text("₹"+deliveryCharges);
    $discount_element.text("₹"+totalDiscount);
    $billAmount_element.text("₹"+totalBill);

  }
