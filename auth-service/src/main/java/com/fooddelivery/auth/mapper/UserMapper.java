package com.fooddelivery.auth.mapper;

import com.fooddelivery.auth.dto.AuthResponseDto;
import com.fooddelivery.auth.entity.User;
import org.springframework.stereotype.Component;

@Component
public class UserMapper {

    public AuthResponseDto toAuthResponse(User user, String token) {
        return AuthResponseDto.builder()
                .token(token)
                .tokenType("Bearer")
                .userId(user.getId())
                .email(user.getEmail())
                .role(user.getRole())
                .referenceId(user.getReferenceId())
                .build();
    }
}
