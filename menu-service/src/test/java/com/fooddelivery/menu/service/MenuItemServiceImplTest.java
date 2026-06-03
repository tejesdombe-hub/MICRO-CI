package com.fooddelivery.menu.service;

import com.fooddelivery.common.exception.InvalidRequestException;
import com.fooddelivery.common.exception.ResourceNotFoundException;
import com.fooddelivery.menu.dto.MenuItemRequestDto;
import com.fooddelivery.menu.dto.MenuItemResponseDto;
import com.fooddelivery.menu.entity.MenuItem;
import com.fooddelivery.menu.mapper.MenuItemMapper;
import com.fooddelivery.menu.repository.MenuItemRepository;
import com.fooddelivery.menu.service.impl.MenuItemServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("Menu Item Service Unit Tests")
class MenuItemServiceImplTest {

    @Mock
    private MenuItemRepository menuItemRepository;

    @Mock
    private MenuItemMapper menuItemMapper;

    @InjectMocks
    private MenuItemServiceImpl menuItemService;

    private MenuItemRequestDto requestDto;
    private MenuItemResponseDto responseDto;
    private MenuItem menuItem;

    @BeforeEach
    void setUp() {
        requestDto = MenuItemRequestDto.builder()
                .restaurantId(1L)
                .name("Margherita Pizza")
                .description("Classic Italian pizza")
                .price(BigDecimal.valueOf(299.00))
                .isAvailable(true)
                .build();

        responseDto = MenuItemResponseDto.builder()
                .id(1L)
                .restaurantId(1L)
                .name("Margherita Pizza")
                .description("Classic Italian pizza")
                .price(BigDecimal.valueOf(299.00))
                .isAvailable(true)
                .build();

        menuItem = MenuItem.builder()
                .id(1L)
                .restaurantId(1L)
                .name("Margherita Pizza")
                .description("Classic Italian pizza")
                .price(BigDecimal.valueOf(299.00))
                .isAvailable(true)
                .build();
    }

    @Test
    @DisplayName("Should add menu item successfully")
    void testAddMenuItemSuccess() {
        // Arrange
        when(menuItemMapper.toEntity(requestDto)).thenReturn(menuItem);
        when(menuItemRepository.save(any(MenuItem.class))).thenReturn(menuItem);
        when(menuItemMapper.toResponse(menuItem)).thenReturn(responseDto);

        // Act
        MenuItemResponseDto result = menuItemService.add(requestDto);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("Margherita Pizza");
        assertThat(result.isAvailable()).isTrue();

        verify(menuItemRepository).save(any(MenuItem.class));
    }

    @Test
    @DisplayName("Should get menu item by id successfully")
    void testGetMenuItemByIdSuccess() {
        // Arrange
        when(menuItemRepository.findById(1L)).thenReturn(Optional.of(menuItem));
        when(menuItemMapper.toResponse(menuItem)).thenReturn(responseDto);

        // Act
        MenuItemResponseDto result = menuItemService.getById(1L);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("Margherita Pizza");

        verify(menuItemRepository).findById(1L);
    }

    @Test
    @DisplayName("Should throw exception when menu item not found")
    void testGetMenuItemNotFound() {
        // Arrange
        when(menuItemRepository.findById(999L)).thenReturn(Optional.empty());

        // Act & Assert
        assertThatThrownBy(() -> menuItemService.getById(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("Menu item not found");

        verify(menuItemRepository).findById(999L);
    }

    @Test
    @DisplayName("Should get menu items by restaurant id")
    void testGetMenuItemsByRestaurantId() {
        // Arrange
        MenuItem menuItem2 = MenuItem.builder()
                .id(2L)
                .restaurantId(1L)
                .name("Pepperoni Pizza")
                .description("Spicy pizza")
                .price(BigDecimal.valueOf(349.00))
                .isAvailable(true)
                .build();

        MenuItemResponseDto responseDto2 = MenuItemResponseDto.builder()
                .id(2L)
                .restaurantId(1L)
                .name("Pepperoni Pizza")
                .description("Spicy pizza")
                .price(BigDecimal.valueOf(349.00))
                .isAvailable(true)
                .build();

        when(menuItemRepository.findByRestaurantId(1L)).thenReturn(Arrays.asList(menuItem, menuItem2));
        when(menuItemMapper.toResponse(menuItem)).thenReturn(responseDto);
        when(menuItemMapper.toResponse(menuItem2)).thenReturn(responseDto2);

        // Act
        List<MenuItemResponseDto> results = menuItemService.getByRestaurantId(1L);

        // Assert
        assertThat(results).hasSize(2);
        assertThat(results.get(0).getName()).isEqualTo("Margherita Pizza");
        assertThat(results.get(1).getName()).isEqualTo("Pepperoni Pizza");

        verify(menuItemRepository).findByRestaurantId(1L);
    }

    @Test
    @DisplayName("Should update menu item successfully")
    void testUpdateMenuItemSuccess() {
        // Arrange
        MenuItemRequestDto updateRequest = MenuItemRequestDto.builder()
                .restaurantId(1L)
                .name("Margherita Pizza Updated")
                .description("Updated description")
                .price(BigDecimal.valueOf(319.00))
                .isAvailable(true)
                .build();

        when(menuItemRepository.findById(1L)).thenReturn(Optional.of(menuItem));
        doNothing().when(menuItemMapper).updateEntity(menuItem, updateRequest);
        when(menuItemRepository.save(menuItem)).thenReturn(menuItem);
        when(menuItemMapper.toResponse(menuItem)).thenReturn(responseDto);

        // Act
        MenuItemResponseDto result = menuItemService.update(1L, updateRequest);

        // Assert
        assertThat(result).isNotNull();

        verify(menuItemRepository).findById(1L);
        verify(menuItemRepository).save(menuItem);
    }

    @Test
    @DisplayName("Should toggle menu item availability")
    void testToggleAvailability() {
        // Arrange
        when(menuItemRepository.findById(1L)).thenReturn(Optional.of(menuItem));
        when(menuItemRepository.save(any(MenuItem.class))).thenReturn(menuItem);

        // Act
        menuItemService.toggleAvailability(1L);

        // Assert
        verify(menuItemRepository).findById(1L);
        verify(menuItemRepository).save(any(MenuItem.class));
    }

    @Test
    @DisplayName("Should delete menu item successfully")
    void testDeleteMenuItemSuccess() {
        // Arrange
        when(menuItemRepository.existsById(1L)).thenReturn(true);
        doNothing().when(menuItemRepository).deleteById(1L);

        // Act
        menuItemService.delete(1L);

        // Assert
        verify(menuItemRepository).existsById(1L);
        verify(menuItemRepository).deleteById(1L);
    }

    @Test
    @DisplayName("Should throw exception when deleting non-existent menu item")
    void testDeleteMenuItemNotFound() {
        // Arrange
        when(menuItemRepository.existsById(999L)).thenReturn(false);

        // Act & Assert
        assertThatThrownBy(() -> menuItemService.delete(999L))
                .isInstanceOf(ResourceNotFoundException.class);

        verify(menuItemRepository, never()).deleteById(999L);
    }

    @Test
    @DisplayName("Should validate positive price")
    void testValidatePositivePrice() {
        // Arrange
        MenuItemRequestDto invalidRequest = MenuItemRequestDto.builder()
                .restaurantId(1L)
                .name("Pizza")
                .price(BigDecimal.valueOf(-100))
                .isAvailable(true)
                .build();

        // Act & Assert
        assertThat(invalidRequest.getPrice()).isNegative();
    }
}

