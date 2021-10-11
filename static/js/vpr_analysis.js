name_of_the_settlement_select = document.getElementById('name_of_the_settlement');
oo_select = document.getElementById('oo');
parallel_select = document.getElementById('parallel');
subject_select = document.getElementById('subject');

fetch('get_districts').then(function(response){
		response.json().then(function(data) {
			optionHTML = '';
			for (district of data.districts) {
				optionHTML += '<option value="' + district.id+'">' + district.name + '</option>'
			}
			name_of_the_settlement_select.innerHTML = optionHTML;
			name_of_the_settlement_select.value = "Выбрать";
		});
});



name_of_the_settlement_select.onchange = function(){
	parallel_select.innerHTML = "Выбрать";
	subject_select.innerHTML = "Выбрать";

	name_of_the_settlement = name_of_the_settlement_select.value;
	fetch('oo/' + name_of_the_settlement).then(function(response){
		response.json().then(function(data) {
			optionHTML = '';
			for (oo of data.oo) {
				optionHTML += '<option value="' + oo.id+'">' + oo.name + '</option>'
			}
			oo_select.innerHTML = optionHTML;
			oo_select.value = "Выбрать";
		});
	});
};

oo_select.onchange = function(){
	
	subject_select.innerHTML = "Выбрать";
	oo = oo_select.value;
	fetch('parallels/' + oo).then(function(response){
		response.json().then(function(data) {
			optionHTML = '';
			for (parallel of data.parallels) {
				optionHTML += '<option value="' + parallel.id+'">' + parallel.name + '</option>'
			}
			parallel_select.innerHTML = optionHTML;
			parallel_select.value = "Выбрать";
		});
	});
};

parallel_select.onchange = function(){
	
	parallel = parallel_select.value;
	fetch('subjects/' + parallel).then(function(response){
		response.json().then(function(data) {
			optionHTML = '';
			for (subject of data.subjects) {
				optionHTML += '<option value="' + subject.id+'">' + subject.name + '</option>'
			}
			subject_select.innerHTML = optionHTML;
			subject_select.value = "Выбрать";
		});
	});
};



$(document).ready(function(){
	$("#submit_btn").click(function(){
		var sendInfo = {
			name_of_the_settlement : name_of_the_settlement_select.value,
           	oo : oo_select.value,
           	parallel : parallel_select.value,
           	subject: subject_select.value
       };
		$.ajax({
		  type : 'POST',
		  url : "/vpr_analysis",
		  contentType: "application/json; charset=utf-8",
		  data: JSON.stringify(sendInfo),
		  success: function(data){
		  	marker = JSON.stringify(data);

        	},
		});
 	});
});
