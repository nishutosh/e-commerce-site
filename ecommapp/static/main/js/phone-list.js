class Phone{
    constructor(name,pk)
    {
        this.name = name;
        this.pk = pk;
    }
    createElement()
    {
        var element = '<tr><td class=""><a href="edit/'+this.pk+'">'+this.name+'</a></td></tr>';
        return element;
    }

}

$('.phone-list-toggle-btn').click(function(){
    var url = $(this).attr('data-url');
    $.ajax({
        type: "GET",
        url: url,
        success: function(result)
                    {
                        console.log(result);
                        var phoneListLength = result.length;
                        // for(i=0;i<phoneListLength;i++)
                        // {
                        //     createNewPhone(result[i],i);
                        // }
                        result.forEach(function(phone){
                            console.log(phone);
                            Object.keys(phone).forEach(function(key){
                                    console.log(key);
                                    createNewPhone(phone[key],key);
                            });
                            

                            
                        });
                    }
    });
});

function createNewPhone(phone_name,pk)
{
    var newPhone = new Phone(phone_name,pk);
    var container = $('#phoneModal .modal-body .phone-list');
    container.append(newPhone.createElement());
}

