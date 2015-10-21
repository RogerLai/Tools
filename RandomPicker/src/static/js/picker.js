jQuery(document).ready(function () {
	jQuery("#pick_btn").click(function(){	
		if(jQuery("#group_count").val()=='')
		{
			alert("请先填写分组数量.");
			jQuery("#error_msg").html("<span class=\"error\">请先填写分组数量.</span>");
			return;
		}
		
		jQuery.ajax({
			type: "get",
			url: "/pick?group_count="+jQuery("#group_count").val()+"&club_member_dispatch_flag="+jQuery("#club_member_dispatch_flag").val(),
			success: function (data) {
				jQuery("#pick_result").html(data);
			},
			error: function () {
				alert("请求失败，请稍后重试");
			}
		});
	});
})