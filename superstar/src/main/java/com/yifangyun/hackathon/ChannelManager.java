package com.yifangyun.hackathon;

import com.egeio.core.log.Logger;
import com.egeio.core.log.LoggerFactory;
import com.egeio.core.log.MyUUID;
import com.yifangyun.hackathon.model.UserSessionInfo;
import com.yifangyun.hackathon.utils.LogUtils;
import io.netty.channel.Channel;
import io.netty.util.AttributeKey;

import java.util.ArrayList;
import java.util.Collection;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Created by think on 2015/7/31.
 * This class manages all the information for each user channel
 */
public class ChannelManager {
    private static Logger logger = LoggerFactory
            .getLogger(ChannelManager.class);
    private static MyUUID uuid = new MyUUID();

    private static final AttributeKey<UserSessionInfo> userSessionKey = AttributeKey
            .valueOf("userSessionInfo");
    private static final ConcurrentHashMap<Long, ArrayList<Channel>> userChannelMapping = new ConcurrentHashMap<Long, ArrayList<Channel>>();

    private static synchronized void setUserSessionInfoInChannel(
            Channel channel, UserSessionInfo info) {
        channel.attr(userSessionKey).set(info);
    }

    private static UserSessionInfo getUserSessionInfoFromChannel(
            Channel channel) {
        return channel.attr(userSessionKey).get();
    }

    public static MyUUID getUserSessionIDFromChannel(Channel channel) {
        UserSessionInfo info = channel.attr(userSessionKey).get();
        if (info == null) {
            return null;
        }
        return info.getSessionID();
    }

    /**
     * add user-channel into the mapping
     *
     * @param info    user session info
     * @param channel user channel
     */
    public static void addUserChannel(UserSessionInfo info, Channel channel)
            throws Exception {
        long userID = info.getUserID();
        if (userChannelMapping.get(userID) == null) {
            userChannelMapping.put(userID, new ArrayList<Channel>());
        }
        setUserSessionInfoInChannel(channel, info);
        userChannelMapping.get(userID).add(channel);

        LogUtils.logSessionInfo(logger, channel,
                "Added to the cache: user {}", userID);
    }

    /**
     * remover user-channel from mapping
     *
     * @param channel user channel
     */
    public static void removeUserChannel(Channel channel) throws Exception {
        UserSessionInfo info = getUserSessionInfoFromChannel(channel);
        if (channel.attr(userSessionKey).get() == null) {
            return;
        }
        LogUtils.logSessionInfo(logger, channel,
                "Try to remove user channel from mapping");
        ArrayList<Channel> session = userChannelMapping.get(info.getUserID());
        if (session == null) {
            LogUtils.logSessionInfo(logger, channel,
                    "cannot find user channel in mapping");
            return;
        }
        LogUtils.logSessionInfo(logger, channel,
                "channel removed from mapping");
        userChannelMapping.get(info.getUserID()).remove(channel);
        if (userChannelMapping.get(info.getUserID()).isEmpty()) {
            userChannelMapping.remove(info.getUserID());            
            LogUtils.logSessionInfo(logger, channel,
                    "Removed from cache: user {}", info.getUserID());
        }
    }

    public static void displayUserChannelMapping() {
        logger.info(uuid, "Current User Channel Mapping: {}",
                userChannelMapping);
    }

    public static long getOnlineUserNum() {
        return userChannelMapping.size();
    }
    
    public static ArrayList<Channel> getAllChannels() {
        ArrayList<Channel> result = new ArrayList<Channel>();
        Collection<ArrayList<Channel>> list = userChannelMapping.values();
        for (ArrayList<Channel> itemList : list){
            for (Channel item: itemList){
                result.add(item);
            }
        }
        return result;
    }

    public static Collection<Channel> getChannelByUserID(long userID) {
        if (userChannelMapping.get(userID) != null) {
            return userChannelMapping.get(userID);
        }
        return new ArrayList<Channel>();
    }
}
