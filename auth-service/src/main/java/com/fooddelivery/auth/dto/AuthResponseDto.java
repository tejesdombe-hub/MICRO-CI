package com.fooddelivery.auth.dto;

import com.fooddelivery.common.enums.Role;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AuthResponseDto {
    private String token;
    private String tokenType;
    private Long userId;
    private String email;
    private Role role;
    private Long referenceId;
}
