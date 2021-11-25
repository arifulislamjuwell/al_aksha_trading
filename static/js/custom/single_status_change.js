function change_status(id, status, sector, url) {
    // if some changes need to happen during status change
    // that goes here
    // var csrf= '{{ csrf_token }}'
    // alert(csrf)
 

    call_function(id, status, sector, url, csrf);
}

function call_function(id, status, sector, url, csrf) {

    var data = {'id': id, 'status': status, 'sector': sector, 'csrfmiddlewaretoken': csrf}
    $.ajax({
        url: url,
        data: data,
        type: "POST",
        success: function (data) {
            toastr.success('Status changed successfully')
            setTimeout(function () {
                location.reload()
            }, 1200);
        },
        error: function (data) {
        }
    });
}

function generate(seller, order_id, to_whom){
    if (seller !=null){
         debugger
         let sellers = null;
         let options = '';
         if(seller.length>3) {
             sellers = JSON.parse(seller.replaceAll("'", '"'));
             for(let sl of sellers){
                 var html_option = `<option value="${sl.seller_id}">${sl.seller_name}</option>`;
                 options +=html_option
             }
             $("#sellers").html(options);
             $("#sellers").select2({
                 theme: "bootstrap4",
             });
             $("#order_id").val(order_id)
             $("#to_whom").val(to_whom)

         }
          $('#sellerModal').modal('show');
          return false
     }
}
function fireModal(order_id){
    $("#deliverOrder").val(order_id)
    $("#agreeModal").modal('show')
}
function deliver_order(order_id){
    debugger
    let data  ={'order_id': order_id.value}
     var url = "/deliver-paperfly/"
     let token = '{{csrf_token}}';
    $.ajax({
        url: url,
        // headers: { "X-CSRFToken": token },
        data: data,
        type: "POST",
        success: function (data) {
            if(data.status==400){
                $("#agreeModal").modal('hide');
                alert("Failed to deliver order through PaperFly")
            }
            if(data.status==200){
                $("#agreeModal").modal('hide');
                alert("Order pass to Paperfly for delivery")
                location.reload()
            }
        }
    });
}