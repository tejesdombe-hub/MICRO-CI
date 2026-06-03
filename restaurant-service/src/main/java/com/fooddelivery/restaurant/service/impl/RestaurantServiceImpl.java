package com.fooddelivery.restaurant.service.impl;
import com.fooddelivery.common.exception.ResourceNotFoundException;
import com.fooddelivery.restaurant.dto.*; import com.fooddelivery.restaurant.entity.Restaurant;
import com.fooddelivery.restaurant.mapper.RestaurantMapper; import com.fooddelivery.restaurant.repository.RestaurantRepository;
import com.fooddelivery.restaurant.service.RestaurantService;
import org.slf4j.Logger; import org.slf4j.LoggerFactory; import org.springframework.stereotype.Service; import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service public class RestaurantServiceImpl implements RestaurantService {
    private static final Logger log = LoggerFactory.getLogger(RestaurantServiceImpl.class);
    private final RestaurantRepository repo; private final RestaurantMapper mapper;
    public RestaurantServiceImpl(RestaurantRepository repo, RestaurantMapper mapper){this.repo=repo;this.mapper=mapper;}
    @Override @Transactional public RestaurantResponseDto create(RestaurantRequestDto r){Restaurant s=repo.save(mapper.toEntity(r));log.info("Restaurant created {}",s.getId());return mapper.toResponse(s);}
    @Override public RestaurantResponseDto getById(Long id){return mapper.toResponse(repo.findById(id).orElseThrow(()->new ResourceNotFoundException("Restaurant not found: "+id)));}
    @Override public List<RestaurantResponseDto> getAll(){return repo.findAll().stream().map(mapper::toResponse).toList();}
    @Override @Transactional public RestaurantResponseDto update(Long id, RestaurantRequestDto r){Restaurant e=repo.findById(id).orElseThrow(()->new ResourceNotFoundException("Restaurant not found: "+id));mapper.update(e,r);return mapper.toResponse(repo.save(e));}
    @Override @Transactional public void delete(Long id){if(!repo.existsById(id))throw new ResourceNotFoundException("Restaurant not found: "+id);repo.deleteById(id);}
}
