jQuery(document).ready(function () {
	jQuery("#pick_btn").click(function(){	
		if(jQuery("#group_count").val()=='')
		{
			alert("请先填写分组数量.");
			jQuery("#error_msg").html("<span class=\"error\">请先填写分组数量.</span>");
			return;
		}
		else{
			jQuery("#error_msg").html("");
		}
		
		var club_member_dispatch_flag = false
		if(jQuery("#club_member_dispatch_flag").get(0).checked==true)
		{
			club_member_dispatch_flag = true
		}
		
		var gender_dispatch_flag = false
		if(jQuery("#gender_dispatch_flag").get(0).checked==true)
		{
			gender_dispatch_flag = true
		}
		
		jQuery.ajax({
			type: "post",
			url: "/pick",
			data: { group_count: jQuery("#group_count").val(), club_member_dispatch_flag: club_member_dispatch_flag, gender_dispatch_flag: gender_dispatch_flag},
			success: function (data) {
				jQuery("#pick_result").html(data);
			},
			error: function () {
				alert("请求失败，请稍后重试");
			}
		});
	});
	
	jQuery("#group_pick_btn").click(function(){
		jQuery("#group_random_pick_div").show();
		jQuery("#pick_result").html("");
	});
	
	jQuery("#pair_pick_btn").click(function(){
		jQuery("#group_random_pick_div").hide();
		jQuery("#pick_result").html("");
		jQuery.ajax({
			type: "post",
			url: "/pair_pick",
			data: {},
			success: function (data) {
				jQuery("#pick_result").html(data);
			},
			error: function () {
				alert("请求失败，请稍后重试");
			}
		});
	});
	
	jQuery("#add_expense_btn").click(function(){	
		if(jQuery("#act_member_count").val()=='')
		{
			alert("请先填写参加人数.");
			jQuery("#error_msg").html("<span class=\"error\">请先填写参加人数.</span>");
			return;
		}
		else{
			jQuery("#error_msg").html("");
		}
		
		if(jQuery("#act_total_cost").val()=='')
		{
			alert("请先填写报销金额.");
			jQuery("#error_msg").html("<span class=\"error\">请先填写报销金额.</span>");
			return;
		}
		else{
			jQuery("#error_msg").html("");
		}
		
		if(jQuery("#act_date").val()=='')
		{
			alert("请先填写活动时间.");
			jQuery("#error_msg").html("<span class=\"error\">请先填写活动时间.</span>");
			return;
		}
		else{
			jQuery("#error_msg").html("");
		}
		
		jQuery.ajax({
			type: "post",
			url: "/interest_group_expense",
			data: { act_member_count: jQuery("#act_member_count").val(),
					act_total_cost: jQuery("#act_total_cost").val() * 100,
					act_date: jQuery("#act_date").val(),
					group_id: jQuery("#group_id").val()},
			success: function (data) {
				jQuery("#add_result").html(data);
			},
			error: function () {
				alert("请求失败，请稍后重试");
			}
		});
	});
})