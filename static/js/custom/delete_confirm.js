
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var delete_modal_html = "" +
"<div id='deleteAlert'>" +
"    <div id=\"confirm_delete_modal\" class=\"modal fade\" tabindex=\"-1\">" +
"        <div class=\"modal-dialog modal-confirm modal-sm\">" +
"            <div class=\"modal-content\">" +
"                <div class=\"modal-header\">" +
"                    <div class=\"icon-box\">" +
"                        <i class=\"material-icons\">&#xE5CD;</i>" +
"                    </div>" +
"                    <h4  class=\"modal-title w-100\">Alert</h4>" +
"                    <button onclick=\"removeDeleteAlert()\" type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">&times;</button>" +
"                </div>" +
"                <div class=\"modal-body\">" +
"                    <input type=\"hidden\" id='confirm_id'>" +
"                    <p>Are you sure delete?</p>" +
"                </div>" +
"                <div class=\"modal-footer\">" +
"                    <button type=\"button\" data=\"false\" class=\"btn btn-sm btn-secondary cancel\" data-dismiss=\"modal\">Cancel</button>" +
"                    <button type=\"button\" data=\"true\" class=\"btn btn-sm btn-danger\" data-dismiss=\"modal\">Delete</button>" +
"                </div>" +
"            </div>" +
"        </div>" +
"    </div>" +
"</div>" +
"";

function removeDeleteAlert() {
    $("#confirm_delete_modal").modal('hide')
    $("#deleteAlert").remove();
    $("div.modal-backdrop").remove();
    $("body").removeClass("modal-open");
}

function deletes(ele) {
    event.preventDefault();
    let btn = $(ele);
    let url = btn.data('href');
    let param = [];
    param['url'] = url;
    param['btn'] = btn;

    $("body").append(delete_modal_html);
    $("#confirm_delete_modal").modal('show')

    $('.modal-footer button').click(function () {
          if($(this).attr('data') == 'true') {
                removeDeleteAlert();
                deleteRow(param);
           } else {
                removeDeleteAlert();
           }
    });
}

function deleteRow(param){
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: param['url'],
        type: 'DELETE',
        data: param['query'],
         headers: { "X-CSRFToken": csrftoken },
        success: function (data) {
            location.reload()
        }

    });
}

function isProductExist(){
    let tr = $(document).find('#tableBody tr');
    var toReturn = false;
    $.each(tr, function (ind, val){
        if($(val).find('input[name=products]').val() == $("#product :selected").val()){
            toReturn = true;
        }

    })

    return toReturn;

}


