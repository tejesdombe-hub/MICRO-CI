package com.fooddelivery.delivery.repository;
import com.fooddelivery.common.enums.DeliveryStatus;
import com.fooddelivery.delivery.entity.DeliveryPartner;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;
public interface DeliveryPartnerRepository extends JpaRepository<DeliveryPartner, Long> {
 List<DeliveryPartner> findByDeliveryStatus(DeliveryStatus status);
 Optional<DeliveryPartner> findByCurrentOrderId(Long orderId);
}
