package com.fooddelivery.menu.controller;
import com.fooddelivery.menu.dto.*; import com.fooddelivery.menu.service.MenuItemService;
import io.swagger.v3.oas.annotations.tags.Tag; import jakarta.validation.Valid;
import org.springframework.http.*; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/menus") @Tag(name="Menu Items")
public class MenuItemController {
    private final MenuItemService service;
    public MenuItemController(MenuItemService service){this.service=service;}
    @PostMapping public ResponseEntity<MenuItemResponseDto> create(@Valid @RequestBody MenuItemRequestDto r){return ResponseEntity.status(HttpStatus.CREATED).body(service.create(r));}
    @GetMapping("/{id}") public ResponseEntity<MenuItemResponseDto> get(@PathVariable Long id){return ResponseEntity.ok(service.getById(id));}
    @GetMapping("/restaurant/{restaurantId}") public ResponseEntity<List<MenuItemResponseDto>> byRestaurant(@PathVariable Long restaurantId){return ResponseEntity.ok(service.getByRestaurant(restaurantId));}
    @PutMapping("/{id}") public ResponseEntity<MenuItemResponseDto> update(@PathVariable Long id,@Valid @RequestBody MenuItemRequestDto r){return ResponseEntity.ok(service.update(id,r));}
    @DeleteMapping("/{id}") public ResponseEntity<Void> delete(@PathVariable Long id){service.delete(id);return ResponseEntity.noContent().build();}
}
