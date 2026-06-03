package com.fooddelivery.restaurant.service;

import com.fooddelivery.common.exception.InvalidRequestException;
import com.fooddelivery.common.exception.ResourceNotFoundException;
import com.fooddelivery.restaurant.dto.RestaurantRequestDto;
import com.fooddelivery.restaurant.dto.RestaurantResponseDto;
import com.fooddelivery.restaurant.entity.Restaurant;
import com.fooddelivery.restaurant.mapper.RestaurantMapper;
import com.fooddelivery.restaurant.repository.RestaurantRepository;
import com.fooddelivery.restaurant.service.impl.RestaurantServiceImpl;
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
@DisplayName("Restaurant Service Unit Tests")
class RestaurantServiceImplTest {

    @Mock
    private RestaurantRepository restaurantRepository;

    @Mock
    private RestaurantMapper restaurantMapper;

    @InjectMocks
    private RestaurantServiceImpl restaurantService;

    private RestaurantRequestDto requestDto;
    private RestaurantResponseDto responseDto;
    private Restaurant restaurant;

    @BeforeEach
    void setUp() {
        requestDto = RestaurantRequestDto.builder()
                .name("Pizza Palace")
                .email("pizza@example.com")
                .phone("9876543210")
                .address("Mumbai, India")
                .cuisineType("Italian")
                .isActive(true)
                .build();

        responseDto = RestaurantResponseDto.builder()
                .id(1L)
                .name("Pizza Palace")
                .email("pizza@example.com")
                .phone("9876543210")
                .address("Mumbai, India")
                .cuisineType("Italian")
                .isActive(true)
                .build();

        restaurant = Restaurant.builder()
                .id(1L)
                .name("Pizza Palace")
                .email("pizza@example.com")
                .phone("9876543210")
                .address("Mumbai, India")
                .cuisineType("Italian")
                .isActive(true)
                .build();
    }

    @Test
    @DisplayName("Should create restaurant successfully")
    void testCreateRestaurantSuccess() {
        // Arrange
        when(restaurantRepository.existsByEmail(requestDto.getEmail())).thenReturn(false);
        when(restaurantMapper.toEntity(requestDto)).thenReturn(restaurant);
        when(restaurantRepository.save(any(Restaurant.class))).thenReturn(restaurant);
        when(restaurantMapper.toResponse(restaurant)).thenReturn(responseDto);

        // Act
        RestaurantResponseDto result = restaurantService.create(requestDto);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("Pizza Palace");
        assertThat(result.isActive()).isTrue();

        verify(restaurantRepository).existsByEmail(requestDto.getEmail());
        verify(restaurantRepository).save(any(Restaurant.class));
    }

    @Test
    @DisplayName("Should throw exception when email already exists")
    void testCreateRestaurantDuplicateEmail() {
        // Arrange
        when(restaurantRepository.existsByEmail(requestDto.getEmail())).thenReturn(true);

        // Act & Assert
        assertThatThrownBy(() -> restaurantService.create(requestDto))
                .isInstanceOf(InvalidRequestException.class)
                .hasMessageContaining("Email already exists");

        verify(restaurantRepository, never()).save(any());
    }

    @Test
    @DisplayName("Should get restaurant by id successfully")
    void testGetRestaurantByIdSuccess() {
        // Arrange
        when(restaurantRepository.findById(1L)).thenReturn(Optional.of(restaurant));
        when(restaurantMapper.toResponse(restaurant)).thenReturn(responseDto);

        // Act
        RestaurantResponseDto result = restaurantService.getById(1L);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("Pizza Palace");

        verify(restaurantRepository).findById(1L);
    }

    @Test
    @DisplayName("Should throw exception when restaurant not found")
    void testGetRestaurantNotFound() {
        // Arrange
        when(restaurantRepository.findById(999L)).thenReturn(Optional.empty());

        // Act & Assert
        assertThatThrownBy(() -> restaurantService.getById(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("Restaurant not found");

        verify(restaurantRepository).findById(999L);
    }

    @Test
    @DisplayName("Should get all active restaurants")
    void testGetAllActiveRestaurants() {
        // Arrange
        Restaurant restaurant2 = Restaurant.builder()
                .id(2L)
                .name("Burger King")
                .email("burger@example.com")
                .cuisineType("American")
                .isActive(true)
                .build();

        RestaurantResponseDto responseDto2 = RestaurantResponseDto.builder()
                .id(2L)
                .name("Burger King")
                .email("burger@example.com")
                .cuisineType("American")
                .isActive(true)
                .build();

        when(restaurantRepository.findByIsActiveTrue()).thenReturn(Arrays.asList(restaurant, restaurant2));
        when(restaurantMapper.toResponse(restaurant)).thenReturn(responseDto);
        when(restaurantMapper.toResponse(restaurant2)).thenReturn(responseDto2);

        // Act
        List<RestaurantResponseDto> results = restaurantService.getAll();

        // Assert
        assertThat(results).hasSize(2);
        assertThat(results.get(0).getName()).isEqualTo("Pizza Palace");
        assertThat(results.get(1).getName()).isEqualTo("Burger King");

        verify(restaurantRepository).findByIsActiveTrue();
    }

    @Test
    @DisplayName("Should update restaurant successfully")
    void testUpdateRestaurantSuccess() {
        // Arrange
        RestaurantRequestDto updateRequest = RestaurantRequestDto.builder()
                .name("Pizza Palace Updated")
                .email("pizza@example.com")
                .cuisineType("Italian")
                .isActive(true)
                .build();

        when(restaurantRepository.findById(1L)).thenReturn(Optional.of(restaurant));
        doNothing().when(restaurantMapper).updateEntity(restaurant, updateRequest);
        when(restaurantRepository.save(restaurant)).thenReturn(restaurant);
        when(restaurantMapper.toResponse(restaurant)).thenReturn(responseDto);

        // Act
        RestaurantResponseDto result = restaurantService.update(1L, updateRequest);

        // Assert
        assertThat(result).isNotNull();

        verify(restaurantRepository).findById(1L);
        verify(restaurantRepository).save(restaurant);
    }

    @Test
    @DisplayName("Should deactivate restaurant successfully")
    void testDeactivateRestaurantSuccess() {
        // Arrange
        when(restaurantRepository.findById(1L)).thenReturn(Optional.of(restaurant));
        when(restaurantRepository.save(any(Restaurant.class))).thenReturn(restaurant);

        // Act
        restaurantService.deactivate(1L);

        // Assert
        verify(restaurantRepository).findById(1L);
        verify(restaurantRepository).save(any(Restaurant.class));
    }
}

