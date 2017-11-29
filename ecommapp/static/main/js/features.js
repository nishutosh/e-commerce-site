$(document).ready(function(){
    var content_container = $(".specifications");
    var content = $(".specifications").text();
    content_container.text('');
    convertTextToElements(content_container,content);
});


function convertTextToElements(container,text)
{
    var length = text.length;
    var h_count = 0;
    var ul_count = 0;
    var li_count = 0;
    //console.log(length);
    for(i=0;i<length;)
    {
        if(text[i]=='*')
        {
            i++;
            if(text[i]=='*')
                {
                    
                    i++;
                    var text_content="";
                    var k = 0;
                    while(text[i]!='*'&&text[i]!='\n')
                    {
                        text_content += text[i];
                        k++;
                        i++;
                    }
                    h_count++;
                    var id = 'h'+h_count;
                    
                    createNewElement('h4',container,{'id':id});
                    var currentHeading = $('#'+id);
                    putTextInElement(currentHeading,text_content);
                    ul_count++;
                    var ul_id = 'ul'+ul_count;
                    
                    createNewElement('ul',container,{'id':ul_id});

                }
            else
            {
                i++;
                var text_content="";
                var k = 0;
                while(text[i]!='*'&&i<length&&text[i]!='\n')
                {
                    text_content += text[i];
                    k++;
                    i++;
                }
               
                
                
                var current_ul = $('#ul'+ul_count);
                createNewElement('li',current_ul,{'text': text_content});
            }    
        }
        else
        {
            i++;
        }
    }
}

function createNewElement(element,parent,opts)
{
    if(opts['id'])
    {
         element = '<'+element+' id='+opts['id']+'></'+element+'>';
    }
    else if(opts['text'])
    {
        element = '<'+element+'>'+opts['text']+'</'+element+'>';
    }
    else
    {
        element = '<'+element+'></'+element+'>';
    }
    
    parent.append(element);
}


function putTextInElement(container,text)
{
    container.text(text);
}