let tg = window.Telegram.WebApp;

let height = document.documentElement.scrollHeight;
let width = document.documentElement.scrollWidth;

tg.expand();

let cost_from=50000,cost_to=15000000;

$("#slider2").ionRangeSlider({
    type: "double",
    skin:"round",
    min: 50000,
    max: 15000000,
    from: 50000,
    to: 15000000,
    step: 1000,
	postfix: '$',
	hide_min_max: true,
    onFinish: function (data) {
    		cost_from=data.from;
    		cost_to=data.to;
    },

});


$("#slider1").ionRangeSlider({
    type: "double",
    skin:"round",
    min: 50000,
    max: 1236000,
    from: 50000,
    to: 15000000,
    step: 1000,
	postfix: '$',
	hide_min_max: true,
    onFinish: function (data) {
    		cost_from=data.from;
    		cost_to=data.to;
    },

});


active = 1;
$(".inner").appendTo($(".container"));
let p = $(".inner2").detach();


function SendData(){
		let data='';
		if (document.getElementById("bt1").checked==1) data+='new_building ';
		if (document.getElementById("bt2").checked==1) data+='from_the_owner ';
		if (document.getElementById("bt2").checked!=1 && document.getElementById("bt1").checked!=1) data+='new_building from_the_owner ';
		data+=cost_from+' '+cost_to+' ';
		if (document.getElementById("el1").checked==1) data+='Dubai ';
		if (document.getElementById("el5").checked==1) data+='apartment ';
		if (document.getElementById("el2").checked==1) data+='townhouse ';
		if (document.getElementById("el6").checked==1) data+='villa ';
		if (document.getElementById("el7").checked==1) data+='studio ';
		if (document.getElementById("el8").checked==1) data+='1-k ';
		if (document.getElementById("el9").checked==1) data+='2-k ';
		if (document.getElementById("el10").checked==1) data+='3-k ';
		if (document.getElementById("el11").checked==1) data+='4-k ';
		if (document.getElementById("el12").checked==1) data+='5-k ';
		if (document.getElementById("el13").checked==1) data+='6-k ';
		if (document.getElementById("el13").checked==1) data+='7-k ';
		console.log(data);
		tg.sendData(data);
}

