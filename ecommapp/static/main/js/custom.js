$(document).ready(
  function(){

    createCanvas();

  }
);


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

  var width = $(".phone-canvas").get(0).naturalWidth;
  var height = $(".phone-canvas").get(0).naturalHeight;

$(".phone").css({
  "width" : width,
  "height": height
})

  $(".phone-canvas").hide();
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


//////////////////
// button controls
///////////////////



$("#crop").click(function(){
  var canvas = document.getElementById('canvas');
  canvas.cropper.crop();
});

$("#clear").click(function(){
  var canvas = document.getElementById('canvas');
  canvas.cropper.clear();
});

$("#reset").click(function(){
  var canvas = document.getElementById('canvas');
  canvas.cropper.reset();
});

$("#get-crop").click(function(){
  var canvas = document.getElementById('canvas');
  var data = canvas.cropper.getCropBoxData();
  console.log(data);

});
$("#done").click(function(){
  var canvas = document.getElementById('canvas');
  var image = document.getElementById('rear-image');
  var phone = document.getElementById('phone-image');

  var data = canvas.cropper.getCropBoxData();
  console.log(data);

  var newImage = new Image();
  newImage.src =  canvas.cropper.getCroppedCanvas().toDataURL(image.src + "new-image");

  newImage.className = "new";
  $(".new").css({
    "width": $(".phone-canvas").get(0).naturalWidth
  });


  console.log(phone.src);
  //$(".phone").append(newImage);

  var phoneCanvas = document.getElementById("phone-canvas");

//  phoneCanvas = canvas.cropper.getCroppedCanvas();
convertImageToCanvas(phoneCanvas,newImage);


});
