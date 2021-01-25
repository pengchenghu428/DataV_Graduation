$(function(){
	// 右下角联系悬浮动画
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

	// 切换月视图
	$(".data_dimension_switch").click(function () {
		var cur_url = window.location.href;
		var new_url = cur_url.replace('year', 'month');
		window.open(new_url, '_blank');
	})
	
	// 时钟刷新
	setInterval(function () {
		var date = new Date();
		var d1 = date.toLocaleString();
		$(".data_time").text(d1);
	}, 1000)

})

