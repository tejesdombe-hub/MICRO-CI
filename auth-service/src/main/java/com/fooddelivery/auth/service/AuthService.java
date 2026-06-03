package com.fooddelivery.auth.service;

import com.fooddelivery.auth.dto.AuthResponseDto;
import com.fooddelivery.auth.dto.LoginRequestDto;
import com.fooddelivery.auth.dto.RegisterRequestDto;

public interface AuthService {
    AuthResponseDto register(RegisterRequestDto request);
    AuthResponseDto login(LoginRequestDto request);
}
