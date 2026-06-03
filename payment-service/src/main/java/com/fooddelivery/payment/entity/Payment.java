package com.fooddelivery.payment.entity;
import com.fooddelivery.common.enums.PaymentStatus;
import jakarta.persistence.*; import lombok.*;
@Entity @Table(name="payments") @Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Payment {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    @Column(nullable=false) private Long orderId;
    @Column(nullable=false) private Double amount;
    @Enumerated(EnumType.STRING) @Column(nullable=false) private PaymentStatus paymentStatus;
    @Column(nullable=false) private String paymentMethod;
}
