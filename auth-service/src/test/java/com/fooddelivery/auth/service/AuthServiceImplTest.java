package com.fooddelivery.auth.service;

import com.fooddelivery.auth.dto.AuthResponseDto;
import com.fooddelivery.auth.dto.LoginRequestDto;
import com.fooddelivery.auth.dto.RegisterRequestDto;
import com.fooddelivery.auth.entity.Auth;
import com.fooddelivery.auth.mapper.AuthMapper;
import com.fooddelivery.auth.repository.AuthRepository;
import com.fooddelivery.auth.service.impl.AuthServiceImpl;
import com.fooddelivery.auth.util.JwtTokenProvider;
import com.fooddelivery.common.exception.InvalidRequestException;
import com.fooddelivery.common.exception.ResourceNotFoundException;
import com.fooddelivery.common.exception.UnauthorizedException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("Auth Service Unit Tests")
class AuthServiceImplTest {

    @Mock
    private AuthRepository authRepository;

    @Mock
    private AuthMapper authMapper;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private JwtTokenProvider jwtTokenProvider;

    @InjectMocks
    private AuthServiceImpl authService;

    private RegisterRequestDto registerRequest;
    private LoginRequestDto loginRequest;
    private Auth authEntity;
    private AuthResponseDto authResponse;

    @BeforeEach
    void setUp() {
        registerRequest = RegisterRequestDto.builder()
                .email("customer@example.com")
                .password("password123")
                .role("CUSTOMER")
                .referenceId(1L)
                .build();

        loginRequest = LoginRequestDto.builder()
                .email("customer@example.com")
                .password("password123")
                .build();

        authEntity = Auth.builder()
                .id(1L)
                .email("customer@example.com")
                .password("encodedPassword")
                .role("CUSTOMER")
                .referenceId(1L)
                .build();

        authResponse = AuthResponseDto.builder()
                .id(1L)
                .email("customer@example.com")
                .role("CUSTOMER")
                .token("jwt.token.here")
                .build();
    }

    @Test
    @DisplayName("Should register user successfully")
    void testRegisterSuccess() {
        // Arrange
        when(authRepository.existsByEmail(registerRequest.getEmail())).thenReturn(false);
        when(passwordEncoder.encode(registerRequest.getPassword())).thenReturn("encodedPassword");
        when(authMapper.toEntity(registerRequest)).thenReturn(authEntity);
        when(authRepository.save(any(Auth.class))).thenReturn(authEntity);
        when(jwtTokenProvider.generateToken(authEntity.getEmail(), authEntity.getRole()))
                .thenReturn("jwt.token.here");
        when(authMapper.toResponse(authEntity)).thenReturn(authResponse);

        // Act
        AuthResponseDto result = authService.register(registerRequest);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getEmail()).isEqualTo("customer@example.com");
        assertThat(result.getRole()).isEqualTo("CUSTOMER");
        assertThat(result.getToken()).isEqualTo("jwt.token.here");

        verify(authRepository).existsByEmail(registerRequest.getEmail());
        verify(authRepository).save(any(Auth.class));
    }

    @Test
    @DisplayName("Should throw exception when email already exists")
    void testRegisterWithDuplicateEmail() {
        // Arrange
        when(authRepository.existsByEmail(registerRequest.getEmail())).thenReturn(true);

        // Act & Assert
        assertThatThrownBy(() -> authService.register(registerRequest))
                .isInstanceOf(InvalidRequestException.class)
                .hasMessageContaining("Email already exists");

        verify(authRepository, never()).save(any(Auth.class));
    }

    @Test
    @DisplayName("Should login successfully with correct credentials")
    void testLoginSuccess() {
        // Arrange
        when(authRepository.findByEmail(loginRequest.getEmail()))
                .thenReturn(Optional.of(authEntity));
        when(passwordEncoder.matches(loginRequest.getPassword(), authEntity.getPassword()))
                .thenReturn(true);
        when(jwtTokenProvider.generateToken(authEntity.getEmail(), authEntity.getRole()))
                .thenReturn("jwt.token.here");
        when(authMapper.toResponse(authEntity)).thenReturn(authResponse);

        // Act
        AuthResponseDto result = authService.login(loginRequest);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getEmail()).isEqualTo("customer@example.com");
        assertThat(result.getToken()).isNotNull();

        verify(authRepository).findByEmail(loginRequest.getEmail());
    }

    @Test
    @DisplayName("Should throw exception when user not found")
    void testLoginUserNotFound() {
        // Arrange
        when(authRepository.findByEmail(loginRequest.getEmail()))
                .thenReturn(Optional.empty());

        // Act & Assert
        assertThatThrownBy(() -> authService.login(loginRequest))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("User not found");

        verify(authRepository).findByEmail(loginRequest.getEmail());
    }

    @Test
    @DisplayName("Should throw exception when password is incorrect")
    void testLoginIncorrectPassword() {
        // Arrange
        when(authRepository.findByEmail(loginRequest.getEmail()))
                .thenReturn(Optional.of(authEntity));
        when(passwordEncoder.matches(loginRequest.getPassword(), authEntity.getPassword()))
                .thenReturn(false);

        // Act & Assert
        assertThatThrownBy(() -> authService.login(loginRequest))
                .isInstanceOf(UnauthorizedException.class)
                .hasMessageContaining("Invalid credentials");

        verify(authRepository).findByEmail(loginRequest.getEmail());
    }

    @Test
    @DisplayName("Should validate JWT token successfully")
    void testValidateToken() {
        // Arrange
        String token = "valid.jwt.token";
        when(jwtTokenProvider.validateToken(token)).thenReturn(true);

        // Act
        boolean result = jwtTokenProvider.validateToken(token);

        // Assert
        assertThat(result).isTrue();
    }

    @Test
    @DisplayName("Should extract email from JWT token")
    void testGetEmailFromToken() {
        // Arrange
        String token = "valid.jwt.token";
        String expectedEmail = "customer@example.com";
        when(jwtTokenProvider.getEmailFromToken(token)).thenReturn(expectedEmail);

        // Act
        String result = jwtTokenProvider.getEmailFromToken(token);

        // Assert
        assertThat(result).isEqualTo(expectedEmail);
    }
}

