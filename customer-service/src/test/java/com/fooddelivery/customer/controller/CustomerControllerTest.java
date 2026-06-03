package com.fooddelivery.customer.controller;

import com.fooddelivery.customer.dto.CustomerRequestDto;
import com.fooddelivery.customer.dto.CustomerResponseDto;
import com.fooddelivery.customer.service.CustomerService;
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

import java.util.Arrays;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@DisplayName("Customer Controller Integration Tests")
class CustomerControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private CustomerService customerService;

    private CustomerRequestDto requestDto;
    private CustomerResponseDto responseDto;

    @BeforeEach
    void setUp() {
        requestDto = CustomerRequestDto.builder()
                .name("John Doe")
                .email("john@example.com")
                .phone("9876543210")
                .address("Mumbai, India")
                .build();

        responseDto = CustomerResponseDto.builder()
                .id(1L)
                .name("John Doe")
                .email("john@example.com")
                .phone("9876543210")
                .address("Mumbai, India")
                .build();
    }

    @Test
    @DisplayName("Should create customer and return 201 status")
    void testCreateCustomerSuccess() throws Exception {
        // Arrange
        when(customerService.create(any(CustomerRequestDto.class)))
                .thenReturn(responseDto);

        // Act & Assert
        mockMvc.perform(post("/customers")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(requestDto)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("John Doe")))
                .andExpect(jsonPath("$.email", is("john@example.com")));

        verify(customerService).create(any(CustomerRequestDto.class));
    }

    @Test
    @DisplayName("Should get customer by id and return 200 status")
    void testGetCustomerByIdSuccess() throws Exception {
        // Arrange
        when(customerService.getById(1L)).thenReturn(responseDto);

        // Act & Assert
        mockMvc.perform(get("/customers/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("John Doe")))
                .andExpect(jsonPath("$.email", is("john@example.com")));

        verify(customerService).getById(1L);
    }

    @Test
    @DisplayName("Should get all customers and return 200 status")
    void testGetAllCustomersSuccess() throws Exception {
        // Arrange
        CustomerResponseDto responseDto2 = CustomerResponseDto.builder()
                .id(2L)
                .name("Jane Doe")
                .email("jane@example.com")
                .phone("9876543211")
                .address("Delhi, India")
                .build();

        when(customerService.getAll())
                .thenReturn(Arrays.asList(responseDto, responseDto2));

        // Act & Assert
        mockMvc.perform(get("/customers"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(2)))
                .andExpect(jsonPath("$[0].id", is(1)))
                .andExpect(jsonPath("$[1].id", is(2)));

        verify(customerService).getAll();
    }

    @Test
    @DisplayName("Should update customer and return 200 status")
    void testUpdateCustomerSuccess() throws Exception {
        // Arrange
        when(customerService.update(eq(1L), any(CustomerRequestDto.class)))
                .thenReturn(responseDto);

        // Act & Assert
        mockMvc.perform(put("/customers/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(requestDto)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id", is(1)))
                .andExpect(jsonPath("$.name", is("John Doe")));

        verify(customerService).update(eq(1L), any(CustomerRequestDto.class));
    }

    @Test
    @DisplayName("Should delete customer and return 204 status")
    void testDeleteCustomerSuccess() throws Exception {
        // Arrange
        doNothing().when(customerService).delete(1L);

        // Act & Assert
        mockMvc.perform(delete("/customers/1"))
                .andExpect(status().isNoContent());

        verify(customerService).delete(1L);
    }

    @Test
    @DisplayName("Should return 400 for invalid customer request")
    void testCreateCustomerInvalidRequest() throws Exception {
        // Arrange
        CustomerRequestDto invalidRequest = CustomerRequestDto.builder()
                .name("")
                .email("")
                .build();

        // Act & Assert
        mockMvc.perform(post("/customers")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidRequest)))
                .andExpect(status().isBadRequest());

        verify(customerService, never()).create(any());
    }

    @Test
    @DisplayName("Should return 404 when customer not found")
    void testGetCustomerNotFound() throws Exception {
        // Arrange
        when(customerService.getById(999L))
                .thenThrow(new com.fooddelivery.common.exception.ResourceNotFoundException("Customer not found: 999"));

        // Act & Assert
        mockMvc.perform(get("/customers/999"))
                .andExpect(status().isNotFound());

        verify(customerService).getById(999L);
    }
}

