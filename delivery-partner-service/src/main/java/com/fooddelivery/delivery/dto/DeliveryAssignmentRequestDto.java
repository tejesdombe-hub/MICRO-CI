package com.fooddelivery.delivery.dto;
import com.fooddelivery.common.enums.DeliveryStatus; import jakarta.validation.constraints.NotNull; import lombok.Data;
@Data public class DeliveryAssignmentRequestDto { @NotNull private Long orderId; }
