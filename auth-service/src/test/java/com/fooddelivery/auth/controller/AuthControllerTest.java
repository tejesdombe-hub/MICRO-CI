package com.fooddelivery.auth.controller;

import com.fooddelivery.auth.dto.AuthResponseDto;
import com.fooddelivery.auth.dto.LoginRequestDto;
import com.fooddelivery.auth.dto.RegisterRequestDto;
import com.fooddelivery.auth.service.AuthService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.assertj.core.api.Assertions.*;
import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@DisplayName("Auth Controller Integration Tests")
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private AuthService authService;

    private RegisterRequestDto registerRequest;
    private LoginRequestDto loginRequest;
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

        authResponse = AuthResponseDto.builder()
                .id(1L)
                .email("customer@example.com")
                .role("CUSTOMER")
                .token("jwt.token.here")
                .build();
    }

    @Test
    @DisplayName("Should register user and return 201 status")
    void testRegisterSuccess() throws Exception {
        // Arrange
        when(authService.register(any(RegisterRequestDto.class)))
                .thenReturn(authResponse);

        // Act & Assert
        mockMvc.perform(post("/api/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(registerRequest)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.email", is("customer@example.com")))
                .andExpect(jsonPath("$.token", notNullValue()));

        verify(authService).register(any(RegisterRequestDto.class));
    }

    @Test
    @DisplayName("Should login user and return JWT token")
    void testLoginSuccess() throws Exception {
        // Arrange
        when(authService.login(any(LoginRequestDto.class)))
                .thenReturn(authResponse);

        // Act & Assert
        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(loginRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.email", is("customer@example.com")))
                .andExpect(jsonPath("$.token", is("jwt.token.here")));

        verify(authService).login(any(LoginRequestDto.class));
    }

    @Test
    @DisplayName("Should return 400 for invalid register request")
    void testRegisterInvalidRequest() throws Exception {
        // Arrange - missing required fields
        String invalidRequest = "{}";

        // Act & Assert
        mockMvc.perform(post("/api/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(invalidRequest))
                .andExpect(status().isBadRequest());

        verify(authService, never()).register(any());
    }

    @Test
    @DisplayName("Should return 400 when email format is invalid")
    void testRegisterInvalidEmail() throws Exception {
        // Arrange
        RegisterRequestDto invalidRequest = RegisterRequestDto.builder()
                .email("invalid-email")
                .password("password123")
                .role("CUSTOMER")
                .referenceId(1L)
                .build();

        // Act & Assert
        mockMvc.perform(post("/api/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidRequest)))
                .andExpect(status().isBadRequest());
    }

    @Test
    @DisplayName("Should return 400 when password is empty")
    void testRegisterEmptyPassword() throws Exception {
        // Arrange
        RegisterRequestDto invalidRequest = RegisterRequestDto.builder()
                .email("customer@example.com")
                .password("")
                .role("CUSTOMER")
                .referenceId(1L)
                .build();

        // Act & Assert
        mockMvc.perform(post("/api/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidRequest)))
                .andExpect(status().isBadRequest());
    }
}

