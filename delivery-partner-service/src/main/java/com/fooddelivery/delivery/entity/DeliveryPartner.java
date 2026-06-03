package com.fooddelivery.delivery.entity;
import com.fooddelivery.common.enums.DeliveryStatus;
import jakarta.persistence.*; import lombok.*;
@Entity @Table(name="delivery_partners") @Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class DeliveryPartner {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    @Column(nullable=false) private String name;
    @Column(nullable=false) private String phone;
    @Column(nullable=false) private String vehicleNumber;
    private Long currentOrderId;
    @Enumerated(EnumType.STRING) private DeliveryStatus deliveryStatus;
}
