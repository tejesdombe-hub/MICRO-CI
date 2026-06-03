package com.fooddelivery.notification.mapper;
import com.fooddelivery.notification.dto.*; import com.fooddelivery.notification.entity.Notification; import org.springframework.stereotype.Component;
@Component public class NotificationMapper {
    public Notification toEntity(NotificationRequestDto d){return Notification.builder().userId(d.getUserId()).message(d.getMessage()).type(d.getType()).build();}
    public NotificationResponseDto toResponse(Notification n){return NotificationResponseDto.builder().id(n.getId()).userId(n.getUserId()).message(n.getMessage()).type(n.getType()).sentAt(n.getSentAt()).build();}
}
