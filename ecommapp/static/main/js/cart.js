$(document).ready(function(){
  getCartItems();
<<<<<<< HEAD
  successModal();
=======
  getWishlistItems();
>>>>>>> fix-front-end
});

function Bill(price,delivery,discount)
{
    this.price = price;
    this.delivery = delivery;
    this.discount = discount;
    this.total = 0;
}

Bill.prototype = {
  calculate: function()
  {
    this.total = this.price+this.delivery-this.discount;
  }
}
var currentBill = new Bill(0,0,0);

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

function getWishlistItems() {
    console.log("get wishlist item called")
    $.ajax({
        type: "GET",
        url: "/wishlist/product/",
        success: function(result) {
            console.log("get cart wishlist call" + result);
            if (result.message == "unauthenticated user") {
                console.log("unauthenticated user")
                var wishlistItems = 0;
                $(".wishlist-item-number").text(wishlistItems);
            } else {
                console.log("wishlist items seen")
                var wishlistItems = result.length;
                $(".wishlist-item-number").text(wishlistItems);
            }
        }
    });
}
function addtowishlist() {
    console.log("cart-button click")
    $.ajax({
        type: "POST",
        url: $(this).attr("data-ajax-url"),
        data: {
            "product": $(this).attr("data-product-id"),
            "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val(),
        },
        success: function() {
         getWishlistItems();
        }
    });
}





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
                            var price = 0;
                            for(const prop in result)
                            {
                              price += result[prop].Price;
                            }
                            currentBill.price = price;
                            currentBillCalculate();
                          }







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
                                         callSuccessModal();                       
                                         getCartItems();

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
         "discount":currentBill.discount,
         "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
         },
    success: function(){
      console.log("hurray quantity changed");
      Couponupdate();
      getCartItems();
    }
  });
   
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
       //currentBillCalculate();
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
                  if(result.message=="coupon code already applied" || result.message=="coupon code applied"){          
                    $(".cta-btn").attr("disabled","disabled")
                    $("#discount-input").attr("disabled","disabled")


                  }
                  $(".discount-value").text(result.value)
                  $(".discount-note").text(result.message)
                  console.log(result)
                  currentBill.discount = result.value;
                  currentBillCalculate();
                           
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
            currentBill.discount = result.value;
            currentBillCalculate();
        }
        });
    });
  });


  //////////////////////////////
  // currentBill Estimation
  /////////////////////////////

  function currentBillCalculate()
  {
    var $cost_element = $("#totalCost");
    var $deliveryCharges_element = $("#deliveryCharges");
    var $discount_element = $("#totalDiscount");
    var $currentBillAmount_element = $("#totalBill");
    var $discount_value = $(".discount-value");
    var $cost_value = $(".product-price");
    var $quantity_value = $(".quantityValue");

    console.log("bil caculate called");
    var totalDiscount = 0,totalcurrentBill = 0,totalCost = 0,deliveryCharges = 100;
    var totalelements = $("#cart-table tbody tr").length;
    // $.each($cost_value,function(index,cost_value){
    //   console.log("stuff1 call");
    //       let quantity = $quantity_value.get(index).value;
    //       cost = parseInt($(this).text())*quantity;
    //       totalCost+=cost;
    //       console.log(totalCost);
    // });

    //       discount = parseInt($discount_value.text());
    //       console.log(discount);
    console.log("current bill in bill function is:");
    console.log(currentBill);
    currentBill.delivery = 100;
   // currentBill.update();
    console.log("currentBill is"+currentBill);
    
    console.log(totalcurrentBill);
    currentBill.calculate();
    $cost_element.text("₹"+currentBill.price);

    $deliveryCharges_element.text("₹"+currentBill.delivery);
    $discount_element.text("₹"+currentBill.discount);
    $currentBillAmount_element.text("₹"+currentBill.total);

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


  function successModal(){
    var element = '<div id="successModal" class="modal fade" role="dialog">'+
    '<div class="modal-dialog">'+
    '<div class="modal-content">'+
      '<div class="modal-header">'+
        '<button type="button" class="close" data-dismiss="modal">&times;</button>'+
        '<h4 class="modal-title">Product added to Cart</h4>'+
      '</div>'+
      '<div class="modal-body">'+
        '<h3>SUCCESS</h3>'+
        '<div>'+
          '<div class="successIcon"><i class="fa fa-check"></i></div>'+
        '</div>'+
        '<div><h5>The product successfully added to cart</h5></div>'
      '</div>'+
      '<div class="modal-footer">'+
        '<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'+
      '</div>'+
    '</div>'+
  '</div>'+
'</div>';
    $('body').append(element);
  }

  function callSuccessModal()
  {
    $('#successModal').modal('show');
  }
