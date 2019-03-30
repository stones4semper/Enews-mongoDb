$(document).ready(function(){
    $('body').on('click', '.reloadAm', function(e){
        e.preventDefault()
        location.reload()
    })
})
function submit_form(formid, btn_id, img_id, show_id, reload){
    var frm = $('#'+formid);
    frm.submit(function(e){
        e.preventDefault();
        $("#"+btn_id).hide();
        $("#"+img_id).show();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data:  new FormData(this),
            contentType: false,
            processData:false,
            success: function (data){ 
                $("#"+btn_id).show();
                $("#"+img_id).hide();         
                $("#"+show_id).addClass('text-'+data.SType).fadeIn().html(data.message);                
                if(reload == 'yes'){
                    setTimeout(function(){
                        location.reload();
                    } , 2000);
                }
                else{
                    frm[0].reset();    
                    setTimeout(function(){
                        $("#"+show_id).removeClass('text-'+data.SType).fadeOut('slow').html(data.message);
                    } , 10000);
                }                
            },
            error: function(data){            
                $("#"+show_id).html(data);
                $("#"+btn_id).show();
                $("#"+img_id).hide();
            },
        });
    });
}