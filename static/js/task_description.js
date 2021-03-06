year_select = document.getElementById('year');
district_select = document.getElementById('district');
oo_select = document.getElementById('oo');
parallel_select = document.getElementById('parallel');
subject_select = document.getElementById('subject');
task_select = document.getElementById('task');
report_select = document.getElementById('report');

fetch('/api/select/task_description/get_year/').then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (year of data.year) {
                                optionHTML += '<option value="' + year.id+'">' + year.name + '</option>'
                        }
                        year_select.innerHTML = optionHTML;

                        if (year_select.length == 1){
                                year_select.defaultSelected = year_select[0];
                                year_select.onchange();
                        }
                        else{
                                year_select.value = "";
                        }

                });
});

year_select.onchange = function(){
    district_select.innerHTML = "";
    oo_select.innerHTML = "";
    parallel_select.innerHTML = "";
    subject_select.innerHTML = "";
    task_select.innerHTML = "";
    report_select.innerHTML = "";
    year = year_select.value;
    fetch('api/select/get_districts/?filter_year_id=' + year).then(function(response){
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
};


district_select.onchange = function(){
        parallel_select.innerHTML = "";
        subject_select.innerHTML = "";
        task_select.innerHTML = "";
        report_select.innerHTML = "";
        year = year_select.value;
        district = district_select.value;
        fetch('api/select/get_oo/?filter_year_id=' + year + "&filter_district_id=" + district).then(function(response){
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
        task_select.innerHTML = "";
        report_select.innerHTML = "";
        year = year_select.value;
        district = district_select.value;
        oo = oo_select.value;
        fetch('api/select/get_parallels/?filter_year_id='+ year + "&filter_district_id="+ district + "&filter_oo_id=" + oo).then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (parallel of data.parallels) {
                                optionHTML += '<option value="' + parallel.id+'">' + parallel.name + '</option>'
                        }
                        parallel_select.innerHTML = optionHTML;
                        parallel_select.value = "";
                });
        });


};


parallel_select.onchange = function(){
        task_select.innerHTML = "";
        report_select.innerHTML = "";
        year = year_select.value;
        district = district_select.value;
        oo = oo_select.value;
        parallel = parallel_select.value;

        fetch('api/select/get_subjects/?filter_year_id='+ year + '&filter_district_id=' + district + '&filter_oo_id=' + oo + '&filter_parallel_id=' + parallel).then(function(response){
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


subject_select.onchange = function(){
        task_select.innerHTML = "";
        report_select.innerHTML = "";
        year = year_select.value;
        id_oo = oo_select.value;
        parallel = parallel_select.value;
        id_subject = subject_select.value;
        fetch('/api/select/task_description/get_task_numbers/?filter_year_id='+ year + '&filter_oo_id=' + id_oo + '&filter_parallel_id=' + parallel + '&filter_subject_id=' + id_subject).then(function(response){
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
fetch('/api/select/task_description/get_reports/?filter_task_number=' + task_number).then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (report of data.reports) {
                                optionHTML += '<option value="' + report.id+'">' + report.name + '</option>'
                        }
                        report_select.innerHTML = optionHTML;
                        if (report_select.length == 1){
                                report_select.defaultSelected = report_select[0];
                        }
                        else{
                                report_select.value = "";
                        }
                });
        });
};

function draw_report(report_type, json_data){
        if (report_type == 4){
                createTable_type_4(json_data);  
        }
        if (report_type == 5){
                createTable_type_5(json_data);  
        }
};

function createTable_type_5(jsonObj){

  let body = document.getElementById('report_place');
  let section = document.createElement('section');
  section.className = "TwoPage";
  section.id = "report_section";
  let container = document.createElement('div');
  container.className = "container_report";
  container.id = "report_container";
  let div = document.createElement('div');
  div.className = "TwoPage__wrapper";
  let title = document.createElement('h3');
  title.className = "TwoPage__wrapper_title scroll-title";
  let names = jsonObj.table_settings.titles;

  let btn = document.createElement('a');
  btn.className = "upload mdi mdi-download";

  let btn_url = "/api/export/?" + "filter_report_id=" + report_select.value  + "&filter_report_name=" + $( "#report option:selected" ).text() + "&filter_district_id=" + district_select.value +
  "&filter_district_name=" + $( "#district option:selected" ).text() + "&filter_oo_id=" + oo_select.value + "&filter_oo_name=" + $( "#oo option:selected" ).text() + "&filter_parallel_id=" + parallel_select.value +
  "&filter_parallel_name=" +  $( "#parallel option:selected" ).text() + "&filter_task_id=" + task_select.value + "&filter_task_name=" + $( "#task option:selected" ).text() +
  "&filter_subject_id=" + subject_select.value + "&filter_subject_name=" + $( "#subject option:selected" ).text() + "&filter_year_id=" + year_select.value + 
  "&filter_year_name=" + $( "#year option:selected" ).text();
  btn.setAttribute("href", btn_url);
  let col_span = Object.keys(jsonObj.values_array).length
  if (col_span == 3){
        var keys = ["all", "district", "oo"]
  }
  if (col_span == 2){
        var keys = ["all", "district"]
  }
  if (col_span == 1){
        var keys = ["all"]
  }

  
  let text = document.createTextNode('???????????????? ?????????????????????? ?????????????????????????? ????????????????????');
  let tbl = document.createElement('table');
  tbl.className = "scroll";
  let tbdy = document.createElement('tbody');
  
  for ([task, dict_values] of Object.entries(jsonObj["values_array"]["all"]["values"])){
        
        let titles = ["???", "????????????, ???????? ????????????????????????", "?????????????? ??????????????????", "???????????????????????? ????????"]
        let values_for_titles = [dict_values["task_number_from_kim"], dict_values["text"], dict_values["level"], dict_values["max_mark"]]
        for (var i = 0; i < titles.length; i++){
                var tr = document.createElement('tr');
                var td = document.createElement('td');
                td.className = "textLeft";
                td.appendChild(document.createTextNode(titles[i]));
                tr.appendChild(td);

                var td = document.createElement('td');
                td.width = "85%";
                td.className = "textLeft";
                //td.style.setProperty("text-align", "justify", "important");
                td.style.paddingRight = "5px";
                
                td.colSpan = col_span;
                td.appendChild(document.createTextNode(values_for_titles[i]));
                tr.appendChild(td);
                tbdy.appendChild(tr);
        }
        let ks_row_span = dict_values["ks"].length;
        let kt_row_span = dict_values["kt"].length;
        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.className = "textLeft";
        td.rowSpan = ks_row_span;
        td.appendChild(document.createTextNode("?????????????????????? ???????????????? ????????????????????"));
        tr.appendChild(td);
        var td = document.createElement('td');
        td.className = "textLeft";
        td.colSpan = col_span;
        td.appendChild(document.createTextNode(1+ ") " + dict_values["ks"][0]));
        tr.appendChild(td);
        tbdy.appendChild(tr);
        if (ks_row_span > 1){
                for (var i=1; i<ks_row_span; i++){
                        var tr = document.createElement('tr');
                        var td = document.createElement('td');
                        td.className = "textLeft";
                        td.colSpan = col_span;
                        td.appendChild(document.createTextNode(i + 1 +") " + dict_values["ks"][i]));
                        tr.appendChild(td);
                        tbdy.appendChild(tr);
                }
        }

        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.className = "textLeft";
        td.rowSpan = kt_row_span;
        td.appendChild(document.createTextNode("?????????????????????? ????????????????????"));
        tr.appendChild(td);
        var td = document.createElement('td');
        td.className = "textLeft";
        td.colSpan = col_span;
        td.appendChild(document.createTextNode(1+ ") " + dict_values["kt"][0]));
        tr.appendChild(td);
        tbdy.appendChild(tr);
        if (kt_row_span > 1){
                for (var i=1; i<kt_row_span; i++){
                        var tr = document.createElement('tr');
                        var td = document.createElement('td');
                        td.className = "textLeft";
                        td.colSpan = col_span;
                        
                        td.appendChild(document.createTextNode(i + 1 + ") " + dict_values["kt"][i]));
                        tr.appendChild(td);
                        tbdy.appendChild(tr);
                }
        }
        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.className = "textLeft";
        tr.appendChild(td);
        for (name of names){
                var td = document.createElement('td');
                td.className = "textWeight";
                td.appendChild(document.createTextNode(name));
                tr.appendChild(td);
        }
        tbdy.appendChild(tr);
        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.className = "textLeft";
        td.appendChild(document.createTextNode("?????????????????? ??????-????"));
        tr.appendChild(td);
        for (key of keys){
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(jsonObj.values_array[key].values[task].values["??????????????????"]["count"]));
                tr.appendChild(td);
        }
        tbdy.appendChild(tr);

        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.className = "textLeft";
        td.appendChild(document.createTextNode("???? ?????????????????? ??????-????"));
        tr.appendChild(td);
        for (key of keys){
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(jsonObj["values_array"][key]["values"][task]["values"]["???? ??????????????????"]["count"]));
                tr.appendChild(td);
        }
        tbdy.appendChild(tr);

        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.className = "textLeft";
        td.appendChild(document.createTextNode("?????????????????? ?? %"));
        tr.appendChild(td);
        for (key of keys){
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(jsonObj["values_array"][key]["values"][task]["values"]["??????????????????"]["%"]));
                tr.appendChild(td);
        }
        tbdy.appendChild(tr);

        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.className = "textLeft";
        td.appendChild(document.createTextNode("???? ?????????????????? %"));
        tr.appendChild(td);
        for (key of keys){
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(jsonObj["values_array"][key]["values"][task]["values"]["???? ??????????????????"]["%"]));
                tr.appendChild(td);
        }
        tbdy.appendChild(tr);
  }
  title.appendChild(text);
  div.appendChild(title);
  tbl.appendChild(tbdy);
  div.appendChild(tbl);
  div.appendChild(btn);
  container.appendChild(div);
  section.appendChild(container);
  body.appendChild(section);
  window.getComputedStyle(div).opacity;
  div.className +=" in";
  return tbl;
};

function createTable_type_4(jsonObj){

  let body = document.getElementById('report_place');
  let section = document.createElement('section');
  section.className = "TwoPage";
  section.id = "report_section";
  let container = document.createElement('div');
  container.className = "container_report";
  container.id = "report_container";
  let div = document.createElement('div');
  div.className = "TwoPage__wrapper";
  let title = document.createElement('h3');
  title.className = "TwoPage__wrapper_title scroll-title";
  let titles_list = jsonObj.table_settings.titles;

  let btn = document.createElement('a');
  btn.className = "upload mdi mdi-download";

 let btn_url = "/api/export/?" + "filter_report_id=" + report_select.value  + "&filter_report_name=" + $( "#report option:selected" ).text() + "&filter_district_id=" + district_select.value +
  "&filter_district_name=" + $( "#district option:selected" ).text() + "&filter_oo_id=" + oo_select.value + "&filter_oo_name=" + $( "#oo option:selected" ).text() + "&filter_parallel_id=" + parallel_select.value +
  "&filter_parallel_name=" +  $( "#parallel option:selected" ).text() + "&filter_task_id=" + task_select.value + "&filter_task_name=" + $( "#task option:selected" ).text() +
  "&filter_subject_id=" + subject_select.value + "&filter_subject_name=" + $( "#subject option:selected" ).text() + "&filter_year_id=" + year_select.value + 
  "&filter_year_name=" + $( "#year option:selected" ).text();

  btn.setAttribute("href", btn_url);
  let text = document.createTextNode('???????????????? ?????????????????????? ?????????????????????????? ????????????????????');
  let tbl = document.createElement('table');
  tbl.className = "scroll";
  let tbdy = document.createElement('tbody');

  var tr = document.createElement('tr');
  tr.className = "adhesive";
  for (var i=0; i<3; i++){
         var td = document.createElement('td');
         td.rowSpan = "2";
         td.appendChild(document.createTextNode(titles_list[i]));
         tr.appendChild(td);

  }
  var tr2 = document.createElement('tr');
  for (var i=3; i<titles_list.length; i++){
         var td = document.createElement('td');
         td.colSpan = "4";
         td.appendChild(document.createTextNode(titles_list[i]));
         tr.appendChild(td);
         for (category of ["?????????????????? ??????-????", "???? ?????????????????? ??????-????", "?????????????????? ?? %", "???? ?????????????????? ?? %"]){
                var td2 = document.createElement('td');
                //td2.style.minWidth = "120px";
                //td2.style.verticalAlign = "top";
                //td2.style.paddingTop = "5px";
                td2.className = "task-title__small";
                td2.appendChild(document.createTextNode(category));
                tr2.appendChild(td2);
         }
  }

  tbdy.appendChild(tr);
  tbdy.appendChild(tr2);
  for (var i = 1; i < Object.keys(jsonObj.values_array.all.values).length + 1; i++){
          var td = document.createElement('td');
          var tr = document.createElement('tr');
          if (i % 2 == 0) {
            tr.className = "dark"
          } else {
             tr.className = "white"
          };
          td.appendChild(document.createTextNode(jsonObj.values_array.all.values[i].task_number_from_kim));
          tr.appendChild(td);

          var td = document.createElement('td');
          //td.style.textAlign = "left";
          //td.style.minWidth = "460px";
          td.className = "mobiles";
          td.appendChild(document.createTextNode(jsonObj.values_array.all.values[i].text));
          tr.appendChild(td);

          var td = document.createElement('td');
          td.appendChild(document.createTextNode(jsonObj.values_array.all.values[i].max_mark));
          tr.appendChild(td);
          td.style.minWidth = "90px";


          var td = document.createElement('td');
          td.appendChild(document.createTextNode(jsonObj.values_array.all.values[i].values["??????????????????"]["count"]));
          tr.appendChild(td);

          var td = document.createElement('td');
          td.appendChild(document.createTextNode(jsonObj.values_array.all.values[i].values["???? ??????????????????"]["count"]));
          tr.appendChild(td);

          var td = document.createElement('td');
          td.appendChild(document.createTextNode(jsonObj.values_array.all.values[i].values["??????????????????"]["%"]));
          tr.appendChild(td);

          var td = document.createElement('td');
          td.appendChild(document.createTextNode(jsonObj.values_array.all.values[i].values["???? ??????????????????"]["%"]));
          tr.appendChild(td);
          if (Object.keys(jsonObj.values_array).length > 1){
                  var td = document.createElement('td');
                  td.appendChild(document.createTextNode(jsonObj.values_array.district.values[i].values["??????????????????"]["count"]));
                  tr.appendChild(td);

                  var td = document.createElement('td');
                  td.appendChild(document.createTextNode(jsonObj.values_array.district.values[i].values["???? ??????????????????"]["count"]));
                  tr.appendChild(td);

                  var td = document.createElement('td');
                  td.appendChild(document.createTextNode(jsonObj.values_array.district.values[i].values["??????????????????"]["%"]));
                  tr.appendChild(td);

                  var td = document.createElement('td');
                  td.appendChild(document.createTextNode(jsonObj.values_array.district.values[i].values["???? ??????????????????"]["%"]));
                  tr.appendChild(td);
          }
          if (Object.keys(jsonObj.values_array).length > 2){
                  var td = document.createElement('td');
                  td.appendChild(document.createTextNode(jsonObj.values_array.oo.values[i].values["??????????????????"]["count"]));
                  tr.appendChild(td);

                  var td = document.createElement('td');
                  td.appendChild(document.createTextNode(jsonObj.values_array.oo.values[i].values["???? ??????????????????"]["count"]));
                  tr.appendChild(td);

                  var td = document.createElement('td');
                  td.appendChild(document.createTextNode(jsonObj.values_array.oo.values[i].values["??????????????????"]["%"]));
                  tr.appendChild(td);

                  var td = document.createElement('td');
                  td.appendChild(document.createTextNode(jsonObj.values_array.oo.values[i].values["???? ??????????????????"]["%"]));
                  tr.appendChild(td);
          }
          tbdy.appendChild(tr); 
  }
  title.appendChild(text);
  div.appendChild(title);
  tbl.appendChild(tbdy);
  div.appendChild(tbl);
  div.appendChild(btn);
  container.appendChild(div);
  section.appendChild(container);
  body.appendChild(section);
  window.getComputedStyle(div).opacity;
  div.className +=" in";
  return tbl;
};


$(document).ready(function(){
        $("#submit_btn").click(function(){
                var year = $('#year').val();
                var id_district = $('#district').val();
                var id_oo = $('#oo').val();
                var id_oo_parallels = $('#parallel').val();
                var id_oo_parallels_subjects = $('#subject').val();
                var id_task = $('#task').val();
                var id_report = $('#report').val();


                var sendInfo = {
                year: {
                        'id': year,
                        "name": $( "#year option:selected" ).text()
                        },
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

                task: {
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
                url : "/task_description",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(sendInfo),

                success: function(data){
                        marker = JSON.stringify(data);
                        var jsonObj = JSON.parse(marker);
                        $(".TwoPage").remove();
                        draw_report(id_report, jsonObj);
                        $("#submit_btn").attr("disabled", false);

        },
        error:function(){
                        alert("???????????? ??????????????");
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
                district_select.innerHTML = "";
                oo_select.innerHTML = "";
                parallel_select.innerHTML = "";
                subject_select.innerHTML = "";
                task_select.innerHTML = "";
                report_select.innerHTML = "";
                year_select.innerHTML = "";

                fetch('api/select/get_year/').then(function(response){
                    response.json().then(function(data) {
                        optionHTML = '';
                        for (year of data.year) {
                                optionHTML += '<option value="' + year.id+'">' + year.name + '</option>'
                        }
                        year_select.innerHTML = optionHTML;

                        if (year_select.length == 1){
                                year_select.defaultSelected = year_select[0];
                                year_select.onchange();
                        }
                        else{
                                year_select.value = "";
                        }
                    });
                });
        });
});
