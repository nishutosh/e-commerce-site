//step class

class Step
{
  constructor(num)
  {
      this.num = num;
      this.active = false;
  }
  toggleDisplay()
  {
    $('#step-'+this.num+' .content').toggle();
    this.changeStatus();
  }
  changeStatus()
  {
    if(this.active === true)
      this.active = false;
    else
     this.active = true; 
  }
}

var step1 = new Step(1);
var step2 = new Step(2);
var step3 = new Step(3);

var main_image;
var custom_image;

// initally step 1 is visible
step1.changeStatus();
//////////////////////////

// for first preview
$('input[type="file"]').change(function(){

  var input = $('#main-image').get(0);
  var file = input.files[0];
  main_image = custom_image;
  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function(imgsrc){
    var img = $('.file-image');
    img.attr("src", imgsrc.target.result);
  
  }
  
  
  $('#file-preview').show();

});


// for finishing form submit for image
$('#imageUploadForm').submit(function(evt){
  evt.preventDefault();
  console.log('event prevented');

  if (window.File && window.FileReader && window.FileList && window.Blob) {
    
        var input = $('#main-image').get(0);
        var file = input.files[0];
        console.log(file);
        getAsImage(file);
        
  
  } else {
    alert('Please use a different browser. This browser does not support the required technology');
  }
  
});

function getAsImage(imageFile) {
  var reader = new FileReader();
  reader.readAsDataURL(imageFile);
  reader.onload = addImg;
}
function addImg(imgsrc) {
  var img = $('.rear-image');
  img.attr("src", imgsrc.target.result);
  step1.toggleDisplay();
  step2.toggleDisplay();
}

$('#back').click(function(){
    if(step2.active)
    {
      step1.toggleDisplay();
      step2.toggleDisplay();
    }
    else if(step3.active)
    {
      step2.toggleDisplay();
      step3.toggleDisplay();
    }

});

$('#confirm').click(function(){
  if(step2.active)
  {
    step2.toggleDisplay();
    step3.toggleDisplay();
  }
  else if(step3.active)
  {
    
  }

  // now create canvas
  createCanvas();
});


function convertImageToCanvas(canvas,image) {
	   canvas.getContext("2d").drawImage(image,
            0,0, image.width, image.height
     );
	return canvas;
}


function createCanvas()
{
  var src = $(".phone").attr("data-src");
  $(".phone").css({
    "background-image" : 'url('+src+')'
  })

  var width = $("#phone-image").get(0).naturalWidth;
  var height = $("#phone-image").get(0).naturalHeight;

$(".phone").css({
  "width" : width,
  "height": height
})

  //$(".phone").hide();
  console.log(width);
  console.log(height);
  initialise();
  var canvas = document.getElementById('canvas');
  canvas.cropper.setCropBoxData({
    top : 150,
    left: 150,
    width: width-10,
    height: height-10
  });

}

function initialise() {
  var canvas = document.getElementById('canvas');
  var image = document.getElementById('rear-image');
  if (image.complete) {
    start.call(image);
  } else {
    image.onload = start;
  }
}


function start() {
  var canvas = document.getElementById('canvas');
      var width = this.naturalWidth;
      var height = this.naturalHeight;
      var ratio = width/height;
      if (width>500)
      {
        width = 500;
        height = width/ratio;
      }

      var cropper;
      canvas.width = width;
      canvas.height = height;
      canvas.getContext('2d').drawImage(
        this,
      //  0, 0, this.naturalWidth, this.naturalHeight,
        0, 0, width, height
      );
      cropper = new Cropper(canvas,{
        preview: $("#preview").get(0),
        responsive: true,
        dragMode: "crop"
      });
      
      console.log(cropper.getCropBoxData());
    }



/////////////////////////
// final submission
//////////////////////////
$('#customForm').submit(function(evt){
  evt.preventDefault();
  console.log('data submission prevented for customForm');
})
$('#final-submit-btn').click(function(){
  var productUrl = $(this).attr('data-product-url');
  var imageUrl = $(this).attr('data-image-url');
  var product_name = $('#product-name').val();
  var product_text = $('#product-text').val(); 
  
  var canvas = document.getElementById('canvas');
  var image = document.getElementById('rear-image');
  console.log(product_name);
  var newImage = new Image();
  var file;
  newImage.src =  canvas.cropper.getCroppedCanvas().toDataURL(image.src + "new-image");
  
 
  var data = {
    "product_name":product_name.toString(),
    "custom_image":canvas.cropper.getCroppedCanvas().toDataURL('image/png'),
    "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
    }

  $.ajax({
    type:'POST',
    url: productUrl,
    data:data,
    success: function(result){

      console.log('image uploaded');
      var pk = result.product;
      var quantity = result.quantity;
      var input = $('#main-image').get(0);
      var file = input.files[0];
      var reader = new FileReader();
       var main_image;
       reader.addEventListener("load", function () {
        main_image = reader.result;
        var picData = {
          'product_name':product_name,
          'product_pk':pk,
          'main_image':main_image,
          'text_to_be_inserted':product_text,
          'preview':canvas.cropper.getCroppedCanvas().toDataURL('image/png')
      }
      $.ajax({
        type:'POST',
        url: imageUrl,
        data:picData,
        success: function(result){
          console.log('image uploaded and product registered');
          console.log('adding to cart');
          var successUrl = $('#successUrl').attr('data-url');
          $.ajax({
            type: "POST",
            url: successUrl,
            data:{
                 "quantity":"1",
                 "product":pk,
                 "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
               
                     },
              success: function(){
                                        
                                         getCartItems()
                        
                                        }
              });

        }
      });
      }, false);

      reader.readAsDataURL(file);
      
    }
  });
  
  


});


$('#preview-btn').click(function(){
  var canvas = document.getElementById('canvas');
    var image = document.getElementById('rear-image');
  var newImage = new Image();
  newImage.src =  canvas.cropper.getCroppedCanvas().toDataURL(image.src + "new-image");
  $('body').append(newImage);
});