package com.fooddelivery.restaurant.controller;
import com.fooddelivery.restaurant.dto.*; import com.fooddelivery.restaurant.service.RestaurantService;
import io.swagger.v3.oas.annotations.tags.Tag; import jakarta.validation.Valid;
import org.springframework.http.*; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/restaurants") @Tag(name="Restaurants")
public class RestaurantController {
    private final RestaurantService service;
    public RestaurantController(RestaurantService service){this.service=service;}
    @PostMapping public ResponseEntity<RestaurantResponseDto> create(@Valid @RequestBody RestaurantRequestDto r){return ResponseEntity.status(HttpStatus.CREATED).body(service.create(r));}
    @GetMapping("/{id}") public ResponseEntity<RestaurantResponseDto> get(@PathVariable Long id){return ResponseEntity.ok(service.getById(id));}
    @GetMapping public ResponseEntity<List<RestaurantResponseDto>> all(){return ResponseEntity.ok(service.getAll());}
    @PutMapping("/{id}") public ResponseEntity<RestaurantResponseDto> update(@PathVariable Long id,@Valid @RequestBody RestaurantRequestDto r){return ResponseEntity.ok(service.update(id,r));}
    @DeleteMapping("/{id}") public ResponseEntity<Void> delete(@PathVariable Long id){service.delete(id);return ResponseEntity.noContent().build();}
}
