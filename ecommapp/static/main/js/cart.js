$(document).ready(function(){
  getCartItems();
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






function getCartItems()
{    console.log("get cart item called")
  $.ajax({
               type: "GET",
               url: "/cart/",
                success: function(result){
                          console.log("get cart item sucess call"+result);
                          if(result.length == 0)
                          {
                            var element = '<h3>Oops! Your cart is empty... </h3>';
                            $(".continue-shopping-cta").before(element);
                            $("#order-btn").addClass("disabled");
                            $("#order-btn").parents(".order-cta").css({
                              "cursor": "not-allowed"
                            });
                            var cartItems = 0;
                            $(".cart-item-number").text(cartItems);
                            console.log("result-len0")
                          }
                          else if(result.message == "no cookie present")
                              {
                                  console.log("no cokkie")
                                var cartItems = 0;
                                $(".cart-item-number").text(cartItems);
                              }
                              
                          else{
                             console.log("cart has some items")
                            var cartItems = result.length;
                            $(".cart-item-number").text(cartItems);
                            
                          }







                }
                });
}
/////////////////////////////////////
// for adding to cart on list page
//////////////////////////////////////
function addtocart(){
   console.log("cart-button click")
    $.ajax({
            type: "POST",
            url: $(this).attr("data-ajax-url"),
            data:{
                 "quantity":"1",
                 "product":$(this).attr("data-product-id"),
                 "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
               
                     },
              success: function(){
                                        
                                         getCartItems()

                                        }
              });
}
$(".cart-btn").click(addtocart);
$(".list-cta-btn").click(addtocart);

/////////////////////////////////
// functionality for decreasing quantity via minus button
$(".reduce-quantity").click(function(){
  var val = $(this).siblings(".quantity-input").children().val();
  var id = $(this).siblings(".quantity-input").attr("data-id");
  var url = $(this).siblings(".quantity-input").attr("data-url");
  var inputElement = $(this).siblings(".quantity-input").children("input").get(0);
  console.log("reduce quantity")
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
    console.log("increase quantity")
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
{ console.log("update cart called");
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
         },
    success: function(){
      console.log("hurray quantity changed");
    }
  });
   Couponupdate();
  billCalculate();
}

function removeFromCart(item)
{ console.log("remove from cart called");
  var id = $(item).attr("data-id");
  var url  = $(item).attr("data-url");

  $.ajax({
    type: "POST",
    url: url,
    data:{
         //"quantity":element.value,
         "product":id,
         "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
         },
    success: function(){
      console.log("item removed");
      getCartItems();
      Couponupdate();
      billCalculate();
    }
    });

      location.reload();

}

/////////////////////////////////////////////
/////////Discount application
////////////////////////////////////////

function Couponupdate()
{    console.log("coupon update")
       $.ajax({
               type: "GET",
               url: "/cart/apply-coupon/",
                success: function(result){
                  $(".discount-value").text(result.value)
                  $(".discount-note").text(result.message)
                  console.log(result)
                  billCalculate();
                           
                }
                });
}
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
             "coupon_entered":discountCode.toString(),
             "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
            
             },
        success: function(result){
            $(".discount-value").text(result.value)
            $(".discount-note").text(result.message)
            console.log(result)
            billCalculate();
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

    console.log("bil caculate called");
    var totalDiscount = 0,totalBill = 0,totalCost = 0,deliveryCharges = 100;
    var totalelements = $("#cart-table tbody tr").length;
    $.each($cost_value,function(index,cost_value){
      console.log("stuff1 call");
          let quantity = $quantity_value.get(index).value;
          cost = parseInt($(this).text())*quantity;
          totalCost+=cost;
          console.log(totalCost);
    });

          discount = parseInt($discount_value.text());
          console.log(discount);
    

   

    totalBill = totalCost + deliveryCharges - discount;
    console.log(totalBill);

    $cost_element.text("₹"+totalCost);
    
    $deliveryCharges_element.text("₹"+deliveryCharges);
    $discount_element.text("₹"+discount);
    $billAmount_element.text("₹"+totalBill);

  }

  //////////////////////////////////////////
  //Cancel Order
  //////////////////////////////////////////

  $(".cancel-package-btn").click(function(){
    var orderId = $(this).attr("data-id");
    var productId = $(this).attr("data-product-id");
    var url = $(this).attr("data-url");
    $.ajax({
      type: "POST",
      url: url,
      data:{
           "order_id":orderId,
           "order_product_id":productId,
           "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val()
         },
      success: function(){
             location.reload();

           }
    });
  });
