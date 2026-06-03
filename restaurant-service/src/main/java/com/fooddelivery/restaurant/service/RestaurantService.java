package com.fooddelivery.restaurant.service;
import com.fooddelivery.restaurant.dto.*;
import java.util.List;
public interface RestaurantService {
 RestaurantResponseDto create(RestaurantRequestDto r);
 RestaurantResponseDto getById(Long id);
 List<RestaurantResponseDto> getAll();
 RestaurantResponseDto update(Long id, RestaurantRequestDto r);
 void delete(Long id);
}
