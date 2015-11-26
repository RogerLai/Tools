package com.yifangyun.hackathon;

import static io.netty.handler.codec.http.HttpMethod.GET;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import com.egeio.core.log.Logger;
import com.egeio.core.log.LoggerFactory;
import com.egeio.core.log.MyUUID;
import com.egeio.core.utils.GsonUtils;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.yifangyun.hackathon.model.ActionType;
import com.yifangyun.hackathon.model.BaseAction;
import com.yifangyun.hackathon.model.BaseResponse;
import com.yifangyun.hackathon.model.Roadmap;
import com.yifangyun.hackathon.model.Task;
import com.yifangyun.hackathon.model.TaskStatus;
import com.yifangyun.hackathon.model.UserSessionInfo;
import com.yifangyun.hackathon.utils.LogUtils;

import io.netty.channel.Channel;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http.FullHttpRequest;
import io.netty.handler.codec.http.HttpRequest;
import io.netty.handler.codec.http.websocketx.CloseWebSocketFrame;
import io.netty.handler.codec.http.websocketx.PingWebSocketFrame;
import io.netty.handler.codec.http.websocketx.TextWebSocketFrame;
import io.netty.handler.codec.http.websocketx.WebSocketFrame;
import io.netty.handler.codec.http.websocketx.WebSocketServerHandshaker;
import io.netty.handler.codec.http.websocketx.WebSocketServerHandshakerFactory;
import io.netty.util.AttributeKey;

/**
 * Created by think on 2015/7/31.
 * This class is the key of the real-time server, it handles http request and establish webSocket connection,
 * perform different action according to the types of action
 */
public class WebSocketHandler extends SimpleChannelInboundHandler<Object> {
    private int port;

    private static Logger logger = LoggerFactory
            .getLogger(WebSocketHandler.class);
    private static MyUUID uuid = new MyUUID();

    //status code
    private static final int OK_STATUS_CODE = 0;
    private static final int FAILED_STATUS_CODE = 1;
    private static final int INVALID_ACTION_STATUS_CODE = 2;

    private WebSocketServerHandshaker handShaker;
    private static final String WEBSOCKET_PATH = "/websocket";
    
    private static int rewardLevel;
    private static int finishedTaskCount;
    private static ArrayList<Task> tasks = new ArrayList<Task>();
    private static ArrayList<Integer> statusList = new ArrayList<Integer>();
    private static Map<Integer, Integer> statusIdToInfoMapping = new HashMap<Integer, Integer>();
    private static Map<Integer, Task> taskIdToTaskMapping = new HashMap<Integer, Task>();
    private static Map<Integer, ArrayList<Task>> statusIdToTasksMapping = new HashMap<Integer, ArrayList<Task>>();
    
    private static final AttributeKey<UserSessionInfo> userSessionKey = AttributeKey
            .valueOf("userSessionInfo");
    
    static {
        finishedTaskCount = 0;
                
        statusList.add(0);
        statusList.add(1);
        statusList.add(2);
        statusList.add(3);
        statusList.add(4);
        statusList.add(5);
        statusList.add(6);
        statusList.add(7);
        
        statusIdToInfoMapping.put(0, TaskStatus.CREATED);
        statusIdToInfoMapping.put(1, TaskStatus.CREATED);
        statusIdToInfoMapping.put(2, TaskStatus.CREATED);
        statusIdToInfoMapping.put(3, TaskStatus.CREATED);
        statusIdToInfoMapping.put(4, TaskStatus.CREATED);
        statusIdToInfoMapping.put(5, TaskStatus.CREATED);
        statusIdToInfoMapping.put(6, TaskStatus.CREATED);
        statusIdToInfoMapping.put(7, TaskStatus.CREATED);
        
        Task taskItem = new Task(1, "后台基础框架搭建", 2, 0, 1);
        Task taskItem2 = new Task(2, "前端基础框架搭建", 1, 0, 1);
        Task taskItem3 = new Task(3, "界面初步设计", 1, 0, 2);
        Task taskItem4 = new Task(4, "完成界面框架", 3, 0, 2);
        Task taskItem5 = new Task(5, "完成后台功能", 3, 2, 3);
        Task taskItem6 = new Task(6, "完成前端功能", 2, 1, 4);
        Task taskItem7 = new Task(7, "提供素材和交互", 1, 1, 5);
        Task taskItem8 = new Task(8, "与designer确定设计", 1, 1, 3);
        Task taskItem9 = new Task(9, "交付后台代码", 2, 4, 7);
        Task taskItem10 = new Task(10, "完成前端功能", 1, 5, 7);
        Task taskItem11 = new Task(11, "完成详细设计", 3, 3, 6);
        Task taskItem12 = new Task(12, "提供素材", 3, 6, 7);
        
        tasks.add(taskItem);
        tasks.add(taskItem2);
        tasks.add(taskItem3);
        tasks.add(taskItem4);
        tasks.add(taskItem5);
        tasks.add(taskItem6);
        tasks.add(taskItem7);
        tasks.add(taskItem8);
        tasks.add(taskItem9);
        tasks.add(taskItem10);
        tasks.add(taskItem11);
        tasks.add(taskItem12);
        
        for (Task task:tasks) {  
            if (statusIdToTasksMapping.get(task.getEndStatusId()) == null) {
                ArrayList<Task> taskList = new ArrayList<Task>();
                statusIdToTasksMapping.put(task.getEndStatusId(), taskList);
            }
            statusIdToTasksMapping.get(task.getEndStatusId()).add(task);            
            taskIdToTaskMapping.put(task.getId(), task);
        }
    }

    public WebSocketHandler(int port) {
        this.port = port;        
    }

    @Override
    protected void messageReceived(ChannelHandlerContext channelHandlerContext,
            Object o) throws Exception {
        if (o instanceof HttpRequest) {
            //HTTP request
            logger.info(uuid, "receive user http request");
            handleHttp(channelHandlerContext, (FullHttpRequest) o);
        }
        else {
            //WebSocket frame
            logger.info(uuid, "receive user websocket frame");
            handleWebSocket(channelHandlerContext, (WebSocketFrame) o);
        }
    }

    /**
     * remove channel from mapping when channel is inactive
     *
     * @param ctx channel context
     * @throws Exception
     */
    @Override public void channelInactive(ChannelHandlerContext ctx)
            throws Exception {
        //        LogUtils.logSessionInfo(logger, ctx.channel(), "channel inactive");
        ChannelManager.removeUserChannel(ctx.channel());
        super.channelInactive(ctx);
    }

    /**
     * remove channel from mapping when channel is unregistered
     *
     * @param ctx channel context
     * @throws Exception
     */
    @Override public void channelUnregistered(ChannelHandlerContext ctx)
            throws Exception {
        //        LogUtils.logSessionInfo(logger, ctx.channel(), "channel unregistered");
        ChannelManager.removeUserChannel(ctx.channel());
        super.channelUnregistered(ctx);
    }

    /**
     * handle http request
     * 1. The http request sent before webSocket establishment
     * 2. The http request sent by HAProxy for load balance
     * 3. The http request sent by EventProcessor to hint new info to push to client
     *
     * @param channelHandlerContext channel context
     * @param request               request sent from client
     * @throws Exception
     */
    private void handleHttp(ChannelHandlerContext channelHandlerContext,
            FullHttpRequest request) throws Exception {
        if (request.method() == GET) {
            if (request.uri().equals(WEBSOCKET_PATH) || request.uri()
                    .equals("/")) {
                //handshake
                WebSocketServerHandshakerFactory wsFactory = new WebSocketServerHandshakerFactory(
                        getWebSocketLocation(), null, true);
                handShaker = wsFactory.newHandshaker(request);
                if (handShaker == null) {
                    WebSocketServerHandshakerFactory
                            .sendUnsupportedVersionResponse(
                                    channelHandlerContext.channel());
                }
                else {
                    handShaker.handshake(channelHandlerContext.channel(),
                            request);
                }
            }
        }
    }

    /**
     * Get webSocket location
     *
     * @return webSocket location
     */
    private String getWebSocketLocation() {
        String protocol = "ws";
        String uri = null;
        try {
            uri = String.format("%s://%s:%s%s", protocol,
                    "", port, WEBSOCKET_PATH);
        }
        catch (Exception e) {
            logger.error(uuid, e, "failed to get the ip address, exit");
            System.exit(-1);
        }
        return uri;
    } 

    /**
     * parse webSocket frame, get the content and perform the correct action
     *
     * @param channelHandlerContext channel context
     * @param frame                 webSocket frame
     * @throws Exception
     */
    private void handleWebSocket(ChannelHandlerContext channelHandlerContext,
            WebSocketFrame frame) throws Exception {
        Gson gson = GsonUtils.getGson();
        Channel channel = channelHandlerContext.channel();
        if (frame instanceof CloseWebSocketFrame) {
            //user closing channel
            LogUtils.logSessionInfo(logger, channel,
                    "Channel closed from client");

            //remove the channel from mapping
            ChannelManager.removeUserChannel(channel);

            handShaker.close(channelHandlerContext.channel(),
                    (CloseWebSocketFrame) frame.retain());
            return;
        }
        else if (frame instanceof PingWebSocketFrame) {
            channel.writeAndFlush(
                    new PingWebSocketFrame(frame.content().retain()));
            return;
        }
        else if (!(frame instanceof TextWebSocketFrame)) {
            throw new UnsupportedOperationException(
                    String.format("%s frame types not supported",
                            frame.getClass().getName()));
        }

        String req = ((TextWebSocketFrame) frame).text();
        String res;
        JsonObject reqJson = gson.fromJson(req, JsonObject.class);
        BaseResponse baseRes = new BaseResponse(
                reqJson.get("action_type").getAsInt(), OK_STATUS_CODE);
        try {
            LogUtils.logSessionInfo(logger, channel, "Channel received {}", reqJson);
            
            int actionTypeId = reqJson.get("action_type").getAsInt();
            int taskId;
            int receiverId;
            int workerId;
            int statusId;
            int percent;
            Collection<Channel> channels;
            BaseResponse response;
            switch (actionTypeId) {
            case ActionType.ACTION_LOGIN:
                String userName = reqJson.get("action_info").getAsString();
                doLogin(userName, channel);
                break;
            case ActionType.ACTION_GET_ROADMAP:
                response = new BaseResponse(actionTypeId, OK_STATUS_CODE);
                Roadmap map = new Roadmap(statusList, tasks);
                response.setActionInfo(map);
                res = gson.toJson(response);
                if (res != null) {
                    channel.writeAndFlush(new TextWebSocketFrame(res));
                }
                return;
            case ActionType.ACTION_SET_REWARD:
                if (!isLeader(channel)) {
                    baseRes.setStatusCode(INVALID_ACTION_STATUS_CODE);
                    baseRes.setErrorMessage("invalid action");
                    return;
                }
                
                rewardLevel = reqJson.get("action_info").getAsInt();
                
                // should notify all others
                channels = ChannelManager.getAllChannels();
                for (Channel ch:channels) {
                    BaseResponse actions = new BaseResponse(actionTypeId, OK_STATUS_CODE);
                    actions.setActionInfo(rewardLevel);
                    if (!ch.isOpen()) {
                        continue;
                    }
                    ch.writeAndFlush(new TextWebSocketFrame(GsonUtils.getGson().toJson(actions)));
                }
                break;                
            case ActionType.ACTION_DONE:
                taskId = reqJson.get("action_info").getAsInt();
                Task currentTask = taskIdToTaskMapping.get(taskId);
                
                // check if any other tasks to the same status
                if (statusIdToTasksMapping.get(currentTask.getEndStatusId()).size() == 1) {
                    taskIdToTaskMapping.get(taskId).setStatus(TaskStatus.ACCEPTED);
                    statusIdToInfoMapping.put(currentTask.getEndStatusId(), TaskStatus.ACCEPTED);
                    finishedTaskCount ++;
                }
                else {
                    taskIdToTaskMapping.get(taskId).setStatus(TaskStatus.DONE);
                }                
                
                percent = (finishedTaskCount * 100) / tasks.size();
                ArrayList<Task> taskList = statusIdToTasksMapping.get(currentTask.getEndStatusId());
                statusId = currentTask.getEndStatusId();                    
                int statusInfo = statusIdToInfoMapping.get(statusId);
                
                for (Task t:taskList) {
                    receiverId = t.getWorkerId();
                    if (receiverId == getCurrentUserId(channel)) {
                        continue;
                    }
                                        
                    channels = ChannelManager.getChannelByUserID(receiverId);
                    for (Channel ch:channels) {
                        response = new BaseResponse(actionTypeId, OK_STATUS_CODE);                        
                        BaseAction actionInfo = new BaseAction(taskId, statusId, statusInfo, percent);
                        response.setActionInfo(actionInfo);
                        if (!ch.isOpen()) {
                            continue;
                        }
                        ch.writeAndFlush(new TextWebSocketFrame(GsonUtils.getGson().toJson(response)));
                    }
                }
                
                break;
            case ActionType.ACTION_ACCEPTED:
                taskId = reqJson.get("action_info").getAsInt();
                workerId = taskIdToTaskMapping.get(taskId).getWorkerId();
                statusId = taskIdToTaskMapping.get(taskId).getEndStatusId();
                
                currentTask = taskIdToTaskMapping.get(taskId);
                taskIdToTaskMapping.get(taskId).setStatus(TaskStatus.ACCEPTED);
                
                taskList = statusIdToTasksMapping.get(currentTask.getEndStatusId());
                
                // check if all tasks related to this status are accepted
                boolean flag = true;
                for (Task t:taskList) {
                    if (t.getStatus() != TaskStatus.ACCEPTED){
                        flag = false;
                        break;
                    }
                }
                
                if (flag == true) {
                    finishedTaskCount ++;
                    statusIdToInfoMapping.put(statusId, TaskStatus.ACCEPTED);
                }
                else {
                    break;
                }
                
                percent = (finishedTaskCount * 100) / tasks.size();
                channels = ChannelManager.getAllChannels();
                for (Channel ch:channels) {
                    response = new BaseResponse(actionTypeId, OK_STATUS_CODE);
                    BaseAction actions = new BaseAction(taskId, statusId, statusIdToInfoMapping.get(statusId), percent);
                    response.setActionInfo(actions);
                    if (!ch.isOpen()) {
                        continue;
                    }
                    ch.writeAndFlush(new TextWebSocketFrame(GsonUtils.getGson().toJson(response)));
                }
                break;
            case ActionType.ACTION_REJECTED:
                taskId = reqJson.get("action_info").getAsInt();
                workerId = taskIdToTaskMapping.get(taskId).getWorkerId();
                statusId = taskIdToTaskMapping.get(taskId).getEndStatusId();
                taskIdToTaskMapping.get(taskId).setStatus(TaskStatus.REJECTED);
                
                channels = ChannelManager.getChannelByUserID(workerId);
                for (Channel ch:channels) {
                    response = new BaseResponse(actionTypeId, OK_STATUS_CODE);
                    BaseAction actions = new BaseAction(taskId, statusId, statusIdToInfoMapping.get(statusId));
                    response.setActionInfo(actions);
                    if (!ch.isOpen()) {
                        continue;
                    }
                    ch.writeAndFlush(new TextWebSocketFrame(GsonUtils.getGson().toJson(response)));
                }
                break;                    

            default:
                baseRes.setStatusCode(INVALID_ACTION_STATUS_CODE);
                baseRes.setErrorMessage("invalid action");
                break;
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            baseRes.setStatusCode(FAILED_STATUS_CODE);
        }

        res = gson.toJson(baseRes);
        if (res != null) {
            channel.writeAndFlush(new TextWebSocketFrame(res));
        }

    }
   
    private boolean isLeader(Channel channel) {
        boolean result = false;
        if (getUserSessionInfoFromChannel(channel).getUserID() == 4) {
            result = true;
        }
        return result;
    }
    
    private int getCurrentUserId(Channel channel) {
        UserSessionInfo info = getUserSessionInfoFromChannel(channel);
        return info.getUserID();
    }
    
    private synchronized void setUserSessionInfoInChannel(
            Channel channel, UserSessionInfo info) {
        channel.attr(userSessionKey).set(info);
    }
    
    private UserSessionInfo getUserSessionInfoFromChannel(
            Channel channel) {
        return channel.attr(userSessionKey).get();
    }
    
    /**
     * add user channel into mapping
     *
     * @param json    json object sent by client
     * @param channel user channel
     * @throws Exception
     */
    private void doLogin(String userName, Channel channel) throws Exception {
        int userId = 0; 
        if (userName.equals("frontend"))
        {
            userId = 1;
        }
        else if (userName.equals("backend"))
        {
            userId = 2;
        }
        else if (userName.equals("designer"))
        {
            userId = 3;
        }
        else if (userName.equals("leader"))
        {
            userId = 4;
        }
        
        UserSessionInfo info = new UserSessionInfo(userId, userName, channel);
        setUserSessionInfoInChannel(channel, info);
        ChannelManager.addUserChannel(info, channel);
        LogUtils.logSessionInfo(logger, channel,
                "Add user {} channel into mapping", info.getUserID());
    }
}
