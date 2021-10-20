$(document).ready(function(){
	$('.other__accordion').click(function() {
		$(this).toggleClass('active');
		let info = $(this).next()[0];
		if (info.style.maxHeight){
		info.style.maxHeight = null;
		} else {
		info.style.maxHeight = info.scrollHeight + "px";
		}
	});

});



