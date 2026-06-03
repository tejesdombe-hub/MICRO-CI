package com.fooddelivery.menu.mapper;
import com.fooddelivery.menu.dto.*; import com.fooddelivery.menu.entity.MenuItem; import org.springframework.stereotype.Component;
@Component public class MenuItemMapper {
    public MenuItem toEntity(MenuItemRequestDto d){return MenuItem.builder().restaurantId(d.getRestaurantId()).itemName(d.getItemName()).description(d.getDescription()).price(d.getPrice()).availability(d.getAvailability()).build();}
    public MenuItemResponseDto toResponse(MenuItem m){return MenuItemResponseDto.builder().id(m.getId()).restaurantId(m.getRestaurantId()).itemName(m.getItemName()).description(m.getDescription()).price(m.getPrice()).availability(m.getAvailability()).build();}
    public void update(MenuItem m, MenuItemRequestDto d){m.setItemName(d.getItemName());m.setDescription(d.getDescription());m.setPrice(d.getPrice());m.setAvailability(d.getAvailability());}
}
