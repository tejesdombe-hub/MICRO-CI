package com.fooddelivery.menu.service;
import com.fooddelivery.menu.dto.*;
import java.util.List;
public interface MenuItemService {
 MenuItemResponseDto create(MenuItemRequestDto r);
 MenuItemResponseDto getById(Long id);
 List<MenuItemResponseDto> getByRestaurant(Long restaurantId);
 MenuItemResponseDto update(Long id, MenuItemRequestDto r);
 void delete(Long id);
}
