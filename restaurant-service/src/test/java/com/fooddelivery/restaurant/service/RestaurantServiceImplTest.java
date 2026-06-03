package com.fooddelivery.restaurant.service;

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
        requestDto = new RestaurantRequestDto();
        requestDto.setRestaurantName("Pizza Palace");
        requestDto.setOwnerName("John Doe");
        requestDto.setAddress("Mumbai, India");
        requestDto.setRating(4.5);

        responseDto = RestaurantResponseDto.builder()
                .id(1L)
                .restaurantName("Pizza Palace")
                .ownerName("John Doe")
                .address("Mumbai, India")
                .rating(4.5)
                .build();

        restaurant = Restaurant.builder()
                .id(1L)
                .restaurantName("Pizza Palace")
                .ownerName("John Doe")
                .address("Mumbai, India")
                .rating(4.5)
                .build();
    }

    @Test
    @DisplayName("Should create restaurant successfully")
    void testCreateRestaurantSuccess() {
        // Arrange
        when(restaurantMapper.toEntity(requestDto)).thenReturn(restaurant);
        when(restaurantRepository.save(any(Restaurant.class))).thenReturn(restaurant);
        when(restaurantMapper.toResponse(restaurant)).thenReturn(responseDto);

        // Act
        RestaurantResponseDto result = restaurantService.create(requestDto);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getRestaurantName()).isEqualTo("Pizza Palace");

        verify(restaurantRepository).save(any(Restaurant.class));
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
        assertThat(result.getRestaurantName()).isEqualTo("Pizza Palace");

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
    @DisplayName("Should get all restaurants")
    void testGetAllRestaurants() {
        // Arrange
        Restaurant restaurant2 = Restaurant.builder()
                .id(2L)
                .restaurantName("Burger King")
                .ownerName("Jane Smith")
                .address("Delhi, India")
                .rating(4.0)
                .build();

        RestaurantResponseDto responseDto2 = RestaurantResponseDto.builder()
                .id(2L)
                .restaurantName("Burger King")
                .ownerName("Jane Smith")
                .address("Delhi, India")
                .rating(4.0)
                .build();

        when(restaurantRepository.findAll()).thenReturn(Arrays.asList(restaurant, restaurant2));
        when(restaurantMapper.toResponse(restaurant)).thenReturn(responseDto);
        when(restaurantMapper.toResponse(restaurant2)).thenReturn(responseDto2);

        // Act
        List<RestaurantResponseDto> results = restaurantService.getAll();

        // Assert
        assertThat(results).hasSize(2);
        assertThat(results.get(0).getRestaurantName()).isEqualTo("Pizza Palace");
        assertThat(results.get(1).getRestaurantName()).isEqualTo("Burger King");

        verify(restaurantRepository).findAll();
    }

    @Test
    @DisplayName("Should update restaurant successfully")
    void testUpdateRestaurantSuccess() {
        // Arrange
        RestaurantRequestDto updateRequest = new RestaurantRequestDto();
        updateRequest.setRestaurantName("Pizza Palace Updated");
        updateRequest.setOwnerName("John Doe");
        updateRequest.setAddress("Mumbai, India");
        updateRequest.setRating(4.8);

        when(restaurantRepository.findById(1L)).thenReturn(Optional.of(restaurant));
        when(restaurantRepository.save(restaurant)).thenReturn(restaurant);
        when(restaurantMapper.toResponse(restaurant)).thenReturn(responseDto);

        // Act
        RestaurantResponseDto result = restaurantService.update(1L, updateRequest);

        // Assert
        assertThat(result).isNotNull();

        verify(restaurantRepository).findById(1L);
        verify(restaurantMapper).update(restaurant, updateRequest);
        verify(restaurantRepository).save(restaurant);
    }

    @Test
    @DisplayName("Should delete restaurant successfully")
    void testDeleteRestaurantSuccess() {
        // Arrange
        when(restaurantRepository.existsById(1L)).thenReturn(true);

        // Act
        restaurantService.delete(1L);

        // Assert
        verify(restaurantRepository).existsById(1L);
        verify(restaurantRepository).deleteById(1L);
    }

    @Test
    @DisplayName("Should throw exception when deleting non-existent restaurant")
    void testDeleteRestaurantNotFound() {
        // Arrange
        when(restaurantRepository.existsById(999L)).thenReturn(false);

        // Act & Assert
        assertThatThrownBy(() -> restaurantService.delete(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("Restaurant not found");

        verify(restaurantRepository).existsById(999L);
        verify(restaurantRepository, never()).deleteById(anyLong());
    }
}

