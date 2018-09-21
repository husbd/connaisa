var db;
$(document).ready(function() {
	db = firebase.database();
	$(".category").change(setSubject);
});

var count=[1, 1];
var group=['Provide', 'Learn'];

function preReg() {
	var rules = {
		rules: {
			pre_name: {
				required: true
			},
			pre_email: {
				required: true,
				email: true
			},
			rev: {
				number: true
			},
			wil: {
				number: true
			}
		},
		errorPlacement: function (error, element) {
            var name = $(element).attr("name");
            error.appendTo($("#" + name + "_validation"));
        },
        submitHandler: function(form) {
        	var name=$("#preRegName").val();
			var email=$("#preRegEmail").val();
			var age=$("#age").val();
			var gender=$("#preRegGender").val();
			var country=$("#preRegCountry").val();
			var language=$("#preRegLanguage").val();
			var revenue=$("#rev").val();
			var pay=$("#wil").val();
			var message=$("#preRegMessage").val();
			var key=
			db.ref('regLists/').push({
				name: name,
				email: email,
				age: age,
				gender: gender,
				country: country,
				language: language,
				revenue: revenue,
				pay: pay,
				message: message
			}).key;
			for(var i=1; i<=count[0]; i++) {
				if($("#subjectProvide"+i).val()) {
					db.ref('regLists/'+key+"/subjectProvide").push({
						subject: $("#subjectProvide"+i).val(),
						description: $("#descriptionProvide"+i).val()
					});
				}
			}
			for(var i=1; i<=count[1]; i++) {
				if($("#subjectLearn"+i).val()) {
					db.ref('regLists/'+key+"/subjectLearn").push({
						subject: $("#subjectLearn"+i).val(),
						description: $("#descriptionLearn"+i).val()
					});
				}
			}
			$("#preRegSendmessage").show();
			$("input, textarea, select").val("");
        }
	};
	$("#preRegForm").validate(rules);


}

function contactSubmit() {
	var rules = {
		rules: {
			con_name: {
				required: true
			},
			con_email: {
				required: true,
				email: true
			}
		},
		errorPlacement: function (error, element) {
            var name = $(element).attr("name");
            error.appendTo($("#" + name + "_validation"));
        },
        submitHandler: function(form) {
        	var name=$("#contactName").val();
			var email=$("#contactEmail").val();
			var message=$("#contactMessage").val();
			var contact_type = document.getElementsByName('contact-type');
			var type="";
			for(var i=0; i<contact_type.length; i++) {
				if(contact_type[i].checked) {
					type = contact_type[i].value
				}
			}
			var key=
			db.ref('contact/').push({
				name: name,
				email: email,
				message: message,
				type: type
			}).key;
			$("#contactSendmessage").show();
			$("input, textarea, select").val("");
        }
	};
	$("#contact-form").validate(rules);
}

function sponsorSubmit() {
	var rules = {
		rules: {
			sp_name: {
				required: true
			},
			sp_email: {
				required: true,
				email: true
			}
		},
		errorPlacement: function (error, element) {
            var name = $(element).attr("name");
            error.appendTo($("#" + name + "_validation"));
        },
        submitHandler: function(form) {
        	var name=$("#spName").val();
			var email=$("#spEmail").val();
			var message=$("#spMessage").val();
			var key=
			db.ref('sponsor/').push({
				name: name,
				email: email,
				message: message
			}).key;

			$("#sponsorSendmessage").show();
			$("input, textarea, select").val("");
        }
	};
	$("#sponsor-form").validate(rules);
}

function addRow(i) {
	count[i]+=1;
	content=
	'<div class="row" id="'+group[i]+count[i]+'">\
		<div class="col-xs-6 col-sm-3 col-md-3">\
			<select class="form-control category" name="category'+group[i]+'" id="category'+group[i]+count[i]+'">\
				<option selected disabled hidden style="display: none" value=""></option>\
				<option value="art">Art</option>\
				<option value="language">Language</option>\
				<option value="academic">Academic</option>\
				<option value="living">Living</option>\
				<option value="sports">Sports</option>\
				<option value="other">Other</option>\
			</select>\
		</div>\
		<div class="col-xs-6 col-sm-3 col-md-3">\
			<select class="form-control" name="subject'+group[i]+'" id="subject'+group[i]+count[i]+'">\
				<option selected disabled hidden style="display: none" value=""></option>\
			</select>\
		</div>\
		<div class="col-xs-8 col-sm-4 col-md-4">\
			<input type="text" name="description'+group[i]+'" class="form-control" id="description'+group[i]+count[i]+'"/>\
		</div>\
	</div>';
	$("#subject"+group[i]+"Group").append(content);
	$(".category").change(setSubject);
}

function removeRow(i) {
	if(count[i]>1) {
		$("#"+group[i]+count[i]).remove();
		count[i]--;
	}
}

function setSubject(event) {
	var $dropdown = $(this);
	var subjectID="#"+$(this).attr('id').replace("category", "subject");
	$.getJSON("jsondata/data.json", function(data) {

	    var key = $dropdown.val();
	    var vals = [];
	              
	    switch(key) {
	      case 'art':
	        vals = data.art.split(",");
	        break;
	      case 'language':
	        vals = data.language.split(",");
	        break;
	      case 'academic':
	        vals = data.academic.split(",");
	        break;
	      case 'living':
	        vals = data.living.split(",");
	        break;
	      case 'sports':
	        vals = data.sports.split(",");
	        break;
	      case 'other':
	        vals = ['Please specify'];
	        break;
	    }
	    
	    var $secondChoice = $(subjectID);
	    $secondChoice.empty();
	    $.each(vals, function(index, value) {
	      $secondChoice.append("<option>" + value + "</option>");
	    });

	});
}