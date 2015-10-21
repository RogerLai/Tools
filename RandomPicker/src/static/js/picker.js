jQuery(document).ready(function () {
	jQuery("#pick_btn").click(function(){	
		if(jQuery("#group_count").val()=='')
		{
			alert("请先填写分组数量.");
			jQuery("#error_msg").html("<span class=\"error\">请先填写分组数量.</span>");
			return;
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
			type: "get",
			url: "/pick?group_count="+jQuery("#group_count").val()+"&club_member_dispatch_flag="+club_member_dispatch_flag+"&gender_dispatch_flag="+gender_dispatch_flag,
			success: function (data) {
				jQuery("#pick_result").html(data);
			},
			error: function () {
				alert("请求失败，请稍后重试");
			}
		});
	});
})