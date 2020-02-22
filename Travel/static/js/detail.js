function beforeSubmit(form) {
    // 人数判断
    if(form.travel_count.value<=0){
    alert('人数不能少于1，请重新输入！');
    form.travel_count.focus();
    return false;}

    // 电话号码判断
    if(form.travel_number.value.length!=11){
        alert('电话号码的长度无效，请重新输入！');
        form.travel_number.focus();
        return false;
    }
    else {
        var Number=/^[1][3,4,5,7,8][0-9]{9}$/;
        if (!Number.test(form.travel_number.value)){
            alert('无效号码，请重新输入！');
            form.travel_number.focus();
            return false;
        }
    }
    // 日期判断
    var date_now = new Date();
    var year = date_now.getFullYear();
	//得到当前月份
	//  1：js中获取Date中的month时，会比当前月份少一个月，所以这里需要先加一
	//  2: 判断当前月份是否小于10，如果小于，那么就在月份的前面加一个 '0' ， 如果大于，就显示当前月份
	var month = date_now.getMonth()+1 < 10 ? "0"+(date_now.getMonth()+1) : (date_now.getMonth()+1);
	//得到当前日子（多少号）
	var date = date_now.getDate() < 10 ? "0"+date_now.getDate() : date_now.getDate();


    // var date2 =date_now.getFullYear()+'-'+(date_now.getMonth()+1)+'-'+date_now.getDate()
    var date2 = year+'-'+month+'-'+date
    if(form.travel_data.value<date2){
        alert(form.travel_data.value+'日期不能少于当前日期，请重新输入！'+date2);
        form.travel_data.focus();
        return false;}
}
