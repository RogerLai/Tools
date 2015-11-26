package com.yifangyun.hackathon.model;

import com.google.gson.annotations.SerializedName;

/**
 * This is the base entity class of responses
 *
 * @author rogerlai
 * @date 2014/12/08
 */

public class BaseResponse {
    @SerializedName("status_code") private int statusCode;

    @SerializedName("action_type") private int actionTypeId;

    @SerializedName("action_info") private Object actionInfo;

    @SerializedName("error_message") private String errorMessage;

    public BaseResponse(int action, int statusCode) {
        this.actionTypeId = action;
        this.statusCode = statusCode;
    }
    
    public void setActionType(int type) {
        this.actionTypeId = type;
    }
    
    public void setActionInfo(Object info) {
        this.actionInfo = info;
    }

    public void setStatusCode(int code) {
        this.statusCode = code;
    }

    public void setErrorMessage(String message) {
        this.errorMessage = message;
    }
}
