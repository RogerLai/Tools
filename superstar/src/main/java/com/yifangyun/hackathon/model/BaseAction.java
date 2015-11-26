package com.yifangyun.hackathon.model;

import com.google.gson.annotations.SerializedName;

/**
 * This is the base entity class of actions
 * 
 * @author rogerlai
 * @date 2014/12/08
 */

public class BaseAction {
    @SerializedName("task_id")
    protected int taskId;
    
    @SerializedName("status_id")
    protected int statusId;
    
    @SerializedName("status_info")
    protected int statusInfo;
    
    @SerializedName("percentage")
    protected int percentage;

    public BaseAction(int taskId, int statusId, int statusInfo) {
        this.statusInfo = statusInfo;
        this.statusId = statusId;
        this.taskId = taskId;
        this.percentage = 0;
    }
    
    public BaseAction(int taskId, int statusId, int statusInfo, int percent) {
        this.statusInfo = statusInfo;
        this.statusId = statusId;
        this.taskId = taskId;
        this.percentage = percent;
    }
}
