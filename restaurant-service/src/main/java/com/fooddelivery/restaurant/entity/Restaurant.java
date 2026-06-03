package com.fooddelivery.restaurant.entity;
import jakarta.persistence.*; import lombok.*;
@Entity @Table(name="restaurants") @Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Restaurant {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    @Column(nullable=false) private String restaurantName;
    @Column(nullable=false) private String ownerName;
    @Column(nullable=false) private String address;
    private Double rating;
}
