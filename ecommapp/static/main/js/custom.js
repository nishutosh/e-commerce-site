
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
var step4 = new Step(4);

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

$('.back').click(function(){
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
    else if(step4.active)
    {
      step3.toggleDisplay();
      step4.toggleDisplay();
    }

});

$('.confirm').click(function(){
  if(step2.active)
  {
    step2.toggleDisplay();
    createCanvas();
    step3.toggleDisplay();
  }
  else if(step3.active)
  {
    step3.toggleDisplay();
    step4.toggleDisplay();
    addTextFunction();
  }

  // now create canvas
  
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
      // var width = this.naturalWidth;
      // var height = this.naturalHeight;
      var width = $("#phone-image").get(0).naturalWidth;
      var height = $("#phone-image").get(0).naturalHeight;
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
        dragMode: "crop",
        ready: function(){
          
        }
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
  var previewCanvas = $("#previewCanvas canvas").get(0);

  console.log(product_name);
  var newImage = new Image();
  var file;
  newImage.src =  canvas.cropper.getCroppedCanvas().toDataURL(image.src + "new-image");
  
 
  var data = {
    "product_name":product_name.toString(),
    "custom_image":previewCanvas.toDataURL('image/png'),
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
          'preview':previewCanvas.toDataURL('image/png')
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


function addTextFunction(){

  var previewCanvas = document.getElementById('preview-canvas');
  var width = $("#phone-image").get(0).naturalWidth;
  var height = $("#phone-image").get(0).naturalHeight;
  var previewimage = $('#preview img').get(0);
  

  processPreviewImage();
  textEditorDisplay();

}


function processPreviewImage()
{
  var div = document.createElement('div');
  var width = $("#phone-image").get(0).naturalWidth;
  var height = $("#phone-image").get(0).naturalHeight;
  var newCanvas = document.createElement('canvas');

  div.id="previewCanvas";
  newCanvas.width = width;
  newCanvas.height = height;
  div.appendChild(newCanvas); 

  var container = document.getElementById('textCanvasContainer');
  container.appendChild(div);
  var canvas = document.getElementById('canvas');
  var image = document.getElementById('rear-image');
  var newImage = new Image();
  newImage.src =  canvas.cropper.getCroppedCanvas().toDataURL('image/jpeg');
  newImage.onload = function(){

    var rearimage = document.getElementById('phone-image');
    var previewcanvas = $('#previewCanvas canvas').get(0);
    var images = {
      'cover':newImage,
      'phone':rearimage
      
    }
    convertPreviewImageToCanvas(previewcanvas,images);
    // convertPreviewImageToCanvas(previewcanvas,rearimage);

  }

  var movableDiv = document.createElement('div');
  movableDiv.id = 'placableText';
  movableDiv.className = 'placableText';
  div.appendChild(movableDiv);

  
    $('body').on('mousedown','#placableText',mousedown);
    document.addEventListener('mouseup',mouseup,true);
    document.addEventListener('mousemove',mousemove,true);
  
  
  // imageELement.src = newImage.src;
  // div.appendChild(imageELement);
}

function convertPreviewImageToCanvas(canvas,image)
{
  var ctx = canvas.getContext("2d");
  var x = 0, y=0,radius = 20,width = canvas.width,height = canvas.height;
  
  ctx.beginPath();
  ctx.strokeStyle = 'black';
  ctx.lineWidth = 10;
  ctx.moveTo(0, 0);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
  

  ctx.clip();
 
    ctx.drawImage(image['cover'],
      0,0, width, height
      );

      ctx.drawImage(image['phone'],
      0,0, width, height
      ); 
  
  
	return canvas;
}




var textContent;


function textEditorDisplay()
{
  
  var container = document.getElementById('textarea');
  
  var Font = Quill.import('formats/font');
  console.log(Font);
  // We do not add Sans Serif since it is the default
  Font.whitelist = ['roboto','bungee','pacifico','lobster','lato','serif'];
  Quill.register(Font, true);
  
  var toolbarOptions = [
    [{ 'font': ['roboto','bungee','pacifico','lobster','lato','serif'] }],
    [{ 'size': ['small', false, 'large', 'huge'] }],

    ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
  
    [{ 'align': [] }],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
    [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
    
  
    [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
    
   
  
    ['clean']                                         // remove formatting button
  ];

  
  var options = {
    debug: 'info',
    modules: {
      toolbar:toolbarOptions
    },
    placeholder: 'Compose an epic...',
    readOnly: false,
    theme: 'snow'
  };
  
  
  console.log("current fonts are:");
  console.log(Font);

  var editor = new Quill(container,options);
  textContent = editor;

  textContent.on('text-change', function(delta, oldDelta, source) {
    if (source == 'api') {
      console.log("An API call triggered this change.");
    } else if (source == 'user') {
      console.log("A user action triggered this change.");
      insertText();
    }
  });
}




$('#textBtn').click(function(){
  insertText();
});

function insertText()
{
  var movable = document.getElementById('placableText');
  var contents = textContent.getContents();
  movable.innerHTML = "";
  console.log(contents);
  for(var i=0;i<contents.ops.length;i++)
  {
      var span = document.createElement('span');

      var attributes = contents.ops[i].attributes;
      
      span.textContent = contents.ops[i].insert;
      assignAttributes(span,attributes);
      
      movable.appendChild(span);
  }
}

function assignAttributes(span,attributes){
    for(var attribute in attributes)
    {
      console.log(attribute+' = '+attributes[attribute]);
      switch(attribute)
      {
        case 'size':{
          switch(attributes[attribute])
          {
            case 'small':{
                size = '0.75em';
                break;
            }
            case 'normal':{
              size = '1em';
              break;
            }
            case 'large':{
              size = '1.5em';
              break;
            }
            case 'huge':{
              size = '2.5em';
              break;
            }
            default:{
              size = '1em';
            }
          }
          span.style['font-size'] = size;
          break;
        }
        case 'font':{
          span.style['font-family'] = attributes[attribute];
          break;
        }
        case 'bold':{
                if(attributes[attribute])
                {
                  span.style['font-weight'] = 700;
                }
                break;
        }
        case 'italic':{
          if(attributes[attribute])
          {
              span.innerHTML = '<em>' + span.innerHTML + '</em>';
          }
          break;

        }
        case 'underline':{
          if(attributes[attribute])
          {
            span.innerHTML = '<u>' + span.innerHTML + '</u>';
          }
          break;
        }
        default:{
          span.style[attribute] = attributes[attribute];
        }
      }
      

    }
}



// moving div in canvas


var offset = [0,0];
var isDown = false;

function mousedown(e)
{
  var div = document.getElementById('placableText');
  console.clear();
  isDown = true;
  console.log('something pressed');
  console.log(e.clientX);
  offset = [
    div.offsetLeft - e.clientX,
    div.offsetTop - e.clientY
];
}

function mouseup()
{
  isDown = false;
}

 function mousemove(event) {
  var div = document.getElementById('placableText');
  event.preventDefault();
  if (isDown) {
      mousePosition = {

          x : event.clientX,
          y : event.clientY

      };
      div.style.left = (mousePosition.x + offset[0]) + 'px';
      div.style.top  = (mousePosition.y + offset[1]) + 'px';
  }
}

$('#fixTextBtn').click(function(){
  renderDivOnCanvas();
});

function renderDivOnCanvas(){
  
  var text = document.getElementById('placableText');
  var position = $('#placableText').position();
  
  var width = text.offsetWidth;
  var height = text.offsetHeight;
  text.style.border = 'none';
  html2canvas(text,{
    onrendered: function(canvas) {
      // canvas is the final rendered <canvas> element
      var previewCanvas = $('#previewCanvas canvas').get(0);
      
      var myImage = new Image();
       myImage.src = canvas.toDataURL("image/png");
      //  var img = '<img src="'+myImage+'" />';
      //  $('body').append(myImage);
      console.log(position.left);
      myImage.onload = function(){
        var position = $('#placableText').position();
        var ctx = previewCanvas.getContext('2d');
        ctx.drawImage(myImage,position.left,position.top,myImage.width,myImage.height);
      }

      
    }
  });
  
  
}