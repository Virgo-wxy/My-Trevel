function custom(form) {
        // 日期判断
    var date_now = new Date();
    var year = date_now.getFullYear();
	var month = date_now.getMonth()+1 < 10 ? "0"+(date_now.getMonth()+1) : (date_now.getMonth()+1);
	var date = date_now.getDate() < 10 ? "0"+date_now.getDate() : date_now.getDate();
	var date2 = year+'-'+month+'-'+date
    if(form.cf_date.value<date2){
        alert(form.cf_date.value+'日期不能少于当前日期，请重新输入！'+date2);
        form.cf_date.focus();
        return false;}

    if(form.travel_data.value<=0){
        alert('人数不能少于1，请重新输入！');
        form.travel_data.focus();
        return false;
    }
    if(form.travel_days.value<=0){
        alert('旅行天数不能少于1，请重新输入！');
        form.travel_days.focus();
        return false;
    }


        // 电话号码判断
    if(form.number.length!=11){
        alert('电话号码的长度无效，请重新输入！');
        form.number.focus();
        return false;
    }
    else {
        var Number=/^[1][3,4,5,7,8][0-9]{9}$/;
        if (!Number.test(form.number.value)){
            alert('无效号码，请重新输入！');
            form.number.focus();
            return false;
        }
    }
}