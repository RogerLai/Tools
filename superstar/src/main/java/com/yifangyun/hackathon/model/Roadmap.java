package com.yifangyun.hackathon.model;

import java.util.ArrayList;

import com.google.gson.annotations.SerializedName;

public class Roadmap {
    @SerializedName("status_list")
    private ArrayList<Integer> statusList;
    
    @SerializedName("task_list")
    private ArrayList<Task> taskList;
    
    @SerializedName("reward_level")
    private int rewardLevel;
    
    public Roadmap(ArrayList<Integer> sList, ArrayList<Task> tList){
        this.statusList = sList;
        this.taskList = tList;
        this.rewardLevel = 1;
    }
    
    public ArrayList<Task> getTaskList(){
        return this.taskList;
    }
    
    public ArrayList<Integer> getStatusList(){
        return this.statusList;
    }
}
