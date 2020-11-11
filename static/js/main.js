$(function(){
	$(".map iframe").load(function() {
		$(".map .loader").css("display", "none")
	})
	function navbar(){
		var j;
		var lilegth = $(".nav li").length;
		for(j=0;j<=lilegth;j++){
			if($(".nav li").eq(j).hasClass("active"))
				return j;
		}
	}
	var first = navbar();
	initnav();
	function initnav(){
		var active = navbar();
		if($(window).width()>768){
		$(".navBg").css("left",(first-1)*90);
		$(".navBg").css("top",0);
		}
		else{
		$(".navBg").css("left",0);
		$(".navBg").css("top",(first-1)*40);
		}
	}
	$(window).resize(function(){
		initnav();
	})
	$(".nav li").mouseenter(function(){
		var i = $(this).index();
		$(".nav li").eq(i).addClass("active");
		$(".nav li").eq(i).siblings().removeClass("active");
		if($(window).width()>768){
		$(".navBg").css("top",0);
		$(".navBg").css("left",(i-1)*90);
		}
		else{
		$(".navBg").css("top",(i-1)*40);
		$(".navBg").css("left",0);
		}
	});
	$(".nav li").mouseleave(function(){
		$(".nav li").eq(first).addClass("active");
		$(".nav li").eq(first).siblings().removeClass("active");
		if($(window).width()>768){
		$(".navBg").css("left",(first-1)*90);
		$(".navBg").css("top",0);
		}
		else{
		$(".navBg").css("left",0);
		$(".navBg").css("top",(first-1)*40);
		
		}
	});
	function scrollauto(){
		var scrollTop = $(window).scrollTop();
		if(scrollTop>=20){
			$(".nav").addClass("scrollNav");
			$(".navbar").addClass("scrollNavbar");
			$(".logo").addClass("scrollLogo");
			$(".navbar-toggle").addClass("scorllNavtol");
		}
		else{
			$(".nav").removeClass("scrollNav");
			$(".navbar").removeClass("scrollNavbar");
			$(".logo").removeClass("scrollLogo");
			$(".navbar-toggle").removeClass("scorllNavtol");
		}
	}
	scrollauto();
	$(window).scroll(function(){
		scrollauto();
	});
})
