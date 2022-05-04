year_select = document.getElementById('year');
parallel_select = document.getElementById('parallel');
subject_select = document.getElementById('subject');
report_select = document.getElementById('report');
var map = L.map('map').fitWorld();
var report_was_created = false;

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
//    maxZoom: 20,
//    subdomains:['mt0','mt1','mt2','mt3']
//});
//googleStreets.addTo(map);
map.setView(new L.LatLng(52.61558902526749, 83.57275390625), 7);


$.getJSON("static/js/districts.json", function(json) {
    for(district of json){
        var name = district.name
        var coordinates = district.coordinates
        for (coord of coordinates){
            var polygon = L.polygon(coord, {color: "green", "name": name});
            polygon.bindTooltip(name,
               {permanent: false, direction: "center"}
            ).openTooltip()
            polygon.addTo(map);
            polygon.on('click', async function () {
                if (report_was_created){
                    console.log("click:", this.options);
		    deleteLayers(L.Marker)
		    var data = await getSchoolsCoordinates(this);
                    for (school of data.schools){
                        await create_marker(
                            school.name,
                            school.value,
                            school.color,
                            school.oo_login,
                            school.coordinates,
                            school.district,
                            school.text
                        );
                    };
                };
            });
        };
    };
});

function getSchoolsCoordinates(polygon){
    send_data = {
            id_year: polygon.options.id_year,
            id_parallels: polygon.options.id_parallels,
            id_subjects: polygon.options.id_subjects,
            id_report: polygon.options.id_report,
            district_name: polygon.options.name
        }
    return $.ajax({
        type : 'GET',
        url :"api/select/map/get_schools_coordinates/",
        data: send_data
    });
};


function getVPR(district_name, id_year, id_parallels, id_subjects, id_report){
    send_data = {
        year: {
            'id': id_year,
            "name": $( "#year option:selected" ).text()
        },
        district: {
            "name": district_name
        },

        parallel: {
            'id': id_parallels,
            "name": $( "#parallel option:selected" ).text()
        },

        subject: {
            'id': id_subjects,
            "name": $( "#subject option:selected" ).text()
        },
        report: {
            'id': id_report,
            "name": $( "#report option:selected" ).text()
        }
    };
    return $.ajax({
        type : 'POST',
        url : "/map",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(send_data)
    });
};

$(document).ready(function(){
    $("#submit_btn").click(function(){
        var arr = [];
        var id_year = $('#year').val();
        var id_parallels = $('#parallel').val();
        var id_subjects = $('#subject').val();
        var id_report = $('#report').val();
        if(id_year == null || id_parallels == null || id_subjects == null || id_report == null) {
            if (id_year == null){
                year_select.style.border = "2px solid red"
            }
            else{
                year_select.style.border = "2px solid #7ecd7e"
            }
            if (id_parallels == null){
                parallel_select.style.border = "2px solid red"
            }
            else{
                parallel_select.style.border = "2px solid #7ecd7e"
            }
            if (id_subjects == null){
                subject_select.style.border = "2px solid red"
            }
            else{
                subject_select.style.border = "2px solid #7ecd7e"
            }
            if (id_report == null){
                report_select.style.border = "2px solid red"
            }
        }
        else {
            year_select.style.border = "";
            parallel_select.style.border = "";
            subject_select.style.border = "";
            report_select.style.border = "";
            map.eachLayer(async function(layer) {
                if (layer instanceof L.Polygon){
			var data = await getVPR(
                        layer.options.name,
                        id_year,
                        id_parallels,
                        id_subjects,
                        id_report
                    );
                    if (data.status == 200){
                        layer.setStyle({color: data.color});
                        layer.options.id_year = id_year;
                        layer.options.id_parallels = id_parallels;
                        layer.options.id_subjects = id_subjects;
                        layer.options.id_report = id_report;
			if (data.value === "Не участвовал"){
                            var title = "<p>" + data.name + "</p>" +
                                    "<p>" + data.value.toString() + "</p>";
                        }
                        else {
                            var title = "<p>" + data.name + "</p>" +
                                    "<p>" + data.text + data.value.toString() + "</p>";
                        }

                        layer.bindPopup(title, {
                            autoClose:false
                        });

                        layer.on('click', function(e){
                            layer.openPopup(e.latlng);
                        });
                    };
                }
                else if (layer instanceof L.Popup){
                    map.removeLayer(layer)
                }
                else if (layer instanceof L.Marker){
                    map.removeLayer(layer)
                }
            });
            report_was_created = true;
        };
    });
});


function create_marker(name, value, color, oo_login, coordinates, district, text){
    var marker = L.marker(coordinates, {
        "name": name,
        "value": value,
        'color': color,
        "oo_login": oo_login,
        "coordinates": coordinates,
        "district": district,
        "text": text
    });
    if (marker.options.value == "Не участвовал"){
        var text = "<p>" + marker.options.district + "</p>" + 
            "<p>" + marker.options.name + "</p>" +
            "<p>" + marker.options.value.toString() + "</p>";
    }
    else {
        var text = "<p>" + marker.options.district + "</p>" +
            "<p>" + marker.options.name + "</p>" +
            "<p>" + marker.options.text + marker.options.value.toString() + "</p>";
    }
    marker.bindPopup(text, {autoClose:false});

    marker.on('click', function(){
        // console.log(this.options);
        marker.openPopup();
    });
    marker.addTo(map);
};

function deleteLayers(LayerType){
    map.eachLayer(async function(layer) {
        if (layer instanceof LayerType){
            map.removeLayer(layer);
        };
    })
};


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

year_select.onchange = function(){
    parallel_select.innerHTML = "";
    subject_select.innerHTML = "";
    report_select.innerHTML = "";
    year = year_select.value;
    fetch('api/select/map/get_parallels/?filter_year_id=' + year).then(function(response){
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
        report_select.innerHTML = "";
        year = year_select.value;
        parallel = parallel_select.value;

        fetch('api/select/map/get_subjects/?filter_year_id='+ year + '&filter_parallel_id=' + parallel).then(function(response){
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
fetch('api/select/map/get_reports').then(function(response){
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
