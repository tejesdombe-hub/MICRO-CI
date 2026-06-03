package com.fooddelivery.common.messaging.idempotency;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

@Component
@Slf4j
public class IdempotencyHandler {

    private final ConcurrentMap<String, ProcessedMessage> processedMessages = new ConcurrentHashMap<>();
    private static final long MESSAGE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

    public boolean isMessageProcessed(String messageId) {
        ProcessedMessage processed = processedMessages.get(messageId);
        
        if (processed == null) {
            return false;
        }

        // Check if message has expired
        if (System.currentTimeMillis() - processed.getTimestamp() > MESSAGE_TTL_MS) {
            processedMessages.remove(messageId);
            return false;
        }

        log.info("Duplicate message detected: messageId={}", messageId);
        return true;
    }

    public void markMessageAsProcessed(String messageId) {
        ProcessedMessage processed = new ProcessedMessage(messageId, System.currentTimeMillis());
        processedMessages.put(messageId, processed);
        log.debug("Message marked as processed: messageId={}", messageId);
    }

    public void cleanupExpiredMessages() {
        long now = System.currentTimeMillis();
        processedMessages.entrySet().removeIf(entry -> {
            boolean expired = now - entry.getValue().getTimestamp() > MESSAGE_TTL_MS;
            if (expired) {
                log.debug("Removed expired message: messageId={}", entry.getKey());
            }
            return expired;
        });
    }

    private static class ProcessedMessage {
        private final String messageId;
        private final long timestamp;

        public ProcessedMessage(String messageId, long timestamp) {
            this.messageId = messageId;
            this.timestamp = timestamp;
        }

        public String getMessageId() {
            return messageId;
        }

        public long getTimestamp() {
            return timestamp;
        }
    }
}
