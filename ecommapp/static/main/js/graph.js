window.onload = function () {
    var graph_data;
    var url = $(".data").attr("data-api-url");
    console.log("the api url is : "+url);
    $.ajax({
        type: "GET",
        url: url,
         success: function(result){
           var required_data = [];
           var keys = Object.keys(result);
           var length = keys.length; 
           console.log(result);
           console.log("the number of objects are: "+length);
           for(i=0;i<length;i++)
           {
                var x = new Date(result[i].x);
                var y = result[i].y;
                var obj = {x:x,y:y};
                required_data[i] = obj;
           }
           console.log(required_data);
           graph_data = required_data;
           plotGraph(graph_data);
         }
    });
    console.log(graph_data)
    
}

function plotGraph(graph_data)
{
    var requiredGraph = new CanvasJS.Chart('graph-container',{
        animationEnabled: true,
        backgroundColor: "transparent",
        theme: "theme2",
        axisX: {
            labelFontSize: 14,
            valueFormatString: "MMM YYYY"
        },
        axisY: {
            labelFontSize: 14,
            
        },
        toolTip: {
            borderThickness: 0,
            cornerRadius: 0
        },
        data: [{
            type: "line",
            showInLegend: true,
            name: "Total Orders",
            markerType: "square",
            xValueFormatString: "DD MMM, YYYY",
            color: "#F08080",
            dataPoints: graph_data
                
            
        }]
    });

    requiredGraph.render();
}