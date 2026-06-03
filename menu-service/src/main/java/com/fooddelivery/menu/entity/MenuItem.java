package com.fooddelivery.menu.entity;
import jakarta.persistence.*; import lombok.*;
@Entity @Table(name="menu_items") @Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class MenuItem {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    @Column(nullable=false) private Long restaurantId;
    @Column(nullable=false) private String itemName;
    private String description;
    @Column(nullable=false) private Double price;
    @Column(nullable=false) private Boolean availability;
}
