package com.fooddelivery.customer.service.impl;

import com.fooddelivery.common.exception.*;
import com.fooddelivery.customer.dto.*;
import com.fooddelivery.customer.entity.Customer;
import com.fooddelivery.customer.mapper.CustomerMapper;
import com.fooddelivery.customer.repository.CustomerRepository;
import com.fooddelivery.customer.service.CustomerService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class CustomerServiceImpl implements CustomerService {
    private static final Logger log = LoggerFactory.getLogger(CustomerServiceImpl.class);
    private final CustomerRepository repository;
    private final CustomerMapper mapper;

    public CustomerServiceImpl(CustomerRepository repository, CustomerMapper mapper) {
        this.repository = repository; this.mapper = mapper;
    }

    @Override @Transactional
    public CustomerResponseDto create(CustomerRequestDto request) {
        if (repository.existsByEmail(request.getEmail())) throw new InvalidRequestException("Email already exists");
        Customer saved = repository.save(mapper.toEntity(request));
        log.info("Customer created id={}", saved.getId());
        return mapper.toResponse(saved);
    }

    @Override
    public CustomerResponseDto getById(Long id) {
        return mapper.toResponse(repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Customer not found: " + id)));
    }

    @Override
    public List<CustomerResponseDto> getAll() {
        return repository.findAll().stream().map(mapper::toResponse).toList();
    }

    @Override @Transactional
    public CustomerResponseDto update(Long id, CustomerRequestDto request) {
        Customer c = repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Customer not found: " + id));
        mapper.updateEntity(c, request);
        return mapper.toResponse(repository.save(c));
    }

    @Override @Transactional
    public void delete(Long id) {
        if (!repository.existsById(id)) throw new ResourceNotFoundException("Customer not found: " + id);
        repository.deleteById(id);
    }
}
