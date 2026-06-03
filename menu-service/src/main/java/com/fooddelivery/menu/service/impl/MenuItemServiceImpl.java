package com.fooddelivery.menu.service.impl;
import com.fooddelivery.common.exception.ResourceNotFoundException;
import com.fooddelivery.menu.dto.*; import com.fooddelivery.menu.entity.MenuItem;
import com.fooddelivery.menu.mapper.MenuItemMapper; import com.fooddelivery.menu.repository.MenuItemRepository;
import com.fooddelivery.menu.service.MenuItemService;
import org.slf4j.Logger; import org.slf4j.LoggerFactory; import org.springframework.stereotype.Service; import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service public class MenuItemServiceImpl implements MenuItemService {
    private static final Logger log = LoggerFactory.getLogger(MenuItemServiceImpl.class);
    private final MenuItemRepository repo; private final MenuItemMapper mapper;
    public MenuItemServiceImpl(MenuItemRepository repo, MenuItemMapper mapper){this.repo=repo;this.mapper=mapper;}
    @Override @Transactional public MenuItemResponseDto create(MenuItemRequestDto r){MenuItem s=repo.save(mapper.toEntity(r));log.info("Menu item created {}",s.getId());return mapper.toResponse(s);}
    @Override public MenuItemResponseDto getById(Long id){return mapper.toResponse(repo.findById(id).orElseThrow(()->new ResourceNotFoundException("Menu item not found: "+id)));}
    @Override public List<MenuItemResponseDto> getByRestaurant(Long restaurantId){return repo.findByRestaurantId(restaurantId).stream().map(mapper::toResponse).toList();}
    @Override @Transactional public MenuItemResponseDto update(Long id, MenuItemRequestDto r){MenuItem e=repo.findById(id).orElseThrow(()->new ResourceNotFoundException("Menu item not found: "+id));mapper.update(e,r);return mapper.toResponse(repo.save(e));}
    @Override @Transactional public void delete(Long id){if(!repo.existsById(id))throw new ResourceNotFoundException("Menu item not found: "+id);repo.deleteById(id);}
}
