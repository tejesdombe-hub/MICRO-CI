package com.fooddelivery.auth.service.impl;

import com.fooddelivery.auth.dto.AuthResponseDto;
import com.fooddelivery.auth.dto.LoginRequestDto;
import com.fooddelivery.auth.dto.RegisterRequestDto;
import com.fooddelivery.auth.entity.User;
import com.fooddelivery.auth.mapper.UserMapper;
import com.fooddelivery.auth.repository.UserRepository;
import com.fooddelivery.auth.security.JwtService;
import com.fooddelivery.auth.service.AuthService;
import com.fooddelivery.common.exception.InvalidRequestException;
import com.fooddelivery.common.exception.UnauthorizedException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthServiceImpl implements AuthService {

    private static final Logger log = LoggerFactory.getLogger(AuthServiceImpl.class);

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final UserMapper userMapper;
    private final AuthenticationManager authenticationManager;

    public AuthServiceImpl(
            UserRepository userRepository,
            PasswordEncoder passwordEncoder,
            JwtService jwtService,
            UserMapper userMapper,
            AuthenticationManager authenticationManager) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
        this.userMapper = userMapper;
        this.authenticationManager = authenticationManager;
    }

    @Override
    @Transactional
    public AuthResponseDto register(RegisterRequestDto request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new InvalidRequestException("Email already registered");
        }
        User user = User.builder()
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .role(request.getRole())
                .referenceId(request.getReferenceId())
                .enabled(true)
                .build();
        user = userRepository.save(user);
        log.info("User registered: {} with role {}", user.getEmail(), user.getRole());
        String token = jwtService.generateToken(user.getEmail(), user.getRole(), user.getId(), user.getReferenceId());
        return userMapper.toAuthResponse(user, token);
    }

    @Override
    public AuthResponseDto login(LoginRequestDto request) {
        try {
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword()));
        } catch (Exception ex) {
            throw new UnauthorizedException("Invalid email or password");
        }
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new UnauthorizedException("Invalid email or password"));
        log.info("User logged in: {}", user.getEmail());
        String token = jwtService.generateToken(user.getEmail(), user.getRole(), user.getId(), user.getReferenceId());
        return userMapper.toAuthResponse(user, token);
    }
}
