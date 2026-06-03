package com.fooddelivery.restaurant.mapper;
import com.fooddelivery.restaurant.dto.*; import com.fooddelivery.restaurant.entity.Restaurant; import org.springframework.stereotype.Component;
@Component public class RestaurantMapper {
    public Restaurant toEntity(RestaurantRequestDto d){return Restaurant.builder().restaurantName(d.getRestaurantName()).ownerName(d.getOwnerName()).address(d.getAddress()).rating(d.getRating()).build();}
    public RestaurantResponseDto toResponse(Restaurant r){return RestaurantResponseDto.builder().id(r.getId()).restaurantName(r.getRestaurantName()).ownerName(r.getOwnerName()).address(r.getAddress()).rating(r.getRating()).build();}
    public void update(Restaurant r, RestaurantRequestDto d){r.setRestaurantName(d.getRestaurantName());r.setOwnerName(d.getOwnerName());r.setAddress(d.getAddress());r.setRating(d.getRating());}
}
