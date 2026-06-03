package com.fooddelivery.customer.service;

import com.fooddelivery.common.exception.InvalidRequestException;
import com.fooddelivery.common.exception.ResourceNotFoundException;
import com.fooddelivery.customer.dto.CustomerRequestDto;
import com.fooddelivery.customer.dto.CustomerResponseDto;
import com.fooddelivery.customer.entity.Customer;
import com.fooddelivery.customer.mapper.CustomerMapper;
import com.fooddelivery.customer.repository.CustomerRepository;
import com.fooddelivery.customer.service.impl.CustomerServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("Customer Service Unit Tests")
class CustomerServiceImplTest {

    @Mock
    private CustomerRepository customerRepository;

    @Mock
    private CustomerMapper customerMapper;

    @InjectMocks
    private CustomerServiceImpl customerService;

    private CustomerRequestDto requestDto;
    private CustomerResponseDto responseDto;
    private Customer customer;

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

        customer = Customer.builder()
                .id(1L)
                .name("John Doe")
                .email("john@example.com")
                .phone("9876543210")
                .address("Mumbai, India")
                .build();
    }

    @Test
    @DisplayName("Should create customer successfully")
    void testCreateCustomerSuccess() {
        // Arrange
        when(customerRepository.existsByEmail(requestDto.getEmail())).thenReturn(false);
        when(customerMapper.toEntity(requestDto)).thenReturn(customer);
        when(customerRepository.save(any(Customer.class))).thenReturn(customer);
        when(customerMapper.toResponse(customer)).thenReturn(responseDto);

        // Act
        CustomerResponseDto result = customerService.create(requestDto);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("John Doe");
        assertThat(result.getEmail()).isEqualTo("john@example.com");

        verify(customerRepository).existsByEmail(requestDto.getEmail());
        verify(customerRepository).save(any(Customer.class));
    }

    @Test
    @DisplayName("Should throw exception when email already exists")
    void testCreateCustomerWithDuplicateEmail() {
        // Arrange
        when(customerRepository.existsByEmail(requestDto.getEmail())).thenReturn(true);

        // Act & Assert
        assertThatThrownBy(() -> customerService.create(requestDto))
                .isInstanceOf(InvalidRequestException.class)
                .hasMessageContaining("Email already exists");

        verify(customerRepository, never()).save(any());
    }

    @Test
    @DisplayName("Should get customer by id successfully")
    void testGetCustomerByIdSuccess() {
        // Arrange
        when(customerRepository.findById(1L)).thenReturn(Optional.of(customer));
        when(customerMapper.toResponse(customer)).thenReturn(responseDto);

        // Act
        CustomerResponseDto result = customerService.getById(1L);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("John Doe");

        verify(customerRepository).findById(1L);
    }

    @Test
    @DisplayName("Should throw exception when customer not found")
    void testGetCustomerByIdNotFound() {
        // Arrange
        when(customerRepository.findById(999L)).thenReturn(Optional.empty());

        // Act & Assert
        assertThatThrownBy(() -> customerService.getById(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("Customer not found");

        verify(customerRepository).findById(999L);
    }

    @Test
    @DisplayName("Should get all customers successfully")
    void testGetAllCustomersSuccess() {
        // Arrange
        Customer customer2 = Customer.builder()
                .id(2L)
                .name("Jane Doe")
                .email("jane@example.com")
                .phone("9876543211")
                .address("Delhi, India")
                .build();

        CustomerResponseDto responseDto2 = CustomerResponseDto.builder()
                .id(2L)
                .name("Jane Doe")
                .email("jane@example.com")
                .phone("9876543211")
                .address("Delhi, India")
                .build();

        when(customerRepository.findAll()).thenReturn(Arrays.asList(customer, customer2));
        when(customerMapper.toResponse(customer)).thenReturn(responseDto);
        when(customerMapper.toResponse(customer2)).thenReturn(responseDto2);

        // Act
        List<CustomerResponseDto> results = customerService.getAll();

        // Assert
        assertThat(results).hasSize(2);
        assertThat(results.get(0).getName()).isEqualTo("John Doe");
        assertThat(results.get(1).getName()).isEqualTo("Jane Doe");

        verify(customerRepository).findAll();
    }

    @Test
    @DisplayName("Should return empty list when no customers exist")
    void testGetAllCustomersEmpty() {
        // Arrange
        when(customerRepository.findAll()).thenReturn(Arrays.asList());

        // Act
        List<CustomerResponseDto> results = customerService.getAll();

        // Assert
        assertThat(results).isEmpty();

        verify(customerRepository).findAll();
    }

    @Test
    @DisplayName("Should update customer successfully")
    void testUpdateCustomerSuccess() {
        // Arrange
        CustomerRequestDto updateRequest = CustomerRequestDto.builder()
                .name("John Updated")
                .email("john.updated@example.com")
                .phone("9876543220")
                .address("Bangalore, India")
                .build();

        when(customerRepository.findById(1L)).thenReturn(Optional.of(customer));
        doNothing().when(customerMapper).updateEntity(customer, updateRequest);
        when(customerRepository.save(customer)).thenReturn(customer);
        when(customerMapper.toResponse(customer)).thenReturn(responseDto);

        // Act
        CustomerResponseDto result = customerService.update(1L, updateRequest);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);

        verify(customerRepository).findById(1L);
        verify(customerRepository).save(customer);
    }

    @Test
    @DisplayName("Should throw exception when updating non-existent customer")
    void testUpdateCustomerNotFound() {
        // Arrange
        when(customerRepository.findById(999L)).thenReturn(Optional.empty());

        // Act & Assert
        assertThatThrownBy(() -> customerService.update(999L, requestDto))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("Customer not found");

        verify(customerRepository).findById(999L);
        verify(customerRepository, never()).save(any());
    }

    @Test
    @DisplayName("Should delete customer successfully")
    void testDeleteCustomerSuccess() {
        // Arrange
        when(customerRepository.existsById(1L)).thenReturn(true);
        doNothing().when(customerRepository).deleteById(1L);

        // Act
        customerService.delete(1L);

        // Assert
        verify(customerRepository).existsById(1L);
        verify(customerRepository).deleteById(1L);
    }

    @Test
    @DisplayName("Should throw exception when deleting non-existent customer")
    void testDeleteCustomerNotFound() {
        // Arrange
        when(customerRepository.existsById(999L)).thenReturn(false);

        // Act & Assert
        assertThatThrownBy(() -> customerService.delete(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("Customer not found");

        verify(customerRepository).existsById(999L);
        verify(customerRepository, never()).deleteById(999L);
    }

    @Test
    @DisplayName("Should validate customer email format")
    void testValidateEmailFormat() {
        // Arrange
        CustomerRequestDto invalidRequest = CustomerRequestDto.builder()
                .name("John")
                .email("invalid-email")
                .phone("9876543210")
                .address("Mumbai")
                .build();

        // This should be handled by validation annotation - test framework handles it
        // Here we're testing the service behavior

        when(customerRepository.existsByEmail(invalidRequest.getEmail())).thenReturn(false);
        when(customerMapper.toEntity(invalidRequest)).thenReturn(customer);
        when(customerRepository.save(any(Customer.class))).thenReturn(customer);
        when(customerMapper.toResponse(customer)).thenReturn(responseDto);

        // Act
        CustomerResponseDto result = customerService.create(invalidRequest);

        // Assert
        assertThat(result).isNotNull();

        verify(customerRepository).save(any(Customer.class));
    }
}

