// Metin2Dream
// 993e8173b607753ca6b1222609c5d486

$(document).ready(function(){	
													 
	$("#scSlider").easySlider({
		auto: false, 
		continuous: true,
	});
	
	$("#nSlider").easySlider({
		auto: true, 
		continuous: true,
		numeric: true,
	});
	
	$("#itemSlider").easySlider({
		auto: false, 
		continuous: true,
	});	
	
	// -------------------------------------------------------
	// Fading
	// -------------------------------------------------------
	
	$(function (){      
			$('#navbar a,.bar,.islider a img,.special-btn,.btn,.bplus').hover(function() {  
					$(this).stop().animate({opacity: 0.7}, 'fast');
			},
			function(){
					$(this).stop().animate({opacity: 1}, 'fast' );
			});
	});
	
});	