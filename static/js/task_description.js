district_select = document.getElementById('district');
oo_select = document.getElementById('oo');
parallel_select = document.getElementById('parallel');
subject_select = document.getElementById('subject');
task_select = document.getElementById('task');
report_select = document.getElementById('report');


fetch('get_districts').then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (district of data.districts) {
                                optionHTML += '<option value="' + district.id+'">' + district.name + '</option>'
                        }
                        district_select.innerHTML = optionHTML;

                        if (district_select.length == 1){
                                district_select.defaultSelected = district_select[0];
                                district_select.onchange();
                        }
                        else{
                                district_select.value = "";
                        }

                });
});



district_select.onchange = function(){
        parallel_select.innerHTML = "";
        subject_select.innerHTML = "";
        report_select.innerHTML = "";

        district = district_select.value;
        fetch('oo/' + district).then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (oo of data.oo) {
                                optionHTML += '<option value="' + oo.id+'">' + oo.name + '</option>'
                        }
                        oo_select.innerHTML = optionHTML;

                        if (oo_select.length == 1){
                                oo_select.defaultSelected = oo_select[0];
                                oo_select.onchange();
                        }
                        else{
                                 oo_select.value = "";
                        }

                });
        });
};
oo_select.onchange = function(){

        subject_select.innerHTML = "";
        report_select.innerHTML = "";

        oo = oo_select.value;
        if (oo == "all" && district_select.value != "all"){
               fetch('parallels_for_district/' + district_select.value).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (parallel of data.parallels) {
                                        optionHTML += '<option value="' + parallel.id+'">' + parallel.name + '</option>'
                                }
                                parallel_select.innerHTML = optionHTML;
                                parallel_select.value = "";
                        });
                }); 
        }else{
                fetch('parallels/' + oo).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (parallel of data.parallels) {
                                        optionHTML += '<option value="' + parallel.id+'">' + parallel.name + '</option>'
                                }
                                parallel_select.innerHTML = optionHTML;
                                parallel_select.value = "";
                        });
                });
        }

};


parallel_select.onchange = function(){
        report_select.innerHTML = "";

        parallel = parallel_select.value;
        if (district_select.value == "all" || oo_select.value == "all"){
                 fetch('all_subjects/' + parallel).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (subject of data.subjects) {
                                        optionHTML += '<option value="' + subject.id+'">' + subject.name + '</option>'
                                }
                                subject_select.innerHTML = optionHTML;
                                subject_select.value = "";
                        });
                });
        }else{
                fetch('subjects/' + parallel).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (subject of data.subjects) {
                                        optionHTML += '<option value="' + subject.id+'">' + subject.name + '</option>'
                                }
                                subject_select.innerHTML = optionHTML;
                                subject_select.value = "";
                        });
                });
        };
};


subject_select.onchange = function(){
id_oo = oo_select.value;
parallel = parallel_select.value;
id_subject = subject_select.value;
fetch('/api/task_description/get_task_numbers/' + id_oo + '/' + parallel + '/' + id_subject).then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (task of data.task_numbers) {
                                optionHTML += '<option value="' + task.id+'">' + task.name + '</option>'
                        }
                        task_select.innerHTML = optionHTML;
                        task_select.value = "";
                });
        });
};


task_select.onchange = function(){
task_number = task_select.value;
fetch('/api/task_description/get_reports/' + task_number).then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (report of data.reports) {
                                optionHTML += '<option value="' + report.id+'">' + report.name + '</option>'
                        }
                        report_select.innerHTML = optionHTML;
                        report_select.value = "";
                });
        });
};





$(document).ready(function(){
        $("#submit_btn").click(function(){

                var id_district = $('#district').val();
                var id_oo = $('#oo').val();
                var id_oo_parallels = $('#parallel').val();
                var id_oo_parallels_subjects = $('#subject').val();
                var id_task = $('#task').val();
                var id_report = $('#report').val();


                var sendInfo = {
                district: {
                        'id': id_district,
                        "name": $( "#district option:selected" ).text()
                        },

                oo:     {
                        'id': id_oo,
                        "name": $( "#oo option:selected" ).text()
                        },

                parallel: {
                                'id': id_oo_parallels,
                                "name": $( "#parallel option:selected" ).text()
                        },

                subject: {
                        'id': id_oo_parallels_subjects,
                        "name": $( "#subject option:selected" ).text()
                         },

                tusk: {
                        'id': id_task,
                        "name": $( "#task option:selected" ).text()
                         }, 

                report: {
                        'id': id_report,
                        "name": $( "#report option:selected" ).text()
                        }
                };
        $(".error").remove();
    if(id_district == null || id_oo == null || id_oo_parallels == null || id_oo_parallels_subjects == null || id_report == null) {
               if (id_district == null){
                district_select.style.border = "2px solid red"
               } else {
                    district_select.style.border = "2px solid #7ecd7e"

               }
               if (id_oo == null){
                       oo_select.style.border = "2px solid red"
               } else {
                    oo_select.style.border = "2px solid #7ecd7e"

               }

               if (id_oo_parallels == null){
                       parallel_select.style.border = "2px solid red"
               } else {
                    parallel_select.style.border = "2px solid #7ecd7e"

               }


               if (id_oo_parallels_subjects == null){
                       subject_select.style.border = "2px solid red"
               } else {
                    subject_select.style.border = "2px solid #7ecd7e"

               }

               if (id_task == null){
                       task_select.style.border = "2px solid red"
               } else {
                    task_select.style.border = "2px solid #7ecd7e"

               }

               if (id_report == null){
                       report_select.style.border = "2px solid red"
               } 
        }else {
        district_select.style.border = "";
                oo_select.style.border = "";
                parallel_select.style.border = "";
                subject_select.style.border = "";
                task_select.style.border = "";
                report_select.style.border = "";
                $("#submit_btn").attr("disabled", true);
                $.ajax({
                type : 'POST',
                url : "/vpr_analysis",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(sendInfo),

                success: function(data){
                        marker = JSON.stringify(data);
                        var jsonObj = JSON.parse(marker);
                        $(".TwoPage").remove();
                        $("#submit_btn").attr("disabled", false);

        },
        error:function(){
                        alert("Ошибка сервера");
                        $("#submit_btn").attr("disabled", false);
        },
                        });
    };
        });
});

$(document).ready(function(){
        $("#clear_btn").click(function(){
                $(".error").remove();
                $(".TwoPage").remove();
        district_select.style.border = ""
                oo_select.style.border = ""
                parallel_select.style.border = ""
                subject_select.style.border = ""
                report_select.style.border = ""
                parallel_select.innerHTML = "";
                subject_select.innerHTML = "";
                task_select.style.border = "";
                report_select.innerHTML = "";

                district = district_select.value;
                fetch('oo/' + district).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (oo of data.oo) {
                                        optionHTML += '<option value="' + oo.id+'">' + oo.name + '</option>'
                                }
                                oo_select.innerHTML = optionHTML;
                                oo_select.value = "";
                        });
                });
        });
});
