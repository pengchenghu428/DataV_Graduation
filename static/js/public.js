$(function(){
    var HOST_PATH = "10.193.0.20:5000"

	$(".callbox").hover(function(){
		$(".call_num").stop().fadeIn();
	},function(){
		$(".call_num").stop().fadeOut();
	})

	$(".wxbox").hover(function(){
		$(".wxpic").stop().fadeIn();
	},function(){
		$(".wxpic").stop().fadeOut();
	})

})
