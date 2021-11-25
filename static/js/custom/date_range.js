function updatedate(){
    var startdate= $('#startdate').val()
    var enddate= $('#enddate').val()
    if (startdate == '' || enddate == ''){
        return toastr.error('invalid date')
    }
    console.log(startdate, enddate)
    $('#start_date').val(startdate)
    $('#end_date').val(enddate)
}


