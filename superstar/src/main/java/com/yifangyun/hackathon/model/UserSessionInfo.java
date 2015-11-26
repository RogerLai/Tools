package com.yifangyun.hackathon.model;

import com.egeio.core.log.MyUUID;
import com.google.gson.annotations.SerializedName;
import io.netty.channel.Channel;

/**
 * Created by think on 2015/7/31.
 * This class defines the information stored in a session for user
 */
public class UserSessionInfo {
    private transient MyUUID sessionID;

    @SerializedName("user_id") private int userID;

    @SerializedName("user_name") private String userName;

    public UserSessionInfo(int userID, String userName,
            Channel channel) {
        //user userID-deviceID in UUID
        this.sessionID = new MyUUID(String.format("%s-%s", userID, channel));
        this.userID = userID;
        this.userName = userName;
    }

    public MyUUID getSessionID() {
        return sessionID;
    }

    public int getUserID() {
        return userID;
    }

    public String getUserName(){
        return userName;
    }

}
