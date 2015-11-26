package com.yifangyun.hackathon.model;

import com.google.gson.annotations.SerializedName;

public class Task {
    @SerializedName("task_id")
    private int id;
    
    @SerializedName("task_name")
    private String name;
    
    @SerializedName("task_status")
    private int status;
    
    @SerializedName("worker_id")
    private int workerId;
    
    @SerializedName("start_status_id")
    private int startStatusId;
    
    @SerializedName("end_status_id")
    private int endStatusId;
    
    public Task(int tid, String tname, int workerId, int startStatusId, int endStatusId)
    {
        this.id = tid;
        this.name = tname;
        this.setWorkerId(workerId);
        this.setStartStatusId(startStatusId);
        this.setEndStatusId(endStatusId);
        
        status = TaskStatus.CREATED;
    }
    
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getStatus() {
        return status;
    }
    public void setStatus(int status) {
        this.status = status;
    }
    public int getId() {
        return id;
    }
    public void setId(int id) {
        this.id = id;
    }

    public int getWorkerId() {
        return workerId;
    }

    public void setWorkerId(int workerId) {
        this.workerId = workerId;
    }

    public int getEndStatusId() {
        return endStatusId;
    }

    public void setEndStatusId(int endStatusId) {
        this.endStatusId = endStatusId;
    }
    
    public int getStartStatusId() {
        return startStatusId;
    }

    public void setStartStatusId(int startStatusId) {
        this.startStatusId = startStatusId;
    }
    
    
}
